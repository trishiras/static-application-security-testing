import os
import git
import uuid
import enums
import logger
import shutil
import traceback


def clone_repo(git_url: str) -> str:
    """
    Clones a repository from the given git URL to a temporary directory and returns the directory path.

    Parameters:
        git_url (str): The URL of the git repository to clone.

    Returns:
        str: The path of the directory where the repository is cloned.
    """
    session = str(uuid.uuid4())
    _dir = os.path.join(
        enums.MixedTypeEnum.HOME_DIR.value,
        enums.MixedTypeEnum.TMP.value,
        session,
    )
    git.Repo.clone_from(
        git_url,
        _dir,
        branch=enums.MixedTypeEnum.SYNC.value,
    )
    logger.logger.debug(f"Cloned repository from {git_url} to {_dir}")
    return _dir


def scrape_data(repo_dir: str) -> list[tuple[str, str]]:
    """
    Scrapes data from the given repository directory by walking through the directory structure.

    Parameters:
        repo_dir (str): The directory path to scrape data from.

    Returns:
        list[tuple[str, str]]: A list of tuples containing the root path and file path of the scraped data.
    """
    scrape_data = []
    try:
        for root, _, files in os.walk(repo_dir):
            if enums.MixedTypeEnum.CI.value in root:
                continue
            if enums.MixedTypeEnum.QA.value in root:
                continue
            for filepath in files:
                if not (
                    filepath.startswith(enums.MixedTypeEnum.RULE.value)
                    and not filepath.endswith(enums.MixedTypeEnum.LICENSE.value)
                ):
                    continue

                scrape_data.append((root, filepath))

        logger.logger.debug(f"Scraped data from {repo_dir}")
    except Exception as err:
        logger.logger.error(err)
        logger.logger.debug(traceback.format_exc())

    return scrape_data


def copy_rules(
    source_file_list: str,
    destination_folder: str,
    repo_dir: str,
):
    """
    A function that copies rules from a source file list to a destination folder while maintaining the directory structure relative to the repository directory.

    Parameters:
        source_file_list (str): List of source files to copy.
        destination_folder (str): Path to the destination folder where rules will be copied.
        repo_dir (str): The root directory of the repository.

    Returns:
        None
    """
    try:
        for root, filepath in source_file_list:
            if not os.path.exists(
                os.path.join(
                    destination_folder,
                    os.path.relpath(
                        root,
                        repo_dir,
                    ),
                )
            ):
                shutil.copytree(
                    root,
                    os.path.join(
                        destination_folder,
                        os.path.relpath(
                            root,
                            repo_dir,
                        ),
                    ),
                )

        logger.logger.debug(
            f"Copied rules from {source_file_list} to {destination_folder}"
        )
    except Exception as err:
        logger.logger.error(err)
        logger.logger.debug(traceback.format_exc())


def empty_directory(directory: str):
    """
    A function that empties the given directory by deleting all files and subdirectories.

    Parameters:
        directory (str): The path of the directory to empty.

    Returns:
        None
    """
    # Verify that the directory exists
    if not os.path.exists(directory):
        logger.logger.debug(f"Directory '{directory}' does not exist.")
        return

    # Remove all files and subdirectories in the directory
    for root, dirs, files in os.walk(directory, topdown=False):

        for file in files:
            file_path = os.path.join(root, file)
            os.remove(file_path)

        for dir in dirs:
            dir_path = os.path.join(root, dir)
            shutil.rmtree(dir_path)
