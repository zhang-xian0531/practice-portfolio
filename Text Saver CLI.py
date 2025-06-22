import tkinter as tk
from tkinter import filedialog, messagebox

def open_file():
    filepath = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if not filepath:
        return
    text_area.delete(1.0, tk.END)
    with open(filepath, "r", encoding="utf-8") as file:
        text_area.insert(tk.END, file.read())
    root.title(f"記事本 - {filepath}")

def save_file():
    filepath = filedialog.asksaveasfilename(defaultextension="txt", filetypes=[("Text Files", "*.txt")])
    if not filepath:
        return
    with open(filepath, "w", encoding="utf-8") as file:
        file.write(text_area.get(1.0, tk.END))
    root.title(f"記事本 - {filepath}")
    messagebox.showinfo("儲存成功", "檔案已儲存")

root = tk.Tk()
root.title("簡易記事本")

text_area = tk.Text(root, wrap="word", font=("Arial", 12))
text_area.pack(expand=1, fill="both")

menu_bar = tk.Menu(root)
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="開啟檔案", command=open_file)
file_menu.add_command(label="儲存檔案", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="離開", command=root.quit)
menu_bar.add_cascade(label="選項", menu=file_menu)

root.config(menu=menu_bar)
root.mainloop()
