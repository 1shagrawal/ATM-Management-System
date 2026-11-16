# ATM Simulator in Python
import os
import time
import pwinput
from datetime import datetime

# Initial Balance & PIN 
FILE_NAME = "atm.txt"
account = {
    "name" : "Bank of India",
    "default_balance" : 10000,  # Initial Balance 
    "pin_code" : "1234",  # PIN for account
    "type" : "savings account"
}

# Define the ATM file
def initialize_file():
    if not os.path.exists(FILE_NAME):
        with open (FILE_NAME, "w", encoding="utf-8") as file:
            file.write(str(account["default_balance"]) + "\n")

# Read account balance from file
def get_balance():
    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            balance = float(file.readline())
        return balance
    except (FileNotFoundError, ValueError):
        print("File error. Initializing account...")
        initialize_file()
        return account["default_balance"] 

# Load transaction history 
def load_transactions():
    transactions = []
    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            file.readline()
            transactions = [
                line.strip()
                for line in file
                if line.strip()
            ]
    except OSError:
        print("Unable to read transaction history.")
    return transactions

# Save balance and transactions
def save_data(balance, transactions):
    try:
        with open(FILE_NAME, "w", encoding="utf-8") as file:
            file.write(str(balance) + "\n")
            for transaction in transactions:
                file.write(transaction + "\n")
    except OSError:
        print("Error saving account data.")

# Welcome Message
def atm():
    print("\nWelcome to BOI ATM!")
    print("================")
    print("BANK OF INDIA")
    print("================")

# ATM Function 1: Check Account Balance
def check_balance(balance):
    date = datetime.now()
    print(f"\n Your current balance is: ₹{balance:g}")
    print(f"Date and Time: {date}")
    print()

# ATM Function 2: Money Deposit 
def deposit_money(balance, transactions):
    try:
        amount = float(input("Enter amount to deposit: "))
    except ValueError:
            print("Invalid amount. Please enter numbers only.")
    else: 
        if amount <= 0:
            print("Amount must be greater than zero.")
        else:
            balance += amount
            timestamp = datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")
            transactions.append(
                f"Deposit: ₹{amount:g} | Balance: ₹{balance:g} | Date-Time: {timestamp}"
            )
            print("Updating...")
            time.sleep(1)
            print(f"₹{amount:g} has been deposited successfully.") 
            print(f"Your new balance is ₹{balance:g}.")
            print(f"Date and Time: {timestamp}")
            save_data(balance, transactions)
    return balance

# ATM Function 3: Money Withdrawal
def withdraw_money(balance, transactions):
    try:
        amount = float(input("Enter the amount to withdraw: "))
    except ValueError:
            print("Invalid entry. Please enter numbers only.")
    else:
        if amount <= 0:
            print("Invalid amount. Enter a positive amount.")
        elif amount > balance:
            print(f"Insufficient balance. Your current balance is ₹{balance:g}")
        else:
            print("Updating...")
            time.sleep(1)
            balance -= amount
            timestamp = datetime.now().strftime("%d-%m-%Y %I:%M:%S %p") 
            transactions.append(
                f"withdrawal: ₹{amount:g} | Balance: ₹{balance:g} | Date-Time: {timestamp}"
            )
            print("Withdrawal Successful. COLLECT YOUR CASH.")
            print(f"₹{amount:g} has been withdrawn.")
            print(f"Your new balance is ₹{balance:g}")
            print(f"Date and Time: {timestamp}")
            save_data(balance, transactions)
    return balance

# ATM Function 4: View Mini Statement 
def mini_statement(transactions):
    print("\n******** MINI STATEMENT ********")
    if not transactions:
        print("No transactions available.")
    else:
        for i, transaction in enumerate(transactions, 1):
            print(f"{i}. {transaction}")
    print("********************************")

# ATM Function 5: Exit the Program
def exit_program():
    print("\nThank You for using BOI ATM!")
    print("Bye Bye!")

# ATM Main Menu
def choice (balance, transactions):
    while True:
        print("\n ******** ATM Menu ********")
        print("1. Check Balance")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Mini Statement")
        print("5. Exit")

        try:
            user_choice = int(input("Enter your choice(1-5): "))
        except ValueError:
            print("Please enter a valid menu option.")
            continue

        if user_choice == 1:
            check_balance(balance)
        elif user_choice == 2:
            balance = deposit_money(balance, transactions)
        elif user_choice == 3:
            balance = withdraw_money(balance, transactions)
        elif user_choice == 4:
            mini_statement(transactions)
        elif user_choice == 5:
            save_data(balance, transactions)
            exit_program()
            break
        else:
            print("Invalid Choice. Please select a valid option.")

# Login Process
# PIN Verification
def run_atm(balance, transactions):
    pin_attempts = 0
    while pin_attempts < 3:
        # Prompt the user to enter the PIN
        enter_pin = pwinput.pwinput(
            "Enter your 4-digit PIN: ", mask="*"
        )
        # Check if the entered PIN is correct
        if enter_pin == account["pin_code"]:
            print("\nLogin successful!!")
            print("PIN is correct.")
            choice(balance, transactions)
            return
        else:
            pin_attempts += 1
            print("Incorrect PIN. Try Again")
    if pin_attempts == 3:
        print("\n Too many incorrect attempts.")
        print("ATM Locked. Contact Customer Service. Exiting.")

# Initialize and Execute the Program
def main():
    initialize_file()
    balance = get_balance()
    transactions = load_transactions()
    atm()
    run_atm(balance, transactions)

# Run the ATM
if __name__ == "__main__":
    main()