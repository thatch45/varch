# Contributor: Thomas S Hatch <thatch45@gmail.com>

pkgname=varch
pkgver=0.7.6
pkgrel=1
pkgdesc="ArchLinux virtual machine builder"
arch=(any)
url="http://code.google.com/p/varch/"
license=("GPL3")
depends=('python'
         'multipath-tools'
         'aif')
makedepends=('python')
optdepends=('virtualbox-ose: To enable support for virtualbox vdi images')
options=(!emptydirs)
source=("http://varch.googlecode.com/files/$pkgname-$pkgver.tar.gz")
md5sums=('8819bcf9eae384790b9c7a3bda1cc61b')

build() {
  cd $srcdir/$pkgname-$pkgver
    python setup.py install --root=$pkgdir/ --optimize=1
        }
        
