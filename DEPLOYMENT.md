# Django Deployment Guide for SMALL.PL Hosting

## Prerequisites
- SSH access to SMALL.PL hosting
- Django project with `requirements.txt` file
- **Binexec** option enabled in hosting panel
- Domain (optional - you can use subdomain {LOGIN}.smallhost.pl)

---

## 0. Adding Custom Domain (Optional)

### Step 1: DNS Configuration at Domain Provider

1. Log in to your domain management panel at your registrar (e.g., OVH, GoDaddy, Namecheap)
2. Go to **DNS** or **DNS Zone** settings
3. Remove or replace existing nameservers
4. Add SMALL.PL nameservers:
   ```
   dns1.small.pl
   dns2.small.pl
   ```
5. Save changes

**Important:** DNS propagation can take from a few minutes to **12 hours**. During this time, the domain may not work.

### Step 2: Adding Domain in SMALL.PL Panel

1. Log in to SMALL.PL panel (https://panel.smallhost.pl)
2. Go to **DNS Zones** tab
3. Click **Add DNS Zone**
4. Enter your domain (e.g., `mywebsite.com`)
5. Save changes

**Wait for DNS propagation** (check with `nslookup mywebsite.com` or at https://dnschecker.org)

### Step 3: Creating Website for Domain

1. In SMALL.PL panel, go to **WWW Websites**
2. Click **Add Website**
3. Select your domain from the dropdown list
4. Choose type: **Python**
5. After saving, the domain folder will automatically appear on the server:
   ```
   /usr/home/{LOGIN}/domains/{mywebsite.com}/
   ```

---

## 1. Website Configuration in Panel

1. Log in to DevilWEB panel (https://panel.smallhost.pl)
2. Go to **WWW Websites** → **Add Website**
3. Choose type: **Python**
4. Set interpreter to: **Python 3.11** (or 3.12 if available)
5. Set interpreter path:
   ```
   /usr/home/{LOGIN}/.virtualenvs/venv_projectv1/bin/python
   ```
   *(fill this in later, after creating virtualenv)*

---

## 2. SSH Connection

```bash
ssh {LOGIN}@s3.small.pl
```

---

## 3. Creating Directory Structure

```bash
# Navigate to domains directory
cd domains

# Navigate to your domain directory
cd {LOGIN}.smallhost.pl
# or if you have custom domain:
# cd mywebsite.com

# Return to home directory
cd ~

# Create directory for virtual environments
mkdir -p .virtualenvs
```

---

## 4. Creating Virtual Environment

```bash
cd .virtualenvs

# Create virtualenv with Python 3.11
virtualenv venv_projectv1 -p /usr/local/bin/python3.11

# Activate environment
source /usr/home/{LOGIN}/.virtualenvs/venv_projectv1/bin/activate
```

After activation, you'll see `(venv_projectv1)` at the beginning of the command line.

---

## 5. Preparing Project Directory

```bash
# Navigate to domain directory
cd ~/domains/{DOMAIN}

# Create public_python directory (if it doesn't exist)
mkdir -p public_python

# Create public/static directory
mkdir -p public/static
mkdir -p public/media
```

---

## 6. Uploading Project Files

### Option A: Via SFTP/SCP
Upload all project files to:
```
/usr/home/{LOGIN}/domains/{DOMAIN}/public_python/
```

Structure should look like this:
```
public_python/
├── manage.py
├── requirements.txt
├── ProjectName/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── app/
└── ...
```

### Option B: Via Git (if you have a repository)
```bash
cd ~/domains/{DOMAIN}/public_python
git clone https://github.com/{user}/{repo}.git .
```

---

## 7. Installing Dependencies

```bash
# Make sure virtualenv is activated
source /usr/home/{LOGIN}/.virtualenvs/venv_projectv1/bin/activate

# Navigate to project directory
cd ~/domains/{DOMAIN}/public_python

# Install packages
pip install -r requirements.txt
```

**Verify Django installation:**
```bash
python -c "import django; print(django.__file__)"
```

Should show path in virtualenv, e.g.:
```
/usr/home/{LOGIN}/.virtualenvs/venv_projectv1/lib/python3.11/site-packages/django/__init__.py
```

---

## 8. Configuring settings.py

Edit `ProjectName/settings.py` file:

```bash
nano ProjectName/settings.py
```

### Changes to implement:

```python
from pathlib import Path
import os

# BASE_DIR as Path (not string!)
BASE_DIR = Path(__file__).resolve().parent.parent

# Production settings
DEBUG = False  # IMPORTANT: disable debug in production!
ALLOWED_HOSTS = ['{YOUR-DOMAIN}', 'www.{YOUR-DOMAIN}', '{LOGIN}.smallhost.pl']

# Static and media files
STATIC_URL = '/static/'
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(BASE_DIR, 'public', 'static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'public', 'media')

STATICFILES_DIRS = [
    BASE_DIR / 'static',  # if you have static folder in project
]

# SECRET_KEY - in production use environment variable or generate new one!
# SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'temporary-key-change-in-production')
```

---

## 9. Creating passenger_wsgi.py File

```bash
cd ~/domains/{DOMAIN}/public_python
nano passenger_wsgi.py
```

Paste the following content (adjust `{LOGIN}` and project name):

```python
import sys, os

# Path to virtualenv - ADJUST {LOGIN}
VENV_PATH = '/usr/home/{LOGIN}/.virtualenvs/venv_projectv1'
sys.path.insert(0, os.path.join(VENV_PATH, 'lib', 'python3.11', 'site-packages'))

# Add project directory to PYTHONPATH
sys.path.append(os.getcwd())

# Django project name - ADJUST if different
os.environ['DJANGO_SETTINGS_MODULE'] = "ProjectName.settings"

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

**Save file:** `Ctrl+O`, `Enter`, `Ctrl+X`

---

## 10. Creating static Directory (if it doesn't exist)

```bash
# Create static directory in project (if you don't have it)
mkdir -p ~/domains/{DOMAIN}/public_python/static
```

---

## 11. Database Migrations

```bash
# Make sure you're in virtual environment
source /usr/home/{LOGIN}/.virtualenvs/venv_projectv1/bin/activate

# Navigate to project directory
cd ~/domains/{DOMAIN}/public_python

# Create migrations
python manage.py makemigrations main

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput
```

---

## 12. Creating Superuser

```bash
python manage.py createsuperuser
```

You'll be prompted for:
- Username (login)
- Email (can be empty, press Enter)
- Password (you won't see characters while typing)
- Password (again) - repeat password

---

## 13. Updating Configuration in WWW Panel

1. Return to DevilWEB panel
2. **WWW Websites** → **Manage** (for your domain)
3. Set **interpreter path**:
   ```
   /usr/home/{LOGIN}/.virtualenvs/venv_projectv1/bin/python
   ```
4. Save changes

---

## 14. Application Restart

### From SSH level:
```bash
devil www restart {DOMAIN}
```

### Or from panel:
**WWW Websites** → **Manage** → **Restart**

---

## 15. SSL Certificate Configuration (HTTPS)

### Step 1: Go to SSL Panel

1. Log in to SMALL.PL panel (https://panel.smallhost.pl)
2. Go to **SSL** tab

### Step 2: Select WWW Websites

1. Click on server IP address (e.g., **128.204.223.38**)
2. You'll see a list of all websites on this server

### Step 3: Managing Certificate for Domain

1. Find your domain on the list
2. Click **Manage** for selected domain
3. In SSL certificates section, select **Let's Encrypt**
4. Click **Generate Certificate**
5. Wait for certificate generation (usually a few seconds)

### Step 4: SSL Verification

1. After certificate generation, refresh the page
2. Visit your domain using **https://** (e.g., `https://mywebsite.com`)
3. Check if padlock icon appears in browser (indicates secure connection)

**Important:** 
- Let's Encrypt certificate is valid for 90 days
- SMALL.PL automatically renews certificate before expiration
- If you want to force HTTPS, add to Django `settings.py`:
  ```python
  # Force HTTPS (for production)
  SECURE_SSL_REDIRECT = True
  SESSION_COOKIE_SECURE = True
  CSRF_COOKIE_SECURE = True
  ```

---

## 16. Verification

1. Open browser and visit your domain (https://{DOMAIN})
2. Check if site works
3. Check if padlock icon (SSL) is visible
4. Visit `/admin` and log in with superuser credentials
5. Check logs in case of errors:
   ```bash
   tail -50 ~/domains/{DOMAIN}/logs/error.log
   ```

---

## Troubleshooting

### Error "No module named django":
```bash
# Check if Django is in virtualenv
source /usr/home/{LOGIN}/.virtualenvs/venv_projectv1/bin/activate
pip list | grep -i django

# If not there, reinstall
pip install django
```

### BASE_DIR Error:
Make sure in `settings.py`:
```python
BASE_DIR = Path(__file__).resolve().parent.parent  # DON'T use os.path.dirname!
```

### Site doesn't load CSS/JS:
```bash
# Make sure collectstatic was executed
python manage.py collectstatic --noinput

# Check permissions
chmod -R 755 ~/domains/{DOMAIN}/public/static
```

### Restart doesn't help:
```bash
# Force restart via restart.txt
mkdir -p ~/domains/{DOMAIN}/public_python/tmp
touch ~/domains/{DOMAIN}/public_python/tmp/restart.txt
```

### Domain doesn't work after DNS change:
```bash
# Check DNS propagation
nslookup {DOMAIN}

# Or online: https://dnschecker.org
# Wait up to 12h for full propagation
```

### SSL certificate doesn't generate:
- Make sure DNS is properly configured and verified
- Check if domain is accessible via HTTP (without SSL)
- Try again after a few minutes
- Check logs in SSL panel

---

## Useful Commands

```bash
# Activate virtualenv
source /usr/home/{LOGIN}/.virtualenvs/venv_projectv1/bin/activate

# Restart application
devil www restart {DOMAIN}

# Check logs
tail -50 ~/domains/{DOMAIN}/logs/error.log

# Check configuration
devil www info {DOMAIN}

# Migrations
python manage.py migrate

# Collectstatic
python manage.py collectstatic --noinput

# Check DNS propagation
nslookup {DOMAIN}
dig {DOMAIN}
```

---

## Final Checklist

- [ ] Domain added at registrar with DNS: dns1.small.pl and dns2.small.pl
- [ ] DNS zone added in SMALL.PL panel
- [ ] DNS propagation completed (verified)
- [ ] Website created for domain
- [ ] Virtualenv created and activated
- [ ] Packages from requirements.txt installed
- [ ] Project files in `public_python/`
- [ ] `settings.py` configured (BASE_DIR, STATIC_ROOT, MEDIA_ROOT, ALLOWED_HOSTS)
- [ ] `passenger_wsgi.py` created with correct paths
- [ ] Migrations executed (`migrate`)
- [ ] Static files collected (`collectstatic`)
- [ ] Superuser created
- [ ] Interpreter path set in WWW panel
- [ ] Application restarted
- [ ] SSL certificate generated (Let's Encrypt)
- [ ] Site works correctly via HTTPS
- [ ] Admin panel accessible
- [ ] Padlock icon (SSL) visible in browser

