import tkinter as tk
from tkinter import messagebox, filedialog
import math

class MathEvaluator:
    def __init__(self, master):
        self.master = master
        master.title("Math Expression Evaluator")
        master.geometry("500x650")

        # ----------------------------
        # Theme Settings
        # ----------------------------
        self.dark_mode = False
        self.light_bg = "#f0f0f0"
        self.light_fg = "#000000"
        self.dark_bg = "#2e2e2e"
        self.dark_fg = "#ffffff"

        # ----------------------------
        # History, Memory, Undo/Redo
        # ----------------------------
        self.history = []
        self.history_index = None
        self.memory = 0
        self.undo_stack = []
        self.redo_stack = []

        # ----------------------------
        # Input Field
        # ----------------------------
        self.entry = tk.Entry(master, font=("Arial", 16))
        self.entry.pack(pady=10, fill=tk.X, padx=10)
        self.entry.focus_set()

        # Keyboard shortcuts
        self.entry.bind("<Return>", self.calculate)
        self.entry.bind("<Up>", self.history_up)
        self.entry.bind("<Down>", self.history_down)
        self.entry.bind("<Control-z>", self.undo)
        self.entry.bind("<Control-y>", self.redo)
        self.entry.bind("<KeyRelease>", self.on_entry_change)

        # ----------------------------
        # Buttons Frame: Memory & Functions
        # ----------------------------
        self.button_frame = tk.Frame(master)
        self.button_frame.pack(pady=5)

        mem_buttons = [("M+", self.memory_add), ("M-", self.memory_subtract),
                       ("MR", self.memory_recall), ("MC", self.memory_clear)]
        for text, cmd in mem_buttons:
            tk.Button(self.button_frame, text=text, width=5, command=cmd).pack(side=tk.LEFT, padx=2)

        func_buttons = ["sqrt", "log", "sin", "cos", "tan", "factorial", "pi", "e"]
        for func in func_buttons:
            tk.Button(self.button_frame, text=func, width=6,
                      command=lambda f=func: self.insert_function(f)).pack(side=tk.LEFT, padx=2)

        # ----------------------------
        # Calculate + Export Button
        # ----------------------------
        self.calc_button = tk.Button(master, text="Calculate", command=self.calculate)
        self.calc_button.pack(pady=5)

        self.export_button = tk.Button(master, text="Export History", command=self.export_history)
        self.export_button.pack(pady=5)

        # ----------------------------
        # Extra Buttons: Theme & History
        # ----------------------------
        self.extra_button_frame = tk.Frame(master)
        self.extra_button_frame.pack(pady=5)

        self.theme_button = tk.Button(self.extra_button_frame, text="Toggle Dark Mode", command=self.toggle_theme)
        self.theme_button.pack(side=tk.LEFT, padx=5)

        self.show_history = True
        self.history_toggle_button = tk.Button(self.extra_button_frame, text="Hide History", command=self.toggle_history)
        self.history_toggle_button.pack(side=tk.LEFT, padx=5)

        self.clear_history_button = tk.Button(self.extra_button_frame, text="Clear History", command=self.clear_history)
        self.clear_history_button.pack(side=tk.LEFT, padx=5)

        # ----------------------------
        # History Listbox
        # ----------------------------
        self.listbox = tk.Listbox(master, font=("Arial", 14))
        self.listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.listbox.bind("<Double-1>", self.copy_result)

        self.apply_theme()

    # ----------------------------
    # Theme Functions
    # ----------------------------
    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.apply_theme()

    def apply_theme(self):
        bg = self.dark_bg if self.dark_mode else self.light_bg
        fg = self.dark_fg if self.dark_mode else self.light_fg

        self.master.configure(bg=bg)
        self.entry.configure(bg=bg, fg=fg, insertbackground=fg)
        self.listbox.configure(bg=bg, fg=fg)
        self.button_frame.configure(bg=bg)
        self.extra_button_frame.configure(bg=bg)
        self.calc_button.configure(bg=bg, fg=fg)
        self.export_button.configure(bg=bg, fg=fg)
        self.theme_button.configure(bg=bg, fg=fg)
        self.history_toggle_button.configure(bg=bg, fg=fg)
        self.clear_history_button.configure(bg=bg, fg=fg)
        for child in self.button_frame.winfo_children():
            child.configure(bg=bg, fg=fg)

    # ----------------------------
    # History Visibility
    # ----------------------------
    def toggle_history(self):
        if self.show_history:
            self.listbox.pack_forget()
            self.history_toggle_button.config(text="Show History")
            self.show_history = False
        else:
            self.listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
            self.history_toggle_button.config(text="Hide History")
            self.show_history = True

    def clear_history(self):
        self.listbox.delete(0, tk.END)
        self.history.clear()
        self.history_index = None

    # ----------------------------
    # Undo/Redo
    # ----------------------------
    def on_entry_change(self, event):
        # Save current entry to undo stack
        if event.keysym not in ["Up", "Down", "Return"]:
            self.undo_stack.append(self.entry.get())

    def undo(self, event=None):
        if self.undo_stack:
            last = self.undo_stack.pop()
            self.redo_stack.append(self.entry.get())
            self.entry.delete(0, tk.END)
            self.entry.insert(0, last)

    def redo(self, event=None):
        if self.redo_stack:
            last = self.redo_stack.pop()
            self.undo_stack.append(self.entry.get())
            self.entry.delete(0, tk.END)
            self.entry.insert(0, last)

    # ----------------------------
    # Evaluate Expression
    # ----------------------------
    def evaluate_expression(self, expr):
        allowed_funcs = {
            "sqrt": math.sqrt, "log": math.log,
            "sin": math.sin, "cos": math.cos, "tan": math.tan,
            "factorial": math.factorial, "pi": math.pi, "e": math.e
        }
        try:
            result = eval(expr, {"__builtins__": None}, allowed_funcs)
            return result
        except Exception as e:
            return f"Error: {str(e)}"

    def calculate(self, event=None):
        expr = self.entry.get()
        if not expr.strip():
            return
        result = self.evaluate_expression(expr)
        display_text = f"{expr} = {result}"
        self.history.append(display_text)
        if self.show_history:
            self.listbox.insert(tk.END, display_text)
        self.history_index = None
        self.entry.delete(0, tk.END)

    # ----------------------------
    # History Navigation
    # ----------------------------
    def history_up(self, event):
        if not self.history:
            return
        if self.history_index is None:
            self.history_index = len(self.history) - 1
        else:
            self.history_index = max(0, self.history_index - 1)
        expr = self.history[self.history_index].split('=')[0].strip()
        self.entry.delete(0, tk.END)
        self.entry.insert(0, expr)

    def history_down(self, event):
        if not self.history or self.history_index is None:
            return
        self.history_index = min(len(self.history) - 1, self.history_index + 1)
        expr = self.history[self.history_index].split('=')[0].strip()
        self.entry.delete(0, tk.END)
        self.entry.insert(0, expr)

    # ----------------------------
    # Copy Result
    # ----------------------------
    def copy_result(self, event):
        try:
            selected = self.listbox.get(self.listbox.curselection())
            result = selected.split('=')[1].strip()
            self.master.clipboard_clear()
            self.master.clipboard_append(result)
            messagebox.showinfo("Copied", f"Result {result} copied to clipboard!")
        except Exception:
            messagebox.showwarning("Error", "No result selected")

    # ----------------------------
    # Memory Functions
    # ----------------------------
    def memory_add(self):
        try:
            val = float(self.entry.get())
            self.memory += val
            messagebox.showinfo("Memory", f"Added {val} to memory. Memory = {self.memory}")
        except:
            messagebox.showwarning("Error", "Invalid input")

    def memory_subtract(self):
        try:
            val = float(self.entry.get())
            self.memory -= val
            messagebox.showinfo("Memory", f"Subtracted {val} from memory. Memory = {self.memory}")
        except:
            messagebox.showwarning("Error", "Invalid input")

    def memory_recall(self):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, str(self.memory))

    def memory_clear(self):
        self.memory = 0
        messagebox.showinfo("Memory", "Memory cleared.")

    # ----------------------------
    # Insert Function Buttons
    # ----------------------------
    def insert_function(self, func_name):
        current = self.entry.get()
        self.entry.delete(0, tk.END)
        if func_name in ["pi", "e"]:
            self.entry.insert(0, f"{current}{func_name}")
        else:
            self.entry.insert(0, f"{current}{func_name}(")

    # ----------------------------
    # Export History
    # ----------------------------
    def export_history(self):
        if not self.history:
            messagebox.showwarning("No History", "Nothing to export!")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text files","*.txt"),("All files","*.*")])
        if file_path:
            with open(file_path, "w") as f:
                for entry in self.history:
                    f.write(f"{entry}\n")
            messagebox.showinfo("Exported", f"History saved to {file_path}")


# ----------------------------
# Run GUI
# ----------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = MathEvaluator(root)
    root.mainloop()
