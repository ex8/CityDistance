import sys
import googlemaps
from googlemaps import convert
import json
from functools import partial


def result(origin, destination, duration, distance, mode):
    print
    print '====================================='
    print '     Distance between 2 places       '
    print '====================================='
    print 'Origin address:', origin[0]
    print 'Destination address:', destination[0]
    print 'Mode:', mode
    print 'Duration:', duration
    print 'Distance:', distance


def calculate(city1, city2, mode):
    gmap = googlemaps.Client(key='AIzaSyA5IMAMDba1savLG8D9R5a_VMG0x_bi7Fk')
    d = distance_matrix(gmap, city1, city2, mode=mode)
    data = json.loads(json.dumps(d))

    origin = data['origin_addresses']
    destination = data['destination_addresses']
    duration = data['rows'][0]['elements'][0]['duration']['text']
    distance = data['rows'][0]['elements'][0]['distance']['text']
    mode = mode[0].upper() + mode[1:]

    result(origin, destination, duration, distance, mode)


def distance_matrix(client, origins, destinations,
                    mode=None, language=None, avoid=None, units=None,
                    departure_time=None, arrival_time=None, transit_mode=None,
                    transit_routing_preference=None, traffic_model=None):
    normal = lambda x: x

    restrictions = {
        mode: ("mode", ("driving", "walking", "bicycling", "transit", None)),
        avoid: ("avoid", ("tolls", "highways", "ferries", None)),
    }

    for val, (name, valid) in restrictions.items():
        if val not in valid:
            raise ValueError("{} is not valid.".format(name))

    variables = {
        "mode": (normal, mode),
        "language": (normal, language),
        "avoid": (normal, avoid),
        "units": (normal, units),
        "departure_time": (convert.time, departure_time),
        "arrival_time": (convert.time, arrival_time),
        "transit_mode": (partial(convert.join_list, '|'), transit_mode),
        "transit_routing_preference": (normal, transit_routing_preference),
        "traffic_model": (normal, traffic_model),
    }

    params = {
        'origins': convert.location_list(origins),
        'destinations': convert.location_list(destinations)
    }

    for var, (func, val) in variables.items():
        if val:
            params[var] = func(val)

    return client._get('/maps/api/distancematrix/json', params)


def main():
    try:
        city1 = raw_input('Please enter your first city: ')
        city2 = raw_input('Please enter your second city: ')
        mode = raw_input('Please enter your transportation method (driving, walking, transit, or bicycling): ')
    except KeyboardInterrupt:
        sys.exit(1)

    calculate(city1, city2, mode)


if __name__ == '__main__':
    main()