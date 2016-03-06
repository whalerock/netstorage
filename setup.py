import re
from setuptools import setup


__version__ = ''
__version__ = ''
with open('netstorage/__init__.py', 'r') as fd:
    reg = re.compile(r'__version__ = [\'"]([^\'"]*)[\'"]')
    for line in fd:
        m = reg.match(line)
        if m:
            __version__ = m.group(1)
            break

setup(
    name='netstorage',
    description='A python wrapper for Akamais Nestorage API',
    author='Matt Chung',
    author_email='mchung@whalerockindustries.com',
    version=__version__,
    packages=['netstorage'],
    install_requires=[
        'requests[security]',
        'lxml'
    ]
)
