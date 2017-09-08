# -*- coding: utf-8 -*-

import requests, bs4, codecs, json
import codecs
import os
import glob

from datetime import datetime, timedelta


def mensa_download(url):
    """
    Grabs the html code of this week's mensa plan
    returns it as a bs4 object
    """
    response = requests.get(url)
    html = response.text

    htmlSoup = bs4.BeautifulSoup(html, 'lxml')

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
    return ("http://www.studierendenwerk-bielefeld.de" + divElem.select('a')[93].get("href"))


def extractInfo(divElem):
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
    beilagen = []
    menuveg = []
    beilagenveg = []
    menu_vit = []
    for i in range(5):
        menus = mensaPlan[i].find_all('tbody')[0]
        menu.append(menus.find_all('tr', class_='odd')[0].find_all('p')[1])
        beilagen.append(menus.find_all('tr', class_='odd')[0].find_all('p')[3])
        menuveg.append(menus.find_all('tr', class_='even')[0].find_all('p')[1])
        beilagenveg.append(menus.find_all('tr', class_='even')[0].find_all('p')[3])
        menu_vit.append(menus.find_all('tr', class_='odd')[1].find_all('p')[1])

    #Dictionary mit den Tagen als key und die Menüs als Value
    food = dict()

    #Dictionary of Dictionaries (key: Datum -> key: Tagesmenü -> value: Gericht Tagesmenü | key: Datum -> key: vegMenü -> value: Gericht vegetarisches Menü)
    for i in range(5):
        food[dates[i]] = {}
        m = menu[i].encode('utf-8')
        mveg = menuveg[i].encode('utf-8')
        b = beilagen[i].encode('utf-8')
        bveg = beilagenveg[i].encode('utf-8')
        mvit = menu_vit[i].encode('utf-8')
        m = bs4.BeautifulSoup(m, 'lxml')
        mveg = bs4.BeautifulSoup(mveg, 'lxml')
        b = bs4.BeautifulSoup(b, 'lxml')
        bveg = bs4.BeautifulSoup(bveg, 'lxml')
        mvit = bs4.BeautifulSoup(mvit, 'lxml')
        for tag in m.find_all('sup'):
            tag.decompose()
        for tag in mveg.find_all('sup'):
            tag.decompose()
        for tag in b.find_all('sup'):
            tag.decompose()
        for tag in bveg.find_all('sup'):
            tag.decompose()
        for tag in mvit.find_all('sup'):
            tag.decompose()
        food[dates[i]]['main_menu'] = m.find('p').getText()
        food[dates[i]]['veg_menu'] = mveg.find('p').getText()
        beilage = b.find('p').getText().replace(' oder', ',').split(',')
        beilage_veg = bveg.find('p').getText().replace(' oder', ',').split(',')
        food[dates[i]]['side_dishes'] = list(set(beilage + beilage_veg))
        food[dates[i]]['mensa_vit'] = mvit.find('p').getText()

    return(food)

def saveToJson(date, food):
    """
    saves the food dictionary as a json file
    """
    with codecs.open(date + '.json', 'w', 'utf-8') as fp:
        json.dump(food, fp, sort_keys = True)

def loadFromJson(date):
    """
    loads the food dictionary from a json file
    """
    with codecs.open(date + '.json', 'r', 'utf-8') as fp:
        food = json.load(fp)

    return food

def findTime(food):
    """
    finds the earliest day in the food dictionary
    """
    keys = sorted(food.keys())
    return keys[0]

def loadNewestJson():
    """
    finds the name of the newest json file
    """
    try:
        newest = max(glob.iglob('*.[Jj][Ss][Oo][Nn]'), key=os.path.getctime)
        return newest
    except:
        pass

def nDaysAgo():
    """
    finds the date of the last monday
    """
    n = datetime.now().weekday()

    date_N_days_ago = datetime.now() - timedelta(days=n)

    date_N_days_ago = str(date_N_days_ago).split()[0]

    return date_N_days_ago

def getMensaInfo():
    """
    grabs the mensa plans for the current and next week from the website
    returns a dictionary that contains the main menus for each day that has them
    (date (main_menu: name, veg_menu:name))
    """
    date = nDaysAgo()
    if(date + '.json' == loadNewestJson()):
        food = loadFromJson(date)

        return food
    else:
        mensa = mensa_download('http://www.studierendenwerk-bielefeld.de/essen-trinken/essen-und-trinken-in-mensen/bielefeld/mensa-gebaeude-x.html')
        div_this_week = getDiv(mensa)
        food_this_week = extractInfo(div_this_week)
        mensa_next_url = getNextWeek(mensa)
        mensa_next = mensa_download(mensa_next_url)
        div_next_week = getDiv(mensa_next)
        food_next_week = extractInfo(div_next_week)
        food = dict(food_this_week.items() + food_next_week.items())
        date = findTime(food)
        saveToJson(date, food)

        return food
    

if __name__ == '__main__':
    #print(type(getMensaInfo()['2017-09-14']['veg_menu']))
    print(getMensaInfo())
    
