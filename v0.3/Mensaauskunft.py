# -*- coding: utf-8 -*-

import logging

import sys
sys.path.append('./mensapagescraper')
import mensapagescraper 

import datetime

from datetime import date

from random import randint

from flask import Flask, render_template

from flask_ask import Ask, statement, question, session


app = Flask(__name__)

ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)



@ask.launch

def welcome():
    """
    welcomes the user and asks for further instructions
    """

    welcome_msg = render_template('welcome')
    session.attributes["greet"] = True

    init_query = render_template('init_query')

    return question(welcome_msg+" "+init_query)


@ask.intent("AskMenu", default={"ThisDate" : date.today().isoformat(), "Menu": "main_menu"}, convert={"ThisDate":datetime.date, "Menu": str})

def main_menu(ThisDate, Menu):
    """
    Greets the user if they haven't been greetet yet.
    Takes a given date (or assumes today's date) and gives back the main menu.
    """
    menu_name = "main_menu"
    if(Menu in ["Tagesmenü", "Hauptgericht", "Fleisch", "fleischig", "mit Fleisch"]):
    
        menu_name = 'main_menu'
    elif(Menu in ["vegetarisch", "ohne Fleisch"]):
        menu_name = 'veg_menu'
    elif(Menu in ["vital", "leichtes"]):
        menu_name = 'mensa_vit'

    
    main_menu = render_template('main_menu', main_menu = mensapagescraper.getMensaInfo()[ThisDate][menu_name])
    
    if "greet" not in session.attributes.keys():
        welcome_msg = render_template('welcome')
        session.attributes["greet"] = True
        main_menu_msg = welcome_msg + " " + main_menu
    else:
        main_menu_msg = main_menu
    
    return question(main_menu_msg)


##@ask.intent("AskVegMenu", default={"ThisDate" : date.today().isoformat()}, convert={"ThisDate":datetime.date})
##
##def veg_menu(ThisDate):
##    """
##    Greets the user if they haven't been greetet yet.
##    Takes a given date (or assumes today's date) and gives back the vegetarian menu.
##    """
##	
##    #print "the date is" + ThisDate
##    
##    veg_menu = render_template('veg_menu', veg_menu = mensapagescraper.getMensaInfo()[ThisDate]['veg_menu'])
##	
##    #print "our info is "+mensapagescraper.getMensaInfo()[ThisDate]
##    
##    if "greet" not in session.attributes.keys():
##        welcome_msg = render_template('welcome')
##        session.attributes["greet"] = True
##        veg_menu_msg = welcome_msg + " " + veg_menu
##    else:
##        veg_menu_msg = veg_menu
##    
##    return question(veg_menu_msg)
##
##@ask.intent("AskMensaVital", default={"ThisDate" : date.today().isoformat()}, convert={"ThisDate":datetime.date})
##
##def mensa_vital(ThisDate):
##    """
##    Greets the user if they haven't been greetet yet.
##    Takes a given date (or assumes today's date) and gives back the main menu.
##    """
##
##    
##    mensa_vital = render_template('mensa_vital', mensa_vital = mensapagescraper.getMensaInfo()[ThisDate]["mensa_vit"])
##
##    
##    
##    if "greet" not in session.attributes.keys():
##        welcome_msg = render_template('welcome')
##        session.attributes["greet"] = True
##        mensa_vital_msg = welcome_msg + " " + mensa_vital
##    else:
##        mensa_vital_msg = mensa_vital
##    
##    return question(mensa_vital_msg)

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
