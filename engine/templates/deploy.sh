#!/usr/bin/env bash
# Deploy {{NAME}} ({{DOMAIN}}) — built {{DATE}} by the Zap site builder.
#
# Usage, from the folder this script is in:
#   ./deploy.sh --docroot /home/<user>/htdocs/<domain> --db-name NAME --db-user USER --db-pass PASS \
#               [--db-host localhost] [--url https://other-domain.co.il] [--owner <unix-user>]
#
# Needs: wp-cli on the server (CloudPanel ships it), an empty database, an empty docroot.
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
DB_HOST=localhost; URL=""; OWNER=""; DOCROOT=""; DB_NAME=""; DB_USER=""; DB_PASS=""
while [ $# -gt 0 ]; do
  case "$1" in
    --docroot) DOCROOT="$2"; shift 2;;
    --db-name) DB_NAME="$2"; shift 2;;
    --db-user) DB_USER="$2"; shift 2;;
    --db-pass) DB_PASS="$2"; shift 2;;
    --db-host) DB_HOST="$2"; shift 2;;
    --url) URL="$2"; shift 2;;
    --owner) OWNER="$2"; shift 2;;
    *) echo "unknown option $1"; exit 1;;
  esac
done
[ -n "$DOCROOT" ] && [ -n "$DB_NAME" ] && [ -n "$DB_USER" ] || { sed -n '4,9p' "$0"; exit 1; }
command -v wp >/dev/null || { echo "wp-cli not found (https://wp-cli.org)"; exit 1; }

if [ -e "$DOCROOT/wp-config.php" ]; then echo "refusing: $DOCROOT already has a WordPress"; exit 1; fi
mkdir -p "$DOCROOT"
echo "→ copying files to $DOCROOT"
cp -a "$here/public_html/." "$DOCROOT/"

cfg="$DOCROOT/wp-config.php"
esc() { printf '%s' "$1" | sed -e 's/[\/&|]/\\&/g' -e "s/'/\\\\'/g"; }
sed -i -e "s|__DB_NAME__|$(esc "$DB_NAME")|" -e "s|__DB_USER__|$(esc "$DB_USER")|" \
       -e "s|__DB_PASSWORD__|$(esc "$DB_PASS")|" -e "s|__DB_HOST__|$(esc "$DB_HOST")|" "$cfg"

WP() { if [ -n "$OWNER" ] && [ "$(id -u)" = 0 ]; then sudo -u "$OWNER" wp --path="$DOCROOT" "$@"; else wp --path="$DOCROOT" "$@"; fi; }
[ -n "$OWNER" ] && chown -R "$OWNER":"$OWNER" "$DOCROOT"

echo "→ importing database"
WP db import "$here/database.sql"
if [ -n "$URL" ] && [ "$URL" != "{{DOMAIN}}" ]; then
  echo "→ moving from {{DOMAIN}} to $URL"
  WP search-replace "{{DOMAIN}}" "$URL" --all-tables --precise --skip-columns=guid --report-changed-only
  WP elementor replace_urls "{{DOMAIN}}" "$URL" || true
fi
PASS="$(head -c 24 /dev/urandom | base64 | tr -dc 'A-Za-z0-9' | head -c 20)"
WP user update zapadmin --user_pass="$PASS" --skip-email >/dev/null
WP rewrite flush --hard >/dev/null 2>&1 || WP rewrite flush
WP elementor flush-css >/dev/null 2>&1 || true
WP yoast index --reindex --skip-confirmation >/dev/null 2>&1 || true
WP cache flush >/dev/null 2>&1 || true

echo
echo "✓ {{NAME}} deployed. Indexing: {{INDEX}}"
echo "  admin: ${URL:-{{DOMAIN}}}/wp-admin   user: zapadmin   password: $PASS   (store it in the password manager now)"
echo "  next: LAUNCH-CHECKLIST.md"
