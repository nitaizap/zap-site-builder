"""Local replica of a Zap base site for testing `zs push`: Hello Elementor + Elementor + Yoast + Ally + Novamira,
AI Abilities on, and an integration admin `zap-builder` with an application password saved (chmod 600) to
work/zapbase/.novamira-cred. Serve it with:
  php -S 127.0.0.1:8790 -t work/zapbase/wp engine/router.php
then: bin/zs push <slug> --site http://127.0.0.1:8790 --cred-file work/zapbase/.novamira-cred
"""
import urllib.request
import sys, subprocess, secrets, json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'engine'))
import env
from pathlib import Path
W = Path(ROOT) / 'work/zapbase/wp'; W.mkdir(parents=True, exist_ok=True)
URL = 'http://127.0.0.1:8790'
def wp(*a, check=True):
    r = env.run(env.wp_cmd() + [f'--path={W}', *a], check=check); return r.stdout.strip()
env.ensure_db()
NOVAMIRA_ZIP = str(Path(ROOT) / 'work/zapbase/novamira.zip')
if not os.path.exists(NOVAMIRA_ZIP):
    urllib.request.urlretrieve('https://license.dynamic.ooo/api/novamira/download', NOVAMIRA_ZIP)
env.sql("DROP DATABASE IF EXISTS zs_zapbase; CREATE DATABASE zs_zapbase CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
if not (W/'wp-load.php').exists(): wp('core','download','--force')
(W/'wp-config.php').unlink(missing_ok=True)
wp('config','create','--dbname=zs_zapbase',f'--dbuser={env.DB_USER}',f'--dbhost={env.DB_HOST}:{env.DB_PORT}',f'--dbpass={env.DB_PASS}','--skip-check')
wp('config','set','WP_ENVIRONMENT_TYPE','local')
wp('core','install',f'--url={URL}','--title=Basic Site - Zap Group','--admin_user=zapadmin',f'--admin_password={secrets.token_urlsafe(16)}','--admin_email=zapsites@d.co.il','--skip-email')
for p in ('elementor','wordpress-seo','pojo-accessibility'): wp('plugin','install',p,'--activate','--force')
wp('theme','install','hello-elementor','--activate','--force')
wp('plugin','install',NOVAMIRA_ZIP,'--activate','--force')
wp('rewrite','structure','/%postname%/','--hard')
wp('option','update','WPLANG','he_IL'); wp('language','core','install','he_IL',check=False)
# Zap base placeholder home, like the real one
pid = wp('post','create','--post_type=page','--post_status=publish','--post_title=כותרת ראשית עמוד הבית','--porcelain')
wp('option','update','show_on_front','page'); wp('option','update','page_on_front',pid)
# what an admin does once on the BASE site: enable abilities (domain-locked) + integration user + app password
wp('option','update','novamira_ai_abilities_enabled','1'); wp('option','update','novamira_ai_abilities_domain','127.0.0.1')
wp('user','create','zap-builder','builder@zapsites.invalid','--role=administrator','--porcelain')
pw = wp('user','application-password','create','zap-builder','zap-site-builder','--porcelain')
cred = Path(ROOT) / 'work/zapbase/.novamira-cred'; cred.write_text(json.dumps({'user':'zap-builder','app_password':pw})); cred.chmod(0o600)
print('base ready', URL, 'home id', pid)
