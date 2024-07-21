from setuptools import find_packages, setup
from typing import List

HYPHEN_E_DOT = '-e .'

def get_requirements(file_path:str) -> List[str]:

    # This function will return the list of requirements

    requirements = []

    with open(file_path) as file_obj:
        requirements = file_obj.readlines() # but this also reads the \n at the end of each line, hence we need to remove it.

        # So, we try to replace this \n with a space using .replace() function
        requirements = [req.replace("\n","") for req in requirements]

        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)
        
    return requirements


setup(
name = 'Student Performance',
version = '0.0.1',
author = 'Sai Aditya',
author_email = '21mm01022@iitbbs.ac.in',
packages = find_packages(),
install_requires = get_requirements('requirements.txt')
)