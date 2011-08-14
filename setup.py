#!/usr/bin/python

from distutils.core import setup

setup(name='varch',
      version='0.9.1',
      description='Virtual machine generator for ArchLinux',
      author='Thomas S Hatch',
      author_email='thatch45@gmail.com',
      url='https://github.com/thatch45/varch',
      packages=['varch'],
      scripts=['scripts/varch'],
      data_files=[('/etc/varch',
                    ['conf/base.aif',
                     'conf/base-lvm.aif',
                     'conf/base-single.aif',
                     'conf/kde-lvm.aif',
                     'conf/kde-single.aif',
                     'conf/sshon-lvm.aif',
                     'conf/sshon-single.aif',
                     ]),
                   ('/usr/share/man/man1',
                    ['man/varch.1',
                    ]),
                 ],
     )

