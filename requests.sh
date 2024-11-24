#!/bin/bash

curl -X 'GET' \
  'http://localhost:8001/api/api/reports/nomenclature/JSON' \
  -H 'accept: application/text'


curl -X 'GET' \
  'http://localhost:8001/api/api/reports/formats' \
  -H 'accept: application/json'

curl -X 'POST' \
  'http://localhost:8001/api/api/filter/nomenclature' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "с",
  "filter_name": "LIKE",
  "unique_code": "",
  "filter_unique_code": "LIKE"
}'

curl -X 'GET' \
  'http://localhost:8001/api/api/block_period/get' \
  -H 'accept: application/text'


curl -X 'POST' \
  'http://localhost:8000/api/api/block_period/set' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "block_period": "2023-10-01"
}'

curl -X 'PATCH' \
  'http://localhost:8000/api/api/nomenclature' \
  -H 'accept: text/html' \
  -H 'Content-Type: application/json' \
  -d '{
  "unique_code": "88ec2e81c1b941b29b91758d3d5bc3de",
  "name": "Ваниль",
  "group_id": "8181c24fafb64526ae3641ad2fce49eb",
  "range_id": "66148f2b8d134b8c8aabc8c90be1530c"
}'