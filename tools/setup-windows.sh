#!/usr/bin/env bash
# Optional: run the builder on a Windows machine (Git Bash). Portable PHP + MariaDB + WP-CLI into .tools/.
# Cloud sessions do not need this (bin/setup-cloud.sh).
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p .tools && cd .tools
PHP_ZIP=$(curl -sL https://windows.php.net/downloads/releases/ | grep -oE 'php-8\.3\.[0-9]+-nts-Win32-vs16-x64\.zip' | sort -uV | tail -1)
MDB=$(curl -s https://archive.mariadb.org/ | grep -oE 'mariadb-11\.4\.[0-9]+' | sort -uV | tail -1)
[ -d php ] || { curl -sSLo php.zip "https://windows.php.net/downloads/releases/$PHP_ZIP"; mkdir -p php; unzip -qo php.zip -d php; }
[ -d "$MDB-winx64" ] || { curl -sSLo mariadb.zip "https://archive.mariadb.org/$MDB/winx64-packages/$MDB-winx64.zip"; unzip -qo mariadb.zip; }
[ -f wp-cli.phar ] || curl -sSLo wp-cli.phar https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar
[ -f php/cacert.pem ] || curl -sSLo php/cacert.pem https://curl.se/ca/cacert.pem
if [ ! -f php/php.ini ]; then
  cp php/php.ini-development php/php.ini
  for e in mysqli pdo_mysql gd mbstring openssl curl zip intl fileinfo exif sodium; do sed -i "s/^;extension=$e\$/extension=$e/" php/php.ini; done
  sed -i 's#^;extension_dir = "ext"#extension_dir = "ext"#; s/^memory_limit = .*/memory_limit = 512M/' php/php.ini
  ca="$(cd php && pwd -W)/cacert.pem"; printf '\ncurl.cainfo = "%s"\nopenssl.cafile = "%s"\n' "$ca" "$ca" >> php/php.ini
fi
py -m pip install -q pillow playwright
echo "done. Try: bin/zs doctor"
