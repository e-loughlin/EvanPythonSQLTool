from setuptools import setup, find_packages

setup(
    name='evanpythonsqltool',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'sqlalchemy',
        'numpy',
        'scipy',
        'matplotlib',
        'ibis-framework',
    ],
    description='A Python library to streamline SQL-related tasks and enhance workflow efficiency for data scientists and engineers.',
    author='Evan Loughlin',
    author_email='evan.m.loughlin@gmail.com',
    url='https://github.com/e-loughlin/evanpythonsqltool',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    include_package_data=True,
    zip_safe=False,
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)
