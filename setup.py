from setuptools import setup

setup(
    name='dude',
    version='0.0.0',
    py_modules=['dude'],
    install_requires=[
        'Click',
        'pychalk',
        'apiai'
    ],
    entry_points='''
        [console_scripts]
        dude=dude:cli
    '''
)
