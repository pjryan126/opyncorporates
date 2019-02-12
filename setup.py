from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='opyncorporates',
    version='0.0.2',
    description='a Python package for calling the OpenCorporates API',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://opyncorporates.readthedocs.io/en/latest/',
    author='Patrick J. Ryan',
    author_email='pjryan126@gmail.com',
    license='MIT',
    install_requires=[
        'requests'
    ],
    packages=[
        'opyncorporates',
    ],
    test_suite='tests',
    zip_safe=False,
)
