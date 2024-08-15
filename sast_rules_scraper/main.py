import os
import sys
import enums
import utils
import logger


def main():

    logger.logger.info("Starting sast rules scraper.")
    rules_dir = os.path.join(
        os.getcwd(),
        enums.MixedTypeEnum.RULES.value,
    )
    tmp_dir = os.path.join(
        os.getcwd(),
        enums.MixedTypeEnum.TMP.value,
    )
    if not os.path.isdir(rules_dir):
        os.mkdir(rules_dir)
    if not os.path.isdir(tmp_dir):
        os.mkdir(tmp_dir)
    logger.logger.info(f"{rules_dir} and {tmp_dir} directories created successfully.")

    # Cloning sast rules repo
    logger.logger.info("Cloning sast rules repo.")
    repo_dir = utils.clone_repo(git_url=enums.MixedTypeEnum.SAST_RULES_GIT_URL.value)

    # Generating list of rules files to copy rules
    logger.logger.info("Generating list of rules files to copy rules.")
    gitlab_list_of_rule_files = utils.scrape_data(repo_dir=repo_dir)

    # Creating path where rules files will be copied
    logger.logger.info("Creating path where rules files will be copied.")
    destination = os.path.join(
        enums.MixedTypeEnum.HOME_DIR.value,
        enums.MixedTypeEnum.RULES.value,
    )

    # Copying gitlab-sast rules files to scanner sast rules folder
    logger.logger.info("Copying gitlab-sast rules files to scanner sast rules folder.")
    utils.copy_rules(
        source_file_list=gitlab_list_of_rule_files,
        destination_folder=destination,
        repo_dir=repo_dir,
    )

    # Get temporary directory path and deleting it's content
    logger.logger.info("Deleting temporary directory.")
    tmp_dir_path = os.path.join(
        enums.MixedTypeEnum.HOME_DIR.value,
        enums.MixedTypeEnum.TMP.value,
    )
    utils.empty_directory(
        directory=tmp_dir_path,
    )

    ### FINISHED SUCCESSFULLY ###
    logger.logger.info("###-------------FINISHED SUCCESSFULLY-------------###")


if __name__ == "__main__":
    input_text = sys.argv[1]
    if input_text == enums.MixedTypeEnum.RUN_CMD.value:
        main()
    else:
        logger.logger.error(
            f"Invalid input !!!. Please enter '{enums.MixedTypeEnum.RUN_CMD.value}'"
        )
        sys.exit(1)
