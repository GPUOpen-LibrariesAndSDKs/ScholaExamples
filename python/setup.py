# Copyright (c) 2025 Advanced Micro Devices, Inc. All Rights Reserved.
from setuptools import setup, find_packages
import sys


def get_version():
    # PATCH: allow for version to be passed on the command line
    KWD = "--version="
    opt = [x for x in sys.argv if x.startswith(KWD)]
    if len(opt) > 0:
        version = opt[0][len(KWD):]
        sys.argv.remove(opt[0])
        return version
    else:
        return "1.0"

if __name__ == "__main__":
    # load readme
    desc = None
    with open("../README.md", "rt") as readme:
        desc = readme.read()
        assert desc != None, "failed to load readme"
        desc = desc.split("## Contributing")[0]

    setup(  
        name='schola_examples',  
        version=get_version(),  
        author="Advanced Micro Devices, Inc.",
        author_email="alexcann@amd.com",
        description="Example Environments Built Using Schola",
        long_description=desc,
        long_description_content_type="text/markdown",
        packages=find_packages(),  
        install_requires=[  
            'gymnasium==0.29.1',  
            'schola'  
        ],
        extras_require={
            'test' : ['pytest', 'pytest-cov', 'pytest-xdist', 'pytest-timeout','pytest-mock','schola[test]'],
        },  
        package_data={  
            'schola_examples': ['bin/**/*','bin/*'], 
        },  
        classifiers=[    
            'Programming Language :: Python :: 3',    
            'Programming Language :: Python :: 3.9',    
            'Operating System :: Microsoft :: Windows',
            'Operating System :: POSIX :: Linux'  
        ],    
        python_requires='>=3.9',  
        platforms=['Windows', 'Linux']  
    )  
