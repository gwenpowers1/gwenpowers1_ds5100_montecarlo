from setuptools import setup, find_packages

setup(
    name='ds5100_montecarlo',
    version='1.0.0',
    author = 'Gwen Powers',
    author_email = 'gp8cf@virginia.edu',
    url = 'https://github.com/gwenpowers1/gwenpowers1_ds5100_montecarlo',
    license = 'MIT',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
    ],
)
