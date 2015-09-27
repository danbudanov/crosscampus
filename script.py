from urllib2 import Request, urlopen
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
import json
import time


app = Flask(__name__)
app.config.from_object(__name__)


app.debug=True

@app.route("/")
def index():
    request = Request("http://m.gatech.edu/w/buses/c/api/stop")
    data = json.load(urlopen(request))


    stop_info = {}

    for stop in data:
        stop_info.update({str(stop['stop_id']): [str(stop['route_id']),str(stop['stop_name']),
                                                 {'lat':str(stop['stop_lat']), 'lon':str(stop['stop_lon'])}]})

    #print stop_info

    request = Request("http://m.gatech.edu/w/buses/c/api/position")
    data2 = json.load(urlopen(request))

    request = Request("http://m.gatech.edu/w/buses/c/api/predict/yellow?stop=fersatmrt")
    data3 = json.load(urlopen(request))


    bus_info = {}

    for bus in data2:
        bus_info.update({str(bus['id']): {'route':str(bus['route']),
                                          'plat':str(bus['plat']),
                                          'plng':str(bus['plng'])
                                          }})

    ETAo = {"BusID1":5, "BusID2":11, "BusID3":13}
    ETAf = {"BusID1":20, "BusID2":27, "BusID3":34}

    lat_user = 33.7759698
    lon_user = -84.3953635

    lat_stop = stop_info['klaubldg'][2]['lat']
    lon_stop = stop_info['klaubldg'][2]['lon']

    #print lat_stop, lon_stop

    lat_stopF = stop_info['studcentr'][2]['lat']
    lon_stopF = stop_info['studcentr'][2]['lon']

    #print lat_stopF, lon_stopF

    final_lat = 33.7741327
    final_lon = -84.4007868


    api_key = "AIzaSyAZRRCcgqF6KSDlrsGCSbPSB7Pus44YEYU"

    user_to_stop = "https://maps.googleapis.com/maps/api/directions/json?origin="+str(lat_user)+","+str(lon_user)+"&destination="+str(lat_stop)+","+str(lon_stop)+"&mode=walking&key=AIzaSyAZRRCcgqF6KSDlrsGCSbPSB7Pus44YEYU"
    stop_to_final = "https://maps.googleapis.com/maps/api/directions/json?origin="+str(lat_stopF)+","+str(lon_stopF)+"&destination="+str(final_lat)+","+str(final_lon)+"&mode=walking&key=AIzaSyAZRRCcgqF6KSDlrsGCSbPSB7Pus44YEYU"
    user_to_final = "https://maps.googleapis.com/maps/api/directions/json?origin="+str(lat_user)+","+str(lon_user)+"&destination="+str(final_lat)+","+str(final_lon)+"&mode=walking&key=AIzaSyAZRRCcgqF6KSDlrsGCSbPSB7Pus44YEYU"


    request = Request(user_to_stop)
    data = json.load(urlopen(request))

    request2 = Request(stop_to_final)
    data2 = json.load(urlopen(request2))

    request3 = Request(user_to_final)
    data3 = json.load(urlopen(request3))

    #print data
    #print data2
    #print data3


    duration_items = [["duration_U2S", data["routes"][0]["legs"][0]["duration"]["text"]],
        ["duration_S2F", data2["routes"][0]["legs"][0]["duration"]["text"]],
        ["duration_U2F", data3["routes"][0]["legs"][0]["duration"]["text"]]]


    duration = {}

    item_no = 0

    for item in duration_items:
        numb = ''
        
        for number in str(item[1]):
            try:
                a = int(number)
                numb += str(number)
                #print number

            except:
                break

        duration.update({duration_items[item_no][0]:str(numb)})
        item_no = item_no + 1

    #print duration

    for arrival in ETAo.items():
        if int(duration["duration_U2S"]) <= arrival[1]:
            bus = arrival[0]
            break

        else:
            continue

    final = ETAf[bus] + int(duration["duration_S2F"])
    print final


            
            
    context = {"final":str(final),
               "stop_data":stop_info,
               "bus_data":bus_info
               }

    return render_template("index.html", final=final)




if __name__ == '__main__':
    app.run(debug=True, port=8080)

