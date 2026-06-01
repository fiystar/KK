"""Setup configuration for KK package"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="kk-trading",
    version="1.0.0",
    author="fiystar",
    author_email="67568400+fiystar@users.noreply.github.com",
    description="Professional K-line recognition and analysis tool using Binance API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fiystar/KK",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business :: Financial :: Investment",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "kk-analyze=main:main",
        ],
    },
    keywords="kline candlestick trading binance analysis technical-indicators pattern-recognition",
    project_urls={
        "Bug Reports": "https://github.com/fiystar/KK/issues",
        "Source": "https://github.com/fiystar/KK",
        "Documentation": "https://github.com/fiystar/KK#readme",
    },
    include_package_data=True,
    zip_safe=False,
)
