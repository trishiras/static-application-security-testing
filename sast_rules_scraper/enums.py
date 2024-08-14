import enum


class MixedTypeEnum(enum.Enum):
    CI = "/ci"
    QA = "/qa"
    TMP = "tmp"
    RULE = "rule"
    SYNC = "main"
    RULES = "rules"
    RUN_CMD = "start"
    LICENSE = "LICENSE"
    HOME_DIR = "/usr/src/app"
    SAST_RULES_GIT_URL = (
        "https://gitlab.com/gitlab-org/security-products/sast-rules.git"
    )
    WATCH_DIR = [
        "c",
        "go",
        "java",
        "scala",
        "rules",
        "python",
        "csharp",
        "javascript",
    ]
