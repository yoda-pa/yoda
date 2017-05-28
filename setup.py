from setuptools import setup

setup(
    name='yoda',
    version='0.1.0',
    py_modules=['yoda'],
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
    entry_points='''
        [console_scripts]
        yoda=yoda:cli
    '''
)
