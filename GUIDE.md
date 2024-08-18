## Guide for Static Application Security Testing (SAST) Tool

This guide provides detailed instructions on how to build, run, and use the Static Application Security Testing (SAST) Tool designed to scan for security vulnerabilities in source code using Semgrep. The tool is designed to generate reports based on rules scraped from a GitLab repository.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Project Structure](#project-structure)
3. [Building the Docker Image](#building-the-docker-image)
4. [Running the Docker Container](#running-the-docker-container)
5. [Tool Usage](#tool-usage)
6. [Troubleshooting](#troubleshooting)
7. [Additional Information](#additional-information)

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- Docker
- Git (optional, for cloning the repository)

## Project Structure

```
static_application_security_testing/
├── .dockerignore
├── .gitignore
├── Dockerfile
├── GUIDE.md
├── README.md
├── requirements.txt
├── setup.py
|
├── sast_rules_scraper/
│   ├── __init__.py
│   ├── enums.py
│   ├── logger.py
│   ├── main.py
│   ├── requirements.txt
│   └── urils.py
|
└── static_application_security_testing/
    ├── __init__.py
    ├── __version__.py
    ├── main.py
    |
    ├── core/
    |   ├── __init__.py
    |   ├── input.py
    |   ├── logger.py
    |   └── models.py
    |
    ├── service/
    |   ├── __init__.py
    |   └── semgrep.py
    |
    └── support/
        ├── __init__.py
        └── enums.py
```

## Building the Docker Image

1. Open a terminal and navigate to the project directory:

   ```bash
   cd path/to/static-application-security-testing
   ```

2. Build the Docker image using the following command:

   ```bash
   sudo docker build --build-arg RUN_CMD="start" --no-cache . -f Dockerfile -t static-application-security-testing:latest
   ```

   This command builds a Docker image named static-application-security-testing based on the instructions in the Dockerfile.

## Running the Docker Container

To run the Static Application Security Testing Tool inside a Docker container, use the following command structure:

```bash
sudo docker run --rm -it -v $(pwd)/output:/output -v /path/to/scan:/scan static-application-security-testing:latest [arguments]
```

Replace `[arguments]` with the actual arguments for the tool.

### Explanation of Docker run options:

- `--rm`: Automatically remove the container when it exits.
- `-it`: Run container in interactive mode.
- `-v $(pwd)/output:/output`: Mount the local `output` directory to `/output` in the container.
- `-v /path/to/scan:/scan`: Mount the directory to be scanned to `/scan` in the container.
- `secret-exposure-analysis`: The name of the Docker image to run.
- `static-application-security-testing:latest`: The name of the Docker image to run.

## Tool Usage

The Static Application Security Testing Tool accepts several command-line arguments:

- `-t, --target`: (Required) Target as path to scan.
- `-ov, --output-via`: (Required) Specify output method: "file" or "webhook".
- `-w, --webhook`: Webhook URL (required if output_via is "webhook").
- `-o, --output`: File path for output (required if output_via is "file").
- `-l, --log`: Log level (DEBUG or ERROR, default is DEBUG).

### Example Commands:

1. Scan a local directory and output to a file:
   ```bash
    sudo docker run --rm -it -v $(pwd)/output:/output -v /path/to/scan:/scan static-application-security-testing:latest -t /scan -ov file -o /output/results.json
   ```

2. To enter the container for debugging or exploration:
   ```bash
    sudo docker run -it --entrypoint /bin/sh static-application-security-testing:latest
   ```


Note: When using file output or scanning local directories, you need to mount volumes to access the results or scan targets from your host machine.

## Troubleshooting

1. **Permission Issues**: If you encounter permission problems when writing to mounted volumes, you may need to adjust the permissions or use a named volume.

2. **Network Issues**: Ensure your Docker network settings allow the container to access the target network or webhook URL.

3. **Missing Requirements**: If the build fails due to missing requirements, check that your `requirements.txt` file is up to date and includes all necessary dependencies.

4. **Rule Scraping Issues**: If there are problems with rule scraping, ensure that the GitLab repository is accessible and that the scraping script is functioning correctly.


## Additional Information

- The tool uses Python 3.12 as specified in the Dockerfile.
- The tool integrates Semgrep for static code analysis. For detailed information about Semgrep's capabilities, refer to its documentation or use the semgrep --help command inside the container.
- The SAST Tool scrapes rules from the GitLab SAST Rules Repository during the Docker build process. https://gitlab.com/gitlab-org/security-products/sast-rules.git

### Semgrep Command Options

Semgrep provides several commands and options:

- `scan`: Run semgrep rules on files
- `ci`: The recommended way to run semgrep in CI
- `install-semgrep-pro`: Install the Semgrep Pro Engine
- `login`: Obtain and save credentials for semgrep.dev
- `logout`: Remove locally stored credentials to semgrep.dev
- `lsp`: Start the Semgrep LSP server (useful for IDEs)
- `publish`: Upload rule to semgrep.dev
- `show`: Show various information about Semgrep
- `test`: Test the rules
- `validate`: Validate the rules


For a complete list of options, use semgrep --help inside the container.

```
Usage: semgrep [OPTIONS] COMMAND [ARGS]...

  To get started quickly, run `semgrep scan --config auto`

  Run `semgrep SUBCOMMAND --help` for more information on each subcommand

  If no subcommand is passed, will run `scan` subcommand by default

Options:
  -h, --help  Show this message and exit.

Commands:
  ci                   The recommended way to run semgrep in CI
  install-semgrep-pro  Install the Semgrep Pro Engine
  login                Obtain and save credentials for semgrep.dev
  logout               Remove locally stored credentials to semgrep.dev
  lsp                  Start the Semgrep LSP server (useful for IDEs)
  publish              Upload rule to semgrep.dev
  scan                 Run semgrep rules on files
  show                 Show various information about Semgrep
  test                 Test the rules
  validate             Validate the rules
```

For more information or to report issues, please refer to the project's documentation or repository.