#!/bin/bash
ROOTDIR=`dirname $0`
HNAME=$1
echo $ROOTDIR

### create server key
openssl genrsa -out ${ROOTDIR}/keys/server.key 2048

openssl req -key ${ROOTDIR}/keys/server.key -new -out ${ROOTDIR}/keys/server.req -subj  "/C=AU/ST=NSW/O=Organisation/CN=server1/CN=$HNAME/emailAddress=user@domain.com"

openssl x509 -passin pass:foobar -req -in ${ROOTDIR}/keys/server.req -CA ${ROOTDIR}/keys/ca.pem -CAkey ./privkey.pem -CAserial ${ROOTDIR}/keys/file.srl -out ${ROOTDIR}/keys/server.crt -days 3650

cat ${ROOTDIR}/keys/server.key ${ROOTDIR}/keys/server.crt > ${ROOTDIR}/keys/out/${HNAME}-server.pem

openssl verify -CAfile ${ROOTDIR}/keys/ca.pem ${ROOTDIR}/keys/out/${HNAME}-server.pem