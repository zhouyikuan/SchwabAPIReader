# SchwabAPIReader
This is a minimal implementation of accessing Schwab API using python.

Prerequisites:
1. Own a Schwab brokerage account
2. Be registered on the Schwab API Developer Portal (this is a separate account).
    - You must wait for your account to approved 
    - You must have an App with "Ready For Use" status
    - Fill in the following three pieces of information into the code: (app_key, app_secret, auth_callback_url)

Note:
    In the production environment, the one time code will be delivered to your specified 
    callback address. Here we will need to manually input to our code.
