'''
The Wok library is used to navigate and download menus from
UW-Madison's dining menu pages (dining.housing.wisc.edu).
'''
import json
import urllib.request
import urllib.parse
import re
import bs4


COOKIE = 'afmokubrljrurynkobboechd'


class Wok():

    url = 'http://dining.housing.wisc.edu/NetNutrition/1'
    re_getid = re.compile('[\D]+(?P<id>\d+)[\D]+')

    def __init__(self):
        self.locations = []

    def get_location(self):
        if not self.locations:
            raise IndexError('You have not fetched any locations')
        # TODO: return a location

    def fetch_locations(self):
        r = urllib.request.Request(self.url, None, {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'Cookie': 'CBORD.netnutrition2=NNexternalID=1&Layout=; ASP.NET_SessionId=' + COOKIE})
        page = bs4.BeautifulSoup(urllib.request.urlopen(r))
        locations = page.select('.cbo_nn_sideUnitCell a')

        self.locations = []  # Clear out and repopulate the list
        for loc in locations:
            name = loc.get_text()
            lid = int(re.match(self.re_getid, loc.get('onclick')).group('id'))
            self.locations.append(Location(lid, name))


class Location():

    url = 'http://dining.housing.wisc.edu/NetNutrition/1/Unit/SelectUnitFromSideBar'
    re_getid = re.compile('[\D]+(?P<id>\d+)[\D]+')

    def __init__(self, lid, name):
        self.id = lid
        self.name = name

        self.stations = []

    def fetch_stations(self):
        postdata = urllib.parse.urlencode({'unitOid': self.id}).encode('utf8')
        r = urllib.request.Request(self.url, postdata, {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'Cookie': 'CBORD.netnutrition2=NNexternalID=1&Layout=; ASP.NET_SessionId=' + COOKIE})
        page = json.loads(urllib.request.urlopen(r).read().decode('utf8'))
        for panel in page['panels']:
            if panel['id'] == 'childUnitsPanel':
                page = bs4.BeautifulSoup(panel['html'])
                break

        stations = page.select('.cbo_nn_childUnitsCell a')

        self.stations = []  # Clear out and repopulate the list
        for stat in stations:
            name = stat.get_text()
            sid = int(re.match(self.re_getid, stat.get('onclick')).group('id'))
            self.stations.append(Station(sid, name))

    def __repr__(self):
        return '<Location: %i: %s>' % (self.id, self.name)


class Station():

    url = 'http://dining.housing.wisc.edu/NetNutrition/1/Unit/SelectUnitFromChildUnitsList'
    re_getid = re.compile('[\D]+(?P<id>\d+)[\D]+')

    def __init__(self, sid, name):
        self.id = sid
        self.name = name

        self.menus = []

    def fetch_menus(self):
        postdata = urllib.parse.urlencode({'unitOid': self.id}).encode('utf8')
        r = urllib.request.Request(self.url, postdata, {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'Cookie': 'CBORD.netnutrition2=NNexternalID=1&Layout=; ASP.NET_SessionId=' + COOKIE})
        page = json.loads(urllib.request.urlopen(r).read().decode('utf8'))
        for panel in page['panels']:
            if panel['id'] == 'menuPanel':
                page = bs4.BeautifulSoup(panel['html'])
                break

        menus = page.select('.cbo_nn_menuCell table')
        for menu in menus:
            datetext = menu.select('tr td')[0].get_text()
            for timeofday in menu.select('tr td a')[1:]:
                mid = int(re.match(self.re_getid, timeofday.get('onclick')).group('id'))
                self.menus.append(Menu(mid, datetext, timeofday.get_text()))

    def __repr__(self):
        return '<Location: %i: %s>' % (self.id, self.name)


class Menu():

    url = 'http://dining.housing.wisc.edu/NetNutrition/1/Menu/SelectMenu'
    re_getid = re.compile('[\D]+(?P<id>\d+)[\D]+\d+[\D+]')

    def __init__(self, mid, datetext, timeofday):
        self.id = mid
        self.datetext = datetext
        self.timeofday = timeofday

        self.items = []

    def fetch_menu(self):
        postdata = urllib.parse.urlencode({'menuOid': self.id}).encode('utf8')
        r = urllib.request.Request(self.url, postdata, {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'Cookie': 'CBORD.netnutrition2=NNexternalID=1&Layout=; ASP.NET_SessionId=' + COOKIE})
        page = json.loads(urllib.request.urlopen(r).read().decode('utf8'))
        for panel in page['panels']:
            if panel['id'] == 'itemPanel':
                page = bs4.BeautifulSoup(panel['html'])
                break

        items = page.select('.cbo_nn_itemPrimaryRow')
        for item in items:
            subsel = item.select('.cbo_nn_itemHover')[0]
            name = subsel.get_text()
            iid = int(re.match(self.re_getid, subsel.get('onmouseover')).group('id'))
            price = item.select('td')[-1].get_text()
            serving = item.select('td')[2].get_text()
            self.items.append(Item(iid, name, serving, price))

    def __repr__(self):
        return '<Menu: %i: %s: %s>' % (self.id, self.datetext, self.timeofday)


class Item():
    def __init__(self, iid, name, servingsize, price):
        self.id = iid
        self.name = name
        self.servingsize = servingsize
        self.price = price

    def __repr__(self):
        return '<Item %i: %s: %s: %s>' % (self.id, self.name, self.servingsize,
                                          self.price)
