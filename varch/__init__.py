import sys

import varch.image
import varch.aif
import varch.grub
import varch.clean
import varch.post

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
        # TODO: Need to wrap these function calls with try/except blocks to
        # catch failures and keystrokes so that the environment can be properly
        # cleaned up in the event of a failure.
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

