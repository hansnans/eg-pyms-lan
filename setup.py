from setuptools import setup

with open('eg_pms2_lan/README.md', "r") as fh:
    long_description = fh.read()

setup(
    name='eg_pyms_lan',
    version='2.0',
    packages=['eg_pms2_lan'],
long_description    author='Marios Christodoulou',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author_email='marios.christodoulou@fkie.fraunhofer.de',
    description='CLI and module for controlling EG-PMS2-LAN multiplug socket',
    scripts=['eg_pms2_lan/pymslan']
)
