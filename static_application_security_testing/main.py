import os
import json
from argparse import Namespace
from static_application_security_testing.services import semgrep
from static_application_security_testing.core.logger import logger
from static_application_security_testing.core.input import parse_args
from static_application_security_testing.support.enums import MixedTypeEnum


class StaticApplicationSecurityTesting(object):
    def __init__(
        self,
        arguments: Namespace,
    ):
        self.data = {}
        self.target = arguments.target
        self.output_via = arguments.output_via
        self.webhook = arguments.webhook
        self.output_file_path = arguments.output_file_path

    def run(self):

        logger.info(
            f"Started generating static application security testing report for target :- {self.target}"
        )

        if self.webhook:
            logger.info(f"Webhook URL :- {self.webhook}")

        if self.output_file_path:
            logger.info(f"Output file path :- {self.output_file_path}")

        output_dir = os.path.join(
            os.getcwd(),
            MixedTypeEnum.OUTPUT.value,
        )
        tmp_dir = os.path.join(
            os.getcwd(),
            MixedTypeEnum.TMP.value,
        )
        if not os.path.isdir(output_dir):
            os.mkdir(output_dir)
        if not os.path.isdir(tmp_dir):
            os.mkdir(tmp_dir)

        semgrep_response = semgrep.run(
            target=self.target,
        )

        if semgrep_response.success:
            self.data = semgrep_response.data
        else:
            logger.error(semgrep_response.message)

        with open(self.output_file_path, "w") as fp:
            json.dump(self.data, fp, indent=4, default=str)

        logger.info(
            f"Finished generating static application security testing report for target :- {self.target}"
        )


def main():

    arguments, unknown = parse_args()

    static_application_security_testing = StaticApplicationSecurityTesting(
        arguments=arguments
    )
    static_application_security_testing.run()
