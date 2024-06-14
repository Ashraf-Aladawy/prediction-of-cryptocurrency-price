# CryptoPre

## Project Description

CryptoPre is a web application  where users can view current prices of major cryptocurrencies, get predictions for future prices, and stay updated with the latest cryptocurrency news.

## Features

- Display current prices for major cryptocurrencies.
- Predict future prices for Bitcoin, Ethereum, Litecoin, and Monero.
- Provide the latest news in the cryptocurrency market.
- User authentication for accessing personalized features.
- Contact form for user inquiries.

##Technologies Used

Frontend: HTML, CSS, JavaScript, Bootstrap
Backend: Flask, Python
Database: SQL
Others: Node.js, Express.js


## Prerequisites

Make sure you have the following installed:

- [Python] (https://www.python.org/downloads/)
- [Node.js] (https://nodejs.org/)

## Backend Run

 ==> OPEN TERMINAL-command prompt

1. Create a virtual environment and activate it:

    '''sh
     python -m venv venv
     venv\Scripts\activate
    '''
2. Install the required packages:
   '''sh
    pip install -r (requirements.txt)
   '''
3. Set up environment variables:

     Create a `.env` file in the root directory.
     Add the following environment variables:

    ```plaintext

       DB_CONNECTION=mysql
       DB_HOST=127.0.0.1
       DB_PORT=3306
       DB_DATABASE=cryptopre
       DB_USERNAME=root
       DB_PASSWORD=

    ```

4. Run the Flask application:

    '''sh

    cd venv/scripts
    acitvate
    cd ../..
    python app.py
    
    '''
5. Run node.js

   '''sh
    node server.js

   '''

## Usage

1. Open your web browser and navigate to `http://127.0.0.1:5050/`.
2. Explore the features: view cryptocurrency current prices, predict future prices, read news, and use the contact form.


