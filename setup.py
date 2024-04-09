from setuptools import find_packages,setup

setup(
name='mcqgenerator',
version='0.0.1',
author='Edu V',
author_email="edukondaluvallapuneni@gmail.com",
install_requires=["openai","langchain","streamlit","python-dotenv","PyPDF2","langchain_openai"],
packages=find_packages()
)