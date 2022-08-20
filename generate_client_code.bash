#!/bin/bash -eu

pushd be > /dev/null
poetry run ./scripts/generate_openapi.py
popd > /dev/null

OPENAPI_YAML="openapi.yaml"

if [ ! -e "${OPENAPI_YAML}" ]; then
    echo "${OPENAPI_YAML} not found."
    exit 1
fi
if [ ! -e "${PWD}/${OPENAPI_YAML}" ]; then
    echo "${OPENAPI_YAML} not found in this directory."
    exit 1
fi

docker run --rm \
    -v "${PWD}:/local" \
    -u $(id -u):$(id -g) \
    openapitools/openapi-generator-cli generate \
    -i /local/${OPENAPI_YAML} \
    -g typescript-fetch \
    -o /local/fe/src/client
