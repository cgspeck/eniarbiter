from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

with open('requirements-test.txt') as f:
    required_test = [x for x in f.read().splitlines() if not x.startswith('-r')]
    required_test.extend(required)

setup(
    name='eniarbiter',
    description='''
    AWS Elastic Network Interface Arbiter/Assigner
    ''',
    version='1.0.1',
    author='Chris Speck',
    author_email='chris@chrisspeck.com',
    url='https://github.com/cgspeck/eniarbiter',
    download_url = 'https://github.com/cgspeck/eniarbiter/tarball/1.0.1',
    keywords = ['AWS', 'ec2', 'ENI', 'boto'],
    packages=['eniarbiter'],
    entry_points={
        'console_scripts': [
            'eniarbiter = eniarbiter.utilrunner:main'
        ]
    },
    install_requires=required,
    extras_require={
        'tests': required_test
    }
)
