'''
Manage everything from the install to the grub-install
'''
import os
import shutil
import subprocess

class Grub:
    '''
    Manage preparing the environment for grub
    '''
    def __init__(self, opts, target, nbd):
        self.opts = opts
        self.target = target
        self.nbd = nbd

    def _grub_conf(self):
        '''
        Edits the grub config and returns the grub root for the grub install
        '''
        # TODO: Grow up and use a with statement
        lst = os.path.join(self.target, 'boot/grub/menu.lst')
        lines = open(lst, 'r').readlines()
        grub_root = ''
        for ind in range(0, len(lines)):
            if lines[ind].startswith('#'):
                continue
            if lines[ind].startswith('root'):
                grub_root = lines[ind][lines[ind].index('('):]
            if lines[ind].startswith('kernel'):
                s = lines[ind]
                if self.opts['generic']:
                    lines[ind] = s.replace(self.nbd + 'p', '/dev/sda')
                else:
                    lines[ind] = s.replace(self.nbd + 'p', '/dev/vda')
        open(lst, 'w').writelines(lines)
        return grub_root

    def _fstab(self):
        '''
        Edit the fstab with the propper devices!
        '''
        fstab = os.path.join(self.target, 'etc/fstab')
        lines = open(fstab, 'r').readlines()
        for ind in range(0, len(lines)):
            if lines[ind].startswith('#'):
                continue
            if lines[ind].startswith('/dev/mapper/loop'):
                s = lines[ind]
                if self.opts['generic']:
                    lines[ind] = s.replace(self.nbd + 'p', '/dev/sda')
                else:
                    lines[ind] = s.replace(self.nbd + 'p', '/dev/vda')
        open(fstab, 'w').writelines(lines)

    def _copy_stages(self):
        '''
        Copy in the boot stages
        '''
        shutil.copy('/boot/grub/stage1',
                os.path.join(self.target, 'boot/grub/'))
        shutil.copy('/boot/grub/stage2',
                os.path.join(self.target, 'boot/grub/'))


    def _install_grub(self, grub_root):
        '''
        Um... install grub!
        '''
        g_cmd = 'grub --batch --no-floppy --device-map=/dev/null'
        g_lines = 'device (hd0) ' + self.opts['image'] + '\n'\
                + 'root ' + grub_root + '\n'\
                + 'setup (hd0)\n'\
                + 'quit\n'
        print(g_lines)
        g_lines = str.encode(g_lines)

        grub = subprocess.Popen(g_cmd, shell=True, stdin=subprocess.PIPE)
        grub.communicate(g_lines)
        rc = grub.wait()

    def setup_boot(self):
        '''
        Run the routines that will setup booting the virtual machine.
        '''
        grub_root = self._grub_conf()
        self._fstab()
        self._copy_stages()
        self._install_grub(grub_root)
