import setuptools
from pkg_resources import parse_requirements  # noqa

with open('README.md', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='PyTrucoEngine',
    version='1.0.1',
    author='Lautaro Linquiman',
    author_email='lylinquiman@gmail.com',
    description='Motor de truco argentino escrito en python',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://softwarebrc.com.ar/',
    project_urls={
        'Bug Tracker': 'https://github.com/Ymil/libPyTruco',
    },
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    python_requires='>=3.6',
    # install_requires=parse_requirements('requirements.txt'),
)
