from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import datetime
import pandas as pd
import re
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Helper functions
def load_users():
    try:
        users_df = pd.read_csv('users.csv')
    except FileNotFoundError:
        users_df = pd.DataFrame(columns=['Username', 'Password', 'LastLogin'])
        users_df.to_csv('users.csv', index=False)
    return users_df

def load_orders():
    try:
        orders_df = pd.read_csv('orders.csv')
    except FileNotFoundError:
        orders_df = pd.DataFrame(columns=['Username', 'Item', 'Quantity', 'TotalPrice', 'OrderTime'])
        orders_df.to_csv('orders.csv', index=False)
    return orders_df

def load_menu():
    try:
        menu_df = pd.read_csv('menu.csv')
    except FileNotFoundError:
        menu_df = pd.DataFrame(columns=['Item', 'Price'])
        menu_df.to_csv('menu.csv', index=False)
    return menu_df

def get_price(item_name):
    menu_df = load_menu()
    item_row = menu_df[menu_df['Item'].str.lower() == item_name.lower()]
    if not item_row.empty:
        return float(item_row['Price'].values[0])
    else:
        return None

# Routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        users_df = load_users()
        password_regex = re.compile(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{3,}$')

        if username in users_df['Username'].values:
            flash("Username already exists. Please choose another one.", 'error')
        elif not password_regex.match(password):
            flash("Invalid password. Must contain at least one letter, one number, one special character, and be at least 3 characters long.", 'error')
        else:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            new_user = pd.DataFrame({'Username': [username], 'Password': [password], 'LastLogin': [current_time]})
            new_user.to_csv('users.csv', index=False, mode='a', header=False)
            flash("Registration successful. You can now log in.", 'success')
            return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users_df = load_users()

        if username in users_df['Username'].values and password == users_df.loc[users_df['Username'] == username, 'Password'].values[0]:
            session['username'] = username
            last_login = users_df.loc[users_df['Username'] == username, 'LastLogin'].values[0]
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            users_df.loc[users_df['Username'] == username, 'LastLogin'] = current_time
            users_df.to_csv('users.csv', index=False)
            flash(f"Welcome back, {username}! Last login: {last_login}", 'success')
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid username or password. Please try again.", 'error')

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        flash("Please log in to access the dashboard.", 'error')
        return redirect(url_for('login'))

    menu = load_menu().to_dict('records')
    return render_template('dashboard.html', username=session['username'], menu=menu)

@app.route('/place_order', methods=['POST'])
def place_order():
    if 'username' not in session:
        flash("Please log in to place an order.", 'error')
        return redirect(url_for('login'))

    item = request.form['item']
    quantity = int(request.form['quantity'])

    price = get_price(item)
    if price is None:
        flash("Invalid item selected. Please try again.", 'error')
        return redirect(url_for('dashboard'))

    total_price = price * quantity
    order_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_order = pd.DataFrame({'Username': [session['username']], 'Item': [item], 'Quantity': [quantity], 'TotalPrice': [total_price], 'OrderTime': [order_time]})
    new_order.to_csv('orders.csv', index=False, mode='a', header=False)
    flash(f"Order placed successfully for {item} (x{quantity}).", 'success')
    return redirect(url_for('dashboard'))

@app.route('/previous_orders')
def previous_orders():
    if 'username' not in session:
        flash("Please log in to view your orders.", 'error')
        return redirect(url_for('login'))

    orders_df = load_orders()
    user_orders = orders_df[orders_df['Username'] == session['username']]
    return render_template('previous_orders.html', orders=user_orders.to_dict('records'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash("Logged out successfully.", 'success')
    return redirect(url_for('home'))

if __name__ == '__main__':
    # Ensure necessary CSV files exist
    if not os.path.exists('users.csv'):
        pd.DataFrame(columns=['Username', 'Password', 'LastLogin']).to_csv('users.csv', index=False)
    if not os.path.exists('orders.csv'):
        pd.DataFrame(columns=['Username', 'Item', 'Quantity', 'TotalPrice', 'OrderTime']).to_csv('orders.csv', index=False)
    if not os.path.exists('menu.csv'):
        pd.DataFrame(columns=['Item', 'Price']).to_csv('menu.csv', index=False)

    app.run(debug=True, port = 5001)
