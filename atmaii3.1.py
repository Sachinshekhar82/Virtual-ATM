import tkinter as tk
from tkinter import messagebox
import speech_recognition as sr
import pyttsx3


class VirtualATM:
    def __init__(self, root):
        self.root = root
        self.root.title("Virtual ATM")
        self.balance = 1000  # Initial balance

        # Initialize text-to-speech engine
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 150)  # Speech rate
        self.engine.setProperty("volume", 1.0)  # Volume level

        # Create GUI elements
        self.label = tk.Label(root, text="Virtual ATM", font=("Arial", 20))
        self.label.pack(pady=10)

        self.balance_btn = tk.Button(root, text="Check Balance", command=self.check_balance, width=20, height=2)
        self.balance_btn.pack(pady=5)

        self.speech_btn = tk.Button(root, text="Use Voice Command", command=self.voice_command, width=20, height=2)
        self.speech_btn.pack(pady=20)

    def speak(self, message):
        """Speak the given message using text-to-speech."""
        self.engine.say(message)
        self.engine.runAndWait()

    def check_balance(self):
        message = f"Your current balance is ${self.balance}"
        messagebox.showinfo("Balance", message)
        self.speak(message)

    def deposit_money(self, amount):
        if amount > 0:
            self.balance += amount
            message = f"${amount} deposited successfully! Your new balance is ${self.balance}."
            messagebox.showinfo("Success", message)
            self.speak(message)
        else:
            message = "Invalid deposit amount!"
            messagebox.showerror("Error", message)
            self.speak(message)

    def withdraw_money(self, amount):
        if amount > self.balance:
            message = "Insufficient balance!"
            messagebox.showerror("Error", message)
            self.speak(message)
        elif amount > 0:
            self.balance -= amount
            message = f"${amount} withdrawn successfully! Your new balance is ${self.balance}."
            messagebox.showinfo("Success", message)
            self.speak(message)
        else:
            message = "Invalid withdrawal amount!"
            messagebox.showerror("Error", message)
            self.speak(message)

    def voice_command(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            self.speak("Please say a command. You can check balance, deposit money, or withdraw money.")
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
                        message = "I could not understand the deposit amount."
                        messagebox.showerror("Error", message)
                        self.speak(message)
                elif "withdraw" in command:
                    amount = self.extract_amount(command)
                    if amount:
                        self.withdraw_money(amount)
                    else:
                        message = "I could not understand the withdrawal amount."
                        messagebox.showerror("Error", message)
                        self.speak(message)
                else:
                    message = "Command not recognized. Please try again!"
                    messagebox.showerror("Error", message)
                    self.speak(message)
            except sr.UnknownValueError:
                message = "I could not understand your speech. Please try again!"
                messagebox.showerror("Error", message)
                self.speak(message)
            except sr.RequestError as e:
                message = f"Speech recognition service error: {e}"
                messagebox.showerror("Error", message)
                self.speak(message)
            except Exception as e:
                message = f"An error occurred: {e}"
                messagebox.showerror("Error", message)
                self.speak(message)

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