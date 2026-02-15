from .base import INSTALLED_APPS, MIDDLEWARE

INSTALLED_APPS = INSTALLED_APPS + ['silk']
MIDDLEWARE = ['silk.middleware.SilkyMiddleware'] + MIDDLEWARE
# Authentication: require login to access Silk UI
SILKY_AUTHENTICATION = True
# Authorization: only staff users can access Silk UI (is_staff=True)
SILKY_AUTHORISATION = True
# Redirect to admin login page (default /accounts/login/ doesn't exist in this project)
LOGIN_URL = '/admin/login/'
