import os
import re
from setuptools import setup

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

if os.getenv("READTHEDOCS") == "True":
    requirements.append("sphinxcontrib-napoleon")
    requirements.append("Pallets-Sphinx-Themes")


with open("quartcord/__init__.py") as f:
    version = re.search(
        r"^__version__\s*=\s*['\"]([^'\"]*)['\"]", f.read(), re.MULTILINE
    ).group(1)


if not version:
    raise RuntimeError("Version is not set.")


with open("README.md") as f:
    readme = f.read()


extras_require = {
    "docs": [
        "sphinx",
    ],
}

packages = [
    "quartcord",
    "quartcord.models",
]

setup(
    name="quartcord",
    author="Sayan Bhattacharyya",
    author_email="sayan@sn1f3rt.me",
    url="https://github.com/Sn1F3rt/quartcord",
    project_urls={
        "Documentation": "https://quartcord.readthedocs.io/en/latest/",
        "Issue tracker": "https://github.com/Sn1F3rt/quartcord/issues",
        "Support": "https://fumes.top/community",
    },
    version=version,
    packages=packages,
    license="MIT",
    description="Discord OAuth2 extension for Quart.",
    long_description=readme,
    long_description_content_type="text/markdown",
    include_package_data=True,
    install_requires=requirements,
    extra_requirements=extras_require,
    python_requires=">=3.8.0",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
)
