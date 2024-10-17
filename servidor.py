import socket
import threading
import tkinter as tk
from tkinter import scrolledtext


class ServerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Servidor - Chat Multihilo")
        self.clients = {}  # Guardar clientes conectados
        self.current_client = None

        # Interfaz gráfica del servidor
        self.user_list = tk.Listbox(root, width=25)
        self.user_list.grid(row=0, column=0, padx=10, pady=10)
        self.user_list.bind('<<ListboxSelect>>', self.select_user)

        self.chat_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, state=tk.DISABLED, width=50, height=20)
        self.chat_box.grid(row=0, column=1, padx=10, pady=10)

        self.user_log = scrolledtext.ScrolledText(root, wrap=tk.WORD, state=tk.DISABLED, width=50, height=5)
        self.user_log.grid(row=1, column=1, padx=10, pady=10)

        self.message_entry = tk.Entry(root, width=40)
        self.message_entry.grid(row=2, column=1, padx=10, pady=5)

        self.send_button = tk.Button(root, text="Enviar", command=self.send_message)
        self.send_button.grid(row=2, column=2, padx=5, pady=5)

        # Iniciar el servidor
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(("0.0.0.0", 5555))
        self.server_socket.listen(5)
        threading.Thread(target=self.accept_clients, daemon=True).start()

    def accept_clients(self):
        while True:
            client_socket, client_address = self.server_socket.accept()
            threading.Thread(target=self.handle_client, args=(client_socket, client_address), daemon=True).start()

    def handle_client(self, client_socket, client_address):
        client_name = client_socket.recv(1024).decode('utf-8')
        self.clients[client_name] = client_socket
        self.user_list.insert(tk.END, client_name)  # Insertar el nombre del cliente en la lista
        self.update_log(f"{client_name} se ha conectado desde {client_address}")

        while True:
            try:
                message = client_socket.recv(1024).decode('utf-8')
                if message:
                    # Mostrar el mensaje en el chat del servidor
                    self.update_chat(f"{client_name}: {message}")
                    
                    # Retransmitir (broadcast) el mensaje a todos los clientes conectados
                    self.broadcast_message(client_name, message)
            except:
                self.update_log(f"{client_name} se ha desconectado.")
                
                # Eliminar el cliente correctamente de la lista y del diccionario
                self.remove_client(client_name)
                break

    def remove_client(self, client_name):
        """Elimina el cliente del diccionario y de la lista gráfica (Listbox)"""
        if client_name in self.clients:
            self.clients.pop(client_name)  # Eliminar del diccionario de clientes

            # Buscar la posición del cliente en la lista de usuarios y eliminarlo
            user_index = self.user_list.get(0, tk.END).index(client_name)
            self.user_list.delete(user_index)  # Eliminar del Listbox

    def broadcast_message(self, sender, message):
        """Envía el mensaje a todos los clientes conectados excepto al remitente"""
        for client_name, client_socket in self.clients.items():
            if client_name != sender:
                try:
                    client_socket.send(f"{sender}: {message}".encode('utf-8'))
                except:
                    pass

    def select_user(self, event):
        selection = event.widget.curselection()
        if selection:
            self.current_client = event.widget.get(selection[0])

    def send_message(self):
        message = self.message_entry.get()
        if self.current_client and message:
            # Verificar si hay usuarios conectados antes de enviar
            if len(self.clients) > 0:
                self.clients[self.current_client].send(f"Servidor: {message}".encode('utf-8'))
                self.update_chat(f"Yo a {self.current_client}: {message}")
                self.message_entry.delete(0, tk.END)
            else:
                self.update_log("No hay usuarios conectados a quienes enviar el mensaje.")

    def update_chat(self, message):
        self.chat_box.config(state=tk.NORMAL)
        self.chat_box.insert(tk.END, f"{message}\n")
        self.chat_box.config(state=tk.DISABLED)
        self.chat_box.see(tk.END)

    def update_log(self, log_message):
        self.user_log.config(state=tk.NORMAL)
        self.user_log.insert(tk.END, f"{log_message}\n")
        self.user_log.config(state=tk.DISABLED)
        self.user_log.see(tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = ServerApp(root)
    root.mainloop()
