import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="serialgsm",
    version="0.0.1",
    author="Willem Van Iseghem (canihavesomecoffee)",
    author_email="serialgsm@canihavesome.coffee",
    description="Communicate over serial with GSM modems",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/canihavesomecoffee/SerialGSM",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: ISC License",
        "Operating System :: OS Independent",
    ),
)