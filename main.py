import customtkinter as ctk
from tkinter import filedialog, messagebox, scrolledtext
from PIL import Image
import os

CHARSET = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

def pixel_to_luminance(px):
    r,g,b = px[:3]
    return 0.2126*r + 0.7152*g + 0.0722*b

def map_pixels_to_chars(img: Image.Image, invert=False):
    img = img.convert('RGB')
    chars = []
    n = len(CHARSET)
    for y in range(img.height):
        row_chars = []
        for x in range(img.width):
            px = img.getpixel((x,y))
            lum = pixel_to_luminance(px)/255.0
            if invert:
                lum = 1.0 - lum
            idx = int(lum*(n-1))
            row_chars.append(CHARSET[idx])
        chars.append(''.join(row_chars))
    return '\n'.join(chars)

def resize_image(img: Image.Image, width: int, scale=0.55):
    w,h = img.size
    new_h = max(1,int(h/w*width*scale))
    return img.resize((width,new_h))

class GradientASCIIApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("ASCII Art Converter")
        self.geometry('900x650')
        ctk.set_appearance_mode('dark')
        ctk.set_default_color_theme('dark-blue')

        self.file_path = ''
        self.ascii_result = ''

        
        self.frame_top = ctk.CTkFrame(self, corner_radius=15, fg_color="#2b1a44")
        self.frame_top.pack(padx=20, pady=20, fill='x')

        
        self.btn_file = ctk.CTkButton(self.frame_top, text='Select File', command=self.browse_file, corner_radius=10, fg_color='#7b2eff', hover_color='#9c5cff')
        self.btn_file.pack(side='left', padx=10, pady=10)

        self.width_var = ctk.IntVar(value=100)
        self.entry_width = ctk.CTkEntry(self.frame_top, width=60, textvariable=self.width_var, placeholder_text='Width', fg_color='#3a1f55', text_color='white', placeholder_text_color='#d2b3ff')
        self.entry_width.pack(side='left', padx=10)

        self.btn_convert = ctk.CTkButton(self.frame_top, text='Convert', command=self.convert, corner_radius=10, fg_color='#7b2eff', hover_color='#9c5cff')
        self.btn_convert.pack(side='left', padx=10)

        self.btn_copy = ctk.CTkButton(self.frame_top, text='Copy', command=self.copy_to_clipboard, corner_radius=10, fg_color='#7b2eff', hover_color='#9c5cff')
        self.btn_copy.pack(side='left', padx=10)

        
        self.text_area = scrolledtext.ScrolledText(self, wrap='none', font=('Consolas', 10), bg='#321f55', fg='#f0e6ff', insertbackground='white')
        self.text_area.pack(expand=True, fill='both', padx=20, pady=10)

    def browse_file(self):
        path = filedialog.askopenfilename(filetypes=[('Images', '*.png *.jpg *.jpeg *.bmp *.gif')])
        if path:
            self.file_path = path

    def convert(self):
        if not self.file_path or not os.path.isfile(self.file_path):
            messagebox.showerror('Error', 'File not found')
            return
        try:
            img = Image.open(self.file_path)
            img = resize_image(img, self.width_var.get())
            self.ascii_result = map_pixels_to_chars(img)
            self.text_area.delete('1.0', 'end')
            self.text_area.insert('1.0', self.ascii_result)
        except Exception as e:
            messagebox.showerror('Error', str(e))

    def copy_to_clipboard(self):
        if self.ascii_result:
            self.clipboard_clear()
            self.clipboard_append(self.ascii_result)
            messagebox.showinfo('Copied', 'ASCII copied to clipboard')

if __name__ == '__main__':
    app = GradientASCIIApp()
    app.mainloop()
