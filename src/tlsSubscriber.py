#!/usr/bin/env python
import paho.mqtt.client as mqtt
import time, sys
import ssl
import certifi

topic = "#"
useTls = 1


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(topic)

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))


#main
av=sys.argv
if len(av)<2:
  print("no args. use: "+av[0]+" server[:port] <topic>")
  sys.exit()
server=av[1]
port=1883

for p in av:
  if p=="-tls":
    useTls=1
  if p=="-ntls":
    useTls=0

if useTls:
  port=8883

if  ":" in server:
  sp=server.split(":")
  server=sp[0]
  port=sp[1]
if len(av)>2:  
  topic=av[2]

print("Server: %s:%d  Topic: %s"%(server, port, topic))
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
if useTls:
  # client.tls_set("client.crt", tls_version=ssl.PROTOCOL_TLSv1_2)
  client.tls_set('ca.crt', 'client.crt', \
                 'client.key')
  client.tls_insecure_set(True)

client.connect(server, port, 60)
client.loop_forever()
print("fin.")
