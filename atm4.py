import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Simulated account with hashed PIN and balance
account_data = {
    "pin": "1234",  # For simplicity (hashed PINs are better in real applications)
    "balance": 1000
    
}

# Create the main application window
root = tk.Tk()
root.title("Virtual ATM")
root.geometry("500x700")  # Set the size of the ATM window
root.resizable(False, False)  # Disable resizing for a consistent ATM layout

# Load background image (replace with your desired ATM machine image)
try:
    atm_image = Image.open("atm_machine.jpg")  # Replace with your ATM background image
    
    atm_bg = ImageTk.PhotoImage(atm_image)
    bg_label = tk.Label(root, image=atm_bg)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
except FileNotFoundError:
    messagebox.showwarning("Image Not Found", "ATM background image not found!")

# Global variables for current state
current_screen = None
amount_entry = None

# Login Screen
def login_screen():
    global current_screen
    if current_screen:
        current_screen.destroy()

    current_screen = tk.Frame(root, bg="#000")
    current_screen.place(x=70, y=200, width=360, height=300)

    tk.Label(current_screen, text="Enter PIN", font=("Arial", 16), bg="#000", fg="#FFF").pack(pady=20)
    pin_entry = tk.Entry(current_screen, font=("Arial", 14), show="*")
    pin_entry.pack(pady=10)
    tk.Button(current_screen, text="Login", font=("Arial", 14), bg="#0A84FF", fg="#FFF",
              command=lambda: login(pin_entry.get())).pack(pady=20)

def main_menu():
    global current_screen
    if current_screen:
        current_screen.destroy()

    current_screen = tk.Frame(root, bg="#000")
    current_screen.place(x=70, y=200, width=360, height=300)

    tk.Label(current_screen, text="Main Menu", font=("Arial", 16), bg="#000", fg="#FFF").pack(pady=20)
    tk.Button(current_screen, text="Check Balance", font=("Arial", 14), bg="#0A84FF", fg="#FFF",
              command=check_balance).pack(pady=10)
    tk.Button(current_screen, text="Deposit Money", font=("Arial", 14), bg="#0A84FF", fg="#FFF",
              command=lambda: transaction_screen("Deposit")).pack(pady=10)
    tk.Button(current_screen, text="Withdraw Money", font=("Arial", 14), bg="#0A84FF", fg="#FFF",
              command=lambda: transaction_screen("Withdraw")).pack(pady=10)
    tk.Button(current_screen, text="Exit", font=("Arial", 14), bg="#FF3B30", fg="#FFF",
              command=root.destroy).pack(pady=10)

def transaction_screen(action):
    global current_screen, amount_entry
    if current_screen:
        current_screen.destroy()

    current_screen = tk.Frame(root, bg="#000")
    current_screen.place(x=70, y=200, width=360, height=300)

    tk.Label(current_screen, text=f"{action} Money", font=("Arial", 16), bg="#000", fg="#FFF").pack(pady=20)
    amount_entry = tk.Entry(current_screen, font=("Arial", 14))
    amount_entry.pack(pady=10)

    if action == "Deposit":
        tk.Button(current_screen, text="Deposit", font=("Arial", 14), bg="#0A84FF", fg="#FFF",
                  command=deposit_money).pack(pady=10)
    elif action == "Withdraw":
        tk.Button(current_screen, text="Withdraw", font=("Arial", 14), bg="#0A84FF", fg="#FFF",
                  command=withdraw_money).pack(pady=10)

    tk.Button(current_screen, text="Back", font=("Arial", 14), bg="#FF3B30", fg="#FFF", command=main_menu).pack(pady=10)

def login(entered_pin):
    if entered_pin == account_data["pin"]:
        messagebox.showinfo("Login Successful", "Welcome to the ATM!")
        main_menu()
    else:
        messagebox.showerror("Login Failed", "Incorrect PIN. Try again.")

def check_balance():
    messagebox.showinfo("Balance", f"Your current balance is ${account_data['balance']}")

def deposit_money():
    global amount_entry
    try:
        amount = int(amount_entry.get())
        account_data["balance"] += amount
        messagebox.showinfo("Success", f"${amount} deposited successfully.")
        main_menu()
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid amount.")

def withdraw_money():
    global amount_entry
    try:
        amount = int(amount_entry.get())
        if amount > account_data["balance"]:
            messagebox.showerror("Error", "Insufficient balance.")
        else:
            account_data["balance"] -= amount
            messagebox.showinfo("Success", f"${amount} withdrawn successfully.")
        main_menu()
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid amount.")

# Initialize login screen
login_screen()

# Run the application
root.mainloop()
