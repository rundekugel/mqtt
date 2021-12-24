#!/usr/bin/env python
'''
mqtt tx any message
'''

import time,sys
import paho.mqtt.client as mqtt

__VERSION__ = "0.1.0"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

client = mqtt.Client()
client.on_connect = on_connect
retain = False
qos = 0
verbosity = 1

av=sys.argv
if len(av)<3:
  print("no args. use: mytt_tx.py server[:port] <topic> [data] [options]")
  print("-r     retain")
  print("-q=<n>   qos=n")
  print("-n=<n>   repeat n times")
  print("-s=<server>  set servername")
  print("-t=<topic>   set topic")
  print("-d=<data>    set data")
  sys.exit()
server=av[1]
port=1883
topic=av[2]
rep=1

if len(av)>3:
  data=av[3]
else:
  data=None
  
if len(av)>1:
  for p in av[1:]:
    if p[0] != "-":
      continue
    if p == "-r":
      retain=True
    if p[:2]=="-q":
      qos = int(p[3:],10)
    if p[:2]=="-n":
      rep = int(p[3:],10)
    if p[:2]=="-v":
      verbosity = int(p[3:],10)
    if p[:2]=="-s":
      server = p[3:]
    if p[:2]=="-t":
      topic = p[3:]
    if p[:2]=="-d":
      data = p[3:]
      
if ":" in server:
  sp=server.split(":")
  server=sp[0]
  p=int(sp[1],10)
  if p:
    port=p

if verbosity:
  print("r,q,n,v,s,t,port,topic,data",retain,qos,rep,verbosity,server,port,topic,data)
client.connect(server, port, 60)
client.loop_start()

while rep:
    print("tx#%d %s %s [%d, %d]"%(rep, topic, data, qos, retain))
    rep-=1
    client.publish(topic, data, qos, retain)
    time.sleep(1)
print("done.")
#eof
