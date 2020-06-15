# KaplanCodingChallenge - Justin Larkin
This is a repository with the code I created for the Kaplan Coding Challenge


The application I created is a Forex trading bot that will receive alerts, execute a trade via the broker using those alerts, and send SMS messages to a cell phone when trades are executed. This Python script runs a Flask server that continuously receives webhook URL POST messages sent to it's address and executes trades using the OANDA Forex Broker API. After executing a trade or on error of the application, a text will be sent out via the Twilio SMS Messaging API. 

What I'd Like to do next: Add in Forex news alerts, which will be sent out through SMS message.
