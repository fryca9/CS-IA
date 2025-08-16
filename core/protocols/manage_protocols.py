import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk
import pandas as pd
from core.data_manager import DataManager
from core.protocols.add_protocol import AddProtocol
from core.protocols.edit_protocol import EditProtocol

class ManageProtocols:
    def __init__(self, root):
        self.manage_protocols_window = tk.Toplevel(root)
        self.manage_protocols_window.title("Manage Protocols")
        self.manage_protocols_window.geometry("1000x400")

        # Load data
        self.data_manager = DataManager()
        self.df = self.load_df()

        # Options field (buttons)
        options_field = tk.Frame(self.manage_protocols_window)
        options_field.pack(padx=10, pady=10, fill="x")
        for i in range(3):
            options_field.columnconfigure(i, weight=1)

        tk.Button(options_field, text="Create New Protocol",
                  command=lambda: AddProtocol(self.manage_protocols_window, self.refresh_tree)
                  ).grid(row=0, column=0, sticky="ew", padx=5)

        tk.Button(options_field, text="Edit Protocol", command=self.edit_selected_protocol).grid(row=0, column=1, sticky="ew", padx=5)

        tk.Button(options_field, text="Delete Protocol", command=self.delete_selected_protocols).grid(row=0, column=2, sticky="ew", padx=5)

        # Create Treeview (exclude ID column visually)
        columns = [col for col in self.df.columns if col != "ID"]
        self.tree = ttk.Treeview(self.manage_protocols_window, columns=columns, show="headings", selectmode="extended")
        self.tree.bind("<Double-1>", self.edit_selected_protocol)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        for col in columns:
            self.tree.heading(col, text=col, command=lambda _col=col: self.sort_column(_col, True))
            self.tree.column(col, width=80)

        self.update_tree(self.df)
    
    def load_df(self):
        data = self.data_manager.load_protocols()
        if not data:
            # ensure columns exist
            cols = ["Protocol Name", "Total Sets", "Reps Per Set", "Hang Time", "Rest Time", "Rest Between Sets", "Delay Start", "Notes"]
            return pd.DataFrame(columns=cols)
        df = pd.DataFrame(data)
        return df
    
    def refresh_tree(self):
        """Reload sessions from JSON and refresh Treeview."""
        self.df = self.load_df()
        self.update_tree(self.df)

    def update_tree(self, df):
        """Clear and repopulate the Treeview with the given DataFrame."""
        for i in self.tree.get_children():
            self.tree.delete(i)
        if df.empty:
            return
        for _, row in df.iterrows():
            self.tree.insert("", "end", values=list(row))
            
    def sort_column(self, col, reverse):
        """Sort Treeview by column."""
        try:
            sorted_df = self.df.sort_values(by=col, ascending=not reverse)
        except Exception:
            sorted_df = self.df
        self.update_tree(sorted_df)
        # reverse sort for the next time
        self.tree.heading(col, command=lambda: self.sort_column(col, not reverse))

    def edit_selected_protocol(self, event=None):
        """Edit selected protocol via the button or double-click; only if exactly one is selected."""
        selected = self.tree.selection()
        if len(selected) != 1:
            messagebox.showwarning("Warning", "Please select exactly one protocol to edit.")
            return
        row_values = self.tree.item(selected[0], "values")
        protocol_data = dict(zip(self.df.columns, row_values))
        EditProtocol(self.manage_protocols_window, protocol_data, self.refresh_tree)

    def delete_selected_protocols(self):
        """Delete selected protocols."""
        selected_protocols = self.tree.selection()
        if not selected_protocols:
            messagebox.showwarning("Warning", "Please select at least one protocol to delete.")
            return
        # Confirm deletion
        if not messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete the selected protocols?"):
            return
        # Get IDs of selected protocols in the Treeview
        selected_ids = []
        columns = [col for col in self.df.columns]
        for protocol in selected_protocols:
            row_values = self.tree.item(protocol, "values")
            protocol_dict = dict(zip(columns, row_values))
            selected_ids.append(protocol_dict["ID"])

        try:
            self.data_manager.delete_protocols_by_ids(selected_ids)
            self.refresh_tree()
            messagebox.showinfo("Success", f"Deleted {len(selected_ids)} protocol(s).")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete protocols: {e}")

