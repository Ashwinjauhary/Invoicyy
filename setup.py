#!/usr/bin/env python3
"""
🧾 Invoice Maker - Setup Script
Alternative installer using setuptools
"""

from setuptools import setup, find_packages
import os

# Read README
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="invoice-maker",
    version="1.0.0",
    author="Ashwin Jauhary",
    author_email="ashwin2431333@gmail.com",
    description="Professional Billing System for Small Businesses",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Ashwinjauhary/Invoicyy",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Office/Business",
        "Topic :: Office/Business :: Financial",
        "Topic :: Office/Business :: Financial :: Point-Of-Sale",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "black>=22.0",
            "flake8>=4.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "invoice-maker=web_app:main",
            "invoicemaker=web_app:main",
        ],
        "gui_scripts": [
            "invoice-maker-gui=web_app:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.png", "*.jpg", "*.ico", "*.html", "*.css", "*.js"],
    },
    zip_safe=False,
    keywords="invoice billing gst accounting pos small-business",
    project_urls={
        "Bug Reports": "https://github.com/Ashwinjauhary/Invoicyy/issues",
        "Source": "https://github.com/Ashwinjauhary/Invoicyy",
        "Documentation": "https://github.com/Ashwinjauhary/Invoicyy/blob/main/README.md",
        "Live Demo": "https://invoicyy.streamlit.app",
    },
)
