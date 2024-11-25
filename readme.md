Setup:
1. Commands: Run the following commands to setup the server
* docker compose build
* docker compose up

2. Connect to the instantiated docker postgres image via psql cli and run 
scripts/sql/ddl/0.0.1.sql
to create the product table into the database

3. Go to https://webhook.site/ and copy your unique webhook url pass the url into the following step under callback_url parameter.

4. docker compose stop
5. docker compose up

6. Curl: Import the curl in postman to use the api.
api_params: 
offset: start_page
limit: number of page
callback_url: webhook_url


curl --location 'http://0.0.0.0:8007/apis/scrape_product' \
--header 'Content-Type: application/json' \
--data '{
    "reference_number": "dcbe00e1-034c-438b-ace0-d7a7e760805d",
    "offset": 1,
    "limit": 5,
    "callback_url": "https://webhook.site/0aec1fa4-141b-427f-ba64-22fc51547103"
}'

4. wait for th webhook notification arrive.