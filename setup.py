import setuptools
import os
from setuptools import setup


pkg_dir = os.path.dirname(os.path.realpath(__file__))

# package description
with open(os.path.join(pkg_dir, 'README.md')) as f:
    long_description = f.read()
with open(os.path.join(pkg_dir, 'requirements.txt')) as f:
    required = f.read().splitlines()
with open(os.path.join(pkg_dir, 'PACKAGENAME')) as f:
    pkg_name = f.read().strip().strip('\n')
with open(os.path.join(pkg_dir, 'VERSION')) as f:
    version = f.read().strip().strip('\n')
    
setup(
    name=pkg_name,
    version=version,
    author="Sanne Korzec",
    author_email="sanne.korzec@example.com",
    description="A small example python package for openshift",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Alliander/frank-test-python.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=required,
    entry_points={
        'console_scripts': [
            'start_application = sanne_test_python.app:main'
        ]
    }
)
