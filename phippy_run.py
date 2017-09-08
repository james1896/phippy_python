# -*- coding: utf-8 -*-
#!flask/bin/python


# pip freeze > requirements.txt
# pip install -r requirements.txt

# Flask-Script==2.0.5
# livereload==2.3.2
from phippy import app

if __name__ == '__main__':
    # app.run('10.71.12.139', port=5001)
    # app.run('127.0.0.1', port=5001)
    app.run('10.71.66.2', port=5001)
    # https: // itunes.apple.com / ph / app / wechat / id41447da8124?mt = 8