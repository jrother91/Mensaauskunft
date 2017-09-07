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
    session.attributes["greet"] = True

    #init_query = render_template('init_query')

    return statement(welcome_msg)


@ask.intent("AskMainMenu")

def main_menu():
    main_menu = render_template('main_menu')

    if "greet" not in session.attributes.keys():
        welcome_msg = render_template('welcome')
        session.attributes["greet"] = True
        main_menu_msg = welcome_msg + " " + main_menu
    else:
        main_menu_msg = main_menu
    
    return statement(main_menu_msg)


@ask.intent("Done")

def say_no():

    goodbye = render_template('bye')

    return statement(goodbye)


@ask.intent("AskPrice")

def state_price():
	
    price = render_template('price')

    query = render_template('query')

    return question(price +' '+ query)

    
if __name__ == '__main__':

app.run(debug=True)
