from setuptools import setup, find_packages

setup(
    name='ds5100_montecarlo',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
    ],
)