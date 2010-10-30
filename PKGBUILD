# Contributor: Thomas S Hatch <thatch45@gmail.com>

pkgname=varch
pkgver=0.7.0
pkgrel=1
pkgdesc="ArchLinux virtual machine builder"
arch=(any)
url="http://code.google.com/p/varch/"
license=("GPL3")
depends=('python'
         'multipath-tools'
         'aif')
makedepends=('python')
options=(!emptydirs)
source=('http://varch.googlecode.com/files/varch-0.6.9.tar.gz')
md5sums=('6e2dd8b4b2294407693de7cd76ec8998')

build() {
  cd $srcdir/$pkgname-$pkgver
    python setup.py install --root=$pkgdir/ --optimize=1
        }
        
