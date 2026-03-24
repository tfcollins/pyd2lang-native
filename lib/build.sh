#!/bin/bash
# Build the d2lib shared library for Linux/macOS
set -e

cd "$(dirname "$0")"

echo "Building d2lib shared library..."
go build -buildmode=c-shared -o d2lib.so d2lib.go

echo "Copying to d2/resources/..."
mkdir -p ../d2/resources
cp d2lib.so ../d2/resources/

echo "Cleaning up build artifacts..."
rm -f d2lib.so d2lib.h

echo "Done."
