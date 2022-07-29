#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt
import time, sys
from getpass import getpass

topic = "#"

def on_connect(client, userdata, flags, rc):
    res=["ok","?","?","?","?","Auth error"]
    print("Connected with result code " + str(rc) +" "+str(res[rc]))
    client.subscribe(topic)

def on_message(client, userdata, msg):
    if sys.version_info[0]==3:
        msg.payload = msg.payload.decode()
    print(msg.topic + " " + str(msg.payload))


#main
av=sys.argv
if len(av)<2:
  print("no args. use: "+av[0]+" server[:port] <topic>")
  sys.exit()
server=av[1]
port=1883
user=None
passwd=None

if  ":" in server:
  sp=server.split(":")
  server=sp[0]
  port=sp[1]
if len(av)>2:  
  topic=av[2]
  
for p in av[3:]:  
    if p[:2]=="-u":
      user = p[3:]
    if p[:3]=="-pw":
      passwd = p[4:]


print("Server: %s:%d  Topic: %s User: %s"%(server, port, topic, user))
client = mqtt.Client()
if user:
    if not passwd:
        passwd = getpass("Password for "+user+": ")
    client.username_pw_set(user, passwd)  

client.on_connect = on_connect
client.on_message = on_message
client.connect(server, port, 60)
client.loop_forever()
print("fin.")
