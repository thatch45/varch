'''
Manages the image, creation, mounting etc.
'''

import subprocess
import sys
import os
import tempfile
import time
import threading

class ImageException(Exception):
    def __init__(self, value):
        self.value = str(value)
    def __str__(self):
        return repr(self.value)

class Image:
    '''
    Manages the image file.
    '''
    def __init__(self, opts):
        self.opts = opts

    def __run_kpartx(self, sec=10):
        '''
        Run kpartx over and over in a loop for time seconds
        '''
        # This is a hack, and one of the worst methods in varch, I need to
        # change this to be more signal oriented - but the change happens in
        # aif, so I don't know quite how to do it yet
        start = int(time.time())
        stop = start
        while stop - start < sec:
            subprocess.call('kpartx -a ' + self.opts['image'], shell=True)
            stop = int(time.time())

    def _create_img(self):
        '''
        Create the image file
        '''
        if os.path.isfile(self.opts['image']):
            raise ImageException(self.opts['image'])
        i_cmd = 'qemu-img create -f raw ' + self.opts['image']\
              + ' ' + self.opts['size']
        subprocess.call(i_cmd, shell=True)

    def _set_loop(self):
        '''
        Binds the image to a loopback device.
        '''
        m_cmd = 'modprobe loop'
        subprocess.call(m_cmd, shell=True)
        m_cmd = 'modprobe dm-mod'
        subprocess.call(m_cmd, shell=True)
        sf_cmd = 'sfdisk ' + self.opts['image'] + ' << EOF\n'\
               + '0,,\nEOF'
        sf_out = subprocess.Popen(sf_cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT).communicate()[0]
        kq_cmd = 'kpartx -l ' + self.opts['image']
        loc = subprocess.Popen(kq_cmd, shell=True,
                stdout=subprocess.PIPE).communicate()[0]
        loc = bytes.decode(loc.split()[4])
        proc = threading.Thread(target=self.__run_kpartx)
        proc.start()
        tgt = os.path.join('/dev/mapper', os.path.basename(loc))
        if not os.path.exists(tgt):
            os.symlink(loc, tgt)
        return tgt


    def prep_disk(self):
        '''
        Prepares the disk, returns the device node holding the image.
        '''
        self._create_img()
        return self._set_loop()
