import configparser

# My settings
config = configparser.ConfigParser()
config.read("settings.ini")

account_id = config.get("oanda", "account_id")
access_token = config.get("oanda", "access_token")

db_name = "candles"
