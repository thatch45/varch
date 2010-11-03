'''
A numer of operations may need to be executed - post install - like the
application overlay and automated instalation of AUR packages.
There may also be things that are desired which may be easier to do outside
the scope of the aif file
'''

import subprocess
import os
import sys

class Post:
    '''
    Opperate on post install, pre-finalize opperations
    '''
    def __init__(self, opts, target):
        self.opts = opts
        self.target = target

    def overlay(self):
        '''
        Apply an optional overlay
        '''
        if not self.opts['overlay']:
            return
        if os.path.isdir(self.opts['overlay']):
            c_cmd = 'cp -rp ' + self.opts['overlay'] + '/* '\
                  + self.target
            subprocess.call(c_cmd, shell=True)


