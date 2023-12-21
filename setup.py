# QtFusion, AGPL-3.0 license
from setuptools import setup, find_packages

setup(
    name="QtFusion",  # Name of the library
    version="0.5.3",  # Version number
    author="Seasal Wesley",  # Author's name
    author_email="seasalwesley@gmail.com",  # Author's email
    packages=find_packages(),  # List of packages to include
    include_package_data=True,  # Include non-Python files, such as data files
    install_requires=[  # Dependencies required by the library
        "numpy",  # Dependency on the numpy library
        "opencv-python>=4.5.5.64",  # Dependency on the opencv-python library with a minimum version of 4.5.5.64
        "Pillow>=9.0.1",  # Dependency on the Pillow library with a minimum version of 9.0.1
        "PySide6>=6.4.2",  # Dependency on the PySide6 library with a minimum version of 6.4.2
        "PyYAML>=6.0",  # Dependency on the PyYAML library with a minimum version of 6.0
        "IMcore>=0.2.1"  # Dependency on the IMcore library with a minimum version of 0.2.1
    ],
    license="AGPL-3.0",
    url="https://pypi.org/project/QtFusion/",
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Software Development',
        'Topic :: Software Development :: User Interfaces',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
    ],
    data_files=[('', ['LICENSE'])]

)
