from setuptools import setup, find_packages
import os

# Read the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = f.read().splitlines()

setup(
    name="deeprecon",
    version="1.0.0",
    author="Mohammad Rasol Esfandiari",
    author_email="mrasolesfandiari@gmail.com",
    description="A powerful, modular Python library for comprehensive domain and IP analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DeepPythonist/DeepRecon",
    project_urls={
        "Bug Reports": "https://github.com/DeepPythonist/DeepRecon/issues",
        "Source": "https://github.com/DeepPythonist/DeepRecon",
        "Documentation": "https://github.com/DeepPythonist/DeepRecon#readme",
        "Changelog": "https://github.com/DeepPythonist/DeepRecon/blob/main/CHANGELOG.md",
    },
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'deeprecon': ['locales/*.json'],
    },
    install_requires=requirements,
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-cov>=4.0.0',
            'flake8>=5.0.0',
            'black>=22.0.0',
            'isort>=5.0.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'deeprecon=cli:main',
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Security",
        "Topic :: System :: Networking",
        "Topic :: System :: Systems Administration",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: Name Service (DNS)",
        "Topic :: System :: Monitoring",
        "Environment :: Console",
        "Natural Language :: English",
        "Natural Language :: Persian",
    ],
    keywords=[
        "domain", "ip", "dns", "whois", "ssl", "security", 
        "networking", "reconnaissance", "analysis", "geolocation",
        "penetration-testing", "security-tools", "domain-analysis",
        "ip-analysis", "network-analysis", "cyber-security"
    ],
    python_requires=">=3.8",
    zip_safe=False,
)
