# Contributor: Thomas S Hatch <thatch45@gmail.com>

pkgname=varch
pkgver=0.8
pkgrel=2
pkgdesc="ArchLinux virtual machine builder"
arch=(any)
url="http://code.google.com/p/varch/"
license=("GPL3")
depends=('python'
         'multipath-tools'
         'aif'
         'qemu')
makedepends=('python')
optdepends=('virtualbox-ose: To enable support for virtualbox vdi images')
optdepends=('libvirtd: To use generated virtual machines with libvirt')
optdepends=('qemu-kvm: Run kvm virtual machines')
options=(!emptydirs)
source=("http://varch.googlecode.com/files/$pkgname-$pkgver.tar.gz")
md5sums=('45094304353b014733ad6531f543f59f')

build() {
  cd $srcdir/$pkgname-$pkgver
    python setup.py install --root=$pkgdir/ --optimize=1
        }
        
