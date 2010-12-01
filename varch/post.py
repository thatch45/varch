'''
A numer of operations may need to be executed - post install - like the
application overlay.
There may also be things that are desired which may be easier to do outside
the scope of the aif file.
'''

import subprocess
import os
import sys
import shutil

class Post:
    '''
    Opperate on post install, pre-finalize opperations
    '''
    def __init__(self, opts, target):
        self.opts = opts
        self.target = target
        self._dir = os.path.dirname(self.opts['image'])

    def overlay(self):
        '''
        Apply an optional overlay
        '''
        # I am being lazy, I shouldn't have to shell out here
        if not self.opts['overlay']:
            return
        if os.path.isdir(self.opts['overlay']):
            c_cmd = 'cp -rp ' + self.opts['overlay'] + '/* '\
                  + self.target
            subprocess.call(c_cmd, shell=True)

    def pull_boot('self'):
        '''
        Copy out the kernel and initrd before finalizing the virtual machine
        image
        '''
        kernel = os.path.join(self.target, 'boot/vmlinuz26')
        initcpio = os.path.join(self.target, 'boot/kernel26.img')
        shutil.copy(kernel, os.path.join(self._dir, self.opts['image'] +
            '_vmlinuz26'))
        shutil.copy(initcpio, os.path.join(self._dir, self.opts['image'] +
            '_kernel26.img'))

    def run_post(self):
        '''
        Execute the post routines.
        '''
        self.overlay()
        if self.opts['pull_boot']:
            self.pull_boot()

