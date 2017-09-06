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

    query = render_template('query')

    return question(welcome_msg +' '+ query)


@ask.intent("Done")

def say_no():

    goodbye = render_template('bye')

    return statement(goodbye)


@ask.intent("AskPrice")

def state_price():
	
    price = render_template('price')

    return question(price +' '+ query)

    
if __name__ == '__main__':

    app.run(debug=True)
