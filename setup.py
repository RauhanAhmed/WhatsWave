from setuptools import setup, find_packages

HYPEN_E_DOT = "-e ."

def getRequirements(requirementsPath: str) -> list[str]:
    with open(requirementsPath) as file:
        requirements = file.read().split("\n")
    requirements.remove(HYPEN_E_DOT)
    return requirements

setup(
    name="WhatsappX",
    author="Rauhan Ahmed Siddiqui",
    author_email="rauhaan.siddiqui@gmail.com",
    version="0.1",
    packages=find_packages(),
    install_requires=getRequirements(requirementsPath="requirements.txt")
)