from setuptools import setup, find_packages


setup(
    name='yoda',
    version='0.1.0',
    py_modules=['yoda', 'whoosh'],
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
        'unirest'
    ],
    package_data={'': ['*.txt', '*.lst']},
    entry_points='''
        [console_scripts]
        yoda=yoda:cli
    ''',
    test_suite='nose.collector',
    tests_require=['nose'],
)
