from setuptools import setup

setup(
    name = 'PythonDE',
    description = 'Differential evolution optimization (DE)',
    version = '1.0',
    author = 'Shakib Vedaie',
    author_email = 'shakibv@gmail.com',
    url = 'https://github.com/shakibv/PythonDE',
    packages = ['pythonde'],
    install_requires = ["numpy"],
    classifiers=[
        "Programming Language :: Python",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering"]
    )
