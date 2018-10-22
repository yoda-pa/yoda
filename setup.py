from setuptools import setup, find_packages

setup(
    name='yoda',
    version='0.3.0',
    py_modules=['yoda'],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'Pillow',
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
        'future',
        'speedtest-cli',
        'imageio',
        'requests',
        'pydub',
        'pandas',
        'fuzzywuzzy',
        'python-levenshtein'
    ],
    package_data={'': ['*.txt', '*.lst']},
    entry_points='''
        [console_scripts]
        yoda=yoda:cli
    ''',
    test_suite='nose.collector',
    tests_require=['nose'],
)
