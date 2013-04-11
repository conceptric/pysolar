from distutils.core import setup

packages = ['pysolar', 
            'pysolar.utils', 
            'pysolar.data', 
            'pysolar.files', 
            'pysolar.visualisation']
required = ['atpy', 'numpy']

setup(
    name='pysolar',
    version='dev',
    author='James Whinfrey',
    author_email='james@conceptric.co.uk',
    url='none',
    description='Tools for processing solar observation data',
    packages=packages,
    install_requires=required
)