import requests
import customtkinter as ctk
from config import API_KEY

common_currencies = [
    "USD", "EUR", "GBP", "INR", "AED", "SAR", 
    "JPY", "CAD", "AUD", "CHF", "CNY", "PKR"
]

BASE_CURRENCY = "USD"
url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{BASE_CURRENCY}"
response = requests.get(url)
data = response.json()
rates = (data["conversion_rates"])

root = ctk.CTk()
root.title("Currency Converter")
root.geometry("800x800")

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

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