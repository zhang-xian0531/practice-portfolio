import tkinter as tk
from tkinter import filedialog, messagebox, Label
from PIL import Image, ImageTk
import fitz  # PyMuPDF
from PyPDF2 import PdfMerger
import os

class PDFMergerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF 合併工具")
        self.root.geometry("1000x500")  # 視窗預設大小加大兩倍
        self.file_list = []
        self.thumbnails = []
        self.thumb_refs = []
        self.drag_data = {"item": None, "index": None, "img": None, "start_x": 0}
        self.insert_line = None

        self.canvas = tk.Canvas(root, bg="white", height=400)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_drop)

        self.add_merge_frame = tk.Frame(root)
        self.add_merge_frame.pack(pady=10)

        tk.Button(self.add_merge_frame, text="➕ 添加 PDF", command=self.add_files).pack(side=tk.LEFT, padx=10)
        tk.Button(self.add_merge_frame, text="🚀 合併 PDF！", command=self.merge_pdfs, bg="lightgreen").pack(side=tk.LEFT, padx=10)

    def add_files(self):
        files = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
        for file in files:
            if file not in self.file_list:
                self.file_list.append(file)
        self.refresh_canvas()

    def generate_thumbnail(self, pdf_path):
        doc = fitz.open(pdf_path)
        pix = doc[0].get_pixmap(matrix=fitz.Matrix(0.2, 0.2))
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        return ImageTk.PhotoImage(img)

    def refresh_canvas(self):
        self.canvas.delete("all")
        self.thumbnails.clear()
        self.thumb_refs.clear()
        x = 10
        for idx, file in enumerate(self.file_list):
            thumb = self.generate_thumbnail(file)
            self.thumbnails.append(thumb)
            img_id = self.canvas.create_image(x, 10, anchor=tk.NW, image=thumb, tags=(f"thumb{idx}"))
            del_id = self.canvas.create_text(x + 90, 10, text="✕", fill="red", font=("Arial", 14), tags=(f"del{idx}"))
            name_box = tk.Label(self.canvas, text=os.path.basename(file), bg="white", wraplength=100, justify="center")
            text_window = self.canvas.create_window(x + 50, 160, window=name_box, anchor=tk.N)
            self.thumb_refs.append((img_id, name_box, del_id, x))
            x += 120

    def on_click(self, event):
        for idx, (_, _, del_id, _) in enumerate(self.thumb_refs):
            coords = self.canvas.bbox(del_id)
            if coords and coords[0] <= event.x <= coords[2] and coords[1] <= event.y <= coords[3]:
                del self.file_list[idx]
                self.refresh_canvas()
                return
        for idx, (img_id, _, _, _) in enumerate(self.thumb_refs):
            coords = self.canvas.bbox(img_id)
            if coords and coords[0] <= event.x <= coords[2] and coords[1] <= event.y <= coords[3]:
                self.drag_data["item"] = img_id
                self.drag_data["index"] = idx
                self.drag_data["start_x"] = coords[0]
                return

    def on_drag(self, event):
        if self.drag_data["item"] is not None:
            self.canvas.coords(self.drag_data["item"], event.x, 10)
            idx_width = 120
            drop_index = event.x // idx_width
            if drop_index >= len(self.file_list):
                drop_index = len(self.file_list)
            if self.insert_line:
                self.canvas.delete(self.insert_line)
            self.insert_line = self.canvas.create_line(drop_index * idx_width, 0, drop_index * idx_width, 400, fill="blue", width=2, dash=(4, 2))

    def on_drop(self, event):
        if self.drag_data["item"] is not None:
            idx_width = 120
            drop_index = event.x // idx_width
            if drop_index >= len(self.file_list):
                drop_index = len(self.file_list) - 1
            old_index = self.drag_data["index"]
            if drop_index != old_index and 0 <= drop_index < len(self.file_list):
                item = self.file_list.pop(old_index)
                self.file_list.insert(drop_index, item)
            self.drag_data = {"item": None, "index": None, "img": None, "start_x": 0}
            if self.insert_line:
                self.canvas.delete(self.insert_line)
                self.insert_line = None
            self.refresh_canvas()

    def merge_pdfs(self):
        if not self.file_list:
            messagebox.showwarning("警告", "請先選擇要合併的 PDF 檔案！")
            return

        output_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if not output_path:
            return

        merger = PdfMerger()
        try:
            for pdf in self.file_list:
                merger.append(pdf)
            merger.write(output_path)
            merger.close()
            messagebox.showinfo("成功！", f"PDF 合併完成！\n\n儲存位置：{output_path}")
        except Exception as e:
            messagebox.showerror("錯誤", f"合併時發生錯誤：{e}")

if __name__ == "__main__":
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass

    root = tk.Tk()
    app = PDFMergerGUI(root)
    root.mainloop()

