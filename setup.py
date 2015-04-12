from setuptools import setup

kwargs = {'name': 'ctSeg',
          'description': 'NCIPHUB Tool for MOIST run segmentation comparison',
          'version': '0.0.4',
          'long_description': open('README.md').read(),
          'author': 'John Evans',
          'author_email': 'john.g.evans.ne@gmail.com',
          'url': 'https://github.com/quintusdias/ctSeg',
          'packages': ['ctSeg'],
          'package_data': {'ctSeg': ['share/*.db']},
          'entry_points': {
              'console_scripts': ['run_ctseg=ctSeg.command_line:run_ctseg',
                                  'make_ctseg_db=ctSeg.command_line:make_db'],
              },
          'install_requires': ['scikit_image>=0.11.3', 'Pillow>=2.7.8'],
          'license': 'MIT'}

setup(**kwargs)
