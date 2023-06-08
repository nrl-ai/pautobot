import re

from setuptools import find_packages, setup


def get_version():
    """Get package version from app_info.py file"""
    filename = "pautobot/app_info.py"
    with open(filename, encoding="utf-8") as f:
        match = re.search(
            r"""^__version__ = ['"]([^'"]*)['"]""", f.read(), re.M
        )
    if not match:
        raise RuntimeError(f"{filename} doesn't contain __version__")
    version = match.groups()[0]
    return version


def get_install_requires():
    """Get python requirements based on context"""
    install_requires = [
        "langchain>=0.0.194",
        "gpt4all>=0.3.0",
        "chromadb>=0.3.23",
        "llama-cpp-python>=0.1.59",
        "urllib3>=2.0.2",
        "pdfminer.six>=20221105",
        "unstructured>=0.6.6",
        "extract-msg>=0.41.1",
        "tabulate>=0.9.0",
        "pandoc>=2.3",
        "pypandoc>=1.11",
        "tqdm>=4.65.0",
        "python-multipart>=0.0.6",
        "fastapi==0.96.0",
        "SQLAlchemy==2.0.15",
        "alembic==1.11.1",
        "requests",
    ]

    return install_requires


def get_long_description():
    """Read long description from README"""
    with open("README.md", encoding="utf-8") as f:
        long_description = f.read()
    long_description = long_description.replace(
        "![PAutoBot](./docs/screenshot.png)",
        "![PAutoBot](https://raw.githubusercontent.com/nrl-ai/pautobot/main/docs/screenshot.png)",
    )
    long_description = long_description.replace(
        '<img alt="PAutoBot" style="width: 128px; max-width: 100%; height: auto;" src="./docs/pautobot.png"/>',
        '<img alt="PAutoBot" style="width: 128px; max-width: 100%; height: auto;" src="https://raw.githubusercontent.com/nrl-ai/pautobot/main/docs/pautobot.png"/>',
    )
    return long_description


setup(
    name="pautobot",
    version=get_version(),
    packages=find_packages(),
    description="Private AutoGPT Robot - Your private task assistant with GPT!",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Viet-Anh Nguyen",
    author_email="vietanh.dev@gmail.com",
    url="https://github.com/vietanhdev/pautobot",
    install_requires=get_install_requires(),
    license="Apache License 2.0",
    keywords="Personal Assistant, Automation, GPT, LLM, PrivateGPT",
    classifiers=[
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3 :: Only",
    ],
    package_data={
        "pautobot": [
            "pautobot/frontend-dist/**/*",
            "pautobot/frontend-dist/*",
        ]
    },
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "pautobot=pautobot.app:main",
            "pautobot.ingest=pautobot.ingest:main",
        ],
    },
)
