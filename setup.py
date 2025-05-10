# setup.py is used to build our application as a package, which can be deployed further.
from setuptools import find_packages, setup
from typing import List

hyphen_e_dot='-e .'
def get_requirements(file_path:str)->List[str]:
    '''
    this function will return the list of requirements
    '''
    requirements=[]
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        [req.replace('\n',"") for req in requirements]

        if hyphen_e_dot in requirements:
            requirements.remove(hyphen_e_dot)

setup(name = 'mlproject1',
      version = '0.0.1',
      author='Aparna',
      author_email='aparnajoseph.2024@gmail.com',
      packages=find_packages(),
    #   install_requires=['pandas','numpy','seaborn']
      install_requires=get_requirements('requirements.txt')
        )