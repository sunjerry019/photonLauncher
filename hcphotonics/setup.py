from setuptools import setup
from setuptools import find_packages
setup(name='hcphotonics',
      version='0.1',
      description='Utilities and tools for HC Photonics Lab',
      url='https://github.com/sunjerry019/photonLauncher',
      author='HC Photonics',
      author_email='hcphotonics@gmail.com',
      license='Apache 2.0',
      packages=find_packages(),
      install_requires=[
          'matplotlib',
          'numpy',
          'pyserial',
          'python-usbtmc',
          'Gnuplot',
          'libusb1'
    ]   
)

