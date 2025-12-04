#!/bin/bash

set -e

# Create certs directory
mkdir -p certs
pushd certs > /dev/null

# Generate private key for CA
openssl genrsa -out ca.key 4096

# Generate self-signed CA certificate
openssl req -x509 -new -nodes -key ca.key -sha256 -days 200 -out ca.crt \
    -subj "/CN=MyRootCA"

# Generate server private key
openssl genrsa -out server.key 4096

# Generate a certificate signing request (CSR) for the server
openssl req -new -key server.key -out server.csr \
    -subj "/CN=localhost"

# Generate server certificate signed by the CA
openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial \
    -out server.crt -days 3650 -sha256 -extfile ../.ci/server_ext.cnf -extensions v3_req

# Generate client private key
openssl genrsa -out client.key 4096

# Generate a certificate signing request (CSR) for the client
openssl req -new -key client.key -out client.csr \
    -subj "/CN=grpc-client"

# Generate client certificate signed by the CA
openssl x509 -req -in client.csr -CA ca.crt -CAkey ca.key -CAcreateserial \
    -out client.crt -days 200 -sha256

# Verify server certificate
openssl verify -CAfile ca.crt server.crt

# Verify client certificate
openssl verify -CAfile ca.crt client.crt

popd > /dev/null
