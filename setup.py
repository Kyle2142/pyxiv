import re

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('pyxiv/__init__.py', 'r') as fd:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', fd.read(), re.MULTILINE).group(1)
if not version:
    raise RuntimeError('Cannot find version information')

setup(
    name='Pyxiv',
    packages=['pyxiv'],
    version=version,
    description='Pixiv API for Python (with 6.x AppAPI supported)',
    long_description='Pixiv API for Python (with 6.x AppAPI supported): https://github.com/Kyle2142/pyxiv (forked from https://github.com/upbit/pixivpy)',
    long_description_content_type='text/markdown',
    author='kyle2142',
    author_email='Kyle-2142@outlook.com',
    install_requires=['aiohttp', 'asyncio'],
    url='https://github.com/Kyle2142/pyxiv',
    download_url='https://github.com/Kyle2142/pyxiv/releases',
    keywords=['pixiv', 'api', 'pyxiv'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5'
)
