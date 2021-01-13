#!/bin/bash
ROOTDIR=`dirname $0`
echo $ROOTDIR

rm -rf ${ROOTDIR}/keys/out
rm ${ROOTDIR}/privkey.pem
mkdir ${ROOTDIR}/keys/out

### create CA
openssl req -passout pass:foobar -out ${ROOTDIR}/keys/ca.pem -new -x509 -days 3650 -subj "/C=AU/ST=NSW/O=Organisation/CN=root/emailAddress=user@domain.com"
echo "00" > ${ROOTDIR}/keys/file.srl # two random digits number
