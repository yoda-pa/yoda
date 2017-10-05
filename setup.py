from setuptools import setup, find_packages

setup(
    name='yoda',
    version='0.1.0',
    py_modules=['yoda'],
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
    data_files=[('resources', 'resources/*')],
    entry_points='''
        [console_scripts]
        yoda=yoda:cli
    '''
)
