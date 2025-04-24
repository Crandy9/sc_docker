# same settings as production but with debug to true and ssl redirects off
# useful for running vs code or python debugger
# needed to run local Django dev server over http



'''
TO START DEV SERVER 
(NOTE: I discovered that when dev mode is on and howlerjs
html5:true, slider seeking doesn't work on the music player's slidebar. 
But html5: true is required to allow media session API functionality on mobile 
Also downloads do not work on http mode, but work for https just keep that in mind)
run dev server to access site over http:
set backend env DEV_MODE var:
DEV_MODE=True

set frontend vuejs env VUE_APP_DEV_MODE var:
VUE_APP_DEV_MODE=true

stop nginx and gunicorn
sudo systemctl stop nginx
sudo systemctl stop gunicorn
sudo systemctl stop gunicorn.socket

in your browser, open dev tools
clear cache and cookie data in dev tools console (otherwise any previous http redirects will still be in affect)

start dev server:
DJANGO_SETTINGS_MODULE=sheriff_crandy_project.dev_settings python manage.py runserver

open a new terminal and start the frontend npm server
npm run serve

make sure you can access the frontend at
127.0.0.1:8080
and the backend at 
127.0.0.1:8000/api/
'''

from .settings import * 

# for development
DEBUG = True

SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False