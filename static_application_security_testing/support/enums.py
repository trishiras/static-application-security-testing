from enum import Enum


class MixedTypeEnum(Enum):
    # Boolean constants
    SUCCESS = True

    # String constants
    OUTPUT = "output"
    TMP = "tmp"

    # Rules dir
    RULES_DIR = "/usr/src/app/rules"


class ResponseMessage(Enum):
    SEMGREP_MSG = "Semgrep did not return any response"


class STDInput(Enum):
    # To disable Registry rule metrics, use --metrics off.
    SEMGREP = "semgrep --json --quiet --metrics off --no-git-ignore --scan-unknown-extensions --config {rules_dir} --output {output} {target}"
