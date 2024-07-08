# caja_registradora.py

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import mysql.connector

class Database:
    def __init__(self):
        self.host = "127.0.0.1"
        self.user = "root"
        self.password = ""
        self.database = "lasuertedelaolla"
        self.port = 3306

    def connect(self):
        try:
            self.conexion = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port
            )
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Error al conectar a la base de datos: {e}")
            return None
        return self.conexion

    def close(self, cursor, conexion):
        cursor.close()
        conexion.close()

class CajaRegistradoraFrame(Frame):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self.carrito = []
        self.total = 0
        self.create_widgets()

    def create_widgets(self):
        self.label_titulo = Label(self, text="La Suerte de la Olla", font=("Helvetica", 16))
        self.label_titulo.pack(pady=10)

        self.label_productos = Label(self, text="Productos Disponibles")
        self.label_productos.pack(pady=10)

        self.frame_productos = Frame(self)
        self.frame_productos.pack(pady=10)
        
        self.treeview_productos = ttk.Treeview(self.frame_productos, columns=("Nombre", "Precio"), show='headings')
        self.treeview_productos.heading("Nombre", text="Nombre")
        self.treeview_productos.heading("Precio", text="Precio")
        self.treeview_productos.pack(side=LEFT, fill=BOTH, expand=True)

        self.scrollbar_productos = Scrollbar(self.frame_productos, orient=VERTICAL, command=self.treeview_productos.yview)
        self.treeview_productos.config(yscrollcommand=self.scrollbar_productos.set)
        self.scrollbar_productos.pack(side=RIGHT, fill=Y)

        self.btn_agregar = Button(self, text="Agregar al Carrito", command=self.agregar_al_carrito)
        self.btn_agregar.pack(pady=10)

        self.label_carrito = Label(self, text="Carrito de Compras")
        self.label_carrito.pack(pady=10)

        self.frame_carrito = Frame(self)
        self.frame_carrito.pack(pady=10)

        self.treeview_carrito = ttk.Treeview(self.frame_carrito, columns=("Nombre", "Precio"), show='headings')
        self.treeview_carrito.heading("Nombre", text="Nombre")
        self.treeview_carrito.heading("Precio", text="Precio")
        self.treeview_carrito.pack(side=LEFT, fill=BOTH, expand=True)

        self.scrollbar_carrito = Scrollbar(self.frame_carrito, orient=VERTICAL, command=self.treeview_carrito.yview)
        self.treeview_carrito.config(yscrollcommand=self.scrollbar_carrito.set)
        self.scrollbar_carrito.pack(side=RIGHT, fill=Y)

        self.btn_comprar = Button(self, text="Comprar", command=self.comprar)
        self.btn_comprar.pack(pady=10)

        self.cargar_productos()

    def cargar_productos(self):
        conexion = self.db.connect()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT id, nombre, precio FROM producto")
            productos = cursor.fetchall()
            for producto in productos:
                self.treeview_productos.insert("", "end", values=(producto[1], producto[2]))
            self.db.close(cursor, conexion)

    def agregar_al_carrito(self):
        selected_item = self.treeview_productos.selection()
        if selected_item:
            item = self.treeview_productos.item(selected_item)
            self.treeview_carrito.insert("", "end", values=item['values'])
            self.carrito.append(item['values'])
            self.total += float(item['values'][1])

    def comprar(self):
        if not self.carrito:
            messagebox.showwarning("Advertencia", "El carrito está vacío.")
            return

        conexion = self.db.connect()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("INSERT INTO venta (total) VALUES (%s)", (self.total,))
            id_venta = cursor.lastrowid

            for producto in self.carrito:
                cursor.execute("SELECT id FROM producto WHERE nombre=%s", (producto[0],))
                id_producto = cursor.fetchone()[0]
                cursor.execute("INSERT INTO detalles_venta (id_venta, id_producto, cantidad, precio_unitario) VALUES (%s, %s, %s, %s)",
                               (id_venta, id_producto, 1, producto[1]))

            conexion.commit()
            self.db.close(cursor, conexion)
            messagebox.showinfo("Venta", f"Venta realizada con éxito. Total: {self.total}")
            self.treeview_carrito.delete(*self.treeview_carrito.get_children())
            self.carrito = []
            self.total = 0
