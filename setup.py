from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name = "mlops",
    version = 0.1,
    author = "Abdul Samad",
    author_email = "abdul.samad.ali.abbasi.r678@gmail.com",
    description = "MLOPS PROJECT",
    packages = find_packages(),
    install_requires = requirements,
    python_requires = ">=3.7"
)