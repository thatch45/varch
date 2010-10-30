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
source=("http://varch.googlecode.com/files/$pkgname-$pkgver.tar.gz")
md5sums=('4e283a10dda3888366f7c3442ee284f4')

build() {
  cd $srcdir/$pkgname-$pkgver
    python setup.py install --root=$pkgdir/ --optimize=1
        }
        
