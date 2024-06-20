import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import load_model
from keras.models import Sequential
from keras.layers import LSTM, GRU, Dropout, Dense
from io import BytesIO
from flask import Flask, render_template, send_file
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import json
import yfinance as yf
import cryptocompare
from yahoo_fin.stock_info import get_live_price
import base64
import time
from functools import wraps
from flask import Flask, render_template, jsonify, request, redirect, url_for, session
#import mysql.connector
import requests

import os
# Generate a random secret key
secret_key = os.urandom(24)

app = Flask(__name__)
# Set the secret key in Flask app
app.secret_key = secret_key


def price_now(coin):
    ticker_symbol = coin+"-USD"
    current_price = get_live_price(ticker_symbol)
    formatted_price = "{:.2f}".format(current_price)

    return formatted_price


# Function to update plot with new data
def update_plot(coin):
    # Retrieve historical price data for the cryptocurrency for the last 30 days
    historical_data = cryptocompare.get_historical_price_day(
        coin, currency="USD", limit=6)
    df = pd.DataFrame(historical_data)

    # Extract timestamps and prices
    # Convert Unix timestamp to datetime
    dates = pd.to_datetime(df['time'], unit='s')
    historical_prices = df['close']

    # Plot historical data
    plt.figure(figsize=(11, 6), facecolor='#f0f0f0')
    plt.plot(dates, historical_prices, label=f"{
             coin} - {"USD"} (Past 7 days)", color='blue')

    # Retrieve real-time price data
    real_time_data = cryptocompare.get_price(coin, currency="USD")
    current_price = real_time_data[coin]["USD"]

    # Add current price to plot
    current_time = pd.Timestamp.now()
    plt.scatter(current_time, current_price, color='red',
                label=f"{coin} - {"USD"} (Today)")

    plt.xlabel("Date")
    plt.ylabel("Price (USD)")
    # Update legend
    plt.legend()

    # Convert plot to bytes
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_data = base64.b64encode(img.getvalue()).decode()

    return plot_data


def predict(coin, close_price):

    scaler = MinMaxScaler(feature_range=(0, 1))
    SEQUENCE_SIZE = 30

    if coin == "BTC":
        model = load_model('models/btc.h5')
        model = Sequential()
        model.add(GRU(units=30, return_sequences=True,
                  input_shape=(SEQUENCE_SIZE, 1)))
        model.add(Dropout(0.2))
        model.add(GRU(units=60, return_sequences=True))
        model.add(Dropout(0.2))
        model.add(GRU(units=90))
        model.add(Dropout(0.2))
        model.add(Dense(units=1))
    elif coin == "LTC":
        model = load_model('models/ltc.h5')
        model = Sequential()
        model.add(GRU(units=30, return_sequences=True,
                  input_shape=(SEQUENCE_SIZE, 1)))
        model.add(Dropout(0.2))
        model.add(GRU(units=60, return_sequences=True))
        model.add(Dropout(0.2))
        model.add(GRU(units=90))
        model.add(Dropout(0.2))
        model.add(Dense(units=1))
    elif coin == "ETH":
        model = load_model('models/eth.h5')
        model = Sequential()
        model.add(GRU(units=30, return_sequences=True,
                  input_shape=(SEQUENCE_SIZE, 1)))
        model.add(Dropout(0.2))
        model.add(GRU(units=60, return_sequences=True))
        model.add(Dropout(0.2))
        model.add(GRU(units=90))
        model.add(Dropout(0.2))
        model.add(Dense(units=1))
    elif coin == "XMR":
        model = load_model('models/xmr.h5')
        model = Sequential()
        model.add(GRU(units=30, return_sequences=True,
                  input_shape=(SEQUENCE_SIZE, 1)))
        model.add(Dropout(0.2))
        model.add(GRU(units=60, return_sequences=True))
        model.add(Dropout(0.2))
        model.add(GRU(units=90))
        model.add(Dropout(0.2))
        model.add(Dense(units=1))

    # Get data from request

    close_price = np.array(close_price)
    close_price = close_price.reshape(-1, 1)
    # Normalize price
    scaler.fit(close_price)
    close_price_scaled = scaler.transform(close_price)

    # Make predictions
    btcy_pred = model.predict(close_price_scaled)

    # Inverse transform the predictions
    btcy_pred = np.array(btcy_pred)

    btcy_pred = scaler.inverse_transform(btcy_pred)

    return btcy_pred


# Route for the home page

# Function to check if user is logged in
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print(session)
        if 'user_id' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return decorated_function


@app.route('/')
def home():
    priceBtc = price_now('BTC')
    priceLtc = price_now('LTC')
    priceEth = price_now('ETH')
    priceXmr = price_now('XMR')
    return render_template('index.html', priceBtc=priceBtc, priceLtc=priceLtc, priceEth=priceEth, priceXmr=priceXmr)


@app.route('/login.html')
def login():
    return render_template('login.html')


@app.route('/logout')
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect(url_for('index'))


# Route for authentication


@app.route('/authenticate', methods=['POST'])
def authenticate():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # Make a request to the Node.js authentication endpoint
    response = requests.post(
        'http://localhost:5000/login', json={"email": email, "password": password})

    if response.status_code == 200:
        # Save data in the session if authentication is successful
        # For example:
        session['user_id'] = response.json().get('user_id')
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'error': 'An error occurred while logging in.'}), response.status_code


@app.route('/index.html')
def index():
    priceBtc = price_now('BTC')
    priceLtc = price_now('LTC')
    priceEth = price_now('ETH')
    priceXmr = price_now('XMR')
    return render_template('index.html', priceBtc=priceBtc, priceLtc=priceLtc, priceEth=priceEth, priceXmr=priceXmr)


@app.route('/dashboard.html')
@login_required
def dashboard():
    priceBtc = price_now('BTC')
    priceLtc = price_now('LTC')
    priceEth = price_now('ETH')
    priceXmr = price_now('XMR')
    return render_template('dashboard.html', priceBtc=priceBtc, priceLtc=priceLtc, priceEth=priceEth, priceXmr=priceXmr)


@app.route('/update.html')
def update():
    return render_template('update.html')


@app.route('/news.html')
def news():
    return render_template('news.html')


@app.route('/btc.html')
@login_required
def btc():
    historical_data = cryptocompare.get_historical_price_day(
        'BTC', currency="USD", limit=29)
    df = pd.DataFrame(historical_data)
    close_price = df['close'].tolist()
    price = price_now('BTC')
    btcy_pred = predict('BTC', close_price)
    day1 = btcy_pred[0][0]
    day3 = btcy_pred[2][0]
    day7 = btcy_pred[6][0]
    return render_template('btc.html', price=price, next_day_1=day1, next_day_3=day3, next_day_7=day7, plot_data=update_plot('BTC'))


@app.route('/ltc.html')
@login_required
def ltc():
    historical_data = cryptocompare.get_historical_price_day(
        'LTC', currency="USD", limit=29)
    df = pd.DataFrame(historical_data)
    close_price = df['close'].tolist()

    price = price_now('LTC')
    btcy_pred = predict('LTC', close_price)
    day1 = btcy_pred[0][0]
    day3 = btcy_pred[2][0]
    day7 = btcy_pred[6][0]
    return render_template('ltc.html', price=price, next_day_1=day1, next_day_3=day3, next_day_7=day7, plot_data=update_plot('LTC'))


@app.route('/eth.html')
@login_required
def eth():
    historical_data = cryptocompare.get_historical_price_day(
        'ETH', currency="USD", limit=29)
    df = pd.DataFrame(historical_data)
    close_price = df['close'].tolist()

    price = price_now('ETH')
    btcy_pred = predict('ETH', close_price)
    day1 = btcy_pred[0][0]
    day3 = btcy_pred[2][0]
    day7 = btcy_pred[6][0]
    return render_template('eth.html', price=price, next_day_1=day1, next_day_3=day3, next_day_7=day7, plot_data=update_plot('ETH'))


@app.route('/xmr.html')
@login_required
def xmr():
    historical_data = cryptocompare.get_historical_price_day(
        'XMR', currency="USD", limit=29)
    df = pd.DataFrame(historical_data)
    close_price = df['close'].tolist()

    price = price_now('XMR')
    btcy_pred = predict('XMR', close_price)
    day1 = btcy_pred[0][0]
    day3 = btcy_pred[2][0]
    day7 = btcy_pred[6][0]
    return render_template('xmr.html', price=price, next_day_1=day1, next_day_3=day3, next_day_7=day7, plot_data=update_plot('XMR'))


if __name__ == '__main__':
    app.run(port=5050, debug=True)
