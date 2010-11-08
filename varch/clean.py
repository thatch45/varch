'''
We made quite a mess, time to clean it up!
'''

import os
import subprocess

def umount(nbd, dms):
    '''
    Umounts the mounts
    '''
    u_cmd = 'umount ' + nbd + '*'
    print('Unmounting build environment')
    subprocess.call(u_cmd, shell=True)
    for dm_ in dms:
        u_cmd = 'umount ' + dm_ + '*'
        subprocess.call(u_cmd, shell=True)
    print('restoring swap state')
    subprocess.call('swapoff -a', shell=True)
    subprocess.call('swapon -a', shell=True)

def vgchange(dms):
    '''
    Determintes what volume groups are in the virtual machine and deactivates
    them
    '''
    vgq = "vgdisplay | grep 'VG Name' | awk '{print $3}'"
    vgs = subprocess.Popen(vgq,
            shell=True,
            stdout=subprocess.PIPE).communicate()[0].split()
    for dm_ in dms:
        if vgs.count(os.path.basename(dm_)):
            c_cmd = 'vgchange -a n ' + os.path.basename(dm_)
            subprocess.call(c_cmd, shell=True)

def detatch(nbd):
    '''
    Detatches the image
    '''
    k_cmd = 'kpartx -d ' + nbd
    l_cmd = 'losetup -d ' + nbd
    subprocess.call(k_cmd, shell=True)
    subprocess.call(l_cmd, shell=True)

def convert(fmt, image):
    '''
    Checks to see if the desired image format is something other than raw, then
    execute the propper conversion routine.
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
    if fmt == 'vdi':
        rm_ = False
        outimage = image
        if not image.endswith('vdi'):
            outimage = image + '.vdi'
            rm_ = True
        v_cmd = 'VBoxManage convertfromraw ' + image + ' ' + outimage

        print('Converting to vdi')

        subprocess.call(v_cmd, shell=True)
        if rm_:
            os.remove(image)
