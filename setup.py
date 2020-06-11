import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="micropython-tinkerlib",
    version="0.0.1",
    author="Martin Dybdal",
    author_email="dybber@di.ku.dk",
    description="DESCRIPTION",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Datanauterne/micropython-tinkerlib",
    packages=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: Implementation :: MicroPython",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        # PyPI lack's an OS classifier appropriate for MicroPython
    ],
    python_requires='>=3.4',
)
