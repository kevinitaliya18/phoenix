import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageGrab
import pytesseract
import pyperclip
import os

pytesseract.pytesseract.tesseract_cmd = r"D:\Tesseract\tesseract.exe"


def get_clipboard_image():
    img = ImageGrab.grabclipboard()
    return img if isinstance(img, Image.Image) else None

def get_local_image():
    filepath = filedialog.askopenfilename(
        title="Select Image",
        filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp *.tiff *.webp")]
    )
    if filepath and os.path.exists(filepath):
        try:
            return Image.open(filepath)
        except Exception as e:
            messagebox.showerror("Error", f"Could not open image:\n{e}")
    return None

def extract_text_from_image(img):
    text = pytesseract.image_to_string(img).strip()
    pyperclip.copy(text)
    return text or "No text found in image"

def show_image_and_text_window(img, text):
    window = tk.Toplevel()
    window.title("OCR Viewer")
    window.geometry("1000x600")

    window.columnconfigure(0, weight=1)
    window.columnconfigure(1, weight=2)
    window.rowconfigure(0, weight=1)

    # Resize image for display
    display_img = img.resize((400, int(img.height * 400 / img.width)))
    tk_img = ImageTk.PhotoImage(display_img)

    img_label = tk.Label(window, image=tk_img)
    img_label.image = tk_img
    img_label.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    text_area = tk.Text(window, wrap="word", font=("Arial", 14))
    text_area.insert("1.0", text)
    text_area.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

    # Add scrollbar
    scrollbar = tk.Scrollbar(window, command=text_area.yview)
    scrollbar.grid(row=0, column=2, sticky="ns")
    text_area.config(yscrollcommand=scrollbar.set)

def process_image(source):
    img = get_clipboard_image() if source == "clipboard" else get_local_image()
    if img:
        text = extract_text_from_image(img)
        show_image_and_text_window(img, text)
    else:
        messagebox.showerror("Error", "No image found or selected.")

def main_ui():
    root = tk.Tk()
    root.title("Image to Text (OCR)")
    root.geometry("400x220")

    tk.Label(root, text="Choose Image Source", font=("Helvetica", 16)).pack(pady=20)

    tk.Button(root, text="📋 From Clipboard", font=("Arial", 14),
              command=lambda: process_image("clipboard")).pack(pady=10)

    tk.Button(root, text="🖼️ From Local File", font=("Arial", 14),
              command=lambda: process_image("local")).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main_ui()
