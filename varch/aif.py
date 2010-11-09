'''
Manages the aif files, takes one as input and modifies it to make the virtual
image.
'''

import os
import sys
import tempfile
import time
import subprocess

class AIFException(Exception):
    '''
    Raise this exception if there is any problem with the aif system
    '''
    def __init__(self, value):
        self.value = str(value)
    def __str__(self):
        return repr(self.value)

class AIF:
    '''
    Manages the aif files, and executes the aif application
    '''
    def __init__(self, opts, nbd):
        self.opts = opts
        self.nbd = nbd
        self.aif, self.target = self.__mk_conf()
        self.dms = self.__verify_env()

    def __mk_conf(self):
        '''
        Generate the configuration file passed to AIF, returns the path to the
        modified aif file
        '''
        target = tempfile.mkdtemp()
        lines = open(self.opts['conf'], 'r').readlines()
        err = 0
        for index in range(0, len(lines)):
            lines[index] = lines[index].replace('GRUB_DEVICE=/dev/sda',
                    'GRUB_DEVICE=' + self.nbd)
            lines[index] = lines[index].replace('GRUB_DEVICE=/dev/vda',
                    'GRUB_DEVICE=' + self.nbd)
            lines[index] = lines[index].replace('/dev/sda ', self.nbd + ' ')
            lines[index] = lines[index].replace('/dev/sda', self.nbd + 'p')
            lines[index] = lines[index].replace('/dev/vda ', self.nbd + ' ')
            lines[index] = lines[index].replace('/dev/vda', self.nbd + 'p')
            if lines[index].count('/dev/vd') or lines[index].count('/dev/sd') or lines[index].count('/dev/hd'):
                print('''References are made in the aif file to a second disk,
                        only one disk is supported, EXITING''',
                        file=sys.stderr)
                sys.exit()
        lines.append('var_TARGET_DIR=' + target  + '\n')
        lines.append('PACMAN_TARGET="pacman --root $var_TARGET_DIR --config /tmp/pacman.conf"\n')
        if not self.opts['generic']:
            lines.extend(['\nworker_mkinitcpio ()\n',
            '{\n',
            'sed -i s,MODULES=\\",MODULES=\\"virtio\\ virtio_blk\\ virtio_pci\\ , $var_TARGET_DIR/etc/mkinitcpio.conf\n',
            'run_mkinitcpio\n',
            '}\n'])
        aif = '/tmp/working.aif'
        open(aif, 'w+').writelines(lines)
        return aif, target

    def __verify_env(self):
        '''
        Verify that none of the disk volumes slated for work by aif exist on
        the system.
        '''
        print('############################################################################')
        print('#Checking that the aif configuration will be safe for the underlying system#')
        time.sleep(1)
        dms = []
        conflict = []
        for line in open(self.aif, 'r').readlines():
            if line.count('/dev/mapper'):
                dev = line.split()[0]
                if dev.count(self.nbd):
                    continue
                dms.append(dev)

        for dm_ in dms:
            if os.path.exists(dm_):
                conflict.append(dm_)

        vgq = "vgdisplay | grep 'VG Name' | awk '{print $3}'"
        vgp = subprocess.Popen(vgq,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
        vgout = vgp.communicate()
        vgs = vgout[0]
        vgs = bytes.decode(vgs).split()

        for dm_ in dms:
            if vgs.count(os.path.basename(dm_)):
                conflict.append(dm_)

        if conflict:
            raise AIFException(conflict)
        return dms
            
    def run_aif(self):
        '''
        If this in run without the correct files and ops in place you may
        destroy your system.  YOU HAVE BEEN WARNED!
        '''
        a_cmd = 'aif -p automatic -c ' + self.aif
        subprocess.call(a_cmd, shell=True)
