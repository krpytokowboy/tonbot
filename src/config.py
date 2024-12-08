BOT_TOKEN = '7668774327:AAF5b5Xm7FhBByAm6XtPEs30B6yM3SdLWtc'
DEPOSIT_ADDRESS = 'UQCEAjaSoRSZyAzhu98sa3qAqJjQUlYA5exr9zLdJlkC45wi'
API_KEY = '1d9296e10823701940f033488d45fcb01ba394319cacf9c99f21f4922598d16e'
RUN_IN_MAINNET = True  # Switch True/False to change mainnet to testnet

if RUN_IN_MAINNET:
    API_BASE_URL = 'https://toncenter.com'
else:
    API_BASE_URL = 'https://testnet.toncenter.com'
