#!/bin/sh
# Build and run locally. CodeCrafters uses the scripts in .codecrafters/.
set -eu
cd "$(dirname "$0")"

# Use the standalone macOS Command Line Tools when no toolchain is selected.
if [ "$(uname -s)" = "Darwin" ] && [ -z "${DEVELOPER_DIR:-}" ] && [ -d /Library/Developer/CommandLineTools ]; then
  export DEVELOPER_DIR=/Library/Developer/CommandLineTools
fi

# The starter has no external dependencies; vcpkg is optional for local builds.
if [ -n "${VCPKG_ROOT:-}" ] && [ -f "$VCPKG_ROOT/scripts/buildsystems/vcpkg.cmake" ]; then
  cmake -B build -S . -DCMAKE_TOOLCHAIN_FILE="$VCPKG_ROOT/scripts/buildsystems/vcpkg.cmake"
else
  cmake -B build -S .
fi
cmake --build build
exec ./build/redis "$@"
