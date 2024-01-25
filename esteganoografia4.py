from stegano import lsb
from PIL import Image
from tkinter import Tk, filedialog, Label, Button, Entry, StringVar, font

class SteganoGUI:
    def __init__(self, master):
        self.master = master
        master.title("Esteganografia GUI ")
        master.geometry("600x400")

        bold_font = font.Font(weight="bold")
        
        self.label = Label(master, text="Selecciona la imagen:", font=bold_font)
        self.label.pack()

        self.select_button = Button(master, text="Seleccionar Imagen", command=self.selec_image)
        self.select_button.pack()

        self.label_message = Label(master, text="Mensaje Ocultar", font=bold_font)
        self.label_message.pack()

        self.entry_message = Entry(master, width=50)
        self.entry_message.pack()

        self.label_password = Label(master, text="Contraseña:", font=bold_font)
        self.label_password.pack()

        self.entry_password = Entry(master, show="*", width=50)
        self.entry_password.pack()

        self.hide_button = Button(master, text="Ocultar Mensaje", command=self.hide_message)
        self.hide_button.pack()

        self.result_label = Label(master, text="", font=bold_font)
        self.result_label.pack()

        self.label_reveal_password = Label(master, text="Contraseña para Revelar:", font=bold_font)
        self.label_reveal_password.pack()

        self.entry_reveal_password = Entry(master, show="*", width=50)
        self.entry_reveal_password.pack()

        self.reveal_button = Button(master, text="Revelar Mensaje", command=self.reveal_message)
        self.reveal_button.pack()

        self.revealed_message_label = Label(master, text="", font=bold_font)
        self.revealed_message_label.pack()
        
    def selec_image(self):
        file_path = filedialog.askopenfilename(title="Seleccionar imagen", filetypes=[("Archivos de imagen", "*.png;*.jpg;*.jpeg")])

        if file_path:
            self.label.config(text=f"Imagen seleccionada: {file_path}")
            self.image_path = file_path

    def hide_message(self):
        mensaje = self.entry_message.get()
        password = self.entry_password.get()
        if mensaje and password:
            try:
                imagen_oculta_path = self.ocultar_info(self.image_path, mensaje, password)
                self.result_label.config(text=f"Imagen con mensaje oculto guardada en: {imagen_oculta_path}")

            except Exception as e:
                self.result_label.config(text=f"Error: {str(e)}")
        
        else:
            self.result_label.config(text="Error: Ingresa un mensaje y una contraseña para ocultar.")

    def ocultar_info(self, image_path, mensaje, password):
        img = Image.open(image_path)
        imagen_oculta_path = image_path.replace(".", "_con_mensaje_oculto.")
        imagen_oculta = lsb.hide(img,f"{mensaje}\n{password}")
        imagen_oculta.save(imagen_oculta_path)
        return imagen_oculta_path
    
    def reveal_message(self):
        reveal_password = self.entry_reveal_password.get()
        try:
            mensaje_recuperado = self.recuperar_info(self.image_path, reveal_password)
            self.revealed_message_label.config(text=f"Mensaje Revelado: {mensaje_recuperado}")

        except Exception as e:
            self.revealed_message_label.config(text=f"Error al revelar mensaje: {str(e)}")

    def recuperar_info(self, image_path, reveal_password):
        img = Image.open(image_path)
        mensaje_recuperado = lsb.reveal(img)
        mensaje, password = mensaje_recuperado.split("\n")
        if password == reveal_password:
            return mensaje
        
        else:
            raise ValueError("Contraseña incorrecta")
        
if __name__ == "__main__":
    root = Tk()
    gui = SteganoGUI(root)
    root.mainloop()