# Wok Readme

Wok is a Python module that can be used to download menu data from UW-Madison's NetNutrition website. It has the ability to download most of the information, including the list of dining locations, the different stations at each location, the different schedules at those stations (breakfast/lunch/dinner/late night offerings), and finally the actual menu items.

## Usage Example

```python
#! /usr/bin/env python3

# This example is based on the more developed menu client:
#   https://github.com/austinhartzheim/menu

import wok

LOCATION_ID = 1  # The ID for Gordon's
STATION_ID = 5  # The ID for the 1849 station

w = wok.Wok()

# Fetch the list of available locations on campus
w.fetch_locations()

# Fetch the stations at this location
loc = w.get_location(LOCATION_ID)
loc.fetch_stations()
station = loc.get_station(STATION_ID)

# Fetch the available menus at the station (which can vary by meal)
station.fetch_menus()

# Fetch all menus:
for menu in station.menus:
    menu.fetch_items()

for menu in station.menus:
    print('Menu: %s: %s' % (menu.datetext, menu.timeofday))
    for item in menu.items:
    	print('  {0:50}{1:20}{2:7}'.format(item.name, item.servingsize, item.price))
```