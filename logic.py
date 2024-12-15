from PyQt6.QtWidgets import *
from PyQt6.QtCore import pyqtSlot
from gui import *
import os
import json
class Logic(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.accounts_file = "accounts.json"
        self.current_account = None

        # Connect buttons
        self.ui.Submit_button_3.clicked.connect(self.create_account)
        self.ui.Submit_button_4.clicked.connect(self.search_account)
        self.ui.Submit_button.clicked.connect(self.process_transaction)
        self.ui.Submit_button_2.clicked.connect(self.logout)

        # Set PIN input to masked mode
        self.ui.PIN_input.setEchoMode(self.ui.PIN_input.EchoMode.Password)

        # Initialize accounts file
        self.initialize_accounts_file()

    def initialize_accounts_file(self):
        if not os.path.exists(self.accounts_file):
            with open(self.accounts_file, "w") as f:
                json.dump({}, f)

    def load_accounts(self):
        with open(self.accounts_file, "r") as f:
            return json.load(f)

    def save_accounts(self, accounts):
        with open(self.accounts_file, "w") as f:
            json.dump(accounts, f)

    @pyqtSlot()
    def create_account(self):
        first_name = self.ui.FirstName_input.text().strip()
        last_name = self.ui.LastName_input.text().strip()
        pin = self.ui.PIN_input.text().strip()

        if not first_name.isalpha():
            QMessageBox.critical(self, "Error", "First name must contain only letters.")
            return

        if not last_name.isalpha():
            QMessageBox.critical(self, "Error", "Last name must contain only letters.")
            return

        if not pin.isdigit():
            QMessageBox.critical(self, "Error", "PIN must contain only letters.")
            return

        accounts = self.load_accounts()

        if pin in accounts:
            QMessageBox.critical(self, "Error", "An account with this PIN already exists.")
            return

        accounts[pin] = {
            "first_name": first_name,
            "last_name": last_name,
            "balance": 0
        }

        self.save_accounts(accounts)
        QMessageBox.information(self, "Success", "Account created successfully.")

    @pyqtSlot()
    def search_account(self):
        pin = self.ui.PIN_input.text().strip()

        accounts = self.load_accounts()

        if pin not in accounts:
            QMessageBox.critical(self, "Error", "No account found with this PIN.")
            return

        self.current_account = pin
        account = accounts[pin]
        QMessageBox.information(
            self, "Account Found",
            f"Welcome, {account['first_name']} {account['last_name']}! Your balance is ${account['balance']}"
        )

    @pyqtSlot()
    def process_transaction(self):
        if not self.current_account:
            QMessageBox.critical(self, "Error", "You must log in to an account first with Search with PIN.")
            return

        try:
            amount = float(self.ui.Amount_input.text().strip())
        except ValueError:
            QMessageBox.critical(self, "Error", "Amount must be a valid number.")
            return

        accounts = self.load_accounts()
        account = accounts[self.current_account]

        if self.ui.Deposit_radio.isChecked():
            account["balance"] += amount
            QMessageBox.information(self, "Success", f"You have successfully deposited ${amount}.")
        elif self.ui.Withdraw_radio.isChecked():
            if amount > account["balance"]:
                QMessageBox.critical(self, "Error", "Insufficient funds.")
                return
            account["balance"] -= amount
            QMessageBox.information(self, "Success", f"You have successfully withdrew ${amount}.")
        else:
            QMessageBox.critical(self, "Error", "Please select Deposit or Withdraw.")
            return

        self.save_accounts(accounts)
        self.ui.AccountBalance_label.setText(f"Current Balance: ${account['balance']}")

    @pyqtSlot()
    def logout(self):
        self.current_account = None
        self.ui.FirstName_input.clear()
        self.ui.LastName_input.clear()
        self.ui.PIN_input.clear()
        self.ui.Amount_input.clear()
        self.ui.AccountBalance_label.clear()
        QMessageBox.information(self, "Logout", "You have successfully logged out.")
