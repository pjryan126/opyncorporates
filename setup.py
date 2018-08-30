from setuptools import setup

setup(
    name='opyncorporates',
    version='0.1',
    description='a Python package for calling the OpenCorporates API',
    url='https://github.com/pjryan126/opyncorporates.git',
    author='Patrick J. Ryan',
    author_email='pjryan126@gmail.com',
    license='GPL 3.0',
    packages=[
        'opyncorporates',
        'pyyaml',
        'requests'
    ],
    test_suite='tests',
    zip_safe=False,
)
