from setuptools import setup, find_packages

setup(
    name='yoda',
    version='0.2.0',
    py_modules=['yoda'],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'pychalk',
        'apiai',
        'emoji',
        'pyyaml',
        'lepl',
        'pycrypto',
        'pyspeedtest',
        'forex-python',
        'dulwich',
        'PyGithub',
        'unirest',
        'future'
    ],
    dependency_links=[
        "git+ssh://git@github.com/tirkarthi/unirest-python.git@f341d8e93304f42cff0b10813e2cc8d2ae121b13#egg=unirest-0.2.1"
    ],
    package_data={'': ['*.txt', '*.lst']},
    entry_points='''
        [console_scripts]
        yoda=yoda:cli
    ''',
    test_suite='nose.collector',
    tests_require=['nose'],
)
