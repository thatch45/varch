import varch.image
import varch.aif
import varch.grub
import varch.clean

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
        image = varch.image.Image(self.opts)
        nbd = image.prep_disk()
        aif = varch.aif.AIF(self.opts, nbd)
        aif.run_aif()
        
        grub = varch.grub.Grub(self.opts, aif.target, nbd)
        grub.setup_boot()

        varch.clean.umount(nbd)
        varch.clean.detatch(nbd)
        varch.clean.convert(self.opts['format'], self.opts['image'])
