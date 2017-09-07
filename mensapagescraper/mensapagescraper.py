# -*- coding: utf-8 -*-

import requests, bs4, codecs


def mensa_download():
    """
    Grabs the html code of this week's mensa plan
    returns it as a bs4 object
    """
    response = requests.get('http://www.studierendenwerk-bielefeld.de/essen-trinken/essen-und-trinken-in-mensen/bielefeld/mensa-gebaeude-x.html')
    html = response.text

    htmlSoup = bs4.BeautifulSoup(html)

    return htmlSoup

def getDiv(htmlSoup):
    """
    returns the main div of a html object
    """
    #print(htmlSoup)
    divElem = htmlSoup.select('div')[35]

    return divElem

def getNextWeek(divElem):
    """
    takes the main div of the original website
    extracts the html for next week's site, grabs it and returns the soup
    """
    #Öffnungszeiten
    #time = divElem.select('p')[1]

    #Link für die nächste Woche
    nextWeek = "http://www.studierendenwerk-bielefeld.de" + divElem.select('a')[19].get("href")

    response = requests.get(nextWeek)
    html = response.text

    htmlSoup = bs4.BeautifulSoup(html)

    return htmlSoup

def extrractInfo(divElem):
    """
    takes the main div of a mensa page
    extracts all needed info: dates that have food, names of the food
    applies some formatting
    returns information as dictionary
    """
    #Wochentage (diese Woche)
    days = divElem.select('h2')[1:6]

    #Liste mit den Daten der aktuellen Woche (amerikanische Schreibweise)
    dates = []
    for i in days:
        date = str(i).split()[2]
        dates.append(date[-4:] + '-' + date[3:5] + '-' + date[0:2])
    

    #alle Informationen zu den Menüs (5 Tage, Montag - Freitag)
    mensaPlan = divElem.find_all('div', class_='mensa plan')[:5]

    #Listen mit Tagesmenü und vegetarisches Menü
    menu = []
    menuveg = []
    for i in range(5):
        menus = mensaPlan[i].find_all('tbody')[0]
        menu.append(menus.find_all('tr', class_='odd')[0].find_all('p')[1])
        menuveg.append(menus.find_all('tr', class_='even')[0].find_all('p')[1])


    #Dictionary mit den Tagen als key und die Menüs als Value
    food = dict()

    #Dictionary of Dictionaries (key: Datum -> key: Tagesmenü -> value: Gericht Tagesmenü | key: Datum -> key: vegMenü -> value: Gericht vegetarisches Menü)
    for i in range(5):
        food[dates[i]] = {}
        m = str(menu[i])
        mveg = str(menuveg[i])
        for ch in ['<p>','</p>', '<sup>', '</sup>']:
            if ch == '<sup>':
                m = m.replace(ch, ' enthält ')
                mveg = mveg.replace(ch, ' enthält ')
            else:
                m = m.replace(ch, '')
                mveg = mveg.replace(ch, '')
        food[dates[i]]['main-Menu'] = m
        food[dates[i]]['veg_menu'] = mveg

    #f = open(dates[0] + '.txt', 'w')
    #f.write('test')
    #f.close()

    return(food)


def main():
    """
    grabs the mensa plans for the current and next week from the website
    returns a dictionary that contains the main menus for each day that has them
    (date (main_menu: name, veg_menu:name))
    """
    mensa = mensa_download()
    div_this_week = getDiv(mensa)
    food_this_week = extractInfo(div_this_week)
    mensa_next = getNextWeek(mensa)
    div_next_week = getDiv(mensa_next)
    food_next_week = extractInfo(div_next_week)
        
    return food_today

mainV2('2017-09-07')
