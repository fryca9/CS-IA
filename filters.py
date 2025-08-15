import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk
import pandas as pd
import json
from tkcalendar import DateEntry
from helper_functions import HelperFunctions as Helper

class Filters:
    def __init__(self, root, df, tree, update_tree_callback):
        self.tree = tree
        self.df_original = df.copy()
        self.update_tree = update_tree_callback

        self.filter_sessions_window = tk.Toplevel(root)
        self.filter_sessions_window.title("Filter Sessions")
        self.filter_sessions_window.geometry("400x300")

        # --- Filters frame ---
        filters_field = tk.Frame(self.filter_sessions_window)
        filters_field.pack(padx=10, pady=10)
        filters_field.columnconfigure(0, weight=1)
        filters_field.columnconfigure(1, weight=1)
        filters_field.columnconfigure(2, weight=1)

        # --- Date Range ---
        tk.Label(filters_field, text="Date Range:", anchor="w", width=16).grid(row=0, column=0, rowspan=2, pady=5, sticky="ew")

        tk.Label(filters_field, text="From:").grid(row=0, column=1, sticky="ew")
        self.start_date_entry = DateEntry(filters_field, background='darkblue', foreground='white', borderwidth=2)
        self.start_date_entry.set_date(df["Date"].min())
        self.start_date_entry.grid(row=1, column=1, padx=(0, 5), pady=5, sticky="ew")

        tk.Label(filters_field, text="To:").grid(row=0, column=2, sticky="ew")
        self.end_date_entry = DateEntry(filters_field, background='darkblue', foreground='white', borderwidth=2)
        self.end_date_entry.set_date(df["Date"].max())
        self.end_date_entry.grid(row=1, column=2, padx=(5, 0), pady=5, sticky="ew")

        # --- Protocol ---
        tk.Label(filters_field, text="Protocol:", anchor="w", width=16).grid(row=3, column=0, pady=5, sticky="ew")
        with open("protocol_manager.json", "r") as f:
            protocols = json.load(f)
        protocol_names = ["All"] + [p["Protocol Name"] for p in protocols]
        self.protocol_var = tk.StringVar(value="All")
        tk.OptionMenu(filters_field, self.protocol_var, *protocol_names).grid(row=3, columnspan=2, column=1, sticky="ew")

        # --- Completed status ---
        tk.Label(filters_field, text="Completed:", anchor="w", width=16).grid(row=4, column=0, pady=5, sticky="ew")
        self.completed_filter_var = tk.StringVar(value="All")
        ttk.OptionMenu(filters_field, self.completed_filter_var, "All", "All", "Completed", "Not Completed").grid(row=4, column=1, columnspan=2, sticky="ew")

        # --- Difficulty ---
        tk.Label(filters_field, text="RPI (difficulty):", anchor="w", width=16).grid(row=5, column=0, pady=5, sticky="ew")
        self.difficulty_entry = tk.Entry(filters_field)
        self.difficulty_entry.grid(row=5, column=1, padx=(0, 5), sticky="ew")
        self.difficulty_var = tk.StringVar(value="Above")
        ttk.OptionMenu(filters_field, self.difficulty_var, "Above", "Above", "Below").grid(row=5, column=2, padx=(5, 0), sticky="ew")

        # --- Added weight ---
        tk.Label(filters_field, text="Added Weight:", anchor="w", width=16).grid(row=6, column=0, pady=5, sticky="ew")
        self.added_weight_entry = tk.Entry(filters_field)
        self.added_weight_entry.grid(row=6, column=1, padx=(0, 5), sticky="ew")
        self.added_weight_var = tk.StringVar(value="Above")
        ttk.OptionMenu(filters_field, self.added_weight_var, "Above", "Above", "Below").grid(row=6, column=2, padx=(5, 0), sticky="ew")

        # --- Total weight ---
        tk.Label(filters_field, text="Total Weight:", anchor="w", width=16).grid(row=7, column=0, pady=5, sticky="ew")
        self.total_weight_entry = tk.Entry(filters_field)
        self.total_weight_entry.grid(row=7, column=1, padx=(0, 5), sticky="ew")
        self.total_weight_var = tk.StringVar(value="Above")
        ttk.OptionMenu(filters_field, self.total_weight_var, "Above", "Above", "Below").grid(row=7, column=2, padx=(5, 0), sticky="ew")

        # --- Buttons ---
        buttons_field = tk.Frame(self.filter_sessions_window)
        buttons_field.pack(pady=10)
        buttons_field.columnconfigure(0, weight=1)
        buttons_field.columnconfigure(1, weight=1)
        buttons_field.columnconfigure(2, weight=1)

        tk.Button(buttons_field, text="Apply Filters", command=self.apply_filters).grid(row=0, column=0, sticky="ew", padx=5)
        tk.Button(buttons_field, text="Clear Filters", command=self.clear_filters).grid(row=0, column=1, sticky="ew", padx=5)
        tk.Button(buttons_field, text="Cancel", command=self.filter_sessions_window.destroy).grid(row=0, column=2, sticky="ew", padx=5)

    # -------------------
    def apply_filters(self):
        errors = []

        start_date = Helper.get_date(self.start_date_entry, errors)
        end_date = Helper.get_date(self.end_date_entry, errors)
        protocol = self.protocol_var.get()

        completed_val = self.completed_filter_var.get()
        completed = None
        if completed_val == "Completed":
            completed = True
        elif completed_val == "Not Completed":
            completed = False

        difficulty = Helper.get_int(self.difficulty_entry, "Difficulty", errors)
        difficulty_filter = self.difficulty_var.get()

        added_weight = Helper.get_float(self.added_weight_entry, "Added weight", errors)
        added_weight_filter = self.added_weight_var.get()

        total_weight = Helper.get_float(self.total_weight_entry, "Total weight", errors)
        total_weight_filter = self.total_weight_var.get()

        if errors:
            messagebox.showerror("Invalid Input", "\n".join([f"• {e}" for e in errors]), icon="error")
            return

        df = self.df_original
        mask = (df["Date"] >= start_date) & (df["Date"] <= end_date)

        if protocol != "All":
            mask &= df["Protocol"] == protocol
        if completed is not None:
            mask &= df["Completed"] == completed

        for column, value, direction in [
            ("Difficulty", difficulty, difficulty_filter),
            ("Added Weight", added_weight, added_weight_filter),
            ("Total Weight", total_weight, total_weight_filter)
        ]:
            if value is not None:
                if direction == "Above":
                    mask &= df[column] > value
                elif direction == "Below":
                    mask &= df[column] < value

        filtered_df = df[mask]
        self.update_tree(filtered_df)
        self.filter_sessions_window.destroy()

    # -------------------
    def clear_filters(self):
        self.update_tree(self.df_original)

        self.start_date_entry.set_date(self.df_original["Date"].min())
        self.end_date_entry.set_date(self.df_original["Date"].max())
        self.protocol_var.set("All")
        self.completed_filter_var.set("All")
        self.difficulty_entry.delete(0, tk.END)
        self.difficulty_var.set("Above")
        self.added_weight_entry.delete(0, tk.END)
        self.added_weight_var.set("Above")
        self.total_weight_entry.delete(0, tk.END)
        self.total_weight_var.set("Above")
