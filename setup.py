
import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='zipfile-dclimplode',
    version="0.0.3.1",
    author='cielavenir',
    author_email='cielartisan@gmail.com',
    description='Monkey patch the standard zipfile module to enable DCL Implode support',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/cielavenir/python-zipfile-ppmd',
    project_urls={
        'Bug Tracker': 'https://github.com/cielavenir/python-zipfile-ppmd/issues',
    },
    keywords='zip zipfile ppmd',
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: System :: Archiving',
        'Topic :: System :: Archiving :: Compression',
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    install_requires=[
        'dclimplode',
    ],
)

