#!/usr/bin/env python
import paho.mqtt.client as mqtt
import time, sys

topic = "#"
verbosity=0
doit=3
timeout = 30 #secs

def on_connect(client, userdata, flags, rc):
    global verbosity
    if verbosity:
      print("Connected with result code " + str(rc))
    client.subscribe(topic)

def on_message(client, userdata, msg):
    global doit
    print(msg.topic + " " + str(msg.payload))
    doit=0

#main
av=sys.argv
if len(av)<2:
  print("no args. use: "+av[0]+" server[:port] <topic>")
  sys.exit()
server=av[1]
port=1883
if  ":" in server:
  sp=server.split(":")
  server=sp[0]
  port=sp[1]
if len(av)>2:  
  topic=av[2]
if len(av)>3:
  for p in av[3:]:
    if p[:2]=="-t":
      timeout = int(p[3:],10)

if verbosity:
  print("Server: %s:%d  Topic: %s"%(server, port, topic))
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(server, port, 60)
#client.loop_forever()
client.loop_start()
endtime = time.time() +timeout
while doit:
  time.sleep(.5) # don't block cpu
  if time.time() > endtime:
    print("timeout!")
    doit = 0
time.sleep(0.2)
client.disconnect() # disconnect gracefully
#time.sleep(1) #wait for finish
if verbosity:
  print("fin.")

#eof
