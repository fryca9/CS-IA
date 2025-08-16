import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk
from tkcalendar import DateEntry
from core.helper_methods import HelperMethods as Helper

class FilterSessions:
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
        protocols = self.data_manager.load_protocols()
        protocol_names = ["All"] + [p["Protocol Name"] for p in protocols]
        self.protocol_var = tk.StringVar(value="All")
        tk.OptionMenu(filters_field, self.protocol_var, *protocol_names).grid(row=3, columnspan=2, column=1, sticky="ew")

        # --- Completed status ---
        tk.Label(filters_field, text="Completed:", anchor="w", width=16).grid(row=4, column=0, pady=5, sticky="ew")
        self.completed_filter_var = tk.StringVar(value="All")
        ttk.OptionMenu(filters_field, self.completed_filter_var, "All", "All", "Completed", "Not Completed").grid(row=4, column=1, columnspan=2, sticky="ew")

        # --- Difficulty ---
        tk.Label(filters_field, text="RPI (difficulty):", anchor="w", width=16).grid(row=5, column=0, pady=5, sticky="ew")
        self.difficulty_var = tk.IntVar(value=1)
        difficulty_spinbox = tk.Spinbox(
            filters_field, from_=1, to=10, textvariable=self.difficulty_var
        )
        difficulty_spinbox.grid(row=5, column=1, padx=(0, 5), sticky="ew")
        self.difficulty_opt = tk.StringVar(value="Above")
        ttk.OptionMenu(filters_field, self.difficulty_opt, "Above", "Above", "Below").grid(row=5, column=2, padx=(5, 0), sticky="ew")

        # --- Added weight ---
        tk.Label(filters_field, text="Added Weight:", anchor="w", width=16).grid(row=6, column=0, pady=5, sticky="ew")
        self.added_weight_var = tk.DoubleVar(value=0.00)
        self.added_weight_spinbox = tk.Spinbox(
            filters_field, from_=0.00, to=1000.00, increment=0.50, textvariable=self.added_weight_var, format="%.2f"
        )
        self.added_weight_spinbox.grid(row=6, column=1, padx=(0, 5), sticky="ew")
        self.added_weight_opt = tk.StringVar(value="Above")
        ttk.OptionMenu(filters_field, self.added_weight_opt, "Above", "Above", "Below").grid(row=6, column=2, padx=(5, 0), sticky="ew")

        # --- Total weight ---
        tk.Label(filters_field, text="Total Weight:", anchor="w", width=16).grid(row=7, column=0, pady=5, sticky="ew")
        self.total_weight_var = tk.DoubleVar(value=0.00)
        self.total_weight_spinbox = tk.Spinbox(
            filters_field, from_=0.00, to=1000.00, increment=0.50, textvariable=self.total_weight_var, format="%.2f"
        )
        self.total_weight_spinbox.grid(row=7, column=1, padx=(0, 5), sticky="ew")
        self.total_weight_opt = tk.StringVar(value="Above")
        ttk.OptionMenu(filters_field, self.total_weight_opt, "Above", "Above", "Below").grid(row=7, column=2, padx=(5, 0), sticky="ew")

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

        start_date = self.start_date_entry.get_date()
        end_date = self.end_date_entry.get_date()
        protocol = self.protocol_var.get()
        completed_val = self.completed_filter_var.get()
        completed = None
        if completed_val == "Completed":
            completed = True
        elif completed_val == "Not Completed":
            completed = False

        difficulty = Helper.get_int(self.difficulty_var, "Difficulty", errors)
        difficulty_filter = self.difficulty_opt.get()
        added_weight = Helper.get_float(self.added_weight_var, "Added weight", errors)
        added_weight_filter = self.added_weight_opt.get()
        total_weight = Helper.get_float(self.total_weight_var, "Total weight", errors)
        total_weight_filter = self.total_weight_opt.get()

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
        self.difficulty_var.set(1)
        self.difficulty_opt.set("Above")
        self.added_weight_var.set(0.0) # find a way to display "0.00"
        self.added_weight_opt.set("Above")
        self.total_weight_var.set(0.0) # find a way to display "0.00"
        self.total_weight_opt.set("Above")
