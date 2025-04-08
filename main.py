import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import subprocess
import json
import os

CATEGORY_COLORS = {
    'convention': 'blue',
    'refactor': 'orange',
    'warning': 'gold',
    'error': 'red',
    'fatal': 'darkred'
}

def run_pylint(file_path):
    try:
        result = subprocess.run([
            'pylint',
            '--output-format=json',
            file_path
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if result.returncode == 32:  # File not found or error
            return []

        return json.loads(result.stdout)
    except Exception as e:
        print(f"Error running pylint: {e}")
        return []

class CodeAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Code Analyzer")

        self.create_widgets()

    def create_widgets(self):
        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=10, pady=10, fill='both', expand=True)

        self.load_button = tk.Button(self.frame, text="Load Python File", command=self.load_file)
        self.load_button.pack(pady=5)

        self.tree = ttk.Treeview(self.frame, columns=("Type", "Message", "Line"), show='headings')
        self.tree.heading("Type", text="Type")
        self.tree.heading("Message", text="Message")
        self.tree.heading("Line", text="Line")
        self.tree.pack(pady=5, fill='both', expand=True)

        self.scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Python files", "*.py")])
        if file_path:
            issues = run_pylint(file_path)
            self.display_issues(issues)

    def display_issues(self, issues):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for issue in issues:
            category = issue.get("type")
            msg = issue.get("message")
            line = issue.get("line")

            tag = category
            self.tree.insert("", "end", values=(category, msg, line), tags=(tag,))

        for category, color in CATEGORY_COLORS.items():
            self.tree.tag_configure(category, background=color)

if __name__ == '__main__':
    root = tk.Tk()
    app = CodeAnalyzerApp(root)
    root.mainloop()
