import sys

import varch.image
import varch.aif
import varch.grub
import varch.clean
import varch.post
import varch.genconf

class VArch:
    '''
    Runs the virtual machine maker.
    '''
    def __init__(self, opts):
        self.opts = opts

    def make_vm(self):
        '''
        Create a virtual machine image.
        '''
        try:
            print('############################################################################')
            print('#                    Creating virtual machine image                        #')
            image = varch.image.Image(self.opts)
            nbd = image.prep_disk()
            aif = varch.aif.AIF(self.opts, nbd)
            print('############################################################################')
            print('#                             Executing AIF                                #')
            print('############################################################################')
            aif.run_aif()
            
            print('############################################################################')
            print('#                        Setting up the bootloader                         #')
            print('############################################################################')
            grub = varch.grub.Grub(self.opts, aif.target, nbd)
            grub.setup_boot()

            print('############################################################################')
            print('#                     Executing post install operations                    #')
            post = varch.post.Post(self.opts, aif.target)
            post.run_post()

            print('############################################################################')
            print('#                     Cleaning up the build environment                    #')
            print('############################################################################')
            varch.clean.umount(nbd, aif.dms)
            varch.clean.vgchange(aif.dms)
            varch.clean.detatch(nbd)
            varch.clean.convert(self.opts['format'], self.opts['image'])
            varch.clean.backup_log()
            if self.opts['kvm_conf']:
                print('############################################################################')
                print('#              Generating virtual machine configuration files              #')
                print('############################################################################')
                genconf = varch.genconf.GenConf(self.opts)
                if self.opts['kvm_conf']:
                    genconf.gen_kvm()

        except varch.aif.AIFException as e:
            print('The following device conflicts were found ' + e.value,
                    file=sys.stderr)
            sys.exit(42)
        except varch.image.ImageException as e:
            print('The image already exists: ' + e.value,
                    file=sys.stderr)
            sys.exit(43)
        except:
            print('############################################################################')
            print('#                     Cleaning up the build environment                    #')
            print('############################################################################')
            varch.clean.umount(nbd, aif.dms)
            varch.clean.vgchange(aif.dms)
            varch.clean.detatch(nbd)
            varch.clean.backup_log()

