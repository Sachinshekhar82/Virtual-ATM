import tkinter as tk
from tkinter import messagebox
import speech_recognition as sr


class VirtualATM:
    def __init__(self, root):
        self.root = root
        self.root.title("Virtual ATM")
        self.balance = 1000  # Initial balance

        # Create GUI elements
        self.label = tk.Label(root, text="Virtual ATM", font=("Arial", 20))
        self.label.pack(pady=10)

        self.balance_btn = tk.Button(root, text="Check Balance", command=self.check_balance, width=20, height=2)
        self.balance_btn.pack(pady=5)

        self.speech_btn = tk.Button(root, text="Use Voice Command", command=self.voice_command, width=20, height=2)
        self.speech_btn.pack(pady=20)

    def check_balance(self):
        messagebox.showinfo("Balance", f"Your current balance is ${self.balance}")

    def deposit_money(self, amount):
        if amount > 0:
            self.balance += amount
            messagebox.showinfo("Success", f"${amount} deposited successfully!\nNew balance: ${self.balance}")
        else:
            messagebox.showerror("Error", "Invalid deposit amount!")

    def withdraw_money(self, amount):
        if amount > self.balance:
            messagebox.showerror("Error", "Insufficient balance!")
        elif amount > 0:
            self.balance -= amount
            messagebox.showinfo("Success", f"${amount} withdrawn successfully!\nNew balance: ${self.balance}")
        else:
            messagebox.showerror("Error", "Invalid withdrawal amount!")

    def voice_command(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            messagebox.showinfo("Listening", "Please say a command: check balance, deposit, or withdraw.")
            try:
                audio = recognizer.listen(source, timeout=5)
                command = recognizer.recognize_google(audio).lower()
                print(f"Recognized command: {command}")

                if "balance" in command:
                    self.check_balance()
                elif "deposit" in command:
                    amount = self.extract_amount(command)
                    if amount:
                        self.deposit_money(amount)
                    else:
                        messagebox.showerror("Error", "Could not understand the deposit amount.")
                elif "withdraw" in command:
                    amount = self.extract_amount(command)
                    if amount:
                        self.withdraw_money(amount)
                    else:
                        messagebox.showerror("Error", "Could not understand the withdrawal amount.")
                else:
                    messagebox.showerror("Error", "Command not recognized. Try again!")
            except sr.UnknownValueError:
                messagebox.showerror("Error", "Could not understand your speech. Try again!")
            except sr.RequestError as e:
                messagebox.showerror("Error", f"Speech recognition service error: {e}")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def extract_amount(self, command):
        """Extract numerical amount from the command."""
        words = command.split()
        for word in words:
            if word.isdigit():
                return int(word)
        return None


# Create the main window
if __name__ == "__main__":
    root = tk.Tk()
    atm = VirtualATM(root)
    root.mainloop()
