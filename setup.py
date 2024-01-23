from setuptools import find_packages, setup

setup(
    name='debias',
    version='0.0.1',
    description='Debias for music llm',
    author='debias team',
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    install_requires=[
        # 'numpy',
    ],
    python_requires='>=3.5',
)
