#!/usr/bin/python

from distutils.core import setup

setup(name='virtualarch',
      version='0.7.8',
      description='Virtual machine generator for ArchLinux',
      author='Thomas S Hatch',
      author_email='thatch45@gmail.com',
      url='http://code.google.com/p/enterprise-archlinux/',
      packages=['varch'],
      scripts=['scripts/varch'],
      data_files=[('/etc/varch',
                    ['conf/base.aif',
                     'conf/base-lvm.aif'])],
     )

