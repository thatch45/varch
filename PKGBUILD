# Contributor: Thomas S Hatch <thatch45@gmail.com>

pkgname=varch
pkgver=0.8.1
pkgrel=1
pkgdesc="ArchLinux virtual machine builder"
arch=(any)
url="http://code.google.com/p/varch/"
license=("GPL3")
depends=('python'
         'multipath-tools'
         'aif'
         'qemu')
makedepends=('python')
optdepends=('virtualbox-ose: To enable support for virtualbox vdi images'
            'libvirtd: To use generated virtual machines with libvirt'
            'qemu-kvm: Run kvm virtual machines')
options=(!emptydirs)
source=("http://varch.googlecode.com/files/$pkgname-$pkgver.tar.gz")
md5sums=('3d842f42333b696ff73fbc5324c1d54b')

build() {
  cd $srcdir/$pkgname-$pkgver
    python setup.py install --root=$pkgdir/ --optimize=1
        }
        
