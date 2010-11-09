'''
We made quite a mess, time to clean it up!
'''

import os
import shutil
import time
import subprocess

def umount(nbd, dms):
    '''
    Umounts the mounts
    '''
    u_cmd = 'umount ' + nbd + '*'
    print('Unmounting build environment')
    subprocess.getoutput(u_cmd)
    for dm_ in dms:
        u_cmd = 'umount ' + dm_ + '*'
        subprocess.getoutput(u_cmd)
    print('restoring swap state')
    subprocess.getoutput('swapoff -a')
    subprocess.getoutput('swapon -a')

def vgchange(dms):
    '''
    Determintes what volume groups are in the virtual machine and deactivates
    them
    '''
    vgq = "vgdisplay | grep 'VG Name' | awk '{print $3}'"
    vgp = subprocess.Popen(vgq,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
    vgout = vgp.communicate()
    vgs = bytes.decode(vgout[0]).split()
    for dm_ in dms:
        if vgs.count(os.path.basename(dm_)):
            c_cmd = 'vgchange -a n ' + os.path.basename(dm_)
            subprocess.getoutput(c_cmd)

def detatch(nbd):
    '''
    Detatches the image
    '''
    k_cmd = 'kpartx -d ' + nbd
    l_cmd = 'losetup -d ' + nbd
    subprocess.getoutput(k_cmd)
    subprocess.getoutput(l_cmd)
    if os.path.islink(nbd):
        os.remove(nbd)

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

def backup_log():
    '''
    Makes a backup of the mkinitcpio and the pacman log used by aif.
    '''
    tag = str(int(time.time()))
    p_src = '/var/log/aif/pacman.log'
    p_dst = p_src + '.' + tag + '.bak'
    m_src = '/var/log/aif/mkinitcpio.log'
    m_dst = m_src + '.' + tag + '.bak'

    if os.path.isfile(p_src):
        shutil.move(p_src, p_dst)
    if os.path.isfile(m_src):
        shutil.move(m_src, m_dst)

