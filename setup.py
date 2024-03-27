from setuptools import setup, find_packages, get_dependencies

setup(
    name='My Personal MLOps Utility Package',
    version='0.1',
    packages=find_packages(),
    description='A package for managing Machine Learning Operations for my projects.',
    author='Tushar Sharma',
    author_email='tusharmahalya.com',
    url='https://github.com/tushar-mahalya/MLOps_Utils',
    install_requires=get_dependencies(),
)