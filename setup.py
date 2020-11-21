from distutils.core import setup

setup(name='xit',
      version='0.1.4',
      description='eXcel Interaction Tool: A tool that makes capture/collection easy',
      author='Callum Fleming',
      author_email='howzitcallum@gmail.com',
      url='https://hcal.cf',
      install_requires=[
          'openpyxl',
          'pyinstaller',
          'pillow',
          'cryptography',
          'bcrypt',
          'tkcalendar',
          'babel'
      ],
      )
