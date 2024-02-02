import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess

class ConverterApp:
    def __init__(self, master):
        self.master = master
        self.master.title("File Converter")
        self.master.geometry("400x250")

        self.label = tk.Label(master, text="Seleccionar archivo o carpeta:", font=("Helvetica", 12))
        self.label.pack(pady=10)

        self.file_button = tk.Button(master, text="Elegir Archivo", command=self.select_file)
        self.file_button.pack(pady=5)

        self.folder_button = tk.Button(master, text="Elegir Carpeta", command=self.selec_folder)
        self.folder_button.pack(pady=5)

        self.convert_button = tk.Button(master, text="Convertir a .exe", command=self.convert_to_exe, bg="blue", fg="white", font=("Helvetica", 12))
        self.convert_button.pack(pady=5)

        self.selected_path = ""

    def select_file(self):
        self.selected_path = filedialog.askopenfilename()
        if self.selected_path:
            self.label.config(text=f"Archivo Seleccionado: {self.selected_path}")

    def selec_folder(self):
        self.selected_path = filedialog.askdirectory()
        if self.selected_path:
            self.label.config(text=f"Carpeta seleccionada: {self.selected_path}")
        
    def convert_to_exe(self):
        if not self.selected_path:
            messagebox.showerror("Error", "Por favor, Seleccione un archivo o carpeta primero.")
            return
        try:
            output_file = "output.txt"
            with open(output_file, "w") as f:
                subprocess.run(["pyinstaller", "--onefile", "--noconsole", self.selected_path], check=True, stdout=f, stderr=subprocess.STDOUT)
            messagebox.showinfo("Exito", "El archivo se ha convertido a .exe correctamente.")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Error al convertir el archivo: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {e}")

def main():
    root = tk.Tk()
    app = ConverterApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

