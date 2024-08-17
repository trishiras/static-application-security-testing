from setuptools import setup, find_packages
from static_application_security_testing.__version__ import __version__


setup(
    name="static_application_security_testing",
    version=__version__,
    author="sumit",
    author_email="sumit@mail.com",
    description="static-application-security-testing",
    long_description=open("README.md").read(),
    classifiers=[
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.12",
    packages=find_packages(exclude=["sast_rules_scraper"]),
    entry_points={
        "console_scripts": [
            "static_application_security_testing=static_application_security_testing.main:main",
        ],
    },
)
