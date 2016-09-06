from setuptools import setup

setup(
    name='VOCALOID Announcer Converter',
    version='2.0',
    packages=['vocaloid_announcer'],
    install_requires=['Click', 'xmltodict', 'pydub', 'six'],
    tests_require=['nose', 'coverage'],
    test_suite='nose.collector',
    entry_points={
        'console_scripts': ['vocaloid_announcer_conv=vocaloid_announcer.cli:cli'],
    })
