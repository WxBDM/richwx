from setuptools import setup, find_packages

setup(
        name = 'richwx',
        packages = find_packages(),
        entry_points = {
                'console_scripts': [
                'richwx = cli.cli:cli', # cli_folder.cli_file:cli_function
                ],
        },
        install_requires = [
                'Click',
                'rich',
                'nwsapy'
        ]
     )