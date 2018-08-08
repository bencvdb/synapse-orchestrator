#!/usr/bin/env python
# First, we try to use setuptools. If it's not available locally,
# we fall back on ez_setup.
try:
    from setuptools import setup
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup

long_description = ''

install_requires = []
with open('requirements.txt') as requirements_file:
    for line in requirements_file:
        line = line.strip()
        if len(line) == 0:
            continue
        if line[0] == '#':
            continue
        pinned_version = line.split()[0]
        install_requires.append(pinned_version)

setup(
    name='synapse-orchestrator',
    description='Synapse-based orchestrator for GA4GH workflows',
    packages=['synorchestrator'],
    url='https://github.com/Sage-Bionetworks/synapse-orchestrator',
    download_url='https://github.com/Sage-Bionetworks/synapse-orchestrator',
    entry_points={
        'console_scripts': 'orchestrate=synorchestrator.__main__:main'
    },
    package_data={'': ['trs/client.py',
                       'trs/__init__.py',
                       'wes/client.py',
                       'wes/__init__.py',
                       'utils/setup_run.py',
                       'config_files/submission_queue.json',
                       'config_files/stored_templates.json',
                       'config_files/user_submission_example.json',
                       'config.yaml']},
    include_package_data=True,
    long_description=long_description,
    install_requires=install_requires,
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'pytest-cov', 'mock'],
    license='Apache 2.0',
    zip_safe=False,
    author='Sage Bionetworks CompOnc Team',
    author_email='james.a.eddy@gmail.com',
    version='0.1.1'
)
