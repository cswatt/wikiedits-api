from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("wikiedits/api.py", "r", encoding="utf-8") as f:
    for line in f:
        if line.startswith("__version__"):
            version = line.split("=")[1].strip().strip('"')
            break

setup(
    name="wikiedits-api",
    version=version,
    author="Cecilia Wat-Kim",
    author_email="ceciliawatt@gmail.com",
    description="A Python client library for accessing Wikipedia editor analytics from the Wikimedia Analytics API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cswatt/wikiedits-api",
    project_urls={
        "Bug Tracker": "https://github.com/cswatt/wikiedits-api/issues",
        "Documentation": "https://github.com/cswatt/wikiedits-api#readme",
        "Source Code": "https://github.com/cswatt/wikiedits-api",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: Wiki",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Markup",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.20.0",
        "python-dateutil>=2.8.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-mock>=3.6.0",
        ],
    },
    keywords="wikipedia, wikimedia, analytics, api, editing, statistics, data",
    include_package_data=True,
    zip_safe=False,
)