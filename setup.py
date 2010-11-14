#!/usr/bin/python

from distutils.core import setup

setup(name='varch',
      version='0.7.9',
      description='Virtual machine generator for ArchLinux',
      author='Thomas S Hatch',
      author_email='thatch45@gmail.com',
      url='http://code.google.com/p/enterprise-archlinux/',
      packages=['varch'],
      scripts=['scripts/varch'],
      data_files=[('/etc/varch',
                    ['conf/base.aif',
                     'conf/base-lvm.aif',
                     'conf/base-single.aif',
                     'conf/kde-lvm.aif',
                     'conf/kde-single.aif',
                     'sshon-lvm.aif',
                     'sshon-single.aif',
                     ]),
                 ],
     )

