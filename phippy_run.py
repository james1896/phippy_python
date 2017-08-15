# -*- coding: utf-8 -*-
#!flask/bin/python


from phippy import app

if __name__ == '__main__':
    app.run('10.71.66.2', debug=True, port=5001)