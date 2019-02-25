import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="therewasanattempt",
    version="1.0.0-rc1",
    author="Francis Lavoie-Renaud",
    author_email="francislr@gmail.com",
    description="Django app that logs authentication attempts to database",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/francislr/coding-challenge-login-api",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
