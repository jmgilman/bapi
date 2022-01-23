#!/bin/bash

docker build -t bapi .
docker run --name "BAPI" \
           -e BAPI_ENTRYPOINT \
           -e BAPI_AUTH \
           -e BAPI_STORAGE \
           -e BAPI_S3__BUCKET \
           -e AWS_ACCESS_KEY_ID \
           -e AWS_SECRET_ACCESS_KEY \
           -e AWS_DEFAULT_REGION \
           -p 8080:8080 \
           -d \
           bapi