#!/bin/bash
mkdir -p server/certs
openssl req -x509 -newkey rsa:4096 -keyout server/certs/key.pem -out server/certs/cert.pem -days 365 -nodes -subj "/CN=ghostmesh.local"
echo "[+] Self-signed cert created in server/certs/"
