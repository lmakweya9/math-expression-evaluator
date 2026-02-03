import tkinter as tk
from tkinter import messagebox
import math
import re

# Color Palette for the Modern Look
COLORS = {
    "bg": "#1e1e1e",          # Deep Charcoal
    "entry_bg": "#252526",    # Slightly lighter charcoal
    "text": "#ffffff",        # White text
    "btn_num": "#333333",     # Dark grey for numbers
    "btn_op": "#3e3e42",      # Medium grey for operations
    "btn_eq": "#0e639c",      # Blue accent for equals
    "btn_special": "#2d2d2d", # C, MC, MR, M+
    "accent": "#4ec9b0",      # Emerald Green for the result
    "history": "#888888"      # Dim grey for history
}

class CalculatorEngine:
    """The pure math logic. No GUI code here."""
    def __init__(self):
        self.memory = 0

    def evaluate_expression(self, expr):
        if not expr.strip():
            raise ValueError("Empty expression")

        # Pre-processing
        expr = expr.replace('^', '**')
        expr = expr.replace('pi', str(math.pi))
        expr = expr.replace('e', str(math.e))
        
        # Factorial Regex
        expr = re.sub(r'(\d+)!', r'math.factorial(\1)', expr)

        # Setup Allowed Names for Security
        allowed_names = {k: getattr(math, k) for k in dir(math) if not k.startswith("__")}
        allowed_names.update({"abs": abs, "round": round, "math": math})

        try:
            return eval(expr, {"__builtins__": {}}, allowed_names)
        except ZeroDivisionError:
            raise ZeroDivisionError("division by zero")
        except (ValueError, OverflowError):
            raise ValueError("Math domain error")
        except Exception:
            raise SyntaxError("Invalid expression")

    def memory_add(self, value):
        self.memory += float(value)

    def memory_recall(self):
        return self.memory

    def memory_clear(self):
        self.memory = 0

class MathEvaluatorGUI:
    """The Modern UI Layer."""
    def __init__(self, master):
        self.master = master
        self.engine = CalculatorEngine()
        
        master.title("Advanced Calculator")
        master.geometry("400x620")
        master.configure(bg=COLORS["bg"])
        master.resizable(False, False)

        # --- History Label ---
        self.history_var = tk.StringVar(value="")
        self.history_label = tk.Label(
            master, textvariable=self.history_var, font=("Segoe UI", 10),
            bg=COLORS["bg"], fg=COLORS["history"], anchor="e"
        )
        self.history_label.pack(fill="x", padx=25, pady=(20, 0))

        # --- Main Display ---
        self.entry = tk.StringVar()
        self.display = tk.Entry(
            master, textvariable=self.entry, font=("Segoe UI", 28, "bold"),
            bg=COLORS["entry_bg"], fg=COLORS["accent"],
            insertbackground="white", borderwidth=0, 
            justify='right', highlightthickness=1,
            highlightbackground="#444444"
        )
        self.display.pack(fill="both", padx=20, pady=(5, 20))

        # Keyboard Bindings
        master.bind("<Return>", lambda e: self.calculate())
        master.bind("<Escape>", lambda e: self.entry.set(""))

        # --- Styled Button Layout ---
        button_layout = [
            ("C", "MC", "MR", "/"),
            ("7", "8", "9", "*"),
            ("4", "5", "6", "-"),
            ("1", "2", "3", "+"),
            ("0", ".", "^", "!"),
            ("sqrt", "log", "(", ")"),
            ("M+", "=")
        ]

        for row in button_layout:
            frame = tk.Frame(master, bg=COLORS["bg"])
            frame.pack(expand=True, fill="both", padx=10)
            for text in row:
                btn_color = self.get_btn_color(text)
                btn = tk.Button(
                    frame, text=text, font=("Segoe UI", 14, "bold"),
                    bg=btn_color, fg=COLORS["text"],
                    activebackground=COLORS["accent"],
                    activeforeground="black",
                    relief="flat", bd=0, cursor="hand2",
                    command=lambda t=text: self.button_press(t)
                )
                btn.pack(side="left", expand=True, fill="both", padx=3, pady=3)
                
                # Add Hover Effect
                btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#555555") if b['bg'] != COLORS["btn_eq"] else None)
                btn.bind("<Leave>", lambda e, b=btn, c=btn_color: b.config(bg=c))

    def get_btn_color(self, text):
        if text == "=": return COLORS["btn_eq"]
        if text in ("C", "MC", "MR", "M+"): return COLORS["btn_special"]
        if text.isdigit() or text == ".": return COLORS["btn_num"]
        return COLORS["btn_op"]

    def button_press(self, key):
        if key == "=":
            self.calculate()
        elif key == "C":
            self.entry.set("")
            self.history_var.set("")
        elif key == "M+":
            try:
                res = self.engine.evaluate_expression(self.entry.get() or "0")
                self.engine.memory_add(res)
            except Exception as e:
                self.show_error(str(e))
        elif key == "MR":
            self.entry.set(str(self.engine.memory_recall()))
        elif key == "MC":
            self.engine.memory_clear()
        else:
            self.entry.set(self.entry.get() + key)

    def calculate(self):
        expr = self.entry.get()
        if not expr: return
        try:
            result = self.engine.evaluate_expression(expr)
            self.history_var.set(f"{expr} =") # Set the history
            
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            self.entry.set(str(result))
        except Exception as e:
            self.show_error(str(e))

    def show_error(self, message):
        messagebox.showerror("Error", message)

if __name__ == "__main__":
    root = tk.Tk()
    app = MathEvaluatorGUI(root)
    root.mainloop()