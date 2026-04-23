import requests
import customtkinter as ctk
import json
import os

root = ctk.CTk()
root.title("Currency Converter")
root.geometry("800x800")
root.resizable(False, False)
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
CONFIG_FILE = "config.json"
BASE_CURRENCY = "USD"
rates = {}

common_currencies = [
    "USD", "EUR", "GBP", "INR", "AED", "SAR", 
    "JPY", "CAD", "AUD", "CHF", "CNY", "PKR"
]

def load_key():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            data = json.load(f)
            return data.get("api_key")
    return None

def save_key(key):
    with open(CONFIG_FILE, "w") as f:
        json.dump({"api_key": key}, f)

def fetch_rates(api_key):
    global rates
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{BASE_CURRENCY}"
    response = requests.get(url)
    data = response.json()
    if "conversion_rates" in data:
        rates = data["conversion_rates"]
        return True
    return False

def ask_for_key():
    popup = ctk.CTkToplevel(root)
    popup.geometry("400x220")
    popup.overrideredirect(True)
    popup.grab_set()

    ctk.CTkLabel(popup, text="Enter your free API key:", font=("Arial", 14, "bold")).pack(pady=15)
    ctk.CTkLabel(popup, text="Get yours at exchangerate-api.com", font=("Arial", 11)).pack()

    entry_key = ctk.CTkEntry(popup, width=300)
    entry_key.pack(pady=10)

    def confirm():
        key = entry_key.get().strip()
        if not key:
            return
        if fetch_rates(key):
            save_key(key)
            popup.destroy()
        else:
            entry_key.delete(0, ctk.END)
            ctk.CTkLabel(popup, text="Invalid key. Try again.", text_color="red").pack()

    ctk.CTkButton(popup, text="Save Key", command=confirm,
                  fg_color="#2ecc71", hover_color="#27ae60").pack(pady=10)
    
API_KEY = load_key()
if API_KEY:
    fetch_rates(API_KEY)
else:
    root.after(100, ask_for_key)

ctk.CTkLabel(root, text="Currency Converter", font=("Arial", 20, "bold")).pack(pady=10)
output = ctk.CTkTextbox(root, height=200, width=400,font= ("Arial",14))
output.pack()

def make_button(text, command, fg_color, hover_color):
    ctk.CTkButton(
        root,
        text=text,
        command=command,
        width=200,
        height=40,
        corner_radius=10,
        fg_color=fg_color,
        hover_color=hover_color,
        font=("Arial", 14, "bold")
    ).place(x = 300,y = 450)




ctk.CTkLabel(root, text="From", font=("Arial", 14, "bold")).place(x = 250, y = 270)
dropdown_from = ctk.CTkOptionMenu(root,values=common_currencies)
dropdown_from.place(x = 200,y = 300)
ctk.CTkLabel(root, text="To", font=("Arial", 14, "bold")).place(x = 520, y = 270)
dropdown_to = ctk.CTkOptionMenu(root,values=common_currencies)
dropdown_to.place(x = 460, y = 300)
ctk.CTkLabel(root, text="Enter amount to convert", font=("Arial", 14, "bold")).place(x = 320, y = 350)
entry_amount = ctk.CTkEntry(root, width = 100)
entry_amount.place(x = 350, y = 380)
def convert():
    from_currency = dropdown_from.get()
    to_currency = dropdown_to.get()
    if not entry_amount.get().strip():
        output.insert(ctk.END,"Please enter a amount to convert.\n")
        return
    amount = float(entry_amount.get())
    result = (amount*(rates[to_currency]/rates[from_currency]))
    output.insert(ctk.END,f"{amount} {from_currency} is equal to {result:.2f} {to_currency}\n")
    
make_button("Convert",convert,"#2ecc71","#27ae60")

root.mainloop()