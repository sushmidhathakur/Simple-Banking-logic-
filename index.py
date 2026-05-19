import sqlite3
import dis
from tkinter import *
from tkinter import messagebox

# Database setup
conn = sqlite3.connect('atm.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS users (
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             name TEXT NOT NULL,
             pin TEXT NOT NULL,
             balance REAL NOT NULL)''')
conn.commit()

# Functions
def register_user():
    name = entry_name.get()
    pin = entry_pin.get()
    balance = float(entry_balance.get())
    
    c.execute("INSERT INTO users (name, pin, balance) VALUES (?, ?, ?)", (name, pin, balance))
    conn.commit()
    messagebox.showinfo("Success", "User registered successfully!")
    entry_name.delete(0, END)
    entry_pin.delete(0, END)
    entry_balance.delete(0, END)

    dis.dis(register_user)

def login_user():
    name = entry_name.get()
    pin = entry_pin.get()
    
    c.execute("SELECT * FROM users WHERE name=? AND pin=?", (name, pin))
    user = c.fetchone()
    
    if user:
        messagebox.showinfo("Success", f"Welcome {name}!")
        atm_window(user)
    else:
        messagebox.showerror("Error", "Invalid credentials")

def atm_window(user):
    atm = Toplevel(root)
    atm.title("ATM")
    
    def check_balance():
        messagebox.showinfo("Balance", f"Your balance is: ${user[3]}")
    
    def deposit():
        amount = float(entry_amount.get())
        new_balance = user[3] + amount
        c.execute("UPDATE users SET balance=? WHERE id=?", (new_balance, user[0]))
        conn.commit()
        messagebox.showinfo("Success", f"${amount} deposited successfully!")
        user[3] = new_balance
        entry_amount.delete(0, END)
    
    def withdraw():
        amount = float(entry_amount.get())
        if amount > user[3]:
            messagebox.showerror("Error", "Insufficient balance")
        else:
            new_balance = user[3] - amount
            c.execute("UPDATE users SET balance=? WHERE id=?", (new_balance, user[0]))
            conn.commit()
            messagebox.showinfo("Success", f"${amount} withdrawn successfully!")
            user[3] = new_balance
            entry_amount.delete(0, END)
    
    Label(atm, text="ATM Operations").pack()
    Button(atm, text="Check Balance", command=check_balance).pack()
    Label(atm, text="Amount").pack()
    entry_amount = Entry(atm)
    entry_amount.pack()
    Button(atm, text="Deposit", command=deposit).pack()
    Button(atm, text="Withdraw", command=withdraw).pack()

# GUI setup
root = Tk()
root.title("Smart ATM System")

Label(root, text="Name").pack()
entry_name = Entry(root)
entry_name.pack()

Label(root, text="PIN").pack()
entry_pin = Entry(root, show="*")
entry_pin.pack()

Label(root, text="Initial Balance").pack()
entry_balance = Entry(root)
entry_balance.pack()

Button(root, text="Register", command=register_user).pack()
Button(root, text="Login", command=login_user).pack()

root.mainloop()
conn.close()