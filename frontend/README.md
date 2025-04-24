# sheriffcrandy.com VueJS frontend


*** VUEJS PROJECT SETUP (installing libraries/dependencies) *** 
Vue.js setup:

- install node.js
sudo apt install nodejs

- install npm
sudo apt install npm


- open a new terminal and cd to yourprojectname dir and install vue cli 
(this doesn't have to be in the same place as the Django backend app by the way,
you can place it wherever you want in your system):

sudo npm install -g @vue/cli 
(if you get a bunch of permission errors, run again with sudo)
- check installation:
vue --version

- in main dir (enter 'ls' and you should see LICENSE, README.md, repo) create vue project:
vue create frontend (don't do this for production)
- Don't select a preset,
- select manually select features with space NOT ENTER:
Babel
Router
Vuex (for cart implementation)
CSS pre-processors
- unselect Linter/formatter (idk why, that's what they did in the tutorial lol)
- hit enter
- use 3.x version
- hit enter
- select 'Y' for router history mode and hit enter
- select Sass/SCSS (with dart-sass) and hit enter
- select 'place Babel, ESLint, etc. config files in dedicated config files'
- Select 'n' for saving this preset for future projects
- cd to repo_vue and install axios library used to access Django API data:
npm install axios
- install bulma (css framework)
npm install bulma
- install toast pop when adding items to cart
npm install bulma-toast
- install bulma modal-fx
npm i bulma-modal-fx
- install animate.css
npm install animate.css
- install Howler js for audio library
npm install howler
- install swiper js for carousel
npm i swiper
- install vue-cli-plugin-i18n for internationalization (if you have Vue Cli 3.x) https://kazupon.github.io/vue-i18n
vue add i18n
- add .env file to your parent directory
- add .env vars: 
VUE_APP_I18N_LOCALE=en
VUE_APP_I18N_FALLBACK_LOCALE=en
- update dependcies in:
repo_vue/package-lock.json
repo_vue/package.json
- create new files:
repo_vue/vue.config.js
repo_vue/src/i18n.js
- import i18n in main.js
- create repo_vue/src/components/HelloI18n.vue (may not need it)
- create json files to hold translations repo_vue/src/locales/en.json

- to run vue app on localhost:8080 
npm run serve


*** LIVE PRODUCTION SERVER ***

npm run build creates a 'dist' folder containing required vuejs files
that nginx can serve. But before running this command, change the following env vars:

VUE_APP_DEV_MODE=false

set https backend url needed for axios:
VUE_APP_PRODUCTION_BACKEND_URL=https://sheriffcrandymusic.local:9443/api


*** 
    NOTE:
FOR ACTUAL LIVE PRODUCTION SERVER, CHANGE `VUE_APP_PRODUCTION_BACKEND_URL` TO:

VUE_APP_PRODUCTION_BACKEND_URL=https://sheriffcrandymusic.com/api

BEFORE RUNNING `npm run build`

***

then create the dist folder:

npm run build

cd into `/scripts` directory (sudo mkdir scripts) if you don't have it in your local machine

and create a bash script to scp the new dist folder to the production web server path where
nginx will serve it:

sudo nano scripts/sc-dist-scp

Add this command to it:

```
#!/bin/bash

# Usage: scp updated vuejs dist folder to prod server

scp -r /home/lctec/Desktop/sheriffcrandy_prod/sheriffcrandy_prod/frontend/dist lctec@137.184.248.73:/home/lctec/sheriffcrandy_prod/frontend
```

- make it executable 
chmod +x sc-dist-scp

- restart bashrc:
source ~/.bashrc

now whenever you make updates to the vuejs app in development,
you can run the `npm run build` command and easily transfer the new `dist` folder 
to the correct location on the production web server


- after running the above command, ssh into the production web server and restart nginx:
sudo systemctl restart nginx

- check status
sudo systemctl status nginx


make sure you can access the frontend at
https://sheriffcrandymusic.com



*** DEVELOPMENT ***

*** CREATE HTTP DEV SERVER (using Django's and npm's development servers over http for debugging) ***
create .env file in this dir if you haven't already
(get all API endpoint env vars that need to be added to your .env file from me)

add this var and set it to false:
VUE_APP_DEV_MODE=false

add the two different baseURL paths that axios will use to fetch Django API data:

(for https url name, this will be whatever host name you madeup in your nginx setup):

VUE_APP_PRODUCTION_BACKEND_URL=https://sheriffcrandymusic.local:9443/api
VUE_APP_DEVELOPMENT_BACKEND_URL=http://127.0.0.1:8000/api

run the server:
npm run serve

open your browser and go to the local dev frontend url:
localhost:8080 

to make code changes, npm usually self-restarts. 
But you can also use ctrl+c to stop the server and then re-run it as well

*** CREATE HTTPS LOCAL PRODUCTION SIMULATION SERVER (simulate live website using https self-signed SSL certs) ***

TO SIMULATE PROD SERVER USING HTTPS
First set up Gunicorn, Nginx, self-signed SSL certs, and database locally on your system (see servers_ssl_db_setup folder)

set frontend vuejs env VUE_APP_DEV_MODE var:
VUE_APP_DEV_MODE=false

set https backend url needed for axios:
VUE_APP_PRODUCTION_BACKEND_URL=https://sheriffcrandymusic.local:9443/api


*** 
    NOTE:
FOR ACTUAL LIVE PRODUCTION SERVER, CHANGE `VUE_APP_PRODUCTION_BACKEND_URL` TO:

VUE_APP_PRODUCTION_BACKEND_URL=https://sheriffcrandymusic.com/api

BEFORE RUNNING `npm run build`

***

create vuejs dist folder (you need to make sure nginx's default location path is set to this new folder):

npm run build

make sure you can access the frontend at
https://sheriffcrandymusic.local:9443/
or whatever you named your hosts name in nginx/gnicorn ssl setup




To make changes to code, simply rebuild the vuejs app:
npm run build


Do not need to use npm's development server anymore.