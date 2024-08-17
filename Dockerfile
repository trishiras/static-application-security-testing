# Rule scraping build
FROM python:3.12-alpine AS rules_layer


# Arguments
ARG RUN_CMD


# Update the package index and install git
RUN apk update && \
    apk add --no-cache git


# Changing to workdir for task execution
WORKDIR /usr/src/app


# Copy the current directory contents into the container
COPY . .


# Install dependencies and the package
RUN pip install --no-cache-dir --root-user-action=ignore -r ./sast_rules_scraper/requirements.txt


# Running the scraper app
RUN python3 ./sast_rules_scraper/main.py ${RUN_CMD}



##********************** MAIN BUILD **********************##
FROM python:3.12-alpine


# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


# Set the working directory in the container
WORKDIR /usr/src/app


# Copy the rules
COPY --from=rules_layer /usr/src/app/rules /usr/src/app/rules


# Copy the current directory contents into the container
COPY . .


# Install dependencies and the package
RUN pip install --no-cache-dir --root-user-action=ignore -r requirements.txt && \
    python setup.py install && \
    rm -rf /root/.cache/pip


# Run static-application-security-testing when the container launches
ENTRYPOINT ["static_application_security_testing"]