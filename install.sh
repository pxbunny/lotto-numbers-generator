#!/bin/sh

set -e

root_dir=$(git rev-parse --show-toplevel)
branch_name=$(git rev-parse --abbrev-ref HEAD)

if [ "$branch_name" != "main" ]; then
  echo "Skipping install to $CLI_APP_INSTALLATION_DIR — not on the main branch."
  exit 0
fi

echo "Loading environment variables..."

source $root_dir/.env

if [ -z "$CLI_APP_INSTALLATION_DIR" ]; then
  echo "CLI_APP_INSTALLATION_DIR environment variable is not set."
  exit 1
fi

echo "Creating executable..."

rm -rf $root_dir/dist

pyinstaller $root_dir/lotto/__main__.py \
  --name $CLI_APP_NAME \
  --distpath $root_dir/dist \
  --workpath $root_dir/build \
  --log-level=WARN \
  --exclude-module pyinstaller

echo "Removing existing installation at $CLI_APP_INSTALLATION_DIR..."

rm -rf $CLI_APP_INSTALLATION_DIR/$CLI_APP_NAME

echo "Copying executable to $CLI_APP_INSTALLATION_DIR..."

cp $root_dir/config.yaml $root_dir/dist/$CLI_APP_NAME/config.yaml
cp -r $root_dir/dist/$CLI_APP_NAME $CLI_APP_INSTALLATION_DIR
