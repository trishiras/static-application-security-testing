import os
import json
import uuid
import traceback
from static_application_security_testing.core.logger import logger
from static_application_security_testing.core.models import Response
from static_application_security_testing.support.enums import (
    STDInput,
    MixedTypeEnum,
    ResponseMessage,
)


def run(
    target: str,
) -> Response:
    resp = Response()
    data = None
    file = os.path.join(
        os.path.join(
            os.getcwd(),
            MixedTypeEnum.TMP.value,
        ),
        str(f"{uuid.uuid4()}.json"),
    )
    try:
        os.system(
            STDInput.SEMGREP.value.format(
                rules_dir=MixedTypeEnum.RULES_DIR.value,
                target=target,
                output=file,
            )
        )
        with open(file, "r") as fp:
            data = json.load(fp, strict=False)
        if data:
            resp.success = MixedTypeEnum.SUCCESS.value
            resp.data = data
    except Exception as err:
        resp.message = ResponseMessage.SEMGREP_MSG.value
        logger.error(err)
        logger.debug(traceback.format_exc())

    return resp
