#!/bin/bash

echo createcerts...

echo ca.key could be created with password.
#openssl genrsa -des3 -out ca.key 2048
echo create ca.key !without! password...
openssl genrsa -out ca.key 2048

echo create ca.crt from ca.key...
openssl req -new -x509 -days 2000 -key ca.key -out ca.crt

echo create client key...
openssl genrsa -out client.key 2048

openssl req -new -out client.csr -key client.key

echo sign client cert request with ca.crt...
openssl x509 -req -in client.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out client.crt -days 888

echo generate server key...
openssl genrsa -out server.key 2048

echo generate server cert request...
openssl req -new -out server.csr -key server.key

echo sign server cert request with ca.crt...
openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt -days 360

echo client needs: ca.crt, client.crt, client.key
echo server needs: ca.crt, server.crt, server.key

rm client.csr
rm server.csr

echo done.
