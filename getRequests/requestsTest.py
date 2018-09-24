import requests as req
import RPi.GPIO as GPIO

r = req.get('http://192.168.1.13:8000/getPath/1/get')
pathStreamList = list(r.text)
print(pathStreamList)

for moveCommand in pathStreamList:
    print(moveCommand)
