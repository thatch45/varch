# Contributor: Thomas S Hatch <thatch45@gmail.com>

pkgname=varch
pkgver=0.8.2
pkgrel=3
pkgdesc="ArchLinux virtual machine builder"
arch=(any)
url="http://code.google.com/p/varch/"
license=("GPL3")
depends=('python>=3.1'
         'multipath-tools'
         'aif'
         'qemu')
optdepends=('virtualbox-ose: To enable support for virtualbox vdi images'
            'libvirtd: To use generated virtual machines with libvirt'
            'qemu-kvm: Run kvm virtual machines')
options=(!emptydirs)
source=("http://varch.googlecode.com/files/${pkgname}-${pkgver}.tar.gz")
md5sums=('f85bcd40a4501776f6c07123964526fd')

package() {
  cd ${srcdir}/${pkgname}-${pkgver}
  python setup.py install --root=${pkgdir}/ --optimize=1
}
        
