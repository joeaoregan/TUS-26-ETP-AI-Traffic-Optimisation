#!/bin/bash
# Generate self-signed TLS certificates for inter-service communication.
# These are for development/demo only — production should use a proper CA.

set -e

CERT_DIR="$(dirname "$0")/certs"
mkdir -p "$CERT_DIR"

# Generate CA key and certificate
openssl genrsa -out "$CERT_DIR/ca.key" 2048
openssl req -x509 -new -nodes -key "$CERT_DIR/ca.key" \
  -sha256 -days 365 -out "$CERT_DIR/ca.crt" \
  -subj "/C=IE/ST=Westmeath/L=Athlone/O=TUS/CN=traffic-ca"

# Generate server key and CSR with SANs for all services
openssl genrsa -out "$CERT_DIR/server.key" 2048
cat > "$CERT_DIR/san.cnf" <<EOF
[req]
distinguished_name = req_dn
req_extensions = v3_req
prompt = no

[req_dn]
C = IE
ST = Westmeath
L = Athlone
O = TUS
CN = traffic-services

[v3_req]
subjectAltName = @alt_names

[alt_names]
DNS.1 = rl-inference
DNS.2 = lstm-predictor
DNS.3 = java-gateway
DNS.4 = localhost
EOF

openssl req -new -key "$CERT_DIR/server.key" \
  -out "$CERT_DIR/server.csr" -config "$CERT_DIR/san.cnf"

openssl x509 -req -in "$CERT_DIR/server.csr" \
  -CA "$CERT_DIR/ca.crt" -CAkey "$CERT_DIR/ca.key" -CAcreateserial \
  -out "$CERT_DIR/server.crt" -days 365 -sha256 \
  -extfile "$CERT_DIR/san.cnf" -extensions v3_req

# Clean up intermediate files
rm -f "$CERT_DIR/server.csr" "$CERT_DIR/san.cnf" "$CERT_DIR/ca.srl"

echo "TLS certificates generated in $CERT_DIR/"
echo "  ca.crt      — CA certificate (trust store)"
echo "  server.crt  — Server certificate"
echo "  server.key  — Server private key"
