#!/usr/bin/python2
from wifi import *
import requests
import os
import json
from time import sleep
from prettytable import PrettyTable
apikey = ""
name_adapter = ""
def cls(): os.system('cls' if os.name=='nt' else 'clear')

def values(array):
    res=""
    for val in array[:-1]: res+=val + ","
    return res + array[-1]

while len(apikey) < 10 and len(name_adapter) < 3:
    type = input("""1) API key
2) Login and password
Type of auth: """)
    if type == "1": apikey = input("API key: ")
    elif type == "2":
        login = input("Login: ")
        password = input("Password: ")
        print("Receiving API key ..")
        r = requests.post("http://3wifi.stascorp.com/api/ajax.php?Query=GetApiKeys", data={"Login":login, "Password": password})
        json = json.loads(r.text)
        apikey = json["r"]
        print("Done, api key: " + apikey)
    else: print("Something is wrong")
    name_adapter = input("Name of adapter (default is wlan0): ")
    cls()

list = Cell.all(name_adapter)
count=0
tired=0
for item in list: count+=1
while count < 2:
    count=0
    list = Cell.all(name_adapter)
    for item in list: count+=1
    if count > 1: break
    tired+=1
    if tired > 10: break
    sleep(15)
    
x = PrettyTable(["SSID", "Password", "WPS"]) 
for item in list:
    try:
        r = requests.get("http://3wifi.stascorp.com/api/ajax.php?Query=Find&Key={}&BSSID={}&Version=0.5".format(apikey, item.address))
        json = json.loads(r.text)
        if json["Successes"]:  x.add_column(item.ssid, values(json["Keys"]), values(json["WPS"]))
        else: x.add_column(item.ssid, "-", "-")
    except:
        x.add_column(item.ssid, "error", "error")
print(x)