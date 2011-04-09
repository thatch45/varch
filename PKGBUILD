# Maintainer: Thomas S Hatch <thatch45@gmail.com>

pkgname=varch
pkgver=0.9.0
pkgrel=1
pkgdesc="ArchLinux virtual machine builder"
arch=(any)
url="https://github.com/thatch45/varch"
license=("GPL3")
depends=('python>=3.1'
         'multipath-tools'
         'aif'
         'qemu')
optdepends=('virtualbox: To enable support for virtualbox vdi images'
            'libvirtd: To use generated virtual machines with libvirt'
            'qemu-kvm: Run kvm virtual machines')
options=(!emptydirs)
source=("http://varch.googlecode.com/files/${pkgname}-${pkgver}.tar.gz")
md5sums=('366909e966ccff0593c4df0664559c45')

package() {
  cd ${srcdir}/${pkgname}-${pkgver}
  python setup.py install --root=${pkgdir}/ --optimize=1
}
        
