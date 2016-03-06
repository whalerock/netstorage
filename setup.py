from setuptools import setup

setup(
    name='netstorage',
    description='Human friendly netstorage wrapper',
    author='Matt Chung',
    author_email='mchung@whalerockindustries.com',
    version='0.0.4',
    packages=['netstorage'],
    install_requires=[
        'requests[security]',
        'lxml'
    ]
)
