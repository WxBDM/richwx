from setuptools import setup, find_packages
from pathlib import Path

# The directory containing this file
HERE = Path(__file__).parent
README = (HERE / "README.md").read_text()

version = '0.0.2'

setup(
        name = 'richwx',
        version = version,
        packages = find_packages(),
        license='apache-2.0',
        entry_points = {
                'console_scripts': [
                'richwx = cli.cli:cli', # cli_folder.cli_file:cli_function
                ],
        },
        install_requires = [
                'Click',
                'rich',
                'nwsapy'
        ],
        url = 'https://github.com/WxBDM/richwx', 
        download_url = f'https://github.com/WxBDM/richwx/archive/refs/tags/v{version}.tar.gz', 
        python_requires = '>=3.8',
        classifiers=[
                'Development Status :: 3 - Alpha',
                'Intended Audience :: Developers',   
                'Topic :: Software Development :: Build Tools',
                'License :: OSI Approved :: Apache Software License',
                'Programming Language :: Python :: 3.8',
                'Programming Language :: Python :: 3.9',
                'Programming Language :: Python :: 3.10'
                ],
        author = 'Brandon Molyneaux', 
        email = 'bran.moly@gmail.com',  
        long_description=README,
        long_description_content_type="text/markdown",
     )