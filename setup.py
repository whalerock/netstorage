from setuptools import setup

setup(
    name='netstorage',
    author='Matt Chung',
    author_email='mchung@whalerockindustries.com',
    version='0.0.1',
    description='Human friendly netstorage wrapper',
    packages=['netstorage'],
    install_requires=['requests[security]']
)
