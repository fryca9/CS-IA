import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk
from xml.parsers.expat import errors
from filters import Filters
from session_log import SessionLog
import pandas as pd
from tkcalendar import DateEntry
import json

class ViewSessions:
    def __init__(self, root):
        view_sessions_window = tk.Toplevel(root)
        view_sessions_window.title("View Sessions")
        view_sessions_window.geometry("900x400")
        
        options_field = tk.Frame(view_sessions_window)
        options_field.pack(padx=10, pady=10)
        options_field.columnconfigure(0, weight=1)
        options_field.columnconfigure(1, weight=1)

        tk.Button(options_field, text="Filter Sessions", command= lambda: Filters(view_sessions_window, df, tree)).grid(row=0, column=0, sticky="ew")

        # Read JSON into DataFrame
        df = pd.read_json("session_log.json")
        df["Date"] = pd.to_datetime(df["Date"]).dt.date # keep only the date

        # Create Treeview
        columns = list(df.columns)
        tree = ttk.Treeview(view_sessions_window, columns=columns, show="headings")

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=60)
        for _, row in df.iterrows():
            tree.insert("", "end", values=list(row))

        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    
