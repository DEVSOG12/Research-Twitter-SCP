# Twitter Research Project: A project to fetch and analyze tweets based on usernames 

## Introduction
This project is a research project to fetch and analyze tweets based on usernames. The project is built using Python and the following libraries are used:
* Tweepy

## Installation
The project requires Python 3.6 or higher to run. The following libraries are required to run the project:
* Tweepy

## Usage
The project is divided into two parts:
* Fetching tweets
* Analyzing tweets

### Fetching tweets
The tweets are fetched using the Twitter API. The following steps are required to fetch tweets:
* Create a Twitter developer account
* Create a Twitter app
* Generate the API keys and access tokens
* Create a file named `config.ini` and add the following code:
```ini
[twitter]
api_key = api_key
api_key_secret = api_key_secret
access_token = access_token
access_token_secret = access_token_secret
```

* Run the `main.py` file
* In the ./data folder contains .csv files usernames to fetch tweets for and keywords to filter tweets with
* The tweets are fetched and stored in the ./outputs folder

### Analyzing tweets
The tweets are analyzed using the following steps:
* Within the `api.py` file, keywords are defined to filter tweets with
* Run the `main.py` file
* The tweets are analyzed and stored in the ./outputs folder


## License
MIT License

## Author
* [**Oreofe Solarin**](https://github.com/devsog12)

## Acknowledgements
* **Tweepy**
* [**Twitter API**](https://developer.twitter.com/en/docs/twitter-api)
* [**Python**](https://www.python.org/)
* [**Stack Overflow**](https://stackoverflow.com/)

## Disclaimer
This project is for research purposes only. The author is not responsible for any misuse of the project.
