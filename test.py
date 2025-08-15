import tkinter as tk
from tkcalendar import DateEntry
import tkcalendar



def get_selected_date():
    selected_date = cal.get_date()
    selected_date_label.config(text=f"Selected Date: {selected_date}")

parent = tk.Tk()
parent.title("Date Entry Example")

# Create a Date Entry widget
cal = DateEntry(parent, width=12, background="darkblue", foreground="white", borderwidth=2)
cal.pack(padx=10, pady=10)

# Create a button to get the selected date
get_date_button = tk.Button(parent, text="Get Selected Date", command=get_selected_date)
get_date_button.pack(pady=10)
# Create a label to display the selected date
selected_date_label = tk.Label(parent, text="", font=("Helvetica", 12))
selected_date_label.pack()
parent.mainloop()
print(tkcalendar.__file__)
