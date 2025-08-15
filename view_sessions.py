import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk
import pandas as pd
from filters import Filters
from tkcalendar import DateEntry
import json
from edit_session import EditSession
from add_session import AddSession

class ViewSessions:
    def __init__(self, root):
        self.view_sessions_window = tk.Toplevel(root)
        self.view_sessions_window.title("View Sessions")
        self.view_sessions_window.geometry("900x400")

        # Load data
        self.df = pd.read_json("session_log.json")
        self.df["Date"] = pd.to_datetime(self.df["Date"]).dt.date

        # Options field (buttons)
        options_field = tk.Frame(self.view_sessions_window)
        options_field.pack(padx=10, pady=10, fill="x")
        options_field.columnconfigure(0, weight=1)
        options_field.columnconfigure(1, weight=1)
        options_field.columnconfigure(2, weight=1)
        options_field.columnconfigure(3, weight=1)
        options_field.columnconfigure(4, weight=1)

        tk.Button(
            options_field, 
            text="Filter Sessions", 
            command=lambda: Filters(self.view_sessions_window, self.df, self.tree, self.update_tree)
        ).grid(row=0, column=0, sticky="ew", padx=5)

        tk.Button(
            options_field, 
            text="Clear Filters", 
            command=lambda: self.update_tree(self.df)
        ).grid(row=0, column=1, sticky="ew", padx=5)

        tk.Button(options_field, text="Add Session", command=AddSession(self.view_sessions_window, self.df, self.update_tree)).grid(row=0, column=4, sticky="ew", padx=5)

        tk.Button(options_field, text="Edit Session", command=self.edit_selected_session).grid(row=0, column=2, sticky="ew", padx=5)

        tk.Button(options_field, text="Delete Sessions", command=self.delete_selected_sessions).grid(row=0, column=3, sticky="ew", padx=5)

        # Create Treeview
        columns = [col for col in self.df.columns if col != "ID"]
        self.tree = ttk.Treeview(self.view_sessions_window, columns=columns, show="headings")
        self.tree.bind("<Double-1>", self.edit_selected_session)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        for col in columns:
            self.tree.heading(col, text=col, command=lambda _col=col: self.sort_column(_col, True)) # each column can be sorted
            self.tree.column(col, width=60)
            
        # Initial load
        self.update_tree(self.df)

    def update_tree(self, df):
        """Clear and repopulate the Treeview with the given DataFrame."""
        for i in self.tree.get_children():
            self.tree.delete(i)
        for _, row in df.iterrows():
            self.tree.insert("", "end", values=list(row))
            
    def sort_column(self, col, reverse):
        """Sort Treeview by column."""
        # Sort DataFrame
        try:
            sorted_df = self.df.sort_values(by=col, ascending=not reverse)
        except Exception:
            sorted_df = self.df  # fallback if sort fails

        # Update tree with sorted data
        self.update_tree(sorted_df)
        # Reverse sort next time
        self.tree.heading(col, command=lambda: self.sort_column(col, not reverse))
        
    def edit_selected_session(self, event=None):
        """Edit session via the button; only if exactly one is selected."""
        selected_session = self.tree.selection()
        if len(selected_session) != 1:
            messagebox.showwarning("Warning", "Please select exactly one session to edit.")
            return

        row_values = self.tree.item(selected_session[0], "values")
        session_data = dict(zip(self.df.columns, row_values))
        EditSession(self.view_sessions_window, session_data, self.update_tree)
    
    def delete_selected_sessions(self):
        """Delete selected sessions."""
        selected_sessions = self.tree.selection()
        if not selected_sessions:
            messagebox.showwarning("Warning", "Please select at least one session to delete.")
            return

        # Confirm deletion
        if not messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete the selected sessions?"):
            return

        # Get IDs of selected sessions in the Treeview
        selected_ids = []
        columns = [col for col in self.df.columns]
        for session in selected_sessions:
            row_values = self.tree.item(session, "values")
            session_dict = dict(zip(columns, row_values))
            selected_ids.append(session_dict["ID"])

        # Keep only rows whose ID is NOT in selected_ids
        self.df = self.df[~self.df["ID"].isin(selected_ids)]
        with open("session_log.json", "w") as f:
            json.dump(self.df.to_dict(orient="records"), f, indent=2, default=str)
        # Refresh the Treeview
        self.update_tree(self.df)
