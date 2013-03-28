from distutils.core import setup

packages = ['pygoes', 'pygoes.utils', 'pygoes.xray', 'pygoes.data']
required = ['atpy', 'numpy', 'matplotlib']

setup(
    name='pygoes',
    version='dev',
    author='James Whinfrey',
    author_email='james@conceptric.co.uk',
    url='none',
    description='Tools for importing and manipulating GOES data',
    packages=packages,
    install_requires=required
)