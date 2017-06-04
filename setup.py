from setuptools import setup


VERSION = open('VERSION').read()

setup(
    name='roda',
    version=VERSION,
    packages=['roda'],
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=['nose'],
    author='x6doooo',
    author_email='x6doooo@gmail.com',
    description='...',
    license='MIT',
)
