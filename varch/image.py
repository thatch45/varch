'''
Manages the image, creation, mounting etc.
'''

import subprocess
import sys
import os
import tempfile
import time
import threading

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
            print('The image file already exists, EXITING.',
                    file=sys.stderr)
            sys.exit(42)
        i_cmd = 'qemu-img create -f raw ' + self.opts['image']\
              + ' ' + self.opts['size']
        subprocess.call(i_cmd, shell=True)

    def _set_nbd(self):
        '''
        Abstracts the image as a qemu network block device.
        '''
        m_cmd = 'modprobe nbd max_part=63'
        subprocess.call(m_cmd, shell=True)
        nbd = ''
        for fn_ in os.listdir('/dev'):
            if not fn_.startswith('nbd'):
                continue
            fn_ = os.path.join('/dev', fn_)
            try:
                open(fn_, 'r').read(1)
            except:
                continue
            nbd = fn_
        if not nbd:
            print('''No network block devices are available, please detatch a
                    network block device and try again''', file=sys.stderr)
            sys.exit(42)
        s_cmd = 'qemu-nbd -c ' + nbd + ' ' + self.opts['image']
        subprocess.call(s_cmd, shell=True)
        return nbd

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
        subprocess.call(sf_cmd, shell=True)
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
