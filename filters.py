from email import errors
import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk
from session_log import SessionLog
import pandas as pd
from tkcalendar import DateEntry
import json
from helper_functions import HelperFunctions as helper

class Filters:
  def __init__(self, root, df, tree):
        filter_sessions_window = tk.Toplevel(root)
        filter_sessions_window.title("Filter Sessions")
        filter_sessions_window.geometry("400x300")

        # Create a frame for the filter options
        filters_field = tk.Frame(filter_sessions_window)
        filters_field.pack(padx=10, pady=10)
        filters_field.columnconfigure(0, weight=1)
        filters_field.columnconfigure(1, weight=1)
        filters_field.columnconfigure(2, weight=1)

        # Filter by date
        tk.Label(filters_field, text="Date Range:", anchor="w", width=16).grid(row=0, column=0, rowspan=2, pady=5, sticky="ew")
        tk.Label(filters_field, text="From:").grid(row=0, column=1, sticky="ew")
        start_date_entry = DateEntry(filters_field, background='darkblue', foreground='white', borderwidth=2)
        earliest_date = df["Date"].min()
        start_date_entry.set_date(earliest_date)
        start_date_entry.grid(row=1, column=1, padx=(0, 5), pady=5, sticky="ew")
        tk.Label(filters_field, text="To:").grid(row=0, column=2, sticky="ew")
        end_date_entry = DateEntry(filters_field, background='darkblue', foreground='white', borderwidth=2)
        latest_date = df["Date"].max()
        end_date_entry.set_date(latest_date)
        end_date_entry.grid(row=1, column=2, padx=(5, 0), pady=5, sticky="ew")

        # Filter by protocol
        tk.Label(filters_field, text="Protocol:", anchor="w", width=16).grid(row=3, column=0, pady=5, sticky="ew")
        with open("protocol_manager.json", "r") as f:
            protocols = json.load(f)
        protocol_names = ["All"] + [p["Protocol Name"] for p in protocols]
        protocol_var = tk.StringVar(value=protocol_names[0] if protocol_names else "All")
        protocol_menu = tk.OptionMenu(filters_field, protocol_var, *protocol_names)
        protocol_menu.grid(row=3, columnspan=2, column=1, sticky="ew")

        # Filter by completion status
        tk.Label(filters_field, text="Completed:", anchor="w", width=16).grid(row=4, column=0, pady=5, sticky="ew")
        completed_filter_var = tk.StringVar(value="All")
        completed_filter_menu = ttk.OptionMenu(filters_field, completed_filter_var, "All", "Completed", "Not Completed")
        completed_filter_menu.grid(row=4, column=1, columnspan=2, sticky="ew")
        
        # filter by difficulty
        tk.Label(filters_field, text="RPI (difficulty):", anchor="w", width=16).grid(row=5, column=0, pady=5, sticky="ew")
        difficulty_entry = tk.Entry(filters_field)
        difficulty_entry.grid(row=5, column=1, padx=(0, 5), sticky="ew")
        difficulty_var = tk.StringVar(value="Above")
        difficulty_filter_menu = ttk.OptionMenu(filters_field, difficulty_var, "Above", *["Above", "Below"])
        difficulty_filter_menu.grid(row=5, column=2, padx=(5, 0), sticky="ew")

        # filter by added weight
        tk.Label(filters_field, text="Added Weight:", anchor="w", width=16).grid(row=6, column=0, pady=5, sticky="ew")
        added_weight_entry = tk.Entry(filters_field)
        added_weight_entry.grid(row=6, column=1, padx=(0, 5), sticky="ew")
        added_weight_var = tk.StringVar(value="Above")
        added_weight_filter_menu = ttk.OptionMenu(filters_field, added_weight_var, "Above", *["Above", "Below"])
        added_weight_filter_menu.grid(row=6, column=2, padx=(5, 0), sticky="ew")

        
        # filter by total weight
        tk.Label(filters_field, text="Total Weight:", anchor="w", width=16).grid(row=7, column=0, pady=5, sticky="ew")
        total_weight_entry = tk.Entry(filters_field)
        total_weight_entry.grid(row=7, column=1, padx=(0, 5), sticky="ew")
        total_weight_var = tk.StringVar(value="Above")
        total_weight_filter_menu = ttk.OptionMenu(filters_field, total_weight_var, "Above", *["Above", "Below"])
        total_weight_filter_menu.grid(row=7, column=2, padx=(5, 0), sticky="ew")


        # Add a button to apply the filter
        buttons_field = tk.Frame(filter_sessions_window)
        buttons_field.pack(pady=10)
        buttons_field.columnconfigure(0, weight=1)
        buttons_field.columnconfigure(1, weight=1)
        buttons_field.columnconfigure(2, weight=1)

        tk.Button(buttons_field, text="Apply Filters", command=lambda: self.apply_filter(tree, df, start_date_entry, end_date_entry, protocol_var, completed_filter_var, difficulty_entry, difficulty_var, added_weight_entry, added_weight_var, total_weight_entry, total_weight_var)).grid(row=0, column=0, sticky="ew", padx=5)
        tk.Button(buttons_field, text="Clear Filters", command=lambda: self.clear_filter(tree, df)).grid(row=0, column=1, sticky="ew", padx=5)
        tk.Button(buttons_field, text="Cancel", command=filter_sessions_window.destroy).grid(row=0, column=2, sticky="ew", padx=5)

# TODO make apply filters work. probably move this filter_sessions to a new class. Next do sorting.
  def apply_filter(self, tree, df, start_date_entry, end_date_entry, protocol_var, completed_filter_var, difficulty_entry, difficulty_var, added_weight_entry, added_weight_var, total_weight_entry, total_weight_var):
        errors = []
        
        # --- Collect filter values ---
        start_date = helper.get_date(start_date_entry, errors)
        end_date = helper.get_date(end_date_entry, errors)

        protocol = protocol_var.get()
        completed_val = completed_filter_var.get()
        completed = None
        if completed_val == "Completed":
            completed = True
        elif completed_val == "Not Completed":
            completed = False

        difficulty = helper.get_int(difficulty_entry, "Difficulty", errors)
        difficulty_filter = difficulty_var.get()

        added_weight = helper.get_float(added_weight_entry, "Added weight", errors)
        added_weight_filter = added_weight_var.get()

        total_weight = helper.get_float(total_weight_entry, "Total weight", errors)
        total_weight_filter = total_weight_var.get()

        # Show errors if any
        if errors:
            messagebox.showerror("Invalid Input", "\n".join([f"• {e}" for e in errors]), icon="error")
            return

        # --- Build mask dynamically ---
        mask = pd.Series(True, index=df.index)
        mask &= (df["Date"] >= start_date) & (df["Date"] <= end_date)

        if protocol != "All":
            mask &= df["Protocol"] == protocol
        if completed is not None:
            mask &= df["Completed"] == completed
            
        # Define numeric filters in a loop
        numeric_filters = [
            ("Difficulty", difficulty, difficulty_filter),
            ("Added Weight", added_weight, added_weight_filter),
            ("Total Weight", total_weight, total_weight_filter)
        ]

        for column, value, direction in numeric_filters:
            if value is not None:
                if direction == "Above":
                    mask &= df[column] > value
                elif direction == "Below":
                    mask &= df[column] < value

        # Apply mask to DataFrame
        filtered_df = df[mask]


        # Update the Treeview with the filtered data
        for i in tree.get_children():
            tree.delete(i)
        for _, row in filtered_df.iterrows():
            tree.insert("", "end", values=list(row))
