from setuptools import setup

setup(
    name='VOCALOID Announcer Converter',
    version='1.0',
    packages=['vocaloid_announcer'],
    install_requires=['Click', 'xmltodict', 'pydub'],
    entry_points={
        'console_scripts': ['vocaloid_announcer_conv=vocaloid_announcer.cli:cli'],
    })
