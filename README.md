# scrapper
A simple python API scrapper


# Run the application

## Install requirements 

    pip install -r requirements.txt

## Set the Reddit client ID and SECRET

To fetch the comments from Reddit, you need to create a reddit app (https://ssl.reddit.com/prefs/apps/) and set the two following environment variables:

    SCRAPPER_REDDIT_ID = "reddit-app-id"
    SCRAPPER_REDDIT_SECRET = "reddit-app-secret"

## Set the GOOGLE_APPLICATION_CREDENTIALS

To use Google language processing, you need valid Google application credentials, you can set the GOOGLE_APPLICATION_CREDENTIALS environment variable for that purpose. 
It should ideally point to a service account JSON key that allow access to a GCP project with enabled language API. 

For the environment variable, you can create a .env file with the keys / values pairs. Check the .env.sample for reference. 

## Start the server

From the parent folder, run the following:

    EXPORT FLASK_ENV=development
    EXPORT FLASK_APP=scrapper
    flask run

You can then load the web interface on 127.0.0.1:5000. 

## Obtain a Google Play music Oauth token. 

In order to allow the library creation, you will need to fetch a Google Oauth token. You can do that through the /google_config route. 
Look for the oauth URL in the console and follow the Oauth process.


## TODO

1. Visual feedback on client side when scrapping (sockets implementation + ajax)
2. Allow to cherry pick the songs from google play search results to prevent mistakes 
