import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk
import pandas as pd
from core.sessions.filter_sessions import FilterSessions
from core.sessions.edit_session import EditSession
from core.sessions.add_session import AddSession
from core.data_manager import DataManager

class ViewSessions:
    def __init__(self, root):
        self.view_sessions_window = tk.Toplevel(root)
        self.view_sessions_window.title("View Sessions")
        self.view_sessions_window.geometry("900x400")

        # Load data
        self.data_manager = DataManager()
        self.df = self.load_df()

        # Options field (buttons)
        options_field = tk.Frame(self.view_sessions_window)
        options_field.pack(padx=10, pady=10, fill="x")
        for i in range(5):
            options_field.columnconfigure(i, weight=1)


        tk.Button(options_field, text="Filter Sessions",
                  command=lambda: FilterSessions(self.view_sessions_window, self.df, self.tree, self.update_tree)
                  ).grid(row=0, column=0, sticky="ew", padx=5)

        tk.Button(options_field, text="Clear Filters",
                  command=self.refresh_tree
                  ).grid(row=0, column=1, sticky="ew", padx=5)

        # IMPORTANT: use lambda so AddSession is created on click (not during init)
        tk.Button(options_field, text="Add Session",
                  command=lambda: AddSession(self.view_sessions_window, self.refresh_tree)
                  ).grid(row=0, column=2, sticky="ew", padx=5)

        tk.Button(options_field, text="Edit Session", command=self.edit_selected_session).grid(row=0, column=3, sticky="ew", padx=5)
        
        tk.Button(options_field, text="Delete Sessions", command=self.delete_selected_sessions).grid(row=0, column=4, sticky="ew", padx=5)

        # Create Treeview (exclude ID column visually)
        columns = [col for col in self.df.columns if col != "ID"]
        self.tree = ttk.Treeview(self.view_sessions_window, columns=columns, show="headings", selectmode="extended")
        self.tree.bind("<Double-1>", self.edit_selected_session)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        for col in columns:
            self.tree.heading(col, text=col, command=lambda _col=col: self.sort_column(_col, True))
            self.tree.column(col, width=80)

        self.update_tree(self.df)
    
    
    def load_df(self):
        data = self.data_manager.load_sessions()
        if not data:
            # ensure columns exist
            cols = ["Date", "Protocol", "Added Weight", "Total Weight", "Difficulty", "Completed", "Notes"]
            return pd.DataFrame(columns=cols)
        df = pd.DataFrame(data)
        if "Date" in df.columns: # change the format of dates
            df["Date"] = pd.to_datetime(df["Date"]).dt.date
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
        
    def edit_selected_session(self, event=None):
        """Edit session via the button or double-click; only if exactly one is selected."""
        selected = self.tree.selection()
        if len(selected) != 1:
            messagebox.showwarning("Warning", "Please select exactly one session to edit.")
            return
        row_values = self.tree.item(selected[0], "values")
        session_data = dict(zip(self.df.columns, row_values))
        EditSession(self.view_sessions_window, session_data, self.refresh_tree)
    
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

        try:
            self.data_manager.delete_sessions_by_ids(selected_ids)
            self.refresh_tree()
            messagebox.showinfo("Success", f"Deleted {len(selected_ids)} session(s).")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete sessions: {e}")

#take care of delete selected sessions
