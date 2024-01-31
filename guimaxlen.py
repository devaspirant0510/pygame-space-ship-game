import tkinter as tk

def on_validate(char, entry_value):
    return len(entry_value) <= 10

root = tk.Tk()

validate_cmd = root.register(on_validate)

entry = tk.Entry(root, validate="key", validatecommand=(validate_cmd, "%S", "%P"))
entry.pack(padx=10, pady=10)

root.mainloop()