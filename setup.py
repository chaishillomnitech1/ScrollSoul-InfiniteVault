"""
ScrollSoul-InfiniteVault Setup Configuration
Eternal nexus for multi-layer scaling frameworks
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="scrollsoul-infinitevault",
    version="1.0.0",
    author="ScrollSoul Contributors",
    description="Eternal nexus for multi-layer scaling frameworks, Spotify royalty harvesting, and AI-driven recursive loops",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chaishillomnitech1/ScrollSoul-InfiniteVault",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.31.0",
        "web3>=6.0.0",
        "python-dotenv>=1.0.0",
        "pyyaml>=6.0",
        "numpy>=1.24.0",
    ],
)
