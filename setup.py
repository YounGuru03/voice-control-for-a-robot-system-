"""
Setup script for Voice Control System
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="voice-control-robot-system",
    version="1.0.0",
    author="YounGuru03",
    description="Windows-based offline speech recognition system using AI Agent architecture",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/YounGuru03/voice-control-for-a-robot-system-",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
    install_requires=[
        "openai-whisper>=20231117",
        "numpy>=1.24.3",
        "torch>=2.0.1",
        "torchaudio>=2.0.2",
        "sounddevice>=0.4.6",
        "soundfile>=0.12.1",
        "scipy>=1.11.4",
        "pyyaml>=6.0.1",
    ],
    entry_points={
        'console_scripts': [
            'voice-control=main:main',
        ],
    },
)
