import setuptools

with open('README.md', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='pytrucolib',
    version='0.0.1',
    author='Lautaro Linquiman',
    author_email='lylinquiman@gmail.com',
    description='Libreria',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='softwarebrc.com.ar',
    project_urls={
        'Bug Tracker': '',
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    python_requires='>=3.6',
)
