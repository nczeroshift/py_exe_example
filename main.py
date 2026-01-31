import tkinter.ttk as ttk
import tkinter as tk
from tkinter import filedialog
import pandas as pd

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def pick_file():
    path = filedialog.askopenfilename(
        title="Select a file",
        filetypes=[
            ("All files", "*.*"),
            ("Text files", "*.txt"),
            ("Images", "*.png;*.jpg;*.jpeg;*.gif"),
        ],
    )
    if not path:  # user didn't cancel
        return

    selected_path_var.set(path)
    df = pd.read_excel(path)
    total = pd.to_numeric(df.iloc[:, 0], errors="coerce").sum()
    selected_path_var.set(path + " sum: " + str(total) )

    x = pd.to_numeric(df.iloc[:, 0], errors="coerce")
    y = pd.to_numeric(df.iloc[:, 1], errors="coerce") if df.shape[1] > 1 else None

    # Clear previous plot (if any)
    for w in plot_frame.winfo_children():
        w.destroy()

    fig = Figure(figsize=(6.0, 3.5), dpi=100)
    ax = fig.add_subplot(111)
    ax.grid(True, alpha=0.3)

    if y is not None:
        ax.plot(x, y, marker="o", linewidth=1)
        ax.set_xlabel(df.columns[0] if df.columns.size > 0 else "Column 1")
        ax.set_ylabel(df.columns[1] if df.columns.size > 1 else "Column 2")
    else:
        ax.plot(x, marker="o", linewidth=1)
        ax.set_xlabel(df.columns[0] if df.columns.size > 0 else "Column 1")
        ax.set_ylabel("Value")

    ax.set_title("Excel Data Plot")

    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)



root = tk.Tk()
root.title("File Picker Demo")
root.geometry("480x750")
root.iconbitmap("res/lnec.ico")

img = tk.PhotoImage(file="res/logo.png")
img_label = ttk.Label(root, image=img)
img_label.pack(padx=12, pady=12)

selected_path_var = tk.StringVar(value="No file selected")

label = tk.Label(root, textvariable=selected_path_var, wraplength=480, justify="left")
label.pack(padx=12, pady=(12, 8), fill="x")

button = ttk.Button(root, text="Pick a file…", command=pick_file)
button.pack(padx=12, pady=8)

plot_frame = tk.Frame(root)
plot_frame.pack(padx=12, pady=12, fill="both", expand=True)

root.mainloop()

if __name__ == "__main__":
    root.mainloop()