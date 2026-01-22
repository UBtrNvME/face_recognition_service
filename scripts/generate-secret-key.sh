#!/bin/bash
# Generate a secure random secret key for JWT

echo "Generating secure secret key..."
SECRET_KEY=$(openssl rand -hex 32)
echo ""
echo "Add this to your .env file:"
echo "SECRET_KEY=$SECRET_KEY"
echo ""

