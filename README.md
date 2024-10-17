# ChatMultiHilo
Se realiza la práctica para la materia de Tecnologías de programación sobre un cliente y servidor que funcionen como chat utilizando concurrencia de hilos

# Explicación del Código de Chat Multihilo

## 1. `cliente.py`

El archivo **`cliente.py`** implementa la lógica del lado del cliente para poder entablar una conversación en un chat multihilo. Las funciones principales de este archivo son:

### `ClientApp.__init__(self, root)`
Esta es la función inicializadora de la interfaz gráfica del cliente. Configura la ventana principal del cliente utilizando **Tkinter** y establece los componentes como el campo de texto para el chat, el cuadro de mensajes y el botón para enviar mensajes. También inicia el proceso de conexión con el servidor.

### `ClientApp.connect_to_server(self)`
Esta función establece una conexión con el servidor a través de un socket y solicita al usuario su nombre mediante una ventana emergente. Una vez que el nombre es ingresado, lo envía al servidor y comienza un hilo para recibir mensajes de forma asíncrona con `receive_messages`.

### `ClientApp.receive_messages(self)`
Este método se ejecuta en un hilo separado y está encargado de escuchar mensajes provenientes del servidor. Si el cliente recibe un mensaje, este se muestra en el cuadro de chat. También gestiona las desconexiones inesperadas del servidor.

### `ClientApp.send_message(self)`
Permite al usuario enviar un mensaje al servidor. Si el mensaje es válido, se envía a través del socket y se actualiza el cuadro de chat con el mensaje enviado. En caso de error o desconexión, deshabilita la capacidad de enviar mensajes.

### `ClientApp.update_chat(self, message)`
Actualiza el cuadro de chat con los mensajes que se envían o reciben. Añade un nuevo mensaje en el cuadro de texto de manera que el historial de chat esté visible para el usuario.

---

## 2. `servidor.py`

El archivo **`servidor.py`** implementa la lógica del servidor para el chat multihilo. Las funciones principales de este archivo son:

### `ServerApp.__init__(self, root)`
Inicializa la interfaz gráfica del servidor usando **Tkinter** y establece la estructura básica de la ventana, incluyendo la lista de clientes conectados, el cuadro de chat y el cuadro de logs. También inicia el socket del servidor y el hilo que acepta nuevas conexiones de clientes.

### `ServerApp.accept_clients(self)`
Este método es responsable de aceptar conexiones entrantes de los clientes. Cada vez que un cliente se conecta, se inicia un nuevo hilo para manejar la comunicación con dicho cliente mediante la función `handle_client`.

### `ServerApp.handle_client(self, client_socket, client_address)`
Maneja la interacción con cada cliente. Recibe el nombre del cliente, lo guarda en la lista de clientes conectados, y recibe y retransmite los mensajes que envía el cliente. En caso de desconexión, remueve al cliente de la lista.

### `ServerApp.broadcast_message(self, sender, message)`
Retransmite un mensaje recibido por un cliente a todos los demás clientes conectados, excepto al remitente. Esto permite que todos los usuarios vean los mensajes enviados por los demás.

### `ServerApp.remove_client(self, client_name)`
Elimina al cliente de la lista de usuarios conectados y del diccionario interno de clientes. Esta función se utiliza cuando un cliente se desconecta del servidor.

---

### Conclusión

En este sistema de chat multihilo:
- El **servidor** acepta conexiones de múltiples clientes, retransmite mensajes entre ellos, y maneja la adición o desconexión de clientes.
- El **cliente** se conecta al servidor, envía mensajes y recibe mensajes de otros usuarios de forma asíncrona.

Este diseño utiliza hilos para permitir la comunicación simultánea entre múltiples clientes y el servidor sin bloquear la interfaz gráfica del usuario.
