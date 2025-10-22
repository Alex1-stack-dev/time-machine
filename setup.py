from setuptools import setup, find_packages

setup(
    name="time-machine",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        'PyQt5>=5.15.0',
        'pyserial>=3.5',
        'reportlab>=3.6.8',
        'python-dotenv>=0.19.0',
    ],
    entry_points={
        'console_scripts': [
            'time-machine=main:main',
        ],
    },
    author="Alexander Murphy",
    author_email="alexander_m113@outlook.com",
    description="Professional race timing application",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Professional Athletes",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
    ],
