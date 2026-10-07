#!/usr/bin/env bash
# Environment setup for Claude Code on the web (Ubuntu 24.04, runs as root, cached ~7 days).
# Paste this one line into the environment's "Setup script" field:
#     bash bin/setup-cloud.sh
# Network access for the environment must be "Full" (wordpress.org, downloads.wordpress.org,
# playwright CDN, fonts are vendored so Google Fonts is NOT needed).
set -uo pipefail
log() { echo "[zap-setup] $*"; }

export DEBIAN_FRONTEND=noninteractive
log "apt packages"
apt-get update -qq
PHPV=$(php -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;' 2>/dev/null || echo 8.3)
apt-get install -y -qq mariadb-server mariadb-client \
  "php$PHPV-cli" "php$PHPV-mysql" "php$PHPV-gd" "php$PHPV-mbstring" "php$PHPV-xml" "php$PHPV-zip" \
  "php$PHPV-intl" "php$PHPV-curl" "php$PHPV-bcmath" unzip >/dev/null || log "apt had warnings"

log "wp-cli"
if ! command -v wp >/dev/null; then
  curl -sSLo /usr/local/bin/wp https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar && chmod +x /usr/local/bin/wp
fi

log "mariadb user"
(service mariadb start || service mysql start) >/dev/null 2>&1
for i in $(seq 1 20); do mariadb -e 'select 1' >/dev/null 2>&1 && break; sleep 1; done
mariadb -e "CREATE USER IF NOT EXISTS 'zs'@'localhost' IDENTIFIED BY 'zs';
            CREATE USER IF NOT EXISTS 'zs'@'127.0.0.1' IDENTIFIED BY 'zs';
            GRANT ALL ON *.* TO 'zs'@'localhost'; GRANT ALL ON *.* TO 'zs'@'127.0.0.1'; FLUSH PRIVILEGES;" || log "db user step failed"

log "python deps"
python3 -m pip install -q --break-system-packages pillow playwright 2>/dev/null || python3 -m pip install -q pillow playwright
python3 -m playwright install --with-deps chromium >/dev/null 2>&1 || log "playwright browser install failed (screenshots/QA need it)"

log "warm the WordPress download cache"
mkdir -p /tmp/zs-warm && wp core download --path=/tmp/zs-warm --allow-root --quiet >/dev/null 2>&1 || true
for p in elementor wordpress-seo pojo-accessibility; do wp plugin install "$p" --path=/tmp/zs-warm --allow-root --quiet >/dev/null 2>&1 || true; done

log "done"
exit 0
