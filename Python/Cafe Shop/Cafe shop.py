# import pandas as pd
from datetime import datetime
import time
import re
import tabulate
# from IPython.display import display

# Function to load user data from CSV
def load_users():
    try:
        # Attempt to read user data from CSV file
        users_df = pd.read_csv('users.csv')
    except FileNotFoundError:
        # Create an empty DataFrame if the file doesn't exist
        users_df = pd.DataFrame(columns=['Username', 'Password', 'LastLogin'])
        users_df.to_csv('users.csv', index=False, mode='a')
    return users_df

# Function for user registration
def register(username, password):
    users_df = load_users()

    # Password validation regex
    password_regex = re.compile(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{3,}$')

    if username in users_df['Username'].values:
        # Check if the username already exists
        print("Username already exists. Please choose another one.")
    elif not password_regex.match(password):
        # Validate the password format
        print("Invalid password. Password must contain at least one letter, one number, and one special character (@$!%*#?&), and have a minimum length of 3.")
    else:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Create a new user DataFrame
        new_user = pd.DataFrame({'Username': [username], 'Password': [password], 'LastLogin': [current_time]})
        
        # Save the new user to the CSV file
        new_user.to_csv('users.csv', index=False, mode='a', header=False)
        print(f"Registration successful. Welcome, {username}!")

# Function to load order history from CSV
def load_orders():
    try:
        # Attempt to read order data from CSV file
        orders_df = pd.read_csv('orders.csv')
    except FileNotFoundError:
        # Create an empty DataFrame if the file doesn't exist
        orders_df = pd.DataFrame(columns=['Username', 'Item', 'Quantity', 'TotalPrice', 'OrderTime'])
        orders_df.to_csv('orders.csv', index=False, header=True, mode='a')
        return orders_df

    return orders_df

# Function for user login
def login(username, password):
    users_df = load_users()
    if (username in users_df['Username'].values) and (password == users_df.loc[users_df['Username'] == username, 'Password'].values[0]):
        # Successful login
        last_login = users_df.loc[users_df['Username'] == username, 'LastLogin'].values[0]
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        users_df.loc[users_df['Username'] == username, 'LastLogin'] = current_time
        users_df.to_csv('users.csv', index=False)
        print(f"Welcome back, {username}! Last login: {last_login}")
        return True
    else:
        # Invalid username or password
        print("Invalid username or password. Please try again.")
        return False

# Function to load menu from CSV
def load_menu():
    try:
        # Attempt to read menu data from CSV file
        menu_df = pd.read_csv('menu.csv')
    except FileNotFoundError:
        # Create an empty DataFrame if the file doesn't exist
        print("Menu file not found.")
        menu_df = pd.DataFrame(columns=['Item', 'Price'])
        menu_df.to_csv('menu.csv', index=False, mode='a')
    return menu_df

# Function to display menu

# for jupiter

# def display_menu():
#     menu_df = load_menu()
#     menu_df.index += 1  # Shift the index to start from 1
#     print("Menu:")
#     display(menu_df)


def display_menu():
    menu_df = load_menu()
    menu_df.index += 1  # Shift the index to start from 1
    print("Menu:")
    print(tabulate.tabulate(menu_df, headers='keys', tablefmt='pretty', showindex=True))

quantity = 0

# Function to take order
def take_order():
    global quantity  # Use the global quantity variable
    menu_df = load_menu()
    while True:
        try:
            choice = int(input("Enter the number of the item you want to order: "))
            if 1 <= choice <= len(menu_df):
                quantity = int(input("Enter the quantity: "))  # Set the global quantity variable
                return menu_df.loc[choice - 1, 'Item']
            else:
                print("Invalid choice. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")
            
def get_price(item_name):
    df = load_menu()
    """Get the price of a specific item."""
    
    item_row = df[df['Item'].str.lower() == item_name.lower()]
    
    if not item_row.empty:
        return item_row['Price'].values[0]
    else:
        return "Item not found"
            
def prepare_drink(order):
    # Simulate drink preparation
    print(f"Preparing {order}...")
    time.sleep(0.3)
    total_orders.append(order)

def order_serve(order):
    # Serve the prepared order
    print(f"Here is your {order}.")

def show_bill(order):
    # Display the bill for the ordered item, multiplied by the quantity
    orignal_price = price = get_price(order)
    price = get_price(order) * quantity
    
    print(f"Item: {order}, Orignal Price: {orignal_price}, Quantity: {quantity}, Total Price: Rs.{price:.2f}")

def check_payment(price):
    # Check if the payment amount is sufficient
    bill_amount = price
    amount_due = price  # Initialize amount_due with the total bill amount

    while amount_due > 0:
        try:
            payment = float(input(f"Enter your payment amount (Amount due: Rs.{amount_due:.2f}): Rs."))
            if payment < 0:
                print("Invalid payment amount. Please enter a positive value.")
            elif payment < amount_due:
                amount_due -= payment
                print(f"Payment amount received: Rs.{payment:.2f}. Amount pending: Rs.{amount_due:.2f}")
            else:
                amount_due -= payment
                if amount_due == 0:
                    print("Thank you! Payment received.")
                else:
                    print(f"Thank you! Payment received. Change: Rs.{-amount_due:.2f}")
                break
        except ValueError:
            # Handle invalid payment input (non-numeric)
            print("Invalid input. Please enter a valid payment amount.")

    return amount_due


def thank_you():
    # Display a thank-you message
    print("Thank you for ordering from our Cafe!")

# Function to place an order
def place_order(username):
    global quantity  # Use the global quantity variable
    menu_df = pd.read_csv('menu.csv')
    display_menu()

    item = take_order()

    # Check if the item exists in the menu
    if item not in menu_df['Item'].values:
        print("Invalid item. Please choose a valid item from the menu.")
        return

    total_price = get_price(item) * quantity

    order_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_orders = pd.DataFrame({'Username': [username], 'Item': [item], 'Quantity': [quantity], 'TotalPrice': [total_price], 'OrderTime': [order_time]})
    new_orders.to_csv('orders.csv', index=False, mode='a', header=False)
    print("Order placed successfully!")

    prepare_drink(item)
    order_serve(item)
    show_bill(item)
    check_payment(total_price)

# Function to view previous orders
def view_previous_orders(username):
    orders_df = load_orders()
    user_orders = orders_df[orders_df['Username'] == username]
    if user_orders.empty:
        print("No previous orders.")
    else:
        print("\nPrevious Orders:")
        print(user_orders)

# Function to display the main menu
def main_menu():
    # Display the main menu options
    print("\nMain Menu:")
    print("1. Place an order")
    print("2. View previous orders")
    print("3. Logout")

# Main program
def cafe_shop():
    # Main entry point for the cafe shop management system

    print("Welcome to the Cafe Shop Management System!")

    while True:
        # Main loop for user interactions
        print("\n1. Register\n2. Login\n3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            # User registration
            username = input("Enter your username: ")
            password = str(input("Enter your password: "))
            register(username, password)
        elif choice == '2':
            # User login
            username = input("Enter your username: ")
            password = str(input("Enter your password: "))
            if login(username, password):
                while True:
                    # Sub-menu for logged-in users
                    main_menu()
                    option = input("Enter your choice: ")
                    if option == '1':
                        # Place an order
                        place_order(username)
                    elif option == '2':
                        # View previous orders
                        view_previous_orders(username)
                    elif option == '3':
                        # Logout
                        print("Logging out. Goodbye!")
                        break
                    else:
                        # Invalid option
                        print("Invalid option. Please try again.")
        elif choice == '3':
            # Exit the program
            print("Exiting. Goodbye!")
            break
        else:
            # Invalid choice
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    # Start the cafe shop management system
    total_orders = [] #Added Global List for Total Orders:
    cafe_shop()
