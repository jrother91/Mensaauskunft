# -*- coding: utf-8 -*-

import logging

from random import randint

from flask import Flask, render_template

from flask_ask import Ask, statement, question, session


app = Flask(__name__)

ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)


@ask.launch

def new_game():

    welcome_msg = render_template('welcome')

    return statement(welcome_msg)
	
if __name__ == '__main__':

    app.run(debug=True)