#!/bin/bash
ROOTDIR=`dirname $0`
echo $ROOTDIR

### create client key
openssl genrsa -out ${ROOTDIR}/keys/client.key 2048
openssl req -key ${ROOTDIR}/keys/client.key -new -out ${ROOTDIR}/keys/client.req -subj "/C=AU/ST=NSW/O=Organisation/CN=client1/emailAddress=user@domain.com"
openssl x509 -passin pass:foobar -req -in ${ROOTDIR}/keys/client.req -CA ${ROOTDIR}/keys/ca.pem -CAkey ./privkey.pem -CAserial ${ROOTDIR}/keys/file.srl -out ${ROOTDIR}/keys/client.crt -days 3650
cat ${ROOTDIR}/keys/client.key ${ROOTDIR}/keys/client.crt > ${ROOTDIR}/keys/out/client.pem
openssl verify -CAfile ${ROOTDIR}/keys/ca.pem ${ROOTDIR}/keys/out/client.pem