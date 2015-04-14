from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

with open('requirements-test.txt') as f:
    required_test = f.read().splitlines()

setup(
    name='ENI Arbiter',
    description='''
    AWS Elastic Network Interface Arbiter
    ''',
    version='0.8.0',
    author='Chris Speck',
    author_email='cgspeck@gmail.com',
    url='http://www.chrisspeck.com/',
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
