from setuptools import setup

setup(name='libsearch',
      version='0.1',
      description='libsearch',
      url='',
      author='Team Bit65',
      author_email='',
      license='',
      packages=['libsearch'],
      install_requires=[
            'filemagic',
            'elasticsearch>=6.0.0,<7.0.0'
      ],
      zip_safe=False)