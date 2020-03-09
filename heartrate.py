import json
import random
import datetime
import boto3
import time
import requests

highTemperatureRateNames = ['CAV02', 'CAV03', 'CAV04', 'CAV06', 'CAV08', 'CAV09']
nonhighTemperatureRateNames = ['CAV01', 'CAV05', 'CAV07']

allNames = list(set().union(highTemperatureRateNames, nonhighTemperatureRateNames))

metadata = json.loads(requests.get('http://169.254.169.254/latest/dynamic/instance-identity/document').text)
region = metadata['region']
session = boto3.Session(region_name=region)
iot = session.client('iot-data');

# generate normal heart rate with probability .95
def getNormalTemperatureRate():
    data = {}
    data['temperatureDegree'] = random.randint(25, 35)
    data['degreeType'] = 'NORMAL'
    data['vehicleId'] = random.choice(allNames)
    data['dateTime'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return data
# generate high heart rate with probability .05 (very few)
def getHighTemperatureRate():
    data = {}
    data['temperatureDegree'] = random.randint(35, 45)
    data['degreeType'] = 'HIGH'
    data['vehicleId'] =  random.choice(highTemperatureRateNames)
    data['dateTime'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return data
# generate anomalies heart rate with probability .05 (very few)
def getVeryHighTemperatureRate():
    data = {}
    data['temperatureDegree'] = random.randint(45, 55)
    data['degreeType'] = 'VERYHIGH'
    data['vehicleId'] =  random.choice(highTemperatureRateNames)
    data['dateTime'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return data
# generate anomalies heart rate with probability .05 (very few)
def getVeryLowTemperatureRate():
    data = {}
    data['temperatureDegree'] = random.randint(10, 25)
    data['degreeType'] = 'VERYLOW'
    data['vehicleId'] =  random.choice(highTemperatureRateNames)
    data['dateTime'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return data
while True:
    time.sleep(1)
    rnd = random.random()
    if (rnd < 0.02):
        data = json.dumps(getVeryLowTemperatureRate())
        print(data)
        response = iot.publish(
             topic='/temperature/temperatureDegree',
             payload=data
         )
    elif (rnd < 0.04):
        data = json.dumps(getVeryHighTemperatureRate())
        print(data)
        response = iot.publish(
             topic='/temperature/temperatureDegree',
             payload=data
         )
    elif (rnd < 0.09):
        data = json.dumps(getHighTemperatureRate())
        print(data)
        response = iot.publish(
             topic='/temperature/temperatureDegree',
             payload=data
         )
    else:
        data = json.dumps(getNormalTemperatureRate())
        print(data)
        response = iot.publish(
             topic='/temperature/temperatureDegree',
             payload=data
         )