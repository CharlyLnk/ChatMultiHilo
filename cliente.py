import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, simpledialog


class ClientApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cliente - Chat")
        self.client_socket = None
        self.username = None

        # Interfaz gráfica del cliente
        self.chat_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, state=tk.DISABLED, width=50, height=20)
        self.chat_box.grid(row=0, column=0, padx=10, pady=10)

        self.log_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, state=tk.DISABLED, width=50, height=5)
        self.log_box.grid(row=1, column=0, padx=10, pady=10)

        self.message_entry = tk.Entry(root, width=40)
        self.message_entry.grid(row=2, column=0, padx=10, pady=5)

        self.send_button = tk.Button(root, text="Enviar", command=self.send_message)
        self.send_button.grid(row=2, column=1, padx=5, pady=5)

        self.disable_chat()  # Deshabilitar chat hasta que se ingrese el nombre

        # Conectarse al servidor
        self.connect_to_server()

    def connect_to_server(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect(("127.0.0.1", 5555))
            self.update_log("Conectado al servidor.")

            # Pedir el nombre al usuario a través de una ventana emergente
            self.username = simpledialog.askstring("Nombre", "Introduce tu nombre:", parent=self.root)
            if self.username:
                self.client_socket.send(self.username.encode('utf-8'))  # Enviar nombre de usuario al servidor
                self.update_chat(f"Te has unido como {self.username}.")
                threading.Thread(target=self.receive_messages, daemon=True).start()
                self.enable_chat()  # Habilitar chat después de ingresar el nombre
            else:
                self.update_log("No se ingresó ningún nombre. Cierre la aplicación.")

        except Exception as e:
            self.update_log(f"Error al conectar con el servidor: {e}")
            self.disable_chat()

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if message:
                    # Verificar si el mensaje viene del servidor
                    if message.startswith("Servidor:"):
                        self.update_chat(f"Servidor dice: {message.split('Servidor: ')[1]}")
                    else:
                        self.update_chat(message)
            except:
                self.update_log("Conexión con el servidor perdida.")
                self.disable_chat()
                break

    def send_message(self):
        message = self.message_entry.get()
        if message:
            try:
                self.client_socket.send(message.encode('utf-8'))
                self.update_chat(f"Tú: {message}")
                self.message_entry.delete(0, tk.END)
            except:
                self.update_log("No se pudo enviar el mensaje. Desconectado del servidor.")
                self.disable_chat()

    def disable_chat(self):
        """Deshabilita el campo de texto y el botón de enviar cuando el servidor se desconecta o al inicio"""
        self.message_entry.config(state=tk.DISABLED)
        self.send_button.config(state=tk.DISABLED)

    def enable_chat(self):
        """Habilita el campo de texto y el botón de enviar después de ingresar el nombre"""
        self.message_entry.config(state=tk.NORMAL)
        self.send_button.config(state=tk.NORMAL)

    def update_chat(self, message):
        self.chat_box.config(state=tk.NORMAL)
        self.chat_box.insert(tk.END, f"{message}\n")
        self.chat_box.config(state=tk.DISABLED)
        self.chat_box.see(tk.END)

    def update_log(self, log_message):
        self.log_box.config(state=tk.NORMAL)
        self.log_box.insert(tk.END, f"{log_message}\n")
        self.log_box.config(state=tk.DISABLED)
        self.log_box.see(tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = ClientApp(root)
    root.mainloop()
