#!/usr/bin/env python
'''
mqtt tx any message
'''

import time,sys
import paho.mqtt.client as mqtt

__VERSION__ = "0.0.3"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

client = mqtt.Client()
client.on_connect = on_connect
retain = False
qos = 0

av=sys.argv
if len(av)<3:
  print("no args. use: mytt_tx.py server[:port] <topic> [data] [options]")
  print("-p     retain")
  print("-q=n   qos=n")
  print("-r=n   repeat n times")
  sys.exit()
server=av[1]
port=1883
if  ":" in server:
  sp=server.split(":")
  server=sp[0]
  port=int(sp[1],10)
topic=av[2]
rep=1

if len(av)>3:
  val=av[3]
else:
  val=None
  
if len(av)>4:
  for p in av[4:]:
    if p == "-p":
      retain=True
    if p[:2]=="-q":
      qos = int(p[3:],10)
    if p[:2]=="-r":
      rep = int(p[3:],10)

client.connect(server, port, 60)
client.loop_start()

while rep:
    print("tx#%d %s %s [%d, %d]"%(rep, topic, val, qos, retain))
    rep-=1
    client.publish(topic, val, qos, retain)
    time.sleep(1)
print("done.")
#eof
