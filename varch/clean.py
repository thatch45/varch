'''
We made quite a mess, time to clean it up!
'''

import os
import subprocess

def umount(nbd):
    '''
    Umounts the mounts
    '''
    u_cmd = 'umount ' + nbd + '*'
    print('Unmounting build environment')
    subprocess.call(u_cmd, shell=True)
    print('restoring swap state')
    subprocess.call('swapoff -a', shell=True)
    subprocess.call('swapon -a', shell=True)

def detatch(nbd):
    '''
    Detatches the qemu-nbd
    '''
    k_cmd = 'kpartx -d ' + nbd
    l_cmd = 'losetup -d ' + nbd
    subprocess.call(k_cmd, shell=True)
    subprocess.call(l_cmd, shell=True)

def convert(fmt, image):
    '''
    Checks to see if the desired image format is qcow2, it it is, run qemu
    convert.
    '''
    if fmt == 'qcow2':
        rm_ = False
        outimage = image
        if not image.endswith('qcow2') or not image.endswith('qcow'):
            outimage = image + '.qcow2'
            rm_ = True
        q_cmd = 'qemu-img convert -O qcow2 ' + image + ' ' + outimage

        print('Converting to qcow2')

        subprocess.call(q_cmd, shell=True)
        if rm_:
            os.remove(image)
