# -*- coding: utf-8 -*-

import requests, bs4, codecs, urllib2


def mensa_download():

    response = urllib2.urlopen('http://www.studierendenwerk-bielefeld.de/essen-trinken/essen-und-trinken-in-mensen/bielefeld/mensa-gebaeude-x.html')
    html = response.read()

    htmlSoup = bs4.BeautifulSoup(html)

    #print(htmlSoup)
    divElem = htmlSoup.select('div')[35]

    
    #Öffnungszeiten
    time = divElem.select('p')[1]

    #Link für die nächste Woche
    nextWeek = "http://www.studierendenwerk-bielefeld.de" + divElem.select('a')[19].get("href")


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
        food[dates[i]]['Tagesmenü'] = m
        food[dates[i]]['vegMenü'] = mveg
        
    return(food)

##Gibt das Tagesmenü und vegetarische Menü von einem Datum aus.    
def getMenu(datum, food):
    return [food[datum]['Tagesmenü'], food[datum]['vegMenü']]

def mainV2(date):
    #print(mensa_download())
    mensa = mensa_download()
    food_today = getMenu(date, mensa)
    return food_today
    
print(mainV2('2017-09-07'))
