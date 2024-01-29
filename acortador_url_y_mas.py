import tkinter as tk
from tkinter import ttk, filedialog
import pyshorteners
import pyperclip
import requests
import qrcode
from PIL import ImageTk
import os
import tempfile
import shutil
import webbrowser
import cv2
from pyzbar.pyzbar import decode

class URLShortenerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("URL Shortener/Decoder/QR")
        self.master.configure(background="#f0f0f0")  # Cambiar el color de fondo
        self.master.geometry("890x678")  # Ajustar el tamaño de la ventana

        self.label = ttk.Label(master, text="Enter URL:", font=('Helvetica', 14, 'bold'))
        self.label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.url_entry = ttk.Entry(master, width=70, font=('Helvetica', 12))
        self.url_entry.grid(row=0, column=1, columnspan=3, padx=10, pady=10)

        self.shorten_button = ttk.Button(master, text="Acortar", command=self.shorten_url, width=10)
        self.shorten_button.grid(row=0, column=4, padx=10, pady=10)

        self.decode_button = ttk.Button(master, text="Decode", command=self.decode_url, width=10)
        self.decode_button.grid(row=1, column=4, padx=10, pady=10)

        self.qr_button = ttk.Button(master, text="QR", command=self.generate_qr, width=10)
        self.qr_button.grid(row=2, column=4, padx=10, pady=10)

        self.scan_button = ttk.Button(master, text="Scan QR", command=self.scan_qr, width=10)
        self.scan_button.grid(row=3, column=4, padx=10, pady=10)

        self.result_label = ttk.Label(master, text="", font=('Helvetica', 14, 'bold'))
        self.result_label.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky="w")

        self.copy_button = ttk.Button(master, text="Copy", command=self.copy_shortened_url, width=10)
        self.copy_button.grid(row=3, column=0, columnspan=5, padx=10, pady=10)

        self.download_button = ttk.Button(master, text="Download QR", command=self.download_qr, width=15)
        self.download_button.grid(row=4, column=0, columnspan=5, padx=10, pady=10)

        self.open_button = ttk.Button(master, text="Abrir URL acortada", command=self.open_shortened_url)
        self.open_button.grid(row=5, column=0, columnspan=5, padx=10, pady=10)

        self.qr_image_label = ttk.Label(master)
        self.qr_image_label.grid(row=6, column=0, columnspan=5, padx=10, pady=10)

        self.qr_image_path = None  # Ruta de la imagen del código QR

    def shorten_url(self):
        url = self.url_entry.get()
        if not url:
            self.result_label.config(text="Por favor, introduzca una URL")
            return
        
        try:
            shortener = pyshorteners.Shortener()
            short_url = shortener.tinyurl.short(url)
            self.result_label.config(text=f"URL abreviada: {short_url}")
        except Exception as e:
            self.result_label.config(text=f"Se ha producido un error: {str(e)}")

    def decode_url(self):
        url = self.url_entry.get()
        if not url:
            self.result_label.config(text="Por favor, introduzca una URL")
            return

        try:
            # Seguir los redireccionamientos hasta llegar a la URL final
            response = requests.get(url, allow_redirects=True)
            final_url = response.url

            # Mostrar la URL final
            self.result_label.config(text=f"Original URL: {final_url}")
        except Exception as e:
            self.result_label.config(text=f"Se ha producido un error: {str(e)}")

    def copy_shortened_url(self):
        shortened_url = self.result_label.cget("text").split(":", 1)[-1].strip()
        pyperclip.copy(shortened_url)
        self.master.clipboard_clear()
        self.master.clipboard_append(shortened_url)

    def generate_qr(self):
        url = self.url_entry.get()
        if not url:
            self.result_label.config(text="Ingrese una URL para generar un código QR")
            return

        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Guarda la imagen del código QR temporalmente
        qr_image_path = os.path.join(tempfile.gettempdir(), "temp_qr.png")
        img.save(qr_image_path)
        
        # Muestra la imagen del código QR en la interfaz
        qr_image = ImageTk.PhotoImage(img)
        self.qr_image_label.config(image=qr_image)
        self.qr_image_label.image = qr_image
        
        self.result_label.config(text="Código QR generado con éxito")
        
        # Guarda la ruta de la imagen del código QR
        self.qr_image_path = qr_image_path

    def download_qr(self):
        if self.qr_image_path:
            filename = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if filename:
                # Copia la imagen del código QR a la ubicación seleccionada
                shutil.copyfile(self.qr_image_path, filename)
                self.result_label.config(text="El código QR se descargó con éxito")
        else:
            self.result_label.config(text="Por favor, genere primero un código QR")

    def open_shortened_url(self):
        shortened_url = self.result_label.cget("text").split(":", 1)[-1].strip()
        webbrowser.open(shortened_url)

    def scan_qr(self):
        # Abrir el cuadro de diálogo para seleccionar la imagen del código QR
        file_path = filedialog.askopenfilename(title="Seleccionar imagen del código QR", filetypes=[("Archivos de imagen", "*.png;*.jpg;*.jpeg")])
        if not file_path:
            self.result_label.config(text="No se seleccionó ninguna imagen")
            return

        # Leer la imagen del código QR
        qr_image = cv2.imread(file_path)

        # Decodificar el código QR
        decoded_objects = decode(qr_image)
        if decoded_objects:
            for obj in decoded_objects:
                self.result_label.config(text=f"Código QR detectado: {obj.data.decode('utf-8')}")
                break
        else:
            self.result_label.config(text="No se detectaron códigos QR en la imagen")

def main():
    root = tk.Tk()
    app = URLShortenerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
