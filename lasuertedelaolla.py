from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
import ttkbootstrap as tb
import mysql.connector
from tkinter import messagebox
import tkinter as tk
import webbrowser
from tkinter import PhotoImage
from tkinter import Toplevel, Label
from cajaregistradora import CajaRegistradoraFrame, Database
from mysql.connector import Error
import datetime
from tkinter import filedialog
from tkinter import simpledialog
import io
import os  

class Venta(tb.Window):
    def __init__(self):
        super().__init__(themename='superhero')
        self.db = Database()
        self.login_ventana()
        self.redes_sociales = []  # Inicializa la lista de redes sociales
        self.max_redes = 5



    #---------------------------------------------------------------------
    #VENTANA INICIAL DEL LOGIN Y LA FUNCIONALIDAD CORRESPONDIENTE PARA VOLVER A ESTA VENTANA

    def login_ventana(self):

    
        for widget in self.winfo_children():
            widget.destroy()
        # Cargar la imagen de fondo
        self.bg_image = Image.open("fondo login.png")
        self.img_width, self.img_height = self.bg_image.size

        self.center_window()
        # Guardar la geometría inicial
        self.initial_geometry = f"{self.img_width}x{self.img_height}"

        # Redimensionar la ventana al tamaño de la imagen
        self.geometry(self.initial_geometry)

        # Crear un canvas
        self.canvas = Canvas(self, width=self.img_width, height=self.img_height)
        self.canvas.pack(fill="both", expand=True)

        # Redimensionar la imagen (opcional, si necesitas cambiar el tamaño)
        self.bg_image = self.bg_image.resize((self.img_width, self.img_height), Image.Resampling.LANCZOS)
        self.initial_bg_image = ImageTk.PhotoImage(self.bg_image)
    
        # Mostrar la imagen de fondo
        self.canvas.create_image(0, 0, image=self.initial_bg_image, anchor="nw")

        # Crear un frame sobre el canvas
        self.frame_login = Frame(self.canvas, bg='white')
        self.frame_login.pack()

        # Posicionar el frame_login en el canvas
        self.canvas.create_window(self.img_width // 2, self.img_height // 2, window=self.frame_login, anchor="center")

        # Crear el LabelFrame
        self.lblframe_login = LabelFrame(self.frame_login, text='La Suerte de la Olla', bg='white')
        self.lblframe_login.pack(padx=15, pady=15)

        # Crear el título del login
        lbltitulo = Label(self.lblframe_login, text='Inicio de Sesión', bg='white', font=('Arial ', 25))
        lbltitulo.pack(padx=15, pady=25)

        # Crear el campo de usuario
          # Crear el texto del usuario
        lbltitulo1 = Label(self.lblframe_login, text='Ingrese su usuario: ', bg='gold', font=('Arial ', 10))
        lbltitulo1.pack(padx=0, pady=0)

        self.txt_usuario = ttk.Entry(self.lblframe_login, width=50, justify=LEFT)
        self.txt_usuario.pack(padx=15, pady=15)

          # Crear el texto de la contraseña
        lbltitulo2 = Label(self.lblframe_login, text='Ingrese su contraseña: ', bg='gold', font=('Arial ', 10))
        lbltitulo2.pack(padx=0, pady=0)

        # Crear el campo de contraseña
        self.txt_contraseña = ttk.Entry(self.lblframe_login, show='*', width=48, justify=LEFT)
        self.txt_contraseña.pack(padx=15, pady=15)

        # Crear el botón de acceso
        btn_acceso = ttk.Button(self.lblframe_login, text='Iniciar sesión', width=60, command=self.logeo)
        btn_acceso.pack(padx=15, pady=2)

        #Crear el botón de registrarse en caso de no tener una cuenta

        btn_registrarse = ttk.Button(self.lblframe_login, text="Registrarse", width=60,command=self.registro)
        btn_registrarse.pack(padx=15,pady=2)

    def volver_inicio(self):
        # Restaurar al estado inicial guardado
        self.login_ventana()

    #------------------------------------------------------------------
    #APARTADO DE REGISTRO Y LOGEO CON SUS VALIDACIONES

    def logeo(self):
        usuario = self.txt_usuario.get()
        contraseña = self.txt_contraseña.get()
         
        if usuario and contraseña:
            try:
                self.conexion = mysql.connector.connect(
                    host="127.0.0.1",
                    user="root",
                    password="",
                    database="lasuertedelaolla",
                    port=3306
                )
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Error al conectar a la base de datos: {e}")
                return

            cursor = self.conexion.cursor()

            # Verificar las credenciales del usuario
            query = "SELECT * FROM usuario WHERE nombre = %s AND contraseña = %s"
            cursor.execute(query, (usuario, contraseña))
            resultado = cursor.fetchone()


            if resultado:
                # Credenciales correctas
                self.frame_login.pack_forget()  # Oculta la ventana del login
                messagebox.showinfo("Información", "Inicio de sesión exitoso")

                # Guardar el mensaje en la tabla de registros
                mensaje = "Inicio de sesión exitoso."
                query_registro = "INSERT INTO registros (mensaje) VALUES (%s)"
                cursor.execute(query_registro, (mensaje,))
                self.conexion.commit()

                cursor.close()
                self.conexion.close()
                
                self.ventana_menu()  # Abre el menú principal
            else:
                # Credenciales incorrectas
                messagebox.showerror("Error", "Credenciales incorrectas. Por favor, intenta de nuevo.")
        else:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios")

    def registro(self):
        self.registro_ventana = Toplevel(self)
        self.registro_ventana.title("Registro de Usuario")

        Label(self.registro_ventana, text="Nombre de Usuario:").pack(pady=5)
        self.registro_usuario = Entry(self.registro_ventana, width=50)
        self.registro_usuario.pack(pady=5)

        Label(self.registro_ventana, text="Contraseña:").pack(pady=5)
        self.registro_contraseña = Entry(self.registro_ventana, show='*', width=50)
        self.registro_contraseña.pack(pady=5)

        Label(self.registro_ventana, text="Rol:").pack(pady=5)
        self.registro_rol = Entry(self.registro_ventana, width=50)
        self.registro_rol.pack(pady=5)

        Label(self.registro_ventana, text="Correo:").pack(pady=5)
        self.registro_correo = Entry(self.registro_ventana, width=50)
        self.registro_correo.pack(pady=5)


        Button(self.registro_ventana, text="Registrar", command=self.registrar_usuario).pack(pady=20)

    def registrar_usuario(self):
        usuario = self.registro_usuario.get()
        contraseña = self.registro_contraseña.get()
        rol = self.registro_rol.get()
        correo = self.registro_correo.get()

        if usuario and contraseña and rol:
            # Conectar a la base de datos MySQL
            try:
                self.conexion = mysql.connector.connect(
                    host="127.0.0.1",
                    user="root",
                    password="",
                    database="lasuertedelaolla",
                    port=3306
                )
                print("Conexión establecida correctamente")
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Error al conectar a la base de datos: {e}")
                return

            cursor = self.conexion.cursor()

            # Verificar si el usuario ya existe
            query = "SELECT * FROM usuario WHERE nombre = %s"
            cursor.execute(query, (usuario,))
            if cursor.fetchone():
                messagebox.showinfo("Información", "El usuario ya existe")
                self.registro_ventana.destroy()
                return

            # Insertar el nuevo usuario
            query = "INSERT INTO usuario (nombre, contraseña, rol, correo) VALUES (%s, %s, %s,%s)"
            cursor.execute(query, (usuario, contraseña, rol, correo))
            self.conexion.commit()

            # Guardar el mensaje en la tabla de registros
            mensaje = "Usuario registrado exitosamente."
            query_registro = "INSERT INTO registros (mensaje) VALUES (%s)"
            cursor.execute(query_registro, (mensaje,))
            self.conexion.commit()

            cursor.close()
            self.conexion.close()
                

       
            messagebox.showinfo("Información", "Usuario registrado exitosamente")
            self.registro_ventana.destroy()
        else:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios")

    #----------------------------------------------------------------
    #MENÚ DE INICIO CON TODOS LOS BOTONES
    def ventana_menu(self):
        # Limpiar la ventana
        for widget in self.winfo_children():
            widget.destroy()
        
        
        #aquí debo agregar los metodos para que la ventana se abra en full size

        self.state('zoomed')
        # Centrando la ventana en la pantalla
        self.center_window()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.frame_left = Frame(self, width=200, bg='black')  
        self.frame_left.grid(row=0, column=0, sticky=NS)

        self.frame_center = Frame(self, bg='#333333') 
        self.frame_center.grid(row=0, column=1, sticky=NSEW)

        self.frame_right = Frame(self, width=400, bg='#222222') 
        self.frame_right.grid(row=0, column=2, sticky=NSEW)


        
        #BOTONES
        #------------------------------------------
        btn_inicio= ttk.Button(self.frame_left, text="Inicio (Login)", width=20 ,bootstyle="warning", command=self.volver_inicio)
        btn_inicio.grid(row=0, column=0, padx=10, pady=10)
        #------------------------------------------
        btn_productos= ttk.Button(self.frame_left, text="Productos", width=20,style="outline.TButton", bootstyle="light", command=self.ventana_lista_productos)
        btn_productos.grid(row=1, column=0, padx=10, pady=10)
        #------------------------------------------
        btn_ventas = ttk.Button(self.frame_left, text="Ventas", width=20,style="outline.TButton", bootstyle="light", command=self.ventana_lista_ventas)
        btn_ventas.grid(row=2, column=0, padx=10, pady=10)
        #------------------------------------------
        btn_clientes = ttk.Button(self.frame_left, text="Clientes", width=20,style="outline.TButton", bootstyle="light", command=self.mostrar_clientes)
        btn_clientes.grid(row=3, column=0, padx=10, pady=10)
        #------------------------------------------
        btn_compras= ttk.Button(self.frame_left, text="Compras", width=20,style="outline.TButton", bootstyle="light", command=self.ventana_lista_compras)
        btn_compras.grid(row=4, column=0, padx=10, pady=10)
        #------------------------------------------
        btn_usuarios = ttk.Button(self.frame_left, text="Usuarios", width=20,style="outline.TButton", bootstyle="light", command=self.ventana_lista_usuarios)
        btn_usuarios.grid(row=5, column=0, padx=10, pady=10)
        #------------------------------------------
        btn_reportes = ttk.Button(self.frame_left, text="Reportes", width=20,style="outline.TButton", bootstyle="light",command=self.ventana_reportes)
        btn_reportes.grid(row=6, column=0, padx=10, pady=10)
        #------------------------------------------
        btn_repartidores = ttk.Button(self.frame_left, text="Repartidores", width=20, style="outline.TButton", bootstyle="light", command=self.mostrar_repartidores)
        btn_repartidores.grid(row=7, column=0, padx=10, pady=10)
        #------------------------------------------
        btn_comentarios = ttk.Button(self.frame_left, text="Comentarios", width=20,style="outline.TButton", bootstyle="light", command=self.mostrar_comentarios)
        btn_comentarios.grid(row=8, column=0, padx=10, pady=10)
        #------------------------------------------
        btn_proveedores = ttk.Button(self.frame_left, text="Proveedores", width=20,style="outline.TButton", bootstyle="light", command=self.ventana_proveedores)
        btn_proveedores.grid(row=9, column=0, padx=10, pady=10)
        #------------------------------------------
        btn_mesas = ttk.Button(self.frame_left, text="Mesas", width=20,style="outline.TButton", bootstyle="light",command=self.ventana_mesas)
        btn_mesas.grid(row=10, column=0, padx=10, pady=10)
        #------------------------------------------
        btn_reservas = ttk.Button(self.frame_left, text="Reservas", width=20,style="outline.TButton", bootstyle="light",command=self.ventana_reservas)
        btn_reservas.grid(row=11, column=0, padx=10, pady=10)
        #------------------------------------------
        btn_promociones = ttk.Button(self.frame_left, text="Promociones", width=20,style="outline.TButton", bootstyle="light", command=self.ventana_promociones)
        btn_promociones.grid(row=12, column=0, padx=10, pady=10)
        #------------------------------------------
        self.btn_registradora = ttk.Button(self.frame_left, text="Caja registradora", width=20, style="outline.TButton", bootstyle="light", command=self.mostrar_caja_registradora)
        self.btn_registradora.grid(row=13, column=0, padx=10, pady=10)
        #------------------------------------------
        btn_redes = ttk.Button(self.frame_left, text="Redes", width=20,style="outline.TButton", bootstyle="light",command=self.cargar_redes_sociales)
        btn_redes.grid(row=14, column=0, padx=10, pady=10)
        #------------------------------------------
        #------------------------------------------
        btn_carta = ttk.Button(self.frame_left, text="Menú Especial", width=20, style="outline.TButton", bootstyle="light", command=self.ventana_menu_especial)
        btn_carta.grid(row=15, column=0, padx=10, pady=10)
        #------------------------------------------
        #------------------------------------------
        btn_informes = ttk.Button(self.frame_left, text="Informes", width=20,style="outline.TButton", bootstyle="light")
        btn_informes.grid(row=16, column=0, padx=10, pady=10)
        #------------------------------------------
        #------------------------------------------
        btn_info = ttk.Button(self.frame_left, text="Configuraciones", width=20, bootstyle="Secondary", command=self.abrir_configuraciones)
        btn_info.grid(row=17, column=0, padx=10, pady=10)
        #------------------------------------------
        btn_restaurarBD=ttk.Button(self.frame_left, text="Actualizar DB", width=20, bootstyle="danger")
        btn_restaurarBD.grid(row=18, column=0, padx=10, pady=4)
        #------------------------------------------
        btn_volver=ttk.Button(self.frame_left, text="Volver", width=20, bootstyle="success", command=self.volver)
        btn_volver.grid(row=19, column=0, padx=10, pady=0)


        nav2 = tk.Label(self.frame_center, text="")
        nav2.grid(row=0, column=0, padx=10, pady=10)

        # Cargar y mostrar una imagen en el frame_center
        self.img_path = "fondo menu.jpg"
        self.mostrar_fondo()

        self.frame_right = Frame(self.master)
        self.frame_right.grid(row=0, column=2, padx=10, pady=10, sticky='nsew')

        # Aquí se debería mostrar el inventario disponible con solo los nombres de los platos o productos y sus cantidades correspondientes más su precio
        nav3 = Label(self.frame_right, text="Inventario")
        nav3.grid(row=0, column=0, padx=10, pady=0)

        # Crear Treeview para mostrar el inventario
        self.tree_inventario = ttk.Treeview(self.frame_right, columns=("nombre", "cantidad", "precio"), show='headings')
        self.tree_inventario.heading("nombre", text="Nombre")
        self.tree_inventario.heading("cantidad", text="Cantidad")
        self.tree_inventario.heading("precio", text="Precio")

        self.tree_inventario.column("nombre", width=150)
        self.tree_inventario.column("cantidad", width=100)
        self.tree_inventario.column("precio", width=100)


        self.tree_inventario.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

        # Configurar las columnas y filas del grid
        self.frame_right.grid_columnconfigure(0, weight=1)
        self.frame_right.grid_rowconfigure(1, weight=1)

        # Llamar al método para poblar el inventario
        self.mostrar_inventario()
    #--------------------------------------------------------------
    #CAMBIO DE FONDO MEDIANTE LAS CONFIGURACIONES SE PUEDE SUBIR CUALQUIER IMAGEN Y SE ADAPTA AL FONDO

    def mostrar_fondo(self):
        img = Image.open(self.img_path)
        img = img.resize((1320, 1020), Image.LANCZOS)
        img_tk = ImageTk.PhotoImage(img)

        img_label = tk.Label(self.frame_center, image=img_tk)
        img_label.image = img_tk
        img_label.grid(row=0, column=0, padx=0, pady=0)

    def abrir_configuraciones(self):
        config_win = tk.Toplevel(self)
        config_win.title("Configuraciones")
        
        # Añadir botón para subir nueva imagen de fondo
        btn_subir_imagen = ttk.Button(config_win, text="Subir nueva imagen de fondo", command=self.subir_imagen)
        btn_subir_imagen.pack(pady=10)

    def subir_imagen(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
        if file_path:
            self.img_path = file_path
            self.mostrar_fondo()
    #---------------------------------------------------------------
    #VOLVER
    def volver(self):
        self.ventana_menu()

    #--------------------------------------------------------------
    #ACTUALIZAR BD
    #def actualizar_bd(self):
    #    try:
    #        # Conexión a la base de datos
    #        conexion = mysql.connector.connect(
    #            host="127.0.0.1",
    #            user="root",
    #            password="",
    #            database="lasuertedelaolla",
     #           port=3306
      #      )

#            if conexion.is_connected():
 #               cursor = conexion.cursor()
#
                    # Lista de comandos SQL para actualizar las tablas
   #             comandos_sql = [
  #                  "UPDATE administrador",
 #                   "UPDATE cliente",
     #               "UPDATE comentarios",
    #                "UPDATE detalles_pedido",
       #             "UPDATE detalles_venta",
      #              "UPDATE empleado",
         #           "UPDATE entregas_a_domicilio",
        #            "UPDATE informacion_nutricional",
           #         "UPDATE informes_diarios",
            #        "UPDATE informes_mensuales",
          #          "UPDATE inventario",
              #      "UPDATE menus_especiales",
             #       "UPDATE mesa",
                #    "UPDATE notificacion_promocion",
               #     "UPDATE pedido",
                   # "UPDATE producto",
                    #"UPDATE promocion",
                    #"UPDATE proveedor",
                   # "UPDATE redes_sociales",
                  #  "UPDATE repartidor",
                 #   "UPDATE reserva",
                #    "UPDATE sesion_cliente",
               #     "UPDATE usuario"
              #  ]

               # for comando in comandos_sql:
              #      cursor.execute(comando)

                    # Confirmar los cambios en la base de datos
               # conexion.commit()

                # Mostrar mensaje de éxito en la interfaz gráfica
                #messagebox.showinfo("Actualización Completa", "Cambios realizados con éxito.")

  #      except Error as e:
 #           # Mostrar mensaje de error en la interfaz gráfica
#            messagebox.showerror("Error", f"Error al actualizar la base de datos: {e}")

   #     finally:
    #        if conexion.is_connected():
     #           cursor.close()
      #          conexion.close()
       #         print("Conexión a la base de datos cerrada.")

    #---------------------------------------------------------------
    #MENÚ ESPECIAL

    def ventana_menu_especial(self):
        self.frame_lista_menus = Frame(self.frame_center)
        self.frame_lista_menus.grid(row=0, column=0, columnspan=2, padx=15, pady=15, sticky=NSEW)

        self.lblframe_botones_menus = LabelFrame(self.frame_lista_menus)
        self.lblframe_botones_menus.grid(row=0, column=0, padx=15, pady=15, sticky=NSEW)

        # Botones para nuevo, modificar y eliminar menús
        btn_nuevo_menu = tb.Button(self.lblframe_botones_menus, text="Nuevo", width=20, bootstyle="success", command=self.nuevo_menu)
        btn_nuevo_menu.grid(row=0, column=0, padx=10, pady=10)
        
        btn_modificar_menu = ttk.Button(self.lblframe_botones_menus, text="Modificar", width=20, command=self.modificar_menu)
        btn_modificar_menu.grid(row=0, column=1, padx=10, pady=10)
        
        btn_eliminar_menu = tb.Button(self.lblframe_botones_menus, text="Eliminar", width=20, bootstyle="danger", command=self.eliminar_menu)
        btn_eliminar_menu.grid(row=0, column=2, padx=10, pady=10)

        # Búsqueda de menús existentes
        self.lblframe_busqueda_menus = LabelFrame(self.frame_lista_menus,  text="Buscar Menús")
        self.lblframe_busqueda_menus.grid(row=1, column=0, padx=15, pady=15, sticky=NSEW)

        self.txt_busqueda_menus = ttk.Entry(self.lblframe_busqueda_menus, width=150)
        self.txt_busqueda_menus.grid(row=0, column=0, padx=(10,0), pady=10, sticky=W)

        btn_buscar_menus = tb.Button(self.lblframe_busqueda_menus, text="🔍", width=3, command=self.buscar_menus)
        btn_buscar_menus.grid(row=0, column=1, padx=(0, 10), pady=10)


        # Vista de árbol para mostrar la lista de menús
        self.lblframe_tree_menus = LabelFrame(self.frame_lista_menus)
        self.lblframe_tree_menus.grid(row=2, column=0, sticky=NSEW)

        # Definición de las columnas manualmente acorde a la tabla de menús
        columnas = ("id", "nombre", "descripcion", "inicio", "termino")

        self.tree_lista_menus = tb.Treeview(self.lblframe_tree_menus, columns=columnas, height=45, show="headings", bootstyle="dark")
        self.tree_lista_menus.grid(row=0, column=0, sticky=NSEW)

        # Títulos de cada una de las columnas
        self.tree_lista_menus.heading("id", text="Id", anchor=W)
        self.tree_lista_menus.heading("nombre", text="Nombre", anchor=W)
        self.tree_lista_menus.heading("descripcion", text="Descripción", anchor=W)
        self.tree_lista_menus.heading("inicio", text="Inicio", anchor=W)
        self.tree_lista_menus.heading("termino", text="Termino", anchor=W)
        # Configurar el ancho de cada columna
        self.tree_lista_menus.column("id", width=50, minwidth=50)
        self.tree_lista_menus.column("nombre", width=150, minwidth=100)
        self.tree_lista_menus.column("descripcion", width=300, minwidth=200)
        self.tree_lista_menus.column("inicio", width=100, minwidth=50)
        self.tree_lista_menus.column("termino", width=100, minwidth=50)
        # Crear el scrollbar
        tree_scroll_menus = tb.Scrollbar(self.lblframe_tree_menus, bootstyle='round-dark', orient=VERTICAL, command=self.tree_lista_menus.yview)
        tree_scroll_menus.grid(row=0, column=1, sticky=NSEW)

        # Configuración del scroll
        self.tree_lista_menus.config(yscrollcommand=tree_scroll_menus.set)

        # Configuración de la expansión de columnas para utilizar todo el ancho disponible
        self.lblframe_tree_menus.columnconfigure(0, weight=1)  # Ajustar el tamaño del Treeview

        # Cargar los menús
        self.cargar_menus()
   
    def nuevo_menu(self):
        # Crear una nueva ventana para ingresar los datos del nuevo menú
        self.ventana_nuevo_menu = Toplevel(self.root)
        self.ventana_nuevo_menu.title("Nuevo Menú")
        
        # Crear los campos para ingresar los datos del nuevo menú
        lbl_nombre = tk.Label(self.ventana_nuevo_menu, text="Nombre:")
        lbl_nombre.grid(row=0, column=0, padx=10, pady=10)

        self.txt_nombre_menu = tk.Entry(self.ventana_nuevo_menu, width=30)
        self.txt_nombre_menu.grid(row=0, column=1, padx=10, pady=10)
        
        lbl_descripcion = tk.Label(self.ventana_nuevo_menu, text="Descripción:")
        lbl_descripcion.grid(row=1, column=0, padx=10, pady=10)

        self.txt_descripcion_menu = tk.Entry(self.ventana_nuevo_menu, width=30)
        self.txt_descripcion_menu.grid(row=1, column=1, padx=10, pady=10)

        lbl_inicio = tk.Label(self.ventana_nuevo_menu, text="Fecha Inic.:")
        lbl_inicio.grid(row=2, column=0, padx=10, pady=10)

        self.txt_inicio = tk.Entry(self.ventana_nuevo_menu, width=30)
        self.txt_inicio.grid(row=2, column=1, padx=10, pady=10)
        
        lbl_termino = tk.Label(self.ventana_nuevo_menu, text="Fecha Term.:")
        lbl_termino.grid(row=3, column=0, padx=10, pady=10)

        self.txt_termino = tk.Entry(self.ventana_nuevo_menu, width=30)
        self.txt_termino.grid(row=3, column=1, padx=10, pady=10)

        # Botón para guardar el nuevo menú
        btn_guardar = ttk.Button(self.ventana_nuevo_menu, text="Guardar", command=self.guardar_nuevo_menu)
        btn_guardar.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    def guardar_nuevo_menu(self):
        # Obtener los valores de los campos
        nombre = self.txt_nombre_menu.get()
        descripcion = self.txt_descripcion_menu.get()
        inicio = self.txt_inicio.get()
        termino = self.txt_termino.get()
        # Validar que todos los campos estén completos
        if nombre and descripcion and inicio and termino:
            try:
                # Conectar a la base de datos
                conexion = mysql.connector.connect(
                    host="127.0.0.1",
                    user="root",
                    password="",
                    database="lasuertedelaolla",
                    port=3306
                )
                
                cursor = conexion.cursor()
                
                # Insertar el nuevo menú en la base de datos
                query = "INSERT INTO menus_especiales (nombre, descripcion, fecha_inicio, fecha_fin) VALUES (%s, %s, %s, %s)"
                cursor.execute(query, (nombre, descripcion, inicio, termino))
                
                conexion.commit()
                # Guardar el mensaje en la tabla de registros
                mensaje = "Menú añadido exitosamente."
                query_registro = "INSERT INTO registros (mensaje) VALUES (%s)"
                cursor.execute(query_registro, (mensaje,))
                conexion.commit()

                cursor.close()
                conexion.close()
                
                # Mostrar mensaje de éxito
                messagebox.showinfo("Nuevo Menú", "Menú creado exitosamente.")
                
                # Cerrar la ventana de nuevo menú
                self.ventana_nuevo_menu.destroy()
                
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Error al conectar a la base de datos: {e}")
        else:
            # Mostrar mensaje de advertencia si no se completaron todos los campos
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
    
    def modificar_menu(self):
        # Crear una nueva ventana para seleccionar el menú a modificar
        self.ventana_modificar_menu = Toplevel(self)
        self.ventana_modificar_menu.title("Modificar Menú")
        
        # Etiqueta y campo de entrada para seleccionar el menú por su nombre
        lbl_nombre = Label(self.ventana_modificar_menu, text="Nombre del menú:")
        lbl_nombre.grid(row=0, column=0, padx=10, pady=10)
        self.txt_nombre_modificar_menu = Entry(self.ventana_modificar_menu, width=30)
        self.txt_nombre_modificar_menu.grid(row=0, column=1, padx=10, pady=10)
        
        # Botón para buscar el menú
        btn_buscar = ttk.Button(self.ventana_modificar_menu, text="Buscar", command=self.buscar_menu_modificar)
        btn_buscar.grid(row=0, column=2, padx=10, pady=10)
        
        # Campos de entrada para modificar los datos del menú
        lbl_nombre_nuevo = Label(self.ventana_modificar_menu, text="Nuevo nombre:")
        lbl_nombre_nuevo.grid(row=1, column=0, padx=10, pady=10)
        self.txt_nombre_nuevo_menu = Entry(self.ventana_modificar_menu, width=30)
        self.txt_nombre_nuevo_menu.grid(row=1, column=1, padx=10, pady=10)
        
        lbl_descripcion_nueva = Label(self.ventana_modificar_menu, text="Nueva descripción:")
        lbl_descripcion_nueva.grid(row=2, column=0, padx=10, pady=10)
        self.txt_descripcion_nueva_menu = Entry(self.ventana_modificar_menu, width=30)
        self.txt_descripcion_nueva_menu.grid(row=2, column=1, padx=10, pady=10)
        
        lbl_nuevo_inic = Label(self.ventana_modificar_menu, text="Nueva fecha inicio:")
        lbl_nuevo_inic.grid(row=3, column=0, padx=10, pady=10)
        self.txt_inicio_nuevo = Entry(self.ventana_modificar_menu, width=30)
        self.txt_inicio_nuevo.grid(row=3, column=1, padx=10, pady=10)

        lbl_nuevo_term = Label(self.ventana_modificar_menu, text="Nueva fecha termino:")
        lbl_nuevo_term.grid(row=4, column=0, padx=10, pady=10)
        self.txt_term_nuevo = Entry(self.ventana_modificar_menu, width=30)
        self.txt_term_nuevo.grid(row=4, column=1, padx=10, pady=10)
        
        # Botón para guardar los cambios
        btn_guardar = ttk.Button(self.ventana_modificar_menu, text="Guardar cambios", command=self.guardar_cambios_menu)
        btn_guardar.grid(row=6, column=0, columnspan=3, padx=10, pady=10)
        
    def buscar_menu_modificar(self):
        # Obtener el nombre del menú a buscar
        nombre = self.txt_nombre_modificar_menu.get()
        
        if nombre:
            try:
                # Conectar a la base de datos
                self.conexion = mysql.connector.connect(
                    host="127.0.0.1",
                    user="root",
                    password="",
                    database="lasuertedelaolla",
                    port=3306
                )
                
                cursor = self.conexion.cursor()
                
                # Buscar el menú en la base de datos
                query = "SELECT * FROM menus_especiales WHERE nombre = %s"
                cursor.execute(query, (nombre,))
                menu = cursor.fetchone()
                
                cursor.close()
                self.conexion.close()
                
                if menu:
                    # Mostrar los datos actuales del menú en los campos de entrada
                    self.txt_nombre_nuevo_menu.insert(0, menu[1])
                    self.txt_descripcion_nueva_menu.insert(0, menu[2])
                    self.txt_inicio_nuevo.insert(0, menu[3])
                    self.txt_term_nuevo.insert(0,menu[4])
                else:
                    messagebox.showwarning("Advertencia", "No se encontró el menú.")
                    
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Error al conectar a la base de datos: {e}")
        else:
            messagebox.showwarning("Advertencia", "El campo de nombre es obligatorio.")
            
    def guardar_cambios_menu(self):
        # Obtener los nuevos valores de los campos
        nombre_nuevo = self.txt_nombre_nuevo_menu.get()
        descripcion_nueva = self.txt_descripcion_nueva_menu.get()
        inicio_nuevo = self.txt_inicio_nuevo.get()
        termino_nuevo = self.txt_term_nuevo.get()
        if nombre_nuevo and descripcion_nueva and inicio_nuevo and termino_nuevo:
            try:
                # Conectar a la base de datos
                self.conexion = mysql.connector.connect(
                    host="127.0.0.1",
                    user="root",
                    password="",
                    database="lasuertedelaolla",
                    port=3306
                )
                
                cursor = self.conexion.cursor()
                
                # Actualizar el menú en la base de datos
                query = "UPDATE menus_especiales SET nombre = %s, descripcion = %s, fecha_inicio = %s, fecha_fin=%s WHERE nombre = %s"
                cursor.execute(query, (nombre_nuevo, descripcion_nueva, inicio_nuevo, termino_nuevo, self.txt_nombre_modificar_menu.get()))
                
                self.conexion.commit()
                # Guardar el mensaje en la tabla de registros
                mensaje = "Menú modificado exitosamente."
                query_registro = "INSERT INTO registros (mensaje) VALUES (%s)"
                cursor.execute(query_registro, (mensaje,))
                self.conexion.commit()

                cursor.close()
                self.conexion.close()
                
                messagebox.showinfo("Modificar Menú", "Menú modificado exitosamente.")
                self.ventana_modificar_menu.destroy()
                
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Error al conectar a la base de datos: {e}")
        else:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
        
    def eliminar_menu(self):
        # Crear una nueva ventana para eliminar un menú
        self.ventana_eliminar_menu = Toplevel(self)
        self.ventana_eliminar_menu.title("Eliminar Menú")
        
        # Etiqueta y campo de entrada para ingresar el nombre del menú a eliminar
        lbl_nombre = Label(self.ventana_eliminar_menu, text="Nombre del menú:")
        lbl_nombre.grid(row=0, column=0, padx=10, pady=10)
        
        self.txt_nombre_eliminar_menu = Entry(self.ventana_eliminar_menu, width=30)
        self.txt_nombre_eliminar_menu.grid(row=0, column=1, padx=10, pady=10)
        
        # Botón para eliminar el menú
        btn_eliminar = ttk.Button(self.ventana_eliminar_menu, text="Eliminar", command=self.confirmar_eliminar_menu)
        btn_eliminar.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
        
    def confirmar_eliminar_menu(self):
        # Obtener el nombre del menú a eliminar
        nombre = self.txt_nombre_eliminar_menu.get()
        
        if nombre:
            try:
                # Conectar a la base de datos
                self.conexion = mysql.connector.connect(
                    host="127.0.0.1",
                    user="root",
                    password="",
                    database="lasuertedelaolla",
                    port=3306
                )
                
                cursor = self.conexion.cursor()
                
                # Eliminar el menú de la base de datos
                query = "DELETE FROM menus_especiales WHERE nombre = %s"
                cursor.execute(query, (nombre,))
                
                self.conexion.commit()
                # Guardar el mensaje en la tabla de registros
                mensaje = "Menú eliminado exitosamente."
                query_registro = "INSERT INTO registros (mensaje) VALUES (%s)"
                cursor.execute(query_registro, (mensaje,))
                self.conexion.commit()

                cursor.close()
                self.conexion.close()
                
                
                messagebox.showinfo("Eliminar Menú", "Menú eliminado exitosamente.")
                self.ventana_eliminar_menu.destroy()
                
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Error al conectar a la base de datos: {e}")
        else:
            messagebox.showwarning("Advertencia", "El campo de nombre es obligatorio.")

    def cargar_menus(self):
        try:
            # Conectar a la base de datos
            self.conexion = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="",
                database="lasuertedelaolla",
                port=3306
            )

            cursor = self.conexion.cursor()
            
            # Obtener todos los menús especiales de la base de datos
            query = "SELECT * FROM menus_especiales"
            cursor.execute(query)
            menus = cursor.fetchall()
            
            # Limpiar el Treeview
            for item in self.tree_lista_menus.get_children():
                self.tree_lista_menus.delete(item)
            
            # Insertar los menús en el Treeview
            for menu in menus:
                self.tree_lista_menus.insert("", "end", values=menu)
            
            cursor.close()
            self.conexion.close()

        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Error al conectar a la base de datos: {e}")

    def buscar_menus(self):
        termino_busqueda = self.txt_busqueda_menus.get().strip()
        if termino_busqueda:
            try:
                self.conexion = mysql.connector.connect(
                    host="127.0.0.1",
                    user="root",
                    password="",
                    database="lasuertedelaolla",
                    port=3306
                )

                cursor = self.conexion.cursor()
                query = """
                SELECT id, nombre, descripcion, fecha_inicio, fecha_fin
                FROM menus_especiales
                WHERE id LIKE %s OR nombre LIKE %s OR descripcion LIKE %s OR fecha_inicio LIKE %s OR fecha_fin LIKE %s 
                """
                cursor.execute(query, ("%"+termino_busqueda+"%", "%"+termino_busqueda+"%", "%"+termino_busqueda+"%", "%"+termino_busqueda+"%", "%"+termino_busqueda+"%"))
                menus = cursor.fetchall()

                cursor.close()
                self.conexion.close()

                for item in self.tree_lista_menus.get_children():
                    self.tree_lista_menus.delete(item)

                for menu in menus:
                    self.tree_lista_menus.insert("", "end", values=menu)

            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Error al conectar a la base de datos: {e}")
        else:
            self.cargar_menus()

    #------------------------------------------------------------
    #REPORTES
    def ventana_reportes(self):
        self.frame_lista_reportes = Frame(self.frame_center)
        self.frame_lista_reportes.grid(row=0, column=0, columnspan=2, padx=15, pady=15, sticky=NSEW)

        # Configuración del árbol o lista para mostrar los reportes (usando un Treeview)
        columnas = ("ID", "mensaje", "fecha")

        self.tree_reportes = ttk.Treeview(self.frame_lista_reportes, columns=columnas, show="headings")
        self.tree_reportes.pack(fill=BOTH, expand=True)

        # Configurar las columnas del Treeview
        for col in columnas:
            self.tree_reportes.heading(col, text=col)
            self.tree_reportes.column(col, width=150)

                # Crear el scrollbar
        tree_scroll_reportes= tb.Scrollbar(self.tree_reportes, bootstyle='round-dark', orient=VERTICAL, command=self.tree_reportes.yview)
        tree_scroll_reportes.grid(row=0, column=1, sticky=NSEW)

        # Configuración del scroll
        self.tree_reportes.config(yscrollcommand=tree_scroll_reportes.set)

        # Configuración de la expansión de columnas para utilizar todo el ancho disponible
        self.tree_reportes.columnconfigure(0, weight=2)  # Ajustar el tamaño del Treeview
        # Cargar los reportes desde la base de datos
        self.cargar_reportes()

    def cargar_reportes(self):
        try:
            # Conectar a la base de datos
            self.conexion = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="",
                database="lasuertedelaolla",
                port=3306
            )

            cursor = self.conexion.cursor()
            
            # Obtener todos los reportes de la base de datos
            query = "SELECT * FROM registros"
            cursor.execute(query)
            reportes = cursor.fetchall()
            
            # Limpiar el Treeview de reportes
            for item in self.tree_reportes.get_children():
                self.tree_reportes.delete(item)
            
            # Insertar los reportes en el Treeview
            for reporte in reportes:
                self.tree_reportes.insert("", "end", values=reporte)
            
            cursor.close()
            self.conexion.close()

        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Error al conectar a la base de datos: {e}")

    
    #--------------------------------------------------------------
    #CAJA REGISTRADORA
    def mostrar_caja_registradora(self):
        caja_registradora = Toplevel(self)
        CajaRegistradoraFrame(caja_registradora, self.db).pack(fill='both', expand=True)
        self.state('zoomed')
        # Centrando la ventana en la pantalla
        self.center_window()

    #--------------------------------------------------------------
    #CLIENTES

    def mostrar_clientes(self):
        self.frame_lista_clientes = Frame(self.frame_center)
        self.frame_lista_clientes.grid(row=0, column=0, columnspan=2, padx=15, pady=15, sticky=NSEW)

        self.lblframe_botones_cliente = LabelFrame(self.frame_lista_clientes)
        self.lblframe_botones_cliente.grid(row=0, column=0, padx=15, pady=15, sticky=NSEW)

        # Panel de botones para agregar, modificar y eliminar clientes
        btn_nuevo_cliente = tb.Button(self.lblframe_botones_cliente, text="Nuevo Cliente", width=20, bootstyle="success", command=self.agregar_cliente)
        btn_nuevo_cliente.grid(row=0, column=0, padx=10, pady=10)
        btn_modificar_cliente = tb.Button(self.lblframe_botones_cliente, text="Modificar", width=20, bootstyle="info", command=self.editar_cliente)
        btn_modificar_cliente.grid(row=0, column=1, padx=10, pady=10)
        btn_eliminar_cliente = tb.Button(self.lblframe_botones_cliente, text="Eliminar", width=20, bootstyle="danger", command=self.eliminar_cliente)
        btn_eliminar_cliente.grid(row=0, column=2, padx=10, pady=10)

        # Búsqueda de clientes existentes
        self.lblframe_busqueda_clientes = LabelFrame(self.frame_lista_clientes,  text="Buscar Clientes")
        self.lblframe_busqueda_clientes.grid(row=1, column=0, padx=15, pady=15, sticky=NSEW)

        # Barra de búsqueda de clientes, donde se puede ingresar el nombre del cliente
        self.txt_busqueda_clientes = ttk.Entry(self.lblframe_busqueda_clientes, width=150)
        self.txt_busqueda_clientes.grid(row=0, column=0, padx=10, pady=10, sticky=W)

        
        btn_buscar_clientes = tb.Button(self.lblframe_busqueda_clientes, text="🔍", width=3, command=self.buscar_clientes)
        btn_buscar_clientes.grid(row=0, column=1, padx=(0, 10), pady=10)

        # Vista de árbol para mostrar la lista de clientes
        self.lblframe_tree_clientes = LabelFrame(self.frame_lista_clientes)
        self.lblframe_tree_clientes.grid(row=2, column=0, sticky=NSEW)

        # Definición de las columnas manualmente acorde a la tabla de clientes
        columnas = ("id", "nombre", "correo", "telefono")
        total_width = self.lblframe_tree_clientes.winfo_width()  # Ancho disponible en el contenedor

        # Distribuimos el ancho disponible entre las columnas
        column_widths = {
            "id": int(total_width * 0.1),
            "nombre": int(total_width * 0.3),
            "correo": int(total_width * 0.3),
            "telefono": int(total_width * 0.3)
        }

        self.tree_lista_clientes = tb.Treeview(self.lblframe_tree_clientes, columns=columnas, height=75, show="headings", bootstyle="dark")
        self.tree_lista_clientes.grid(row=0, column=0, sticky=NSEW)

        # Títulos de cada una de las columnas
        self.tree_lista_clientes.heading("id", text="Id", anchor=W)
        self.tree_lista_clientes.heading("nombre", text="Nombre", anchor=W)
        self.tree_lista_clientes.heading("correo", text="Correo", anchor=W)
        self.tree_lista_clientes.heading("telefono", text="Teléfono", anchor=W)

        self.tree_lista_clientes['displaycolumns'] = ("id", "nombre", "correo", "telefono")

        # Configurar el ancho de cada columna
        for col, width in column_widths.items():
            self.tree_lista_clientes.column(col, width=width, minwidth=50)

        # Crear el scroll
        tree_scroll_clientes = tb.Scrollbar(self.lblframe_tree_clientes, bootstyle='round-dark', orient=VERTICAL, command=self.tree_lista_clientes.yview)
        tree_scroll_clientes.grid(row=0, column=1, sticky=NSEW)

        # Configuración del scroll
        self.tree_lista_clientes.config(yscrollcommand=tree_scroll_clientes.set)

        # Configuración de la expansión de columnas para utilizar todo el ancho disponible
        self.lblframe_tree_clientes.columnconfigure(0, weight=1)

        # Cargar los clientes
        self.cargar_clientes()

    def agregar_cliente(self):

        # Crear una nueva ventana para ingresar los datos del nuevo usuario
        self.ventana_nuevo_cliente = Toplevel(self)
        self.ventana_nuevo_cliente.title("Nuevo cliente")
  
 
        lbl_nombre = tk.Label(self.ventana_nuevo_cliente, text="Nombre:")
        lbl_nombre.pack(pady=5)
        self.entry_nombre = tk.Entry(self.ventana_nuevo_cliente)
        self.entry_nombre.pack(pady=5)

        lbl_correo = tk.Label(self.ventana_nuevo_cliente, text="Correo:")
        lbl_correo.pack(pady=5)
        self.entry_correo = tk.Entry(self.ventana_nuevo_cliente)
        self.entry_correo.pack(pady=5)

        lbl_telefono = tk.Label(self.ventana_nuevo_cliente, text="Teléfono:")
        lbl_telefono.pack(pady=5)
        self.entry_telefono = tk.Entry(self.ventana_nuevo_cliente)
        self.entry_telefono.pack(pady=5)

        btn_guardar = ttk.Button(self.ventana_nuevo_cliente, text="Guardar", command=self.guardar_cliente)
        btn_guardar.pack(pady=10)

    def guardar_cliente(self):
        
        nombre = self.entry_nombre.get()
        correo = self.entry_correo.get()
        telefono = self.entry_telefono.get()

         # Validar que todos los campos estén completos
        if  nombre and correo and telefono:
            try:
                # Conectar a la base de datos
                self.conexion = mysql.connector.connect(
                    host="127.0.0.1",
                    user="root",
                    password="",
                    database="lasuertedelaolla",
                    port=3306
                )
                
                cursor = self.conexion.cursor()
                
                # Insertar el nuevo cliente en la base de datos
                query = "INSERT INTO cliente (nombre, correo, telefono) VALUES (%s, %s, %s)"
                cursor.execute(query, (nombre, correo, telefono))
                
                self.conexion.commit()

                # Guardar el mensaje en la tabla de registros
                mensaje = "Cliente agregado exitosamente."
                query_registro = "INSERT INTO registros (mensaje) VALUES (%s)"
                cursor.execute(query_registro, (mensaje,))
                self.conexion.commit()

                cursor.close()
                self.conexion.close()
                

                # Mostrar mensaje de éxito
                messagebox.showinfo("Nuevo Cliente", mensaje)
                # Cerrar la ventana de nuevo cliente
                self.ventana_nuevo_cliente.destroy()
                
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Error al conectar a la base de datos: {e}")
        else:
            # Mostrar mensaje de advertencia si no se completaron todos los campos
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")

    def editar_cliente(self):
        selected_item = self.tree_lista_clientes.selection()
        if selected_item:
            item = self.tree_lista_clientes.item(selected_item)
            values = item['values']

            self.ventana_editar_clientes = Toplevel(self)
            self.ventana_editar_clientes.title("Editar Cliente")

            lbl_nombre = tk.Label(self.ventana_editar_clientes, text="Nombre:")
            lbl_nombre.pack(pady=5)
            self.entry_nombre_editar = tk.Entry(self.ventana_editar_clientes)
            self.entry_nombre_editar.pack(pady=5)
            self.entry_nombre_editar.insert(0, values[1])

            lbl_correo = tk.Label(self.ventana_editar_clientes, text="Correo:")
            lbl_correo.pack(pady=5)
            self.entry_correo_editar = tk.Entry(self.ventana_editar_clientes)
            self.entry_correo_editar.pack(pady=5)
            self.entry_correo_editar.insert(0, values[2])

            lbl_telefono = tk.Label(self.ventana_editar_clientes, text="Teléfono:")
            lbl_telefono.pack(pady=5)
            self.entry_telefono_editar = tk.Entry(self.ventana_editar_clientes)
            self.entry_telefono_editar.pack(pady=5)
            self.entry_telefono_editar.insert(0, values[3])

            btn_guardar = ttk.Button(self.ventana_editar_clientes, text="Guardar",  command=lambda: self.guardar_cambios_cliente(selected_item, values[0]))
            btn_guardar.pack(pady=10)
        else:
            messagebox.showwarning("Advertencia", "Seleccione un cliente para editar")

    def guardar_cambios_cliente(self, selected_item, cliente_id):
        nombre = self.entry_nombre_editar.get()
        correo = self.entry_correo_editar.get()
        telefono = self.entry_telefono_editar.get()

        if nombre and correo and telefono:
            try:
                self.conexion = mysql.connector.connect(
                    host="127.0.0.1",
                    user="root",
                    password="",
                    database="lasuertedelaolla",
                    port=3306
                )
                
                cursor = self.conexion.cursor()
                query = "UPDATE cliente SET nombre=%s, correo=%s, telefono=%s WHERE id=%s"
                cursor.execute(query, (nombre, correo, telefono, cliente_id))
                
                self.conexion.commit()
                
                # Guardar el mensaje en la tabla de registros
                mensaje = "Cliente actualizado exitosamente."
                query_registro = "INSERT INTO registros (mensaje) VALUES (%s)"
                cursor.execute(query_registro, (mensaje,))
                self.conexion.commit()

                cursor.close()
                self.conexion.close()

                
                messagebox.showinfo("Cliente", "Cliente editado exitosamente.")
                self.tree_lista_clientes.item(selected_item, values=(cliente_id, nombre, correo, telefono))
                
                self.cargar_clientes()


                self.ventana_editar_clientes.destroy()
                
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Error al conectar a la base de datos: {e}")
        else:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")

    def eliminar_cliente(self):
        selected_item = self.tree_lista_clientes.selection()
        if selected_item:
            if messagebox.askyesno("Confirmar Eliminación", "¿Está seguro de eliminar el cliente seleccionado?"):
                item = self.tree_lista_clientes.item(selected_item)
                cliente_id = item['values'][0]
                self.eliminar_cliente_bd(cliente_id)
                self.tree_lista_clientes.delete(selected_item)
        else:
            messagebox.showwarning("Advertencia", "Seleccione un cliente para eliminar")

    def eliminar_cliente_bd(self, cliente_id):
        if cliente_id:
            try:
                self.conexion = mysql.connector.connect(
                    host="127.0.0.1",
                    user="root",
                    password="",
                    database="lasuertedelaolla",
                    port=3306
                )
                
                cursor = self.conexion.cursor()
                query = "DELETE FROM cliente WHERE id = %s"
                cursor.execute(query, (cliente_id,))
                
                self.conexion.commit()
                # Guardar el mensaje en la tabla de registros
                mensaje = "Cliente eliminado exitosamente."
                query_registro = "INSERT INTO registros (mensaje) VALUES (%s)"
                cursor.execute(query_registro, (mensaje,))
                self.conexion.commit()

                cursor.close()
                self.conexion.close()
                    
                messagebox.showinfo("Cliente eliminado", "Cliente eliminado exitosamente.")
                
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Error al conectar a la base de datos: {e}")
        else:
            messagebox.showwarning("Advertencia", "No se ha podido identificar el cliente a eliminar.")

    def cargar_clientes(self):
                # Conectar a la base de datos MySQL
        try:
            conexion = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="",
                database="lasuertedelaolla",
                port=3306
            )
            cursor = conexion.cursor()
            cursor.execute("SELECT id, nombre, correo, telefono FROM cliente")

            # Limpiar el Treeview
            for row in self.tree_lista_clientes.get_children():
                self.tree_lista_clientes.delete(row)

            # Insertar los datos en el Treeview
            for (id, nombre,correo,telefono) in cursor:
                self.tree_lista_clientes.insert("", "end", values=(id, nombre, correo, telefono))

            cursor.close()
            conexion.close()
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def buscar_clientes(self):
        termino_busqueda = self.txt_busqueda_clientes.get().strip()
        if termino_busqueda:
            try:
                self.conexion = mysql.connector.connect(
                    host="127.0.0.1",
                    user="root",
                    password="",
                    database="lasuertedelaolla",
                    port=3306
                )

                cursor = self.conexion.cursor()
                query = """
                SELECT id, nombre, correo, telefono
                FROM cliente
                WHERE id LIKE %s OR nombre LIKE %s OR correo LIKE %s OR telefono LIKE %s 
                """
                cursor.execute(query, ("%"+termino_busqueda+"%", "%"+termino_busqueda+"%", "%"+termino_busqueda+"%", "%"+termino_busqueda+"%"))
                clientes = cursor.fetchall()

                cursor.close()
                self.conexion.close()

                for item in self.tree_lista_clientes.get_children():
                    self.tree_lista_clientes.delete(item)

                for cliente in clientes:
                    self.tree_lista_clientes.insert("", "end", values=cliente)

            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Error al conectar a la base de datos: {e}")
        else:
            self.cargar_clientes()



    #-------------------------------------------------------------------------------
    #INVENTARIO

    def obtener_inventario_bd(self):
        try:
            # Conectar a la base de datos
            conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="lasuertedelaolla",
            port=3306
            )
            
            cursor = conexion.cursor()
            query = "SELECT nombre, cantidad_disponible, precio FROM producto"
            cursor.execute(query)
            inventario = cursor.fetchall()
            cursor.close()
            conexion.close()
            return inventario
        except mysql.connector.Error as e:
            messagebox.showerror("Error al obtener inventario", f"No se pudo obtener el inventario: {e}")
            return []

    def mostrar_inventario(self):
        inventario = self.obtener_inventario_bd()
        
        # Limpiar el Treeview antes de poblarlo
        for item in self.tree_inventario.get_children():
            self.tree_inventario.delete(item)
        
        # Insertar cada producto en el Treeview
        for producto in inventario:
            self.tree_inventario.insert("", "end", values=producto)

    #-------------------------------------------------------------------------------
    #USUARIOS
    def ventana_lista_usuarios(self):
        self.frame_lista_usuarios = Frame(self.frame_center)
        self.frame_lista_usuarios.grid(row=0, column=0, columnspan=2, padx=15, pady=15, sticky=NSEW)

        self.lblframe_botones_usuarios = LabelFrame(self.frame_lista_usuarios)
        self.lblframe_botones_usuarios.grid(row=0, column=0, padx=15, pady=15, sticky=NSEW)

        # Botones para nuevo, modificar y eliminar usuarios
        btn_nuevo_usuario = tb.Button(self.lblframe_botones_usuarios, text="Nuevo", width=20, bootstyle="success", command=self.nuevo_usuario)
        btn_nuevo_usuario.grid(row=0, column=0, padx=10, pady=10)
        
        btn_modificar_usuario = ttk.Button(self.lblframe_botones_usuarios, text="Modificar", width=20, command=self.modificar_usuario)
        btn_modificar_usuario.grid(row=0, column=1, padx=10, pady=10)
        
        btn_eliminar_usuario = tb.Button(self.lblframe_botones_usuarios, text="Eliminar", width=20, bootstyle="danger", command=self.eliminar_usuario)
        btn_eliminar_usuario.grid(row=0, column=2, padx=10, pady=10)

        # Búsqueda de usuarios existentes
        self.lblframe_busqueda_usuarios = LabelFrame(self.frame_lista_usuarios,  text="Buscar Usuarios")
        self.lblframe_busqueda_usuarios.grid(row=1, column=0, padx=15, pady=15, sticky=NSEW)

        self.txt_busqueda_usuarios = ttk.Entry(self.lblframe_busqueda_usuarios, width=150)
        self.txt_busqueda_usuarios.grid(row=0, column=0, padx=(10,0), pady=10, sticky=W)

        
        btn_buscar_usuarios = tb.Button(self.lblframe_busqueda_usuarios, text="🔍", width=3, command=self.buscar_usuarios)
        btn_buscar_usuarios.grid(row=0, column=1, padx=(0, 10), pady=10)

        # Vista de árbol para mostrar la lista de usuarios
        self.lblframe_tree_usuarios = LabelFrame(self.frame_lista_usuarios)
        self.lblframe_tree_usuarios.grid(row=2, column=0, sticky=NSEW)

        # Definición de las columnas manualmente acorde a la tabla de usuarios
        columnas = ("id", "nombre", "rol", "correo", "contraseña")

        # Calculamos el ancho total disponible para las columnas
        total_width = self.lblframe_tree_usuarios.winfo_width()  # Ancho disponible en el contenedor

        # Distribuimos el ancho disponible entre las columnas
        column_widths = {
            "id": int(total_width * 0.1),       
            "nombre": int(total_width * 0.2),    
            "rol": int(total_width * 0.15),      
            "correo": int(total_width * 0.3),    
            "contraseña": int(total_width * 0.25) 
        }

        self.tree_lista_usuarios = tb.Treeview(self.lblframe_tree_usuarios, columns=columnas, height=45, show="headings", bootstyle="dark")
        self.tree_lista_usuarios.grid(row=0, column=0, sticky=NSEW)

        # Títulos de cada una de las columnas
        self.tree_lista_usuarios.heading("id", text="Id", anchor=W)
        self.tree_lista_usuarios.heading("nombre", text="Nombre", anchor=W)
        self.tree_lista_usuarios.heading("rol", text="Rol", anchor=W)
        self.tree_lista_usuarios.heading("correo", text="Correo", anchor=W)
        self.tree_lista_usuarios.heading("contraseña", text="Contraseña", anchor=W)

        self.tree_lista_usuarios['displaycolumns'] = ("id", "nombre", "rol", "correo")  # Ocultar la columna de la contraseña

        # Configurar el ancho de cada columna
        for col, width in column_widths.items():
            self.tree_lista_usuarios.column(col, width=width, minwidth=50)  # Mantener el ancho mínimo

        # Crear el scrollbar
        tree_scroll_usuarios = tb.Scrollbar(self.lblframe_tree_usuarios, bootstyle='round-dark', orient=VERTICAL, command=self.tree_lista_usuarios.yview)
        tree_scroll_usuarios.grid(row=0, column=1, sticky=NSEW)

        # Configuración del scroll
        self.tree_lista_usuarios.config(yscrollcommand=tree_scroll_usuarios.set)

        # Configuración de la expansión de columnas para utilizar todo el ancho disponible
        self.lblframe_tree_usuarios.columnconfigure(0, weight=1)  # Ajustar el tamaño del Treeview

        # Cargar los usuarios
        self.cargar_usuarios()

    def nuevo_usuario(self):
        # Crear una nueva ventana para ingresar los datos del nuevo usuario
        self.ventana_nuevo_usuario = Toplevel(self)
        self.ventana_nuevo_usuario.title("Nuevo Usuario")
        
        # Crear los campos para ingresar los datos del nuevo usuario
        lbl_nombre = tk.Label(self.ventana_nuevo_usuario, text="Nombre:")
        lbl_nombre.grid(row=0, column=0, padx=10, pady=10)

        self.txt_nombre = tk.Entry(self.ventana_nuevo_usuario, width=30)
        self.txt_nombre.grid(row=0, column=1, padx=10, pady=10)
        
        lbl_contraseña = tk.Label(self.ventana_nuevo_usuario, text="Contraseña:")
        lbl_contraseña.grid(row=1, column=0, padx=10, pady=10)

        self.txt_contraseña = tk.Entry(self.ventana_nuevo_usuario, show="*", width=30)
        self.txt_contraseña.grid(row=1, column=1, padx=10, pady=10)

        lbl_rol = tk.Label(self.ventana_nuevo_usuario, text="Rol:")
        lbl_rol.grid(row=2, column=0, padx=10, pady=10)

        self.txt_rol = tk.Entry(self.ventana_nuevo_usuario, width=30)
        self.txt_rol.grid(row=2, column=1, padx=10, pady=10)

        lbl_correo = tk.Label(self.ventana_nuevo_usuario, text="Correo:")
        lbl_correo.grid(row=3, column=0, padx=10, pady=10)

        self.txt_correo = tk.Entry(self.ventana_nuevo_usuario, width=30)
        self.txt_correo.grid(row=3, column=1, padx=10, pady=10)
        
        # Botón para guardar el nuevo usuario
        btn_guardar = ttk.Button(self.ventana_nuevo_usuario, text="Guardar", command=self.guardar_nuevo_usuario)
        btn_guardar.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    def guardar_nuevo_usuario(self):
        # Obtener los valores de los campos
        nombre = self.txt_nombre.get()
        contraseña = self.txt_contraseña.get()
        rol = self.txt_rol.get()
        correo = self.txt_correo.get()
        
        # Validar que todos los campos estén completos
        if nombre and contraseña and rol and correo:
            try:
                # Conectar a la base de datos
                conexion = mysql.connector.connect(
                    host="127.0.0.1",
                    user="root",
                    password="",
                    database="lasuertedelaolla",
                    port=3306
                )
                
                cursor = conexion.cursor()
                
                # Insertar el nuevo usuario en la base de datos
                query = "INSERT INTO usuario (nombre, contraseña, rol, correo) VALUES (%s, %s, %s, %s)"
                cursor.execute(query, (nombre, contraseña, rol, correo))
                
                conexion.commit()
                # Guardar el mensaje en la tabla de registros
                mensaje = "Usuario agregado exitosamente."
                query_registro = "INSERT INTO registros (mensaje) VALUES (%s)"
                cursor.execute(query_registro, (mensaje,))
                conexion.commit()

                cursor.close()
                conexion.close()

                # Mostrar mensaje de éxito
                messagebox.showinfo("Nuevo Usuario", "Usuario creado exitosamente.")
                
                self.cargar_usuarios()
                # Cerrar la ventana de nuevo usuario
                self.ventana_nuevo_usuario.destroy()
                
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Error al conectar a la base de datos: {e}")
        else:
            # Mostrar mensaje de advertencia si no se completaron todos los campos
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")

    def modificar_usuario(self):
        # Crear una nueva ventana para seleccionar el usuario a modificar
        self.ventana_modificar = Toplevel(self)
        self.ventana_modificar.title("Modificar Usuario")
        
        # Etiqueta y campo de entrada para seleccionar el usuario por su nombre
        lbl_nombre = Label(self.ventana_modificar, text="Nombre del usuario:")
        lbl_nombre.grid(row=0, column=0, padx=10, pady=10)
        self.txt_nombre_modificar = Entry(self.ventana_modificar, width=30)
        self.txt_nombre_modificar.grid(row=0, column=1, padx=10, pady=10)
        
        # Botón para buscar el usuario
        btn_buscar = ttk.Button(self.ventana_modificar, text="Buscar", command=self.buscar_usuario_modificar)
        btn_buscar.grid(row=0, column=2, padx=10, pady=10)
        
        # Campos de entrada para modificar los datos del usuario
        lbl_nombre_nuevo = Label(self.ventana_modificar, text="Nuevo nombre:")
        lbl_nombre_nuevo.grid(row=1, column=0, padx=10, pady=10)
        self.txt_nombre_nuevo = Entry(self.ventana_modificar, width=30)
        self.txt_nombre_nuevo.grid(row=1, column=1, padx=10, pady=10)
        
        lbl_contraseña_nueva = Label(self.ventana_modificar, text="Nueva contraseña:")
        lbl_contraseña_nueva.grid(row=2, column=0, padx=10, pady=10)
        self.txt_contraseña_nueva = Entry(self.ventana_modificar, show="*", width=30)
        self.txt_contraseña_nueva.grid(row=2, column=1, padx=10, pady=10)

                
        lbl_rol_nueva = Label(self.ventana_modificar, text="Nuevo rol:")
        lbl_rol_nueva.grid(row=3, column=0, padx=10, pady=10)
        self.txt_rol_nueva = Entry(self.ventana_modificar, width=30)
        self.txt_rol_nueva.grid(row=3, column=1, padx=10, pady=10)


                
        lbl_correo_nueva = Label(self.ventana_modificar, text="Nueva correo:")
        lbl_correo_nueva.grid(row=4, column=0, padx=10, pady=10)
        self.txt_correo_nueva = Entry(self.ventana_modificar, width=30)
        self.txt_correo_nueva.grid(row=4, column=1, padx=10, pady=10)
        
        # Botón para guardar los cambios
        btn_guardar = ttk.Button(self.ventana_modificar, text="Guardar cambios", command=self.guardar_modificacion_usuario)
        btn_guardar.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    def buscar_usuario_modificar(self):
        # Obtener el nombre del usuario a modificar desde la entrada
        nombre_usuario = self.txt_nombre_modificar.get()
        
        # Validar que el nombre del usuario no esté vacío
        if nombre_usuario:
            try:
                # Conectar a la base de datos
                self.conexion = mysql.connector.connect(
                    host="127.0.0.1",
                    user="root",
                    password="",
                    database="lasuertedelaolla",
                    port=3306
                )
                
                cursor = self.conexion.cursor()
                
                # Consultar el usuario en la base de datos
                query = "SELECT id, nombre,rol,correo, contraseña FROM usuario WHERE nombre = %s"
                cursor.execute(query, (nombre_usuario,))
                
                # Obtener el resultado de la consulta
                usuario = cursor.fetchone()
                
                if usuario:
                    # Mostrar los datos del usuario encontrado en los campos de entrada
                    self.txt_nombre_nuevo.delete(0, END)
                    self.txt_nombre_nuevo.insert(0, usuario[1])  # Nombre
                    self.txt_contraseña_nueva.delete(0, END)
                    self.txt_contraseña_nueva.insert(0, usuario[2])  # Contraseña
                else:
                    messagebox.showwarning("Usuario no encontrado", f"No se encontró ningún usuario con el nombre '{nombre_usuario}'.")
                
                cursor.close()
                self.conexion.close()
                
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Error al conectar a la base de datos: {e}")
        else:
            messagebox.showwarning("Nombre de usuario vacío", "Por favor ingresa el nombre de usuario a modificar.")
            
    def guardar_modificacion_usuario(self):
        # Obtener los valores modificados del usuario desde los campos de entrada
        nombre_nuevo = self.txt_nombre_nuevo.get()
        contraseña_nueva = self.txt_contraseña_nueva.get()
        rol_nuevo=self.txt_rol_nueva.get()
        correo_nuevo=self.txt_correo_nueva.get()
        
        # Obtener el nombre original del usuario desde el campo de búsqueda
        nombre_original = self.txt_nombre_modificar.get()
        
        # Validar que todos los campos estén completos
        if nombre_nuevo and contraseña_nueva and correo_nuevo and rol_nuevo and nombre_original:
            try:
                # Conectar a la base de datos
                self.conexion = mysql.connector.connect(
                    host="127.0.0.1",
                    user="root",
                    password="",
                    database="lasuertedelaolla",
                    port=3306
                )
                
                cursor = self.conexion.cursor()
                
                # Actualizar los datos del usuario en la base de datos
                query = "UPDATE usuario SET nombre = %s, contraseña = %s, rol=%s, correo=%s WHERE nombre = %s"
                cursor.execute(query, (nombre_nuevo, contraseña_nueva,rol_nuevo,correo_nuevo, nombre_original))
                
                self.conexion.commit()
                # Guardar el mensaje en la tabla de registros
                mensaje = "Usuario actualizado exitosamente."
                query_registro = "INSERT INTO registros (mensaje) VALUES (%s)"
                cursor.execute(query_registro, (mensaje,))
                self.conexion.commit()

                cursor.close()
                self.conexion.close()
                
                # Mostrar mensaje de éxito
                messagebox.showinfo("Usuario modificado", "Usuario modificado exitosamente.")
                
                self.cargar_usuarios()
                # Cerrar la ventana de modificar usuario
                self.ventana_modificar.destroy()
                
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Error al conectar a la base de datos: {e}")
        else:
            # Mostrar mensaje de advertencia si no se completaron todos los campos
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")

    def eliminar_usuario(self):
        # Crear una nueva ventana para seleccionar el usuario a eliminar
        self.ventana_eliminar = Toplevel(self)
        self.ventana_eliminar.title("Eliminar Usuario")
        
        # Etiqueta y campo de entrada para seleccionar el usuario por su nombre
        lbl_id = Label(self.ventana_eliminar, text="Id del usuario:")
        lbl_id.grid(row=0, column=0, padx=10, pady=10)
        self.txt_id_eliminar = Entry(self.ventana_eliminar, width=30)
        self.txt_id_eliminar.grid(row=0, column=1, padx=10, pady=10)
        
        # Botón para eliminar el usuario
        btn_eliminar = ttk.Button(self.ventana_eliminar, text="Eliminar", command=self.eliminar_usuario_bd)
        btn_eliminar.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    def eliminar_usuario_bd(self):
        # Obtener el nombre del usuario a eliminar desde la entrada
        id_usuario = self.txt_id_eliminar.get()
        
        # Validar que el nombre del usuario no esté vacío
        if id_usuario:
            try:
                # Conectar a la base de datos
                self.conexion = mysql.connector.connect(
                    host="127.0.0.1",
                    user="root",
                    password="",
                    database="lasuertedelaolla",
                    port=3306
                )
                
                cursor = self.conexion.cursor()
                        
                queries_relaciones = [

                    "DELETE FROM empleado WHERE id_usuario= %s",

                ]

                for query in queries_relaciones:
                    cursor.execute(query, (id_usuario,))

                # Actualizar el id_usuario en la tabla de venta a NULL
                query_actualizar_venta = "UPDATE venta SET id_usuario = NULL WHERE id_usuario = %s"
                cursor.execute(query_actualizar_venta, (id_usuario,))

                # Eliminar el usuario de la tabla usuario
                query1 = "DELETE FROM usuario WHERE id = %s"
                cursor.execute(query1, (id_usuario,))
                self.conexion.commit()

                # Guardar el mensaje en la tabla de registros
                mensaje = "Usuario eliminado exitosamente."
                query_registro = "INSERT INTO registros (mensaje) VALUES (%s)"
                cursor.execute(query_registro, (mensaje,))
                self.conexion.commit()

                cursor.close()
                self.conexion.close()
                
                # Mostrar mensaje de éxito
                messagebox.showinfo("Usuario eliminado", f"Usuario '{id_usuario}' eliminado exitosamente.")
                
                self.cargar_usuarios()
                # Cerrar la ventana de eliminar usuario
                self.ventana_eliminar.destroy()
                
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Error al conectar a la base de datos: {e}")
        else:
            messagebox.showwarning("Nombre de usuario vacío", "Por favor ingresa el nombre de usuario a eliminar.")

    def cargar_usuarios(self):
        # Conectar a la base de datos MySQL
        try:
            conexion = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="",
                database="lasuertedelaolla",
                port=3306
            )
            cursor = conexion.cursor()
            cursor.execute("SELECT id, nombre, rol, correo FROM usuario")

            # Limpiar el Treeview
            for row in self.tree_lista_usuarios.get_children():
                self.tree_lista_usuarios.delete(row)

            # Insertar los datos en el Treeview
            for (id, nombre, rol, correo) in cursor:
                self.tree_lista_usuarios.insert("", "end", values=(id, nombre, rol, correo))

            cursor.close()
            conexion.close()
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def buscar_usuarios(self):
        termino_busqueda = self.txt_busqueda_usuarios.get().strip()
        if termino_busqueda:
            try:
                self.conexion = mysql.connector.connect(
                    host="127.0.0.1",
                    user="root",
                    password="",
                    database="lasuertedelaolla",
                    port=3306
                )

                cursor = self.conexion.cursor()
                query = """
                SELECT id, nombre, rol, correo
                FROM usuario
                WHERE id LIKE %s OR nombre LIKE %s OR rol LIKE %s OR correo LIKE %s 
                """
                cursor.execute(query, ("%"+termino_busqueda+"%", "%"+termino_busqueda+"%", "%"+termino_busqueda+"%", "%"+termino_busqueda+"%"))
                usuarios = cursor.fetchall()

                cursor.close()
                self.conexion.close()

                for item in self.tree_lista_usuarios.get_children():
                    self.tree_lista_usuarios.delete(item)

                for usuario in usuarios:
                    self.tree_lista_usuarios.insert("", "end", values=usuario)

            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Error al conectar a la base de datos: {e}")
        else:
            self.cargar_usuarios()



    #-------------------------------------------------------------------------
    #REDES SOCIALES

    def cargar_redes_sociales(self):
        try:
            self.conexion = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="",
                database="lasuertedelaolla",
                port=3306
            )
            cursor = self.conexion.cursor()
            cursor.execute("SELECT id, plataforma, enlace, imagen_path FROM redes_sociales")
            redes = cursor.fetchall()
            
            self.redes_sociales = []  # Inicializa la lista de redes sociales

            for red in redes:
                img_path = red[3]
                if img_path and os.path.exists(img_path):
                    img = Image.open(img_path)
                    img = img.resize((50, 50), Image.LANCZOS)
                    img_red = ImageTk.PhotoImage(img)
                else:
                    img_red = None

                self.redes_sociales.append({
                    "id": red[0],
                    "name": red[1],
                    "url": red[2],
                    "image": img_red,
                    "image_path": img_path
                })
            
            self.mostrar_redes_sociales()
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Error al conectar a la base de datos: {e}")

    def mostrar_redes_sociales(self):
        

        for widget in self.frame_center.winfo_children():
            widget.destroy()

        self.ventana_redes = Frame(self.frame_center)
        self.ventana_redes.grid(row=1, column=0, pady=10)

        for idx, red in enumerate(self.redes_sociales):
            frame_red = Frame(self.ventana_redes)
            frame_red.pack(side="left", padx=10, pady=10)

            lbl_red = Label(frame_red, image=red["image"], cursor="hand2")
            lbl_red.pack()

            btn_eliminar = Label(frame_red, text="X", fg="red", cursor="hand2")
            btn_eliminar.pack()
            btn_eliminar.bind("<Button-1>", lambda e, idx=idx: self.eliminar_red_social(idx))

            lbl_red.bind("<Button-1>", lambda e, url=red["url"]: webbrowser.open_new(url))

        if len(self.redes_sociales) < self.max_redes:
            btn_agregar = Label(self.ventana_redes, text="+", fg="blue", cursor="hand2")
            btn_agregar.pack(side="left", padx=10, pady=10)
            btn_agregar.bind("<Button-1>", lambda e: self.agregar_red_social())

    def agregar_red_social(self):
        nombre_red = simpledialog.askstring("Agregar red social", "Nombre de la red social:")
        if not nombre_red:
            return
        url_red = simpledialog.askstring("Agregar red social", "URL de la red social:")
        if not url_red:
            return

        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
        if not file_path:
            return

        try:
            img_red = Image.open(file_path).resize((50, 50), Image.LANCZOS)
            os.makedirs("images", exist_ok=True)
            img_save_path = f"images/{nombre_red}.png"
            img_red.save(img_save_path, format='PNG')
            img_red = ImageTk.PhotoImage(img_red)
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar la imagen: {e}")
            return

        try:
            self.conexion = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="",
                database="lasuertedelaolla",
                port=3306
            )
            cursor = self.conexion.cursor()
            
            query = "INSERT INTO redes_sociales (plataforma, enlace, imagen_path) VALUES (%s, %s, %s)"
            cursor.execute(query, (nombre_red, url_red, img_save_path))
            
            self.conexion.commit()
            
            red_id = cursor.lastrowid
            self.redes_sociales.append({"id": red_id, "name": nombre_red, "url": url_red, "image": img_red, "image_path": img_save_path})
            
            cursor.close()

            self.mostrar_redes_sociales()
            messagebox.showinfo("Agregar Red Social", "Red social agregada exitosamente.")
        
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Error al conectar a la base de datos: {e}")

    def eliminar_red_social(self, idx):
        red_id = self.redes_sociales[idx]["id"]
        img_path = self.redes_sociales[idx]["image_path"]

        try:
            self.conexion = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="",
                database="lasuertedelaolla",
                port=3306
            )
            cursor = self.conexion.cursor()
            
            query = "DELETE FROM redes_sociales WHERE id = %s"
            cursor.execute(query, (red_id,))
            
            self.conexion.commit()
            
            del self.redes_sociales[idx]
            cursor.close()

            if img_path and os.path.exists(img_path):
                os.remove(img_path)

            self.mostrar_redes_sociales()
            messagebox.showinfo("Eliminar Red Social", "Red social eliminada exitosamente.")
        
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Error al conectar a la base de datos: {e}")


    #-------------------------------------------------------------------------
    #PRODUCTOS
    def ventana_lista_productos(self):
        self.frame_lista_productos = Frame(self.frame_center)
        self.frame_lista_productos.grid(row=0, column=0, columnspan=2, padx=15, pady=15, sticky=NSEW)

        self.lblframe_botones_productos = LabelFrame(self.frame_lista_productos)
        self.lblframe_botones_productos.grid(row=0, column=0, padx=15, pady=15, sticky=NSEW)

        # Botones para nuevo, modificar y eliminar productos
        btn_nuevo_producto = tb.Button(self.lblframe_botones_productos, text="Nuevo", width=20, bootstyle="success", command=self.agregar_producto)
        btn_nuevo_producto.grid(row=0, column=0, padx=10, pady=10)
        
        btn_modificar_producto = ttk.Button(self.lblframe_botones_productos, text="Modificar", width=20, command=self.modificar_producto)
        btn_modificar_producto.grid(row=0, column=1, padx=10, pady=10)
        
        btn_eliminar_producto = tb.Button(self.lblframe_botones_productos, text="Eliminar", width=20, bootstyle="danger", command=self.eliminar_producto)
        btn_eliminar_producto.grid(row=0, column=2, padx=10, pady=10)

        # Búsqueda de productos existentes
        self.lblframe_busqueda_productos = LabelFrame(self.frame_lista_productos,  text="Buscar Productos")
        self.lblframe_busqueda_productos.grid(row=1, column=0, padx=15, pady=15, sticky=NSEW)

        self.txt_busqueda_productos = ttk.Entry(self.lblframe_busqueda_productos, width=150)
        self.txt_busqueda_productos.grid(row=0, column=0, padx=(10,0), pady=10)

        btn_buscar_productos = tb.Button(self.lblframe_busqueda_productos, text="🔍", width=3, command=self.buscar_productos)
        btn_buscar_productos.grid(row=0, column=1, padx=(0, 10), pady=10)

        # Vista de árbol para mostrar la lista de productos
        self.lblframe_tree_productos = LabelFrame(self.frame_lista_productos)
        self.lblframe_tree_productos.grid(row=2, column=0, sticky=NSEW)

        
        columnas = ("id", "nombre", "descripcion", "precio", "cantidad_disponible", "promocion", "descuento_promocion")

        
        total_width = self.lblframe_tree_productos.winfo_width()  # Ancho disponible en el contenedor

        
        column_widths = {
            "id": int(total_width * 0.05),                  
            "nombre": int(total_width * 0.15),              
            "descripcion": int(total_width * 0.35),        
            "precio": int(total_width * 0.1),              
            "cantidad_disponible": int(total_width * 0.1),  
            "promocion": int(total_width * 0.1),          
            "descuento_promocion": int(total_width * 0.15) 
        }

        self.tree_lista_productos = tb.Treeview(self.lblframe_tree_productos, columns=columnas, height=45, show="headings", bootstyle="dark")
        self.tree_lista_productos.grid(row=0, column=0, padx=15, sticky=NSEW)

        # Títulos de cada una de las columnas
        self.tree_lista_productos.heading("id", text="Id", anchor=W)
        self.tree_lista_productos.heading("nombre", text="Nombre", anchor=W)
        self.tree_lista_productos.heading("descripcion", text="Descripción", anchor=W)
        self.tree_lista_productos.heading("precio", text="Precio", anchor=W)
        self.tree_lista_productos.heading("cantidad_disponible", text="Cantidad disponible", anchor=W)
        self.tree_lista_productos.heading("promocion", text="Promoción", anchor=W)
        self.tree_lista_productos.heading("descuento_promocion", text="Descuento", anchor=W)

        self.tree_lista_productos['displaycolumns'] = ("id", "nombre", "descripcion", "precio", "cantidad_disponible", "promocion", "descuento_promocion")

        # Configurar el ancho de cada columna
        for col, width in column_widths.items():
            self.tree_lista_productos.column(col, width=width, minwidth=50)  # Mantener el ancho mínimo

        # Crear el scrollbar
        tree_scroll_productos = tb.Scrollbar(self.lblframe_tree_productos, bootstyle='round-dark', orient=VERTICAL, command=self.tree_lista_productos.yview)
        tree_scroll_productos.grid(row=0, column=1, padx=10, pady=5, sticky=NSEW)

        # Configuración del scroll
        self.tree_lista_productos.config(yscrollcommand=tree_scroll_productos.set)

        # Configuración de la expansión de columnas para utilizar todo el ancho disponible
        self.lblframe_tree_productos.columnconfigure(0, weight=1)  # Ajustar el tamaño del Treeview

        # Cargar los productos
        self.cargar_productos()

    def cargar_productos(self):
        # Conectar a la base de datos MySQL
        try:
            conexion = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="",
                database="lasuertedelaolla",
                port=3306
            )
            cursor = conexion.cursor()
            cursor.execute("SELECT id, nombre, descripcion, precio, cantidad_disponible,promocion,descuento_promocion FROM producto")

            # Limpiar el Treeview
            for row in self.tree_lista_productos.get_children():
                self.tree_lista_productos.delete(row)

            # Insertar los datos en el Treeview
            for (id, nombre,descripcion, precio, cantidad_disponible,promocion,descuento_promocion) in cursor:
                self.tree_lista_productos.insert("", "end", values=(id, nombre,descripcion, precio, cantidad_disponible,promocion,descuento_promocion))

            cursor.close()
            conexion.close()
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def agregar_producto(self):
        # Crear una nueva ventana para agregar productos
        self.ventana_agregar_producto = Toplevel(self.master)
        self.ventana_agregar_producto.title("Agregar Producto")
        
        # Campos de entrada para agregar un nuevo producto
        lbl_nombre = Label(self.ventana_agregar_producto, text="Nombre:")
        lbl_nombre.grid(row=0, column=0, padx=10, pady=10)

        self.txt_nombre = Entry(self.ventana_agregar_producto, width=30)
        self.txt_nombre.grid(row=0, column=1, padx=10, pady=10)
        
        lbl_descripcion = Label(self.ventana_agregar_producto, text="Descripción:")
        lbl_descripcion.grid(row=1, column=0, padx=10, pady=10)

        self.txt_descripcion = Entry(self.ventana_agregar_producto, width=30)
        self.txt_descripcion.grid(row=1, column=1, padx=10, pady=10)
        
        lbl_precio = Label(self.ventana_agregar_producto, text="Precio:")
        lbl_precio.grid(row=2, column=0, padx=10, pady=10)
        self.txt_precio = Entry(self.ventana_agregar_producto, width=30)
        self.txt_precio.grid(row=2, column=1, padx=10, pady=10)
        
        lbl_cantidad = Label(self.ventana_agregar_producto, text="Cantidad disponible:")
        lbl_cantidad.grid(row=3, column=0, padx=10, pady=10)

        self.txt_cantidad = Entry(self.ventana_agregar_producto, width=30)
        self.txt_cantidad.grid(row=3, column=1, padx=10, pady=10)
        
        lbl_promocion = Label(self.ventana_agregar_producto, text="Promoción:")
        lbl_promocion.grid(row=4, column=0, padx=10, pady=10)

        self.txt_promocion = Entry(self.ventana_agregar_producto, width=30)
        self.txt_promocion.grid(row=4, column=1, padx=10, pady=10)
        
        lbl_descuento = Label(self.ventana_agregar_producto, text="Descuento promoción:")
        lbl_descuento.grid(row=5, column=0, padx=10, pady=10)

        self.txt_descuento = Entry(self.ventana_agregar_producto, width=30)
        self.txt_descuento.grid(row=5, column=1, padx=10, pady=10)
        
        # Botón para agregar el producto
        btn_agregar = ttk.Button(self.ventana_agregar_producto, text="Agregar", command=self.guardar_producto)
        btn_agregar.grid(row=6, column=0, columnspan=2, padx=10, pady=10)
    
    def guardar_producto(self):
        # Obtener los datos del nuevo producto desde los campos de entrada
        nombre = self.txt_nombre.get()
        descripcion = self.txt_descripcion.get()
        precio = float(self.txt_precio.get())
        cantidad = int(self.txt_cantidad.get())
        promocion = self.txt_promocion.get()
        descuento = float(self.txt_descuento.get())
        
        # Llamar al método para agregar producto
        if self.agregar_producto_bd(nombre, descripcion, precio, cantidad, promocion, descuento):
            messagebox.showinfo("Producto agregado", "El producto se ha agregado correctamente.")
            self.ventana_agregar_producto.destroy()
        else:
            messagebox.showerror("Error", "No se pudo agregar el producto.")
    
    def agregar_producto_bd(self, nombre, descripcion, precio, cantidad, promocion, descuento):
        # Conectar a la base de datos
        self.conexion = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="",
            database="lasuertedelaolla",
            port=3306
        )
        try:
            cursor = self.conexion.cursor()
            
            # Insertar el nuevo producto en la base de datos
            query = "INSERT INTO producto (nombre, descripcion, precio, cantidad_disponible, promocion, descuento_promocion) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (nombre, descripcion, precio, cantidad, promocion, descuento))
            
            self.conexion.commit()

            # Guardar el mensaje en la tabla de registros
            mensaje = "Producto agregado exitosamente."
            query_registro = "INSERT INTO registros (mensaje) VALUES (%s)"
            cursor.execute(query_registro, (mensaje,))
            self.conexion.commit()

            cursor.close()
            self.conexion.close()
            return True
        except mysql.connector.Error as e:
            messagebox.showerror("Error al agregar producto", f"No se pudo agregar el producto: {e}")
            return False
   
    def modificar_producto(self):
        # Crear una nueva ventana para modificar productos
        self.ventana_modificar_producto = Toplevel(self.master)
        self.ventana_modificar_producto.title("Modificar Producto")
        
        # Campos de entrada para modificar un producto existente
        lbl_id = Label(self.ventana_modificar_producto, text="ID del Producto:")
        lbl_id.grid(row=0, column=0, padx=10, pady=10)

        self.txt_id = Entry(self.ventana_modificar_producto, width=30)
        self.txt_id.grid(row=0, column=1, padx=10, pady=10)
        
        btn_buscar = ttk.Button(self.ventana_modificar_producto, text="Buscar", command=self.buscar_producto)
        btn_buscar.grid(row=0, column=2, padx=10, pady=10)
        
        lbl_nombre = Label(self.ventana_modificar_producto, text="Nombre:")
        lbl_nombre.grid(row=1, column=0, padx=10, pady=10)

        self.txt_nombre = Entry(self.ventana_modificar_producto, width=30)
        self.txt_nombre.grid(row=1, column=1, padx=10, pady=10)
        
        lbl_descripcion = Label(self.ventana_modificar_producto, text="Descripción:")
        lbl_descripcion.grid(row=2, column=0, padx=10, pady=10)

        self.txt_descripcion = Entry(self.ventana_modificar_producto, width=30)
        self.txt_descripcion.grid(row=2, column=1, padx=10, pady=10)
        
        lbl_precio = Label(self.ventana_modificar_producto, text="Precio:")
        lbl_precio.grid(row=3, column=0, padx=10, pady=10)

        self.txt_precio = Entry(self.ventana_modificar_producto, width=30)
        self.txt_precio.grid(row=3, column=1, padx=10, pady=10)
        
        lbl_cantidad = Label(self.ventana_modificar_producto, text="Cantidad disponible:")
        lbl_cantidad.grid(row=4, column=0, padx=10, pady=10)

        self.txt_cantidad = Entry(self.ventana_modificar_producto, width=30)
        self.txt_cantidad.grid(row=4, column=1, padx=10, pady=10)
        
        lbl_promocion = Label(self.ventana_modificar_producto, text="Promoción:")
        lbl_promocion.grid(row=5, column=0, padx=10, pady=10)

        self.txt_promocion = Entry(self.ventana_modificar_producto, width=30)
        self.txt_promocion.grid(row=5, column=1, padx=10, pady=10)
        
        lbl_descuento = Label(self.ventana_modificar_producto, text="Descuento promoción:")
        lbl_descuento.grid(row=6, column=0, padx=10, pady=10)

        self.txt_descuento = Entry(self.ventana_modificar_producto, width=30)
        self.txt_descuento.grid(row=6, column=1, padx=10, pady=10)
        
        # Botón para aplicar la modificación
        btn_modificar = ttk.Button(self.ventana_modificar_producto, text="Modificar", command=self.aplicar_modificacion)
        btn_modificar.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

    def buscar_producto(self):
        nombre = self.txt_id.get()

        if nombre:
            try:
                conexion = mysql.connector.connect(
                    host="127.0.0.1",
                    user="root",
                    password="",
                    database="lasuertedelaolla",
                    port=3306
                )
                
                cursor = conexion.cursor()

                query = "SELECT id, nombre, descripcion,precio, cantidad_disponible, promocion, descuento_promocion FROM producto WHERE id = %s"
                cursor.execute(query, (nombre,))
                
                producto = cursor.fetchone()
                
                if producto:
                    self.txt_nombre.delete(0, tk.END)
                    self.txt_nombre.insert(0, producto[1])  # Nombre
                    self.txt_descripcion.delete(0, tk.END)
                    self.txt_descripcion.insert(0, producto[2])  # Descripción
                    self.txt_precio.delete(0, tk.END)
                    self.txt_precio.insert(0, producto[3])  # Precio
                    self.txt_cantidad.delete(0, tk.END)
                    self.txt_cantidad.insert(0, producto[4])  # Cantidad
                    self.txt_promocion.delete(0, tk.END)
                    self.txt_promocion.insert(0, producto[5])  # Promoción
                    self.txt_descuento.delete(0, tk.END)
                    self.txt_descuento.insert(0, producto[6])  # Descuento
                else:
                    messagebox.showwarning("Producto no encontrado", f"No se encontró ningún producto con el id '{nombre}'.")
                
                cursor.close()
                conexion.close()
                
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Error al conectar a la base de datos: {e}")
        else:
            messagebox.showwarning("Id de producto vacío", "Por favor ingresa el id del producto a buscar.")
    
    def aplicar_modificacion(self):



        # Obtener los datos modificados del producto desde los campos de entrada
        id_producto = self.txt_id.get()
        nombre = self.txt_nombre.get()
        descripcion = self.txt_descripcion.get()
        precio = float(self.txt_precio.get())
        cantidad = int(self.txt_cantidad.get())
        promocion = self.txt_promocion.get()
        descuento = float(self.txt_descuento.get())
        
        # Llamar al método para modificar producto
        if self.modificar_producto_bd(id_producto, nombre, descripcion, precio, cantidad, promocion, descuento):
            messagebox.showinfo("Producto modificado", "El producto se ha modificado correctamente.")
            self.ventana_modificar_producto.destroy()
        else:
            messagebox.showerror("Error", "No se pudo modificar el producto.")
    
    def modificar_producto_bd(self, id_producto, nombre, descripcion, precio, cantidad, promocion, descuento):
        
        try:
        # Conectar a la base de datos
            self.conexion = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="",
            database="lasuertedelaolla",
            port=3306
            )      
        
            cursor = self.conexion.cursor()
            
            # Modificar el producto en la base de datos
            query = "UPDATE producto SET nombre = %s, descripcion = %s, precio = %s, cantidad_disponible = %s, promocion = %s, descuento_promocion = %s WHERE id = %s"
            cursor.execute(query, (nombre, descripcion, precio, cantidad, promocion, descuento, id_producto))
            
            self.conexion.commit()

            # Guardar el mensaje en la tabla de registros
            mensaje = "Producto actualizado exitosamente."
            query_registro = "INSERT INTO registros (mensaje) VALUES (%s)"
            cursor.execute(query_registro, (mensaje,))
            self.conexion.commit()

            cursor.close()
            self.conexion.close()
            return True
        except mysql.connector.Error as e:
            messagebox.showerror("Error al modificar producto", f"No se pudo modificar el producto: {e}")
            return False

    def eliminar_producto(self):
        # Crear una nueva ventana para eliminar productos
        self.ventana_eliminar_producto = Toplevel(self.master)
        self.ventana_eliminar_producto.title("Eliminar Producto")
        
        # Campo de entrada para el ID del producto a eliminar
        lbl_id = Label(self.ventana_eliminar_producto, text="ID del Producto:")
        lbl_id.grid(row=0, column=0, padx=10, pady=10)

        self.txt_id_eliminar = Entry(self.ventana_eliminar_producto, width=30)
        self.txt_id_eliminar.grid(row=0, column=1, padx=10, pady=10)
        
        # Botón para eliminar el producto
        btn_eliminar = ttk.Button(self.ventana_eliminar_producto, text="Eliminar", command=self.confirmar_eliminar_producto)
        btn_eliminar.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
    
    def confirmar_eliminar_producto(self):
        # Mostrar un mensaje de confirmación y eliminar el producto si el usuario confirma
        id_producto = self.txt_id_eliminar.get()
        
        if messagebox.askyesno("Confirmar Eliminación", f"¿Está seguro de eliminar el producto con ID {id_producto}?"):
            if self.eliminar_producto_bd(id_producto):
                messagebox.showinfo("Producto eliminado", "El producto ha sido eliminado correctamente.")
                self.ventana_eliminar_producto.destroy()
               
            else:
                messagebox.showerror("Error", "No se pudo eliminar el producto.")

    def eliminar_producto_bd(self, id_producto):
        # Obtener el nombre del usuario a eliminar desde la entrada
        id_producto = self.txt_id_eliminar.get()
        
        # Validar que el nombre del usuario no esté vacío
        if id_producto:
            try:
                # Conectar a la base de datos
                self.conexion = mysql.connector.connect(
                    host="127.0.0.1",
                    user="root",
                    password="",
                    database="lasuertedelaolla",
                    port=3306
                )
                
                cursor = self.conexion.cursor()
                
                # Eliminar el usuario de la base de datos
                query = "DELETE FROM producto WHERE id = %s"
                cursor.execute(query, (id_producto,))
                
                self.conexion.commit()
                # Guardar el mensaje en la tabla de registros
                mensaje = "Producto eliminado exitosamente."
                query_registro = "INSERT INTO registros (mensaje) VALUES (%s)"
                cursor.execute(query_registro, (mensaje,))
                self.conexion.commit()

                cursor.close()
                self.conexion.close()
                
                # Mostrar mensaje de éxito
                messagebox.showinfo("Producto eliminado", f"Producto '{id_producto}' eliminado exitosamente.")
                
                # Cerrar la ventana de eliminar usuario
                self.eliminar_producto.destroy()
                
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Error al conectar a la base de datos: {e}")
        else:
            messagebox.showwarning("Id del producto vacío", "Por favor ingresa el id del producto a eliminar.")

    def buscar_productos(self):
        termino_busqueda = self.txt_busqueda_productos.get().strip()
        if termino_busqueda:
            try:
                self.conexion = mysql.connector.connect(
                    host="127.0.0.1",
                    user="root",
                    password="",
                    database="lasuertedelaolla",
                    port=3306
                )

                cursor = self.conexion.cursor()
                query = """
                SELECT id, nombre, descripcion, precio, cantidad_disponible, promocion, descuento_promocion  
                FROM producto
                WHERE id LIKE %s OR nombre LIKE %s OR descripcion LIKE %s OR precio LIKE %s OR cantidad_disponible LIKE %s OR promocion LIKE %s OR descuento_promocion LIKE %s 
                """
                cursor.execute(query, ("%"+termino_busqueda+"%", "%"+termino_busqueda+"%", "%"+termino_busqueda+"%", "%"+termino_busqueda+"%", "%"+termino_busqueda+"%", "%"+termino_busqueda+"%", "%"+termino_busqueda+"%"))
                productos = cursor.fetchall()

                cursor.close()
                self.conexion.close()

                for item in self.tree_lista_productos.get_children():
                    self.tree_lista_productos.delete(item)

                for producto in productos:
                    self.tree_lista_productos.insert("", "end", values=producto)

            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Error al conectar a la base de datos: {e}")
        else:
            self.cargar_productos()

    #------------------------------------------------------------------------------------------
    #VENTAS

    def ventana_lista_ventas(self):
        self.frame_lista_ventas = Frame(self.frame_center)
        self.frame_lista_ventas.grid(row=0, column=0, columnspan=2, padx=15, pady=15, sticky=NSEW)

        self.lblframe_botones_ventas = LabelFrame(self.frame_lista_ventas)
        self.lblframe_botones_ventas.grid(row=0, column=0, padx=15, pady=15, sticky=NSEW)

        # Panel de botones para agregar, modificar y eliminar ventas
        # ---------------------------------------------------------------------------------
        btn_nueva_venta = tb.Button(self.lblframe_botones_ventas, text="Nueva Venta", width=20, bootstyle="success", command=self.nueva_venta)
        btn_nueva_venta.grid(row=0, column=0, padx=10, pady=10)
        # ---------------------------------------------------------------------------------
        btn_modificar_venta = tb.Button(self.lblframe_botones_ventas, text="Modificar", width=20, bootstyle="info", command=self.modificar_venta)
        btn_modificar_venta.grid(row=0, column=1, padx=10, pady=10)
        # ---------------------------------------------------------------------------------
        btn_eliminar_venta = tb.Button(self.lblframe_botones_ventas, text="Eliminar", width=20, bootstyle="danger", command=self.eliminar_venta)
        btn_eliminar_venta.grid(row=0, column=2, padx=10, pady=10)

        # Búsqueda de ventas existentes
        # ---------------------------------------------------------------------------------
        self.lblframe_busqueda_ventas = LabelFrame(self.frame_lista_ventas,  text="Buscar Ventas")
        self.lblframe_busqueda_ventas.grid(row=1, column=0, padx=15, pady=15, sticky=NSEW)
        
        # Barra de búsqueda de ventas, donde se puede ingresar el ID de la venta
        self.txt_busqueda_ventas = ttk.Entry(self.lblframe_busqueda_ventas, width=150)
        self.txt_busqueda_ventas.grid(row=0, column=0, padx=(10,0), pady=10, sticky=W)

        btn_buscar_ventas = tb.Button(self.lblframe_busqueda_ventas, text="🔍", width=3, command=self.buscar_ventas)
        btn_buscar_ventas.grid(row=0, column=1, padx=(0, 10), pady=10)


        # Vista de árbol
        # ================================================
        self.lblframe_tree_ventas = LabelFrame(self.frame_lista_ventas)
        self.lblframe_tree_ventas.grid(row=2, column=0, sticky=NSEW)

        # Definición de las columnas manualmente acorde a la tabla de ventas
        columnas = ("id", "id_usuario", "id_cliente", "fecha", "total", "valor_iva")
        total_width = self.lblframe_tree_ventas.winfo_width()  

        # Distribuimos el ancho disponible entre las columnas
        column_widths = {
            "id": int(total_width * 0.1),
            "id_usuario": int(total_width * 0.15),
            "id_cliente": int(total_width * 0.15),
            "fecha": int(total_width * 0.2),
            "total": int(total_width * 0.2),
            "valor_iva": int(total_width * 0.2)
        }

        self.tree_lista_ventas = tb.Treeview(self.lblframe_tree_ventas, columns=columnas, height=45, show="headings", bootstyle="dark")
        self.tree_lista_ventas.grid(row=0, column=0, sticky=NSEW)

        # Títulos de cada una de las columnas
        self.tree_lista_ventas.heading("id", text="Id", anchor=W)
        self.tree_lista_ventas.heading("id_usuario", text="Id Usuario", anchor=W)
        self.tree_lista_ventas.heading("id_cliente", text="Id Cliente", anchor=W)
        self.tree_lista_ventas.heading("fecha", text="Fecha", anchor=W)
        self.tree_lista_ventas.heading("total", text="Total", anchor=W)
        self.tree_lista_ventas.heading("valor_iva", text="Valor IVA", anchor=W)

        self.tree_lista_ventas['displaycolumns'] = ("id", "id_usuario", "id_cliente", "fecha", "total", "valor_iva")

        # Configurar el ancho de cada columna
        for col, width in column_widths.items():
            self.tree_lista_ventas.column(col, width=width, minwidth=50)

        # Crear el scroll
        tree_scroll_ventas = tb.Scrollbar(self.lblframe_tree_ventas, bootstyle='round-dark', orient=VERTICAL, command=self.tree_lista_ventas.yview)
        tree_scroll_ventas.grid(row=0, column=1, sticky=NSEW)

        # Configuración del scroll
        self.tree_lista_ventas.config(yscrollcommand=tree_scroll_ventas.set)

        # Configuración de la expansión de columnas para utilizar todo el ancho disponible
        self.lblframe_tree_ventas.columnconfigure(0, weight=1)

        # Cargar las ventas
        self.cargar_ventas()

    def nueva_venta(self):
        # Crear una nueva ventana para ingresar los datos de la nueva venta
        self.ventana_nueva_venta = Toplevel(self)
        self.ventana_nueva_venta.title("Nueva Venta")

        # Crear los campos para ingresar los datos de la nueva venta
        lbl_id_usuario = Label(self.ventana_nueva_venta, text="ID Usuario:")
        lbl_id_usuario.grid(row=0, column=0, padx=10, pady=10)

        self.txt_id_usuario = Entry(self.ventana_nueva_venta, width=30)
        self.txt_id_usuario.grid(row=0, column=1, padx=10, pady=10)

        lbl_id_cliente = Label(self.ventana_nueva_venta, text="ID Cliente:")
        lbl_id_cliente.grid(row=1, column=0, padx=10, pady=10)

        self.txt_id_cliente = Entry(self.ventana_nueva_venta, width=30)
        self.txt_id_cliente.grid(row=1, column=1, padx=10, pady=10)

        lbl_fecha = Label(self.ventana_nueva_venta, text="Fecha:")
        lbl_fecha.grid(row=2, column=0, padx=10, pady=10)

        self.txt_fecha = Entry(self.ventana_nueva_venta, width=30)
        self.txt_fecha.grid(row=2, column=1, padx=10, pady=10)

        lbl_total = Label(self.ventana_nueva_venta, text="Total:")
        lbl_total.grid(row=3, column=0, padx=10, pady=10)

        self.txt_total = Entry(self.ventana_nueva_venta, width=30)
        self.txt_total.grid(row=3, column=1, padx=10, pady=10)

        lbl_valor_iva = Label(self.ventana_nueva_venta, text="Valor IVA:")
        lbl_valor_iva.grid(row=4, column=0, padx=10, pady=10)

        self.txt_valor_iva = Entry(self.ventana_nueva_venta, width=30)
        self.txt_valor_iva.grid(row=4, column=1, padx=10, pady=10)

        # Botón para guardar la nueva venta
        btn_guardar = ttk.Button(self.ventana_nueva_venta, text="Guardar", command=self.guardar_nueva_venta)
        btn_guardar.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    def guardar_nueva_venta(self):
        # Obtener los valores de los campos
        id_usuario = self.txt_id_usuario.get()
        id_cliente = self.txt_id_cliente.get()
        fecha = self.txt_fecha.get()
        total = self.txt_total.get()
        valor_iva = self.txt_valor_iva.get()

        # Validar que todos los campos estén completos
        if id_usuario and id_cliente and fecha and total and valor_iva:
            try:
                # Conectar a la base de datos
                self.conexion = mysql.connector.connect(
                    host="127.0.0.1",
                    user="root",
                    password="",
                    database="lasuertedelaolla",
                    port=3306
                )
                
                cursor = self.conexion.cursor()
                
                # Insertar la nueva venta en la base de datos
                query = "INSERT INTO venta (id_usuario, id_cliente, fecha, total, valor_iva) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(query, (id_usuario, id_cliente, fecha, total, valor_iva))
                
                self.conexion.commit()
                # Guardar el mensaje en la tabla de registros
                mensaje = "Venta añadida exitosamente."
                query_registro = "INSERT INTO registros (mensaje) VALUES (%s)"
                cursor.execute(query_registro, (mensaje,))
                self.conexion.commit()

                cursor.close()
                self.conexion.close()
                
                # Mostrar mensaje de éxito
                messagebox.showinfo("Nueva Venta", "Venta registrada exitosamente.")
                
                # Cerrar la ventana de nueva venta
                self.ventana_nueva_venta.destroy()
                
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Error al conectar a la base de datos: {e}")
        else:
            # Mostrar mensaje de advertencia si no se completaron todos los campos
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
            
    def modificar_venta(self):
        # Crear una nueva ventana para seleccionar la venta a modificar
        self.ventana_modificar_venta = Toplevel(self)
        self.ventana_modificar_venta.title("Modificar Venta")
        
        # Etiqueta y campo de entrada para seleccionar la venta por su ID
        lbl_id = Label(self.ventana_modificar_venta, text="ID de la venta:")
        lbl_id.grid(row=0, column=0, padx=10, pady=10)
        self.txt_id_modificar = Entry(self.ventana_modificar_venta, width=30)
        self.txt_id_modificar.grid(row=0, column=1, padx=10, pady=10)
        
        # Botón para buscar la venta
        btn_buscar = ttk.Button(self.ventana_modificar_venta, text="Buscar", command=self.buscar_venta_modificar)
        btn_buscar.grid(row=0, column=2, padx=10, pady=10)
        
        # Crear los campos para modificar los datos de la venta
        lbl_id_usuario_nuevo = Label(self.ventana_modificar_venta, text="Nuevo ID Usuario:")
        lbl_id_usuario_nuevo.grid(row=1, column=0, padx=10, pady=10)
        self.txt_id_usuario_nuevo = Entry(self.ventana_modificar_venta, width=30)
        self.txt_id_usuario_nuevo.grid(row=1, column=1, padx=10, pady=10)
        
        lbl_id_cliente_nuevo = Label(self.ventana_modificar_venta, text="Nuevo ID Cliente:")
        lbl_id_cliente_nuevo.grid(row=2, column=0, padx=10, pady=10)
        self.txt_id_cliente_nuevo = Entry(self.ventana_modificar_venta, width=30)
        self.txt_id_cliente_nuevo.grid(row=2, column=1, padx=10, pady=10)
        
        lbl_fecha_nueva = Label(self.ventana_modificar_venta, text="Nueva Fecha:")
        lbl_fecha_nueva.grid(row=3, column=0, padx=10, pady=10)
        self.txt_fecha_nueva = Entry(self.ventana_modificar_venta, width=30)
        self.txt_fecha_nueva.grid(row=3, column=1, padx=10, pady=10)
        
        lbl_total_nuevo = Label(self.ventana_modificar_venta, text="Nuevo Total:")
        lbl_total_nuevo.grid(row=4, column=0, padx=10, pady=10)
        self.txt_total_nuevo = Entry(self.ventana_modificar_venta, width=30)
        self.txt_total_nuevo.grid(row=4, column=1, padx=10, pady=10)
        
        lbl_valor_iva_nuevo = Label(self.ventana_modificar_venta, text="Nuevo Valor IVA:")
        lbl_valor_iva_nuevo.grid(row=5, column=0, padx=10, pady=10)
        self.txt_valor_iva_nuevo = Entry(self.ventana_modificar_venta, width=30)
        self.txt_valor_iva_nuevo.grid(row=5, column=1, padx=10, pady=10)

        # Botón para guardar los cambios
        btn_guardar = ttk.Button(self.ventana_modificar_venta, text="Guardar cambios", command=self.guardar_modificacion_venta)
        btn_guardar.grid(row=6, column=0, columnspan=3, padx=10, pady=10)

    def buscar_venta_modificar(self):
        # Obtener el ID de la venta a modificar desde la entrada
        id_venta = self.txt_id_modificar.get()
        
        # Validar que el ID de la venta no esté vacío
        if id_venta:
            try:
                # Conectar a la base de datos
                self.conexion = mysql.connector.connect(
                    host="127.0.0.1",
                    user="root",
                    password="",
                    database="lasuertedelaolla",
                    port=3306
                )
                
                cursor = self.conexion.cursor()
                
                # Consultar la venta en la base de datos
                query = "SELECT id, id_usuario, id_cliente, fecha, total, valor_iva FROM venta WHERE id = %s"
                cursor.execute(query, (id_venta,))
                
                # Obtener el resultado de la consulta
                venta = cursor.fetchone()
                
                if venta:
                    # Mostrar los datos de la venta encontrada en los campos de entrada
                    if self.txt_id_usuario_nuevo:
                        print(f"Actualizando ID Usuario: {venta[1]}")
                        self.txt_id_usuario_nuevo.delete(0, END)
                        self.txt_id_usuario_nuevo.insert(0, str(venta[1]))  # ID Usuario
                    if self.txt_id_cliente_nuevo:
                        print(f"Actualizando ID Cliente: {venta[2]}")
                        self.txt_id_cliente_nuevo.delete(0, END)
                        self.txt_id_cliente_nuevo.insert(0, str(venta[2]))  # ID Cliente
                    if self.txt_fecha_nueva:
                        print(f"Actualizando Fecha: {venta[3]}")
                        self.txt_fecha_nueva.delete(0, END)
                        self.txt_fecha_nueva.insert(0, str(venta[3]))  # Fecha
                    if self.txt_total_nuevo:
                        print(f"Actualizando Total: {venta[4]}")
                        self.txt_total_nuevo.delete(0, END)
                        self.txt_total_nuevo.insert(0, str(venta[4]))  # Total
                    if self.txt_valor_iva_nuevo:
                        print(f"Actualizando Valor IVA: {venta[5]}")
                        self.txt_valor_iva_nuevo.delete(0, END)
                        self.txt_valor_iva_nuevo.insert(0, str(venta[5]))  # Valor IVA
                else:
                    messagebox.showwarning("Venta no encontrada", f"No se encontró ninguna venta con el ID '{id_venta}'.")
                
                cursor.close()
                self.conexion.close()
                
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Error al conectar a la base de datos: {e}")
        else:
            messagebox.showwarning("ID de venta vacío", "Por favor ingresa el ID de la venta a modificar.")

    def guardar_modificacion_venta(self):
        # Obtener los valores modificados de la venta desde los campos de entrada
        id_usuario_nuevo = self.txt_id_usuario_nuevo.get()
        id_cliente_nuevo = self.txt_id_cliente_nuevo.get()
        fecha_nueva = self.txt_fecha_nueva.get()
        total_nuevo = self.txt_total_nuevo.get()
        valor_iva_nuevo = self.txt_valor_iva_nuevo.get()
        
        # Obtener el ID original de la venta desde el campo de búsqueda
        id_original = self.txt_id_modificar.get()
        
        # Validar que todos los campos estén completos
        if id_usuario_nuevo and id_cliente_nuevo and fecha_nueva and total_nuevo and valor_iva_nuevo and id_original:
            try:
                # Conectar a la base de datos
                self.conexion = mysql.connector.connect(
                    host="127.0.0.1",
                    user="root",
                    password="",
                    database="lasuertedelaolla",
                    port=3306
                )
                
                cursor = self.conexion.cursor()
                
                # Actualizar los datos de la venta en la base de datos
                query = "UPDATE venta SET id_usuario = %s, id_cliente = %s, fecha = %s, total = %s, valor_iva = %s WHERE id = %s"
                cursor.execute(query, (id_usuario_nuevo, id_cliente_nuevo, fecha_nueva, total_nuevo, valor_iva_nuevo, id_original))
                
                self.conexion.commit()
                # Guardar el mensaje en la tabla de registros
                mensaje = "Venta modificada exitosamente."
                query_registro = "INSERT INTO registros (mensaje) VALUES (%s)"
                cursor.execute(query_registro, (mensaje,))
                self.conexion.commit()

                cursor.close()
                self.conexion.close()
                
                
                # Mostrar mensaje de éxito
                messagebox.showinfo("Venta modificada", "Venta modificada exitosamente.")
                
                # Cerrar la ventana de modificar venta
                self.ventana_modificar_venta.destroy()
                
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Error al conectar a la base de datos: {e}")
        else:
            # Mostrar mensaje de advertencia si no se completaron todos los campos
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")

    def eliminar_venta(self):
        # Crear una nueva ventana para seleccionar la venta a eliminar
        self.ventana_eliminar_venta = Toplevel(self)
        self.ventana_eliminar_venta.title("Eliminar Venta")
        
        # Etiqueta y campo de entrada para seleccionar la venta por su ID
        lbl_id = Label(self.ventana_eliminar_venta, text="ID de la venta:")
        lbl_id.grid(row=0, column=0, padx=10, pady=10)
        self.txt_id_eliminar = Entry(self.ventana_eliminar_venta, width=30)
        self.txt_id_eliminar.grid(row=0, column=1, padx=10, pady=10)
        
        # Botón para eliminar la venta
        btn_eliminar = ttk.Button(self.ventana_eliminar_venta, text="Eliminar", command=self.eliminar_venta_bd)
        btn_eliminar.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    def eliminar_venta_bd(self):
        # Obtener el ID de la venta a eliminar desde la entrada
        id_venta = self.txt_id_eliminar.get()
        
        # Validar que el ID de la venta no esté vacío
        if id_venta:
            try:
                # Conectar a la base de datos
                self.conexion = mysql.connector.connect(
                    host="127.0.0.1",
                    user="root",
                    password="",
                    database="lasuertedelaolla",
                    port=3306
                )
                
                cursor = self.conexion.cursor()
                
                # Eliminar la venta de la base de datos
                query = "DELETE FROM venta WHERE id = %s"
                cursor.execute(query, (id_venta,))
                
                self.conexion.commit()
                # Guardar el mensaje en la tabla de registros
                mensaje = "Venta eliminada exitosamente."
                query_registro = "INSERT INTO registros (mensaje) VALUES (%s)"
                cursor.execute(query_registro, (mensaje,))
                self.conexion.commit()

                cursor.close()
                self.conexion.close()
                
                
                # Mostrar mensaje de éxito
                messagebox.showinfo("Venta eliminada", f"Venta con ID '{id_venta}' eliminada exitosamente.")
                
                # Cerrar la ventana de eliminar venta
                self.ventana_eliminar_venta.destroy()
                
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Error al conectar a la base de datos: {e}")
        else:
            messagebox.showwarning("ID de venta vacío", "Por favor ingresa el ID de la venta a eliminar.")

    def cargar_ventas(self):
        # Conectar a la base de datos MySQL
        try:
            conexion = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="",
                database="lasuertedelaolla",
                port=3306
            )
            cursor = conexion.cursor()
            cursor.execute("SELECT id, id_usuario, id_cliente, fecha, total, valor_iva FROM venta")
            ventas = cursor.fetchall()

            # Limpiar el treeview antes de cargar los datos
            for i in self.tree_lista_ventas.get_children():
                self.tree_lista_ventas.delete(i)

            # Insertar cada venta en el treeview
            for venta in ventas:
                self.tree_lista_ventas.insert("", "end", values=venta)

            cursor.close()
            conexion.close()

        except mysql.connector.Error as e:
            messagebox.showerror("Error de conexión", f"No se pudo conectar a la base de datos: {e}")
    
    def buscar_ventas(self):
        termino_busqueda = self.txt_busqueda_ventas.get().strip()
        if termino_busqueda:
            try:
                self.conexion = mysql.connector.connect(
                    host="127.0.0.1",
                    user="root",
                    password="",
                    database="lasuertedelaolla",
                    port=3306
                )

                cursor = self.conexion.cursor()
                query = """
                SELECT id,id_usuario,id_cliente,fecha,total,valor_iva
                FROM venta
                WHERE id LIKE %s OR id_usuario LIKE %s OR id_cliente LIKE %s OR fecha LIKE %s OR total LIKE %s OR valor_iva LIKE %s
                """
                cursor.execute(query, ("%"+termino_busqueda+"%", "%"+termino_busqueda+"%", "%"+termino_busqueda+"%", "%"+termino_busqueda+"%", "%"+termino_busqueda+"%", "%"+termino_busqueda+"%"))
                ventas = cursor.fetchall()

                cursor.close()
                self.conexion.close()

                for item in self.tree_lista_ventas.get_children():
                    self.tree_lista_ventas.delete(item)

                for venta in ventas:
                    self.tree_lista_ventas.insert("", "end", values=venta)

            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Error al conectar a la base de datos: {e}")
        else:
            self.cargar_ventas()
    #-------------------------------------------------------------------
    #COMPRAS O MÁS BIEN DETALLE DE LAS VENTAS 

    def ventana_lista_compras(self):
        self.frame_lista_compras = Frame(self.frame_center)
        self.frame_lista_compras.grid(row=0, column=0, columnspan=2, padx=15, pady=15, sticky=NSEW)

        self.lblframe_botones_compras = LabelFrame(self.frame_lista_compras)
        self.lblframe_botones_compras.grid(row=0, column=0, padx=15, pady=15, sticky=NSEW)

        btn_nueva_compra = tb.Button(self.lblframe_botones_compras, text="Nueva Compra", width=20, bootstyle="success", command=self.nueva_compra)
        btn_nueva_compra.grid(row=0, column=0, padx=10, pady=10)

        btn_modificar_compra = tb.Button(self.lblframe_botones_compras, text="Modificar Compra", width=20, bootstyle="info", command=self.modificar_compra)
        btn_modificar_compra.grid(row=0, column=1, padx=10, pady=10)

        btn_eliminar_compra = tb.Button(self.lblframe_botones_compras, text="Eliminar Compra", width=20, bootstyle="danger", command=self.eliminar_compra)
        btn_eliminar_compra.grid(row=0, column=2, padx=10, pady=10)

        self.lblframe_busqueda_compras = LabelFrame(self.frame_lista_compras, text="Buscar Compras")
        self.lblframe_busqueda_compras.grid(row=1, column=0, padx=15, pady=15, sticky=NSEW)

        self.txt_busqueda_compras = ttk.Entry(self.lblframe_busqueda_compras, width=150)
        self.txt_busqueda_compras.grid(row=0, column=0, padx=(10,0), pady=10, sticky=W)

        btn_buscar_compras = tb.Button(self.lblframe_busqueda_compras, text="🔍", width=3, command=self.buscar_compras)
        btn_buscar_compras.grid(row=0, column=1, padx=(0, 10), pady=10)

        self.lblframe_tree_compras = LabelFrame(self.frame_lista_compras)
        self.lblframe_tree_compras.grid(row=2, column=0, sticky=NSEW)

        columnas = ("id_venta", "id_producto", "cantidad", "precio_unitario", "promocion_aplicada", "descuento")
        total_width = self.lblframe_tree_compras.winfo_width()  

        column_widths = {
            "id_venta": int(total_width * 0.1),
            "id_producto": int(total_width * 0.1),
            "cantidad": int(total_width * 0.1),
            "precio_unitario": int(total_width * 0.2),
            "promocion_aplicada": int(total_width * 0.2),
            "descuento": int(total_width * 0.2)
        }

        self.tree_lista_compras = tb.Treeview(self.lblframe_tree_compras, columns=columnas, height=75, show="headings", bootstyle="dark")
        self.tree_lista_compras.grid(row=0, column=0, sticky=NSEW)

        self.tree_lista_compras.heading("id_venta", text="ID Venta", anchor=W)
        self.tree_lista_compras.heading("id_producto", text="ID Producto", anchor=W)
        self.tree_lista_compras.heading("cantidad", text="Cantidad", anchor=W)
        self.tree_lista_compras.heading("precio_unitario", text="Precio Unitario", anchor=W)
        self.tree_lista_compras.heading("promocion_aplicada", text="Promoción Aplicada", anchor=W)
        self.tree_lista_compras.heading("descuento", text="Descuento", anchor=W)

        self.tree_lista_compras['displaycolumns'] = ("id_venta", "id_producto", "cantidad", "precio_unitario", "promocion_aplicada", "descuento")

        for col, width in column_widths.items():
            self.tree_lista_compras.column(col, width=width, minwidth=50)

        tree_scroll_compras = tb.Scrollbar(self.lblframe_tree_compras, bootstyle='round-dark', orient=VERTICAL, command=self.tree_lista_compras.yview)
        tree_scroll_compras.grid(row=0, column=1, sticky=NSEW)

        self.tree_lista_compras.config(yscrollcommand=tree_scroll_compras.set)

        self.lblframe_tree_compras.columnconfigure(0, weight=1)

        self.cargar_compras()

    def nueva_compra(self):
        # Crear una nueva ventana para ingresar los datos de la nueva compra
        self.ventana_nueva_compra = Toplevel(self)
        self.ventana_nueva_compra.title("Nueva Compra")

        # Crear los campos para ingresar los datos de la nueva compra
        lbl_id_venta = Label(self.ventana_nueva_compra, text="ID Venta:")
        lbl_id_venta.grid(row=0, column=0, padx=10, pady=10)

        self.txt_id_venta = Entry(self.ventana_nueva_compra, width=30)
        self.txt_id_venta.grid(row=0, column=1, padx=10, pady=10)

        lbl_id_producto = Label(self.ventana_nueva_compra, text="ID Producto:")
        lbl_id_producto.grid(row=1, column=0, padx=10, pady=10)

        self.txt_id_producto = Entry(self.ventana_nueva_compra, width=30)
        self.txt_id_producto.grid(row=1, column=1, padx=10, pady=10)

        lbl_cantidad = Label(self.ventana_nueva_compra, text="Cantidad:")
        lbl_cantidad.grid(row=2, column=0, padx=10, pady=10)

        self.txt_cantidad = Entry(self.ventana_nueva_compra, width=30)
        self.txt_cantidad.grid(row=2, column=1, padx=10, pady=10)

        lbl_precio_unitario = Label(self.ventana_nueva_compra, text="Precio Unitario:")
        lbl_precio_unitario.grid(row=3, column=0, padx=10, pady=10)

        self.txt_precio_unitario = Entry(self.ventana_nueva_compra, width=30)
        self.txt_precio_unitario.grid(row=3, column=1, padx=10, pady=10)

        lbl_promocion_aplicada = Label(self.ventana_nueva_compra, text="Promoción Aplicada:")
        lbl_promocion_aplicada.grid(row=4, column=0, padx=10, pady=10)

        self.txt_promocion_aplicada = Entry(self.ventana_nueva_compra, width=30)
        self.txt_promocion_aplicada.grid(row=4, column=1, padx=10, pady=10)

        lbl_descuento = Label(self.ventana_nueva_compra, text="Descuento:")
        lbl_descuento.grid(row=5, column=0, padx=10, pady=10)

        self.txt_descuento = Entry(self.ventana_nueva_compra, width=30)
        self.txt_descuento.grid(row=5, column=1, padx=10, pady=10)

        # Botón para guardar la nueva compra
        btn_guardar = ttk.Button(self.ventana_nueva_compra, text="Guardar", command=self.guardar_nueva_compra)
        btn_guardar.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

    def guardar_nueva_compra(self):
        # Obtener los valores de los campos
        id_venta = self.txt_id_venta.get()
        id_producto = self.txt_id_producto.get()
        cantidad = self.txt_cantidad.get()
        precio_unitario = self.txt_precio_unitario.get()
        promocion_aplicada = self.txt_promocion_aplicada.get()
        descuento = self.txt_descuento.get()

        # Validar que todos los campos estén completos
        if id_venta and id_producto and cantidad and precio_unitario and promocion_aplicada and descuento:
            try:
                # Conectar a la base de datos
                self.conexion = mysql.connector.connect(
                    host="127.0.0.1",
                    user="root",
                    password="",
                    database="lasuertedelaolla", 
                    port=3306
                )

                cursor = self.conexion.cursor()

                # Insertar la nueva compra en la base de datos
                query = "INSERT INTO detalles_venta (id_venta, id_producto, cantidad, precio_unitario, promocion_aplicada, descuento) VALUES (%s, %s, %s, %s, %s, %s)"
                cursor.execute(query, (id_venta, id_producto, cantidad, precio_unitario, promocion_aplicada, descuento))

                self.conexion.commit()
                # Guardar el mensaje en la tabla de registros
                mensaje = "Compra añadida exitosamente."
                query_registro = "INSERT INTO registros (mensaje) VALUES (%s)"
                cursor.execute(query_registro, (mensaje,))
                self.conexion.commit()

                cursor.close()
                self.conexion.close()
                

                # Mostrar mensaje de éxito
                messagebox.showinfo("Nueva Compra", "Compra creada exitosamente.")

                # Cerrar la ventana de nueva compra
                self.ventana_nueva_compra.destroy()

                # Actualizar la lista de compras
                self.cargar_compras()

            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Error al conectar a la base de datos: {e}")
        else:
            # Mostrar mensaje de advertencia si no se completaron todos los campos
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")

    def modificar_compra(self):
        # Crear una nueva ventana para seleccionar la compra a modificar
        self.ventana_modificar_compra = Toplevel(self)
        self.ventana_modificar_compra.title("Modificar Compra")

        # Etiqueta y campo de entrada para seleccionar la compra por su ID
        lbl_id_venta = Label(self.ventana_modificar_compra, text="ID Venta:")
        lbl_id_venta.grid(row=0, column=0, padx=10, pady=10)
        self.txt_id_venta_modificar = Entry(self.ventana_modificar_compra, width=30)
        self.txt_id_venta_modificar.grid(row=0, column=1, padx=10, pady=10)

        lbl_id_producto = Label(self.ventana_modificar_compra, text="ID Producto:")
        lbl_id_producto.grid(row=1, column=0, padx=10, pady=10)
        self.txt_id_producto_modificar = Entry(self.ventana_modificar_compra, width=30)
        self.txt_id_producto_modificar.grid(row=1, column=1, padx=10, pady=10)

        # Botón para buscar la compra
        btn_buscar = ttk.Button(self.ventana_modificar_compra, text="Buscar", command=self.buscar_compra_modificar)
        btn_buscar.grid(row=0, column=2, padx=10, pady=10)

        # Campos de entrada para modificar los datos de la compra
        lbl_cantidad_nueva = Label(self.ventana_modificar_compra, text="Nueva cantidad:")
        lbl_cantidad_nueva.grid(row=2, column=0, padx=10, pady=10)
        self.txt_cantidad_nueva = Entry(self.ventana_modificar_compra, width=30)
        self.txt_cantidad_nueva.grid(row=2, column=1, padx=10, pady=10)

        lbl_precio_unitario_nuevo = Label(self.ventana_modificar_compra, text="Nuevo precio unitario:")
        lbl_precio_unitario_nuevo.grid(row=3, column=0, padx=10, pady=10)
        self.txt_precio_unitario_nuevo = Entry(self.ventana_modificar_compra, width=30)
        self.txt_precio_unitario_nuevo.grid(row=3, column=1, padx=10, pady=10)

        lbl_promocion_aplicada_nueva = Label(self.ventana_modificar_compra, text="Nueva promoción aplicada:")
        lbl_promocion_aplicada_nueva.grid(row=4, column=0, padx=10, pady=10)
        self.txt_promocion_aplicada_nueva = Entry(self.ventana_modificar_compra, width=30)
        self.txt_promocion_aplicada_nueva.grid(row=4, column=1, padx=10, pady=10)

        lbl_descuento_nuevo = Label(self.ventana_modificar_compra, text="Nuevo descuento:")
        lbl_descuento_nuevo.grid(row=5, column=0, padx=10, pady=10)
        self.txt_descuento_nuevo = Entry(self.ventana_modificar_compra, width=30)
        self.txt_descuento_nuevo.grid(row=5, column=1, padx=10, pady=10)

        # Botón para guardar los cambios
        btn_guardar = ttk.Button(self.ventana_modificar_compra, text="Guardar cambios", command=self.guardar_modificacion_compra)
        btn_guardar.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

    def buscar_compra_modificar(self):
        # Obtener los valores de ID Venta
        id_venta = self.txt_id_venta_modificar.get()

        # Validar que los campos no estén vacíos
        if id_venta :
            try:
                # Conectar a la base de datos
                self.conexion = mysql.connector.connect(
                    host="127.0.0.1",
                    user="root",
                    password="",
                    database="lasuertedelaolla", 
                    port=3306
                )

                cursor = self.conexion.cursor()

                # Consultar la compra en la base de datos
                query = "SELECT cantidad, precio_unitario, promocion_aplicada, descuento FROM detalles_venta WHERE id_venta = %s"
                cursor.execute(query, (id_venta,))

                # Obtener el resultado de la consulta
                compra = cursor.fetchone()

                if compra:
                    # Mostrar los datos de la compra encontrada en los campos de entrada
                    self.txt_cantidad_nueva.delete(0, END)
                    self.txt_cantidad_nueva.insert(0, compra[0])  # Cantidad
                    self.txt_precio_unitario_nuevo.delete(0, END)
                    self.txt_precio_unitario_nuevo.insert(0, compra[1])  # Precio Unitario
                    self.txt_promocion_aplicada_nueva.delete(0, END)
                    self.txt_promocion_aplicada_nueva.insert(0, compra[2])  # Promoción Aplicada
                    self.txt_descuento_nuevo.delete(0, END)
                    self.txt_descuento_nuevo.insert(0, compra[3])  # Descuento
                else:
                    messagebox.showwarning("Compra no encontrada", f"No se encontró ninguna compra con ID Venta '{id_venta}'.")
                
                cursor.close()
                self.conexion.close()

            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Error al conectar a la base de datos: {e}")
        else:
            messagebox.showwarning("Campos vacíos", "Por favor ingresa ID Venta para buscar la compra.")

    def guardar_modificacion_compra(self):
        # Obtener los valores modificados de la compra desde los campos de entrada
        id_venta = self.txt_id_venta_modificar.get()
        id_producto = self.txt_id_producto_modificar.get()
        cantidad_nueva = self.txt_cantidad_nueva.get()
        precio_unitario_nuevo = self.txt_precio_unitario_nuevo.get()
        promocion_aplicada_nueva = self.txt_promocion_aplicada_nueva.get()
        descuento_nuevo = self.txt_descuento_nuevo.get()

        # Validar que todos los campos estén completos
        if id_venta and id_producto and cantidad_nueva and precio_unitario_nuevo and promocion_aplicada_nueva and descuento_nuevo:
            try:
                # Conectar a la base de datos
                self.conexion = mysql.connector.connect(
                    host="127.0.0.1",
                    user="root",
                    password="",
                    database="lasuertedelaolla", 
                    port=3306
                )

                cursor = self.conexion.cursor()

                # Actualizar los datos de la compra en la base de datos
                query = "UPDATE detalles_venta SET cantidad = %s, precio_unitario = %s, promocion_aplicada = %s, descuento = %s WHERE id_venta = %s AND id_producto = %s"
                cursor.execute(query, (cantidad_nueva, precio_unitario_nuevo, promocion_aplicada_nueva, descuento_nuevo, id_venta, id_producto))

                self.conexion.commit()
                # Guardar el mensaje en la tabla de registros
                mensaje = "Compra modificada exitosamente."
                query_registro = "INSERT INTO registros (mensaje) VALUES (%s)"
                cursor.execute(query_registro, (mensaje,))
                self.conexion.commit()

                cursor.close()
                self.conexion.close()
                

                # Mostrar mensaje de éxito
                messagebox.showinfo("Compra modificada", "Compra modificada exitosamente.")

                # Cerrar la ventana de modificar compra
                self.ventana_modificar_compra.destroy()

                # Actualizar la lista de compras
                self.cargar_compras()

            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Error al conectar a la base de datos: {e}")
        else:
            # Mostrar mensaje de advertencia si no se completaron todos los campos
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")

    def eliminar_compra(self):
        # Crear una nueva ventana para seleccionar la compra a eliminar
        self.ventana_eliminar_compra = Toplevel(self)
        self.ventana_eliminar_compra.title("Eliminar Compra")

        # Etiqueta y campo de entrada para seleccionar la compra por su ID Venta y ID Producto
        lbl_id_venta = Label(self.ventana_eliminar_compra, text="ID Venta:")
        lbl_id_venta.grid(row=0, column=0, padx=10, pady=10)
        self.txt_id_venta_eliminar = Entry(self.ventana_eliminar_compra, width=30)
        self.txt_id_venta_eliminar.grid(row=0, column=1, padx=10, pady=10)

        lbl_id_producto = Label(self.ventana_eliminar_compra, text="ID Producto:")
        lbl_id_producto.grid(row=1, column=0, padx=10, pady=10)
        self.txt_id_producto_eliminar = Entry(self.ventana_eliminar_compra, width=30)
        self.txt_id_producto_eliminar.grid(row=1, column=1, padx=10, pady=10)

        # Botón para buscar y eliminar la compra
        btn_eliminar = ttk.Button(self.ventana_eliminar_compra, text="Eliminar Compra", command=self.confirmar_eliminar_compra)
        btn_eliminar.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    def confirmar_eliminar_compra(self):
        # Obtener los valores de ID Venta y ID Producto desde la entrada
        id_venta = self.txt_id_venta_eliminar.get()
        id_producto = self.txt_id_producto_eliminar.get()

        # Validar que los campos no estén vacíos
        if id_venta and id_producto:
            # Mostrar un messagebox de confirmación para eliminar la compra
            respuesta = messagebox.askyesno("Confirmar Eliminación", f"¿Estás seguro que deseas eliminar la compra con ID Venta '{id_venta}' e ID Producto '{id_producto}'?")

            if respuesta:
                try:
                    # Conectar a la base de datos
                    self.conexion = mysql.connector.connect(
                        host="127.0.0.1",
                        user="root",
                        password="",
                        database="lasuertedelaolla", 
                        port=3306
                    )

                    cursor = self.conexion.cursor()

                    # Eliminar la compra de la base de datos
                    query = "DELETE FROM detalles_venta WHERE id_venta = %s AND id_producto = %s"
                    cursor.execute(query, (id_venta, id_producto))

                    self.conexion.commit()
                    # Guardar el mensaje en la tabla de registros
                    mensaje = "Compra eliminada exitosamente."
                    query_registro = "INSERT INTO registros (mensaje) VALUES (%s)"
                    cursor.execute(query_registro, (mensaje,))
                    self.conexion.commit()

                    cursor.close()
                    self.conexion.close()
                
                    # Mostrar mensaje de éxito
                    messagebox.showinfo("Compra Eliminada", "Compra eliminada exitosamente.")

                    # Cerrar la ventana de eliminar compra
                    self.ventana_eliminar_compra.destroy()

                    # Actualizar la lista de compras
                    self.cargar_compras()

                except mysql.connector.Error as e:
                    messagebox.showerror("Error", f"Error al conectar a la base de datos: {e}")
        else:
            messagebox.showwarning("Campos vacíos", "Por favor ingresa ID Venta e ID Producto para eliminar la compra.")

    def cargar_compras(self):
        try:
            # Conectar a la base de datos
            self.conexion = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="",
                database="lasuertedelaolla", 
                port=3306
            )

            cursor = self.conexion.cursor()

            # Seleccionar todas las compras de la tabla compras
            query = "SELECT id_venta, id_producto, cantidad, precio_unitario, promocion_aplicada, descuento FROM detalles_venta"
            cursor.execute(query)

            # Limpiar la tabla antes de cargar los nuevos datos
            registros = self.tree_lista_compras.get_children()
            for registro in registros:
                self.tree_lista_compras.delete(registro)

            # Agregar los registros obtenidos de la base de datos al árbol
            for compra in cursor.fetchall():
                self.tree_lista_compras.insert("", END, values=compra)

            cursor.close()
            self.conexion.close()

        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Error al conectar a la base de datos: {e}")

    def buscar_compras(self):
        termino_busqueda = self.txt_busqueda_compras.get().strip()
        if termino_busqueda:
            try:
                self.conexion = mysql.connector.connect(
                    host="127.0.0.1",
                    user="root",
                    password="",
                    database="lasuertedelaolla",
                    port=3306
                )

                cursor = self.conexion.cursor()
                query = """
                SELECT id_venta,id_producto,cantidad,precio_unitario,promocion_aplicada,descuento
                FROM detalles_venta
                WHERE id_venta LIKE %s OR id_producto LIKE %s OR cantidad LIKE %s OR precio_unitario LIKE %s OR promocion_aplicada LIKE %s OR descuento LIKE %s
                """
                cursor.execute(query, ("%"+termino_busqueda+"%", "%"+termino_busqueda+"%", "%"+termino_busqueda+"%", "%"+termino_busqueda+"%", "%"+termino_busqueda+"%", "%"+termino_busqueda+"%"))
                compras = cursor.fetchall()

                cursor.close()
                self.conexion.close()

                for item in self.tree_lista_compras.get_children():
                    self.tree_lista_compras.delete(item)

                for compra in compras:
                    self.tree_lista_compras.insert("", "end", values=compra)

            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Error al conectar a la base de datos: {e}")
        else:
            self.cargar_compras()


    #------------------------------------------------------------------
    #Repartidores


    def mostrar_repartidores(self):
        self.frame_lista_repartidores = Frame(self.frame_center)
        self.frame_lista_repartidores.grid(row=0, column=0, columnspan=2, padx=15, pady=15, sticky=NSEW)

        self.lblframe_botones_repartidor = LabelFrame(self.frame_lista_repartidores)
        self.lblframe_botones_repartidor.grid(row=0, column=0, padx=15, pady=15, sticky=NSEW)

        btn_nuevo_repartidor = tb.Button(self.lblframe_botones_repartidor, text="Nuevo", width=20, bootstyle="success", command=self.agregar_repartidor)
        btn_nuevo_repartidor.grid(row=0, column=0, padx=10, pady=10)

        btn_modificar_repartidor = tb.Button(self.lblframe_botones_repartidor, text="Modificar", width=20, bootstyle="info", command=self.editar_repartidor)
        btn_modificar_repartidor.grid(row=0, column=1, padx=10, pady=10)

        btn_eliminar_repartidor = tb.Button(self.lblframe_botones_repartidor, text="Eliminar", width=20, bootstyle="danger", command=self.eliminar_repartidor)
        btn_eliminar_repartidor.grid(row=0, column=2, padx=10, pady=10)

        self.lblframe_busqueda_repartidores = LabelFrame(self.frame_lista_repartidores,  text="Buscar Repartidores")
        self.lblframe_busqueda_repartidores.grid(row=1, column=0, padx=15, pady=15, sticky=NSEW)

        self.txt_busqueda_repartidores = ttk.Entry(self.lblframe_busqueda_repartidores, width=150)
        self.txt_busqueda_repartidores.grid(row=0, column=0, padx=(10,0), pady=10, sticky=W)

        btn_buscar_repartidores = tb.Button(self.lblframe_busqueda_repartidores, text="🔍", width=3, command=self.buscar_repartidores)
        btn_buscar_repartidores.grid(row=0, column=1, padx=(0, 10), pady=10)


        self.lblframe_tree_repartidores = LabelFrame(self.frame_lista_repartidores)
        self.lblframe_tree_repartidores.grid(row=2, column=0, sticky=NSEW)

        columnas = ("id", "nombre", "correo", "telefono")
        total_width = self.lblframe_tree_repartidores.winfo_width()  

        column_widths = {
            "id": int(total_width * 0.1),
            "nombre": int(total_width * 0.2),
            "correo": int(total_width * 0.4),
            "telefono": int(total_width * 0.3)
        }

        self.tree_lista_repartidores = tb.Treeview(self.lblframe_tree_repartidores, columns=columnas, height=45, show="headings", bootstyle="dark")
        self.tree_lista_repartidores.grid(row=0, column=0, sticky=NSEW)

        self.tree_lista_repartidores.heading("id", text="Id", anchor=W)
        self.tree_lista_repartidores.heading("nombre", text="Nombre", anchor=W)
        self.tree_lista_repartidores.heading("correo", text="Correo", anchor=W)
        self.tree_lista_repartidores.heading("telefono", text="Teléfono", anchor=W)

        self.tree_lista_repartidores['displaycolumns'] = ("id", "nombre", "correo", "telefono")

        for col, width in column_widths.items():
            self.tree_lista_repartidores.column(col, width=width, minwidth=50)

        tree_scroll_repartidores = tb.Scrollbar(self.lblframe_tree_repartidores, bootstyle='round-dark', orient=VERTICAL, command=self.tree_lista_repartidores.yview)
        tree_scroll_repartidores.grid(row=0, column=1, sticky=NSEW)

        self.tree_lista_repartidores.config(yscrollcommand=tree_scroll_repartidores.set)

        self.lblframe_tree_repartidores.columnconfigure(0, weight=1)

        self.cargar_repartidores()

    def agregar_repartidor(self):
        self.ventana_nuevo_repartidor = Toplevel(self)
        self.ventana_nuevo_repartidor.title("Nuevo Repartidor")

        lbl_nombre = tk.Label(self.ventana_nuevo_repartidor, text="Nombre:")
        lbl_nombre.pack(pady=5)
        self.entry_nombre_repartidor = tk.Entry(self.ventana_nuevo_repartidor)
        self.entry_nombre_repartidor.pack(pady=5)

        lbl_correo = tk.Label(self.ventana_nuevo_repartidor, text="Correo:")
        lbl_correo.pack(pady=5)
        self.entry_correo_repartidor = tk.Entry(self.ventana_nuevo_repartidor)
        self.entry_correo_repartidor.pack(pady=5)

        lbl_telefono = tk.Label(self.ventana_nuevo_repartidor, text="Teléfono:")
        lbl_telefono.pack(pady=5)
        self.entry_telefono_repartidor = tk.Entry(self.ventana_nuevo_repartidor)
        self.entry_telefono_repartidor.pack(pady=5)

        btn_guardar = ttk.Button(self.ventana_nuevo_repartidor, text="Guardar", command=self.guardar_repartidor)
        btn_guardar.pack(pady=10)

    def guardar_repartidor(self):
        nombre = self.entry_nombre_repartidor.get()
        correo = self.entry_correo_repartidor.get()
        telefono = self.entry_telefono_repartidor.get()

        if nombre and correo and telefono:
            try:
                self.conexion = mysql.connector.connect(
                    host="127.0.0.1",
                    user="root",
                    password="",
                    database="lasuertedelaolla",
                    port=3306
                )

                cursor = self.conexion.cursor()
                query = "INSERT INTO repartidor (nombre, correo, telefono) VALUES (%s, %s, %s)"
                cursor.execute(query, (nombre, correo, telefono))

                self.conexion.commit()
                # Guardar el mensaje en la tabla de registros
                mensaje = "Repartidor añadido exitosamente."
                query_registro = "INSERT INTO registros (mensaje) VALUES (%s)"
                cursor.execute(query_registro, (mensaje,))
                self.conexion.commit()

                cursor.close()
                self.conexion.close()
                
                messagebox.showinfo("Nuevo Repartidor", "Repartidor agregado exitosamente.")
                self.ventana_nuevo_repartidor.destroy()
                self.cargar_repartidores()

            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Error al conectar a la base de datos: {e}")
        else:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")

    def editar_repartidor(self):
        selected_item = self.tree_lista_repartidores.selection()
        if selected_item:
            item = self.tree_lista_repartidores.item(selected_item)
            values = item['values']

            self.ventana_editar_repartidores = Toplevel(self)
            self.ventana_editar_repartidores.title("Editar Repartidor")

            lbl_nombre = tk.Label(self.ventana_editar_repartidores, text="Nombre:")
            lbl_nombre.pack(pady=5)
            self.entry_nombre_editar_repartidor = tk.Entry(self.ventana_editar_repartidores)
            self.entry_nombre_editar_repartidor.pack(pady=5)
            self.entry_nombre_editar_repartidor.insert(0, values[1])

            lbl_correo = tk.Label(self.ventana_editar_repartidores, text="Correo:")
            lbl_correo.pack(pady=5)
            self.entry_correo_editar_repartidor = tk.Entry(self.ventana_editar_repartidores)
            self.entry_correo_editar_repartidor.pack(pady=5)
            self.entry_correo_editar_repartidor.insert(0, values[2])

            lbl_telefono = tk.Label(self.ventana_editar_repartidores, text="Teléfono:")
            lbl_telefono.pack(pady=5)
            self.entry_telefono_editar_repartidor = tk.Entry(self.ventana_editar_repartidores)
            self.entry_telefono_editar_repartidor.pack(pady=5)
            self.entry_telefono_editar_repartidor.insert(0, values[3])

            btn_guardar = ttk.Button(self.ventana_editar_repartidores, text="Guardar", command=lambda: self.guardar_cambios_repartidor(selected_item, values[0]))
            btn_guardar.pack(pady=10)
        else:
            messagebox.showwarning("Advertencia", "Seleccione un repartidor para editar")

    def guardar_cambios_repartidor(self, selected_item, repartidor_id):
        nombre = self.entry_nombre_editar_repartidor.get()
        correo = self.entry_correo_editar_repartidor.get()
        telefono = self.entry_telefono_editar_repartidor.get()

        if nombre and correo and telefono:
            try:
                self.conexion = mysql.connector.connect(
                    host="127.0.0.1",
                    user="root",
                    password="",
                    database="lasuertedelaolla",
                    port=3306
                )

                cursor = self.conexion.cursor()
                query = "UPDATE repartidor SET nombre=%s, correo=%s, telefono=%s WHERE id=%s"
                cursor.execute(query, (nombre, correo, telefono, repartidor_id))

                self.conexion.commit()
                # Guardar el mensaje en la tabla de registros
                mensaje = "Repartidor modificado exitosamente."
                query_registro = "INSERT INTO registros (mensaje) VALUES (%s)"
                cursor.execute(query_registro, (mensaje,))
                self.conexion.commit()

                cursor.close()
                self.conexion.close()
                
                messagebox.showinfo("Repartidor", "Repartidor editado exitosamente.")
                self.tree_lista_repartidores.item(selected_item, values=(repartidor_id, nombre, correo, telefono))
                self.ventana_editar_repartidores.destroy()
                self.cargar_repartidores()

            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Error al conectar a la base de datos: {e}")
        else:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")

    def eliminar_repartidor(self):
        selected_item = self.tree_lista_repartidores.selection()
        if selected_item:
            if messagebox.askyesno("Confirmar Eliminación", "¿Está seguro de eliminar el repartidor seleccionado?"):
                item = self.tree_lista_repartidores.item(selected_item)
                repartidor_id = item['values'][0]
                self.eliminar_repartidor_bd(repartidor_id)
                self.cargar_repartidores()
        else:
            messagebox.showwarning("Advertencia", "Seleccione un repartidor para eliminar")

    def eliminar_repartidor_bd(self, repartidor_id):
        if repartidor_id:
            try:
                self.conexion = mysql.connector.connect(
                    host="127.0.0.1",
                    user="root",
                    password="",
                    database="lasuertedelaolla",
                    port=3306
                )

                cursor = self.conexion.cursor()
                query = "DELETE FROM repartidor WHERE id = %s"
                cursor.execute(query, (repartidor_id,))

                self.conexion.commit()
                # Guardar el mensaje en la tabla de registros
                mensaje = "Repartidor eliminado exitosamente."
                query_registro = "INSERT INTO registros (mensaje) VALUES (%s)"
                cursor.execute(query_registro, (mensaje,))
                self.conexion.commit()

                cursor.close()
                self.conexion.close()
                

                messagebox.showinfo("Repartidor eliminado", "Repartidor eliminado exitosamente.")

            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Error al conectar a la base de datos: {e}")
        else:
            messagebox.showwarning("Advertencia", "No se ha podido identificar el repartidor a eliminar.")

    def cargar_repartidores(self):
        try:
            conexion = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="",
                database="lasuertedelaolla",
                port=3306
            )
            cursor = conexion.cursor()
            cursor.execute("SELECT id, nombre, correo, telefono FROM repartidor")

            for row in self.tree_lista_repartidores.get_children():
                self.tree_lista_repartidores.delete(row)

            for (id, nombre, correo, telefono) in cursor:
                self.tree_lista_repartidores.insert("", "end", values=(id, nombre, correo, telefono))

            cursor.close()
            conexion.close()
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def buscar_repartidores(self):
        termino_busqueda = self.txt_busqueda_repartidores.get().strip()
        if termino_busqueda:
            try:
                self.conexion = mysql.connector.connect(
                    host="127.0.0.1",
                    user="root",
                    password="",
                    database="lasuertedelaolla",
                    port=3306
                )

                cursor = self.conexion.cursor()
                query = """
                SELECT id,nombre,apellido, correo,telefono
                FROM repartidor
                WHERE id LIKE %s OR nombre LIKE %s OR apellido LIKE %s OR correo LIKE %s OR telefono LIKE %s 
                """
                cursor.execute(query, ("%"+termino_busqueda+"%", "%"+termino_busqueda+"%", "%"+termino_busqueda+"%", "%"+termino_busqueda+"%", "%"+termino_busqueda+"%"))
                repartidores = cursor.fetchall()

                cursor.close()
                self.conexion.close()

                for item in self.tree_lista_repartidores.get_children():
                    self.tree_lista_repartidores.delete(item)

                for repartidor in repartidores:
                    self.tree_lista_repartidores.insert("", "end", values=repartidor)

            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Error al conectar a la base de datos: {e}")
        else:
            self.cargar_repartidores()


    #------------------------------------------------------------------
    #COMENTARIOS

    def mostrar_comentarios(self):
        self.frame_lista_comentarios = Frame(self.frame_center)
        self.frame_lista_comentarios.grid(row=0, column=0, columnspan=2, padx=15, pady=15, sticky=NSEW)

        self.lblframe_botones_comentario = LabelFrame(self.frame_lista_comentarios)
        self.lblframe_botones_comentario.grid(row=0, column=0, padx=15, pady=15, sticky=NSEW)

        btn_nuevo_comentario = tb.Button(self.lblframe_botones_comentario, text="Nuevo", width=20, bootstyle="success", command=self.agregar_comentario)
        btn_nuevo_comentario.grid(row=0, column=0, padx=10, pady=10)

        btn_modificar_comentario = tb.Button(self.lblframe_botones_comentario, text="Modificar", width=20, bootstyle="info", command=self.editar_comentario)
        btn_modificar_comentario.grid(row=0, column=1, padx=10, pady=10)

        btn_eliminar_comentario = tb.Button(self.lblframe_botones_comentario, text="Eliminar", width=20, bootstyle="danger", command=self.eliminar_comentario)
        btn_eliminar_comentario.grid(row=0, column=2, padx=10, pady=10)

        self.lblframe_busqueda_comentarios = LabelFrame(self.frame_lista_comentarios, text="Buscar Comentarios")
        self.lblframe_busqueda_comentarios.grid(row=1, column=0, padx=15, pady=15, sticky=NSEW)

        self.txt_busqueda_comentarios = ttk.Entry(self.lblframe_busqueda_comentarios, width=150)
        self.txt_busqueda_comentarios.grid(row=0, column=0, padx=(10,0), pady=10, sticky=W)

        
        btn_buscar_comentarios = tb.Button(self.lblframe_busqueda_comentarios, text="🔍", width=3, command=self.buscar_comentarios)
        btn_buscar_comentarios.grid(row=0, column=1, padx=(0, 10), pady=10)


        self.lblframe_tree_comentarios = LabelFrame(self.frame_lista_comentarios)
        self.lblframe_tree_comentarios.grid(row=2, column=0, sticky=NSEW)

        columnas = ("id", "id_cliente", "id_producto", "comentario", "valoracion", "fecha")
        total_width = self.lblframe_tree_comentarios.winfo_width()  

        column_widths = {
            "id": int(total_width * 0.1),
            "id_cliente": int(total_width * 0.1),
            "id_producto": int(total_width * 0.1),
            "comentario": int(total_width * 0.3),
            "valoracion": int(total_width * 0.2),
            "fecha": int(total_width * 0.2)
        }

        self.tree_lista_comentarios = tb.Treeview(self.lblframe_tree_comentarios, columns=columnas, height=45, show="headings", bootstyle="dark")
        self.tree_lista_comentarios.grid(row=0, column=0, sticky=NSEW)

        self.tree_lista_comentarios.heading("id", text="Id", anchor=W)
        self.tree_lista_comentarios.heading("id_cliente", text="Id Cliente", anchor=W)
        self.tree_lista_comentarios.heading("id_producto", text="Id Producto", anchor=W)
        self.tree_lista_comentarios.heading("comentario", text="Comentario", anchor=W)
        self.tree_lista_comentarios.heading("valoracion", text="Valoracion", anchor=W)
        self.tree_lista_comentarios.heading("fecha", text="Fecha", anchor=W)

        self.tree_lista_comentarios['displaycolumns'] = ("id", "id_cliente", "id_producto", "comentario", "valoracion", "fecha")

        for col, width in column_widths.items():
            self.tree_lista_comentarios.column(col, width=width, minwidth=50)

        tree_scroll_comentarios = tb.Scrollbar(self.lblframe_tree_comentarios, bootstyle='round-dark', orient=VERTICAL, command=self.tree_lista_comentarios.yview)
        tree_scroll_comentarios.grid(row=0, column=1, sticky=NSEW)

        self.tree_lista_comentarios.config(yscrollcommand=tree_scroll_comentarios.set)

        self.lblframe_tree_comentarios.columnconfigure(0, weight=1)

        self.cargar_comentarios()

    def agregar_comentario(self):
        self.ventana_nuevo_comentario = Toplevel(self)
        self.ventana_nuevo_comentario.title("Nuevo Comentario")

        lbl_id_cliente = tk.Label(self.ventana_nuevo_comentario, text="Id Cliente:")
        lbl_id_cliente.pack(pady=5)
        self.entry_id_cliente_comentario = tk.Entry(self.ventana_nuevo_comentario)
        self.entry_id_cliente_comentario.pack(pady=5)

        lbl_id_producto = tk.Label(self.ventana_nuevo_comentario, text="Id Producto:")
        lbl_id_producto.pack(pady=5)
        self.entry_id_producto_comentario = tk.Entry(self.ventana_nuevo_comentario)
        self.entry_id_producto_comentario.pack(pady=5)

        lbl_comentario = tk.Label(self.ventana_nuevo_comentario, text="Comentario:")
        lbl_comentario.pack(pady=5)
        self.entry_comentario = tk.Entry(self.ventana_nuevo_comentario)
        self.entry_comentario.pack(pady=5)

        lbl_valoracion = tk.Label(self.ventana_nuevo_comentario, text="Valoracion:")
        lbl_valoracion.pack(pady=5)
        self.entry_valoracion_comentario = tk.Entry(self.ventana_nuevo_comentario)
        self.entry_valoracion_comentario.pack(pady=5)

        lbl_fecha = tk.Label(self.ventana_nuevo_comentario, text="Fecha:")
        lbl_fecha.pack(pady=5)
        self.entry_fecha_comentario = tk.Entry(self.ventana_nuevo_comentario)
        self.entry_fecha_comentario.pack(pady=5)

        btn_guardar = ttk.Button(self.ventana_nuevo_comentario, text="Guardar", command=self.guardar_comentario)
        btn_guardar.pack(pady=10)

    def guardar_comentario(self):
        id_cliente = self.entry_id_cliente_comentario.get()
        id_producto = self.entry_id_producto_comentario.get()
        comentario = self.entry_comentario.get()
        valoracion = self.entry_valoracion_comentario.get()
        fecha = self.entry_fecha_comentario.get()

        if id_cliente and id_producto and comentario and valoracion and fecha:
            try:
                self.conexion = mysql.connector.connect(
                    host="127.0.0.1",
                    user="root",
                    password="",
                    database="lasuertedelaolla",
                    port=3306
                )

                cursor = self.conexion.cursor()
                query = "INSERT INTO comentarios (id_cliente, id_producto, comentario, valoracion, fecha) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(query, (id_cliente, id_producto, comentario, valoracion, fecha))

                self.conexion.commit()
                # Guardar el mensaje en la tabla de registros
                mensaje = "Comentario añadido exitosamente."
                query_registro = "INSERT INTO registros (mensaje) VALUES (%s)"
                cursor.execute(query_registro, (mensaje,))
                self.conexion.commit()

                cursor.close()
                self.conexion.close()
                
                messagebox.showinfo("Nuevo Comentario", "Comentario agregado exitosamente.")
                self.ventana_nuevo_comentario.destroy()
                self.cargar_comentarios()

            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Error al conectar a la base de datos: {e}")
        else:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")

    def editar_comentario(self):
        selected_item = self.tree_lista_comentarios.selection()
        if selected_item:
            item = self.tree_lista_comentarios.item(selected_item)
            values = item['values']

            self.ventana_editar_comentarios = Toplevel(self)
            self.ventana_editar_comentarios.title("Editar Comentario")

            lbl_id_cliente = tk.Label(self.ventana_editar_comentarios, text="Id Cliente:")
            lbl_id_cliente.pack(pady=5)
            self.entry_id_cliente_editar_comentario = tk.Entry(self.ventana_editar_comentarios)
            self.entry_id_cliente_editar_comentario.pack(pady=5)
            self.entry_id_cliente_editar_comentario.insert(0, values[1])

            lbl_id_producto = tk.Label(self.ventana_editar_comentarios, text="Id Producto:")
            lbl_id_producto.pack(pady=5)
            self.entry_id_producto_editar_comentario = tk.Entry(self.ventana_editar_comentarios)
            self.entry_id_producto_editar_comentario.pack(pady=5)
            self.entry_id_producto_editar_comentario.insert(0, values[2])

            lbl_comentario = tk.Label(self.ventana_editar_comentarios, text="Comentario:")
            lbl_comentario.pack(pady=5)
            self.entry_comentario_editar_comentario = tk.Entry(self.ventana_editar_comentarios)
            self.entry_comentario_editar_comentario.pack(pady=5)
            self.entry_comentario_editar_comentario.insert(0, values[3])

            lbl_valoracion = tk.Label(self.ventana_editar_comentarios, text="Valoracion:")
            lbl_valoracion.pack(pady=5)
            self.entry_valoracion_editar_comentario = tk.Entry(self.ventana_editar_comentarios)
            self.entry_valoracion_editar_comentario.pack(pady=5)
            self.entry_valoracion_editar_comentario.insert(0, values[4])

            lbl_fecha = tk.Label(self.ventana_editar_comentarios, text="Fecha:")
            lbl_fecha.pack(pady=5)
            self.entry_fecha_editar_comentario = tk.Entry(self.ventana_editar_comentarios)
            self.entry_fecha_editar_comentario.pack(pady=5)
            self.entry_fecha_editar_comentario.insert(0, values[5])

            btn_guardar = ttk.Button(self.ventana_editar_comentarios, text="Guardar", command=lambda: self.actualizar_comentario(values[0]))
            btn_guardar.pack(pady=10)
        else:
            messagebox.showwarning("Advertencia", "Seleccione un comentario para editar")

    def actualizar_comentario(self, comentario_id):
        id_cliente = self.entry_id_cliente_editar_comentario.get()
        id_producto = self.entry_id_producto_editar_comentario.get()
        comentario = self.entry_comentario_editar_comentario.get()
        valoracion = self.entry_valoracion_editar_comentario.get()
        fecha = self.entry_fecha_editar_comentario.get()

        if id_cliente and id_producto and comentario and valoracion and fecha:
            try:
                self.conexion = mysql.connector.connect(
                    host="127.0.0.1",
                    user="root",
                    password="",
                    database="lasuertedelaolla",
                    port=3306
                )

                cursor = self.conexion.cursor()
                query = "UPDATE comentarios SET id_cliente=%s, id_producto=%s, comentario=%s, valoracion=%s, fecha=%s WHERE id=%s"
                cursor.execute(query, (id_cliente, id_producto, comentario, valoracion, fecha, comentario_id))

                self.conexion.commit()
                # Guardar el mensaje en la tabla de registros
                mensaje = "Comentario modificado/censurado exitosamente."
                query_registro = "INSERT INTO registros (mensaje) VALUES (%s)"
                cursor.execute(query_registro, (mensaje,))
                self.conexion.commit()

                cursor.close()
                self.conexion.close()
                
                messagebox.showinfo("Comentario", "Comentario actualizado exitosamente.")
                self.ventana_editar_comentarios.destroy()
                self.cargar_comentarios()

            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Error al conectar a la base de datos: {e}")
        else:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")

    def eliminar_comentario(self):
        selected_item = self.tree_lista_comentarios.selection()
        if selected_item:
            item = self.tree_lista_comentarios.item(selected_item)
            comentario_id = item['values'][0]

            confirmar = messagebox.askyesno("Confirmar Eliminación", "¿Está seguro de que desea eliminar este comentario?")
            if confirmar:
                try:
                    self.conexion = mysql.connector.connect(
                        host="127.0.0.1",
                        user="root",
                        password="",
                        database="lasuertedelaolla",
                        port=3306
                    )

                    cursor = self.conexion.cursor()
                    query = "DELETE FROM comentarios WHERE id=%s"
                    cursor.execute(query, (comentario_id,))

                    self.conexion.commit()
                    # Guardar el mensaje en la tabla de registros
                    mensaje = "Comentario eliminado exitosamente."
                    query_registro = "INSERT INTO registros (mensaje) VALUES (%s)"
                    cursor.execute(query_registro, (mensaje,))
                    self.conexion.commit()

                    cursor.close()
                    self.conexion.close()
                
                    messagebox.showinfo("Comentario", "Comentario eliminado exitosamente.")
                    self.tree_lista_comentarios.delete(selected_item)
                    self.cargar_comentarios()

                except mysql.connector.Error as e:
                    messagebox.showerror("Error", f"Error al conectar a la base de datos: {e}")
        else:
            messagebox.showwarning("Advertencia", "Seleccione un comentario para eliminar")

    def cargar_comentarios(self):
        try:
            self.conexion = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="",
                database="lasuertedelaolla",
                port=3306
            )

            cursor = self.conexion.cursor()
            query = "SELECT id, id_cliente, id_producto, comentario, valoracion, fecha FROM comentarios"
            cursor.execute(query)
            comentarios = cursor.fetchall()

            cursor.close()
            self.conexion.close()

            for item in self.tree_lista_comentarios.get_children():
                self.tree_lista_comentarios.delete(item)

            for comentario in comentarios:
                self.tree_lista_comentarios.insert("", "end", values=comentario)

        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Error al conectar a la base de datos: {e}")

    def buscar_comentarios(self):
        termino_busqueda = self.txt_busqueda_comentarios.get().strip()
        if termino_busqueda:
            try:
                self.conexion = mysql.connector.connect(
                    host="127.0.0.1",
                    user="root",
                    password="",
                    database="lasuertedelaolla",
                    port=3306
                )

                cursor = self.conexion.cursor()
                query = """
                SELECT id,id_cliente,id_producto,comentario,valoracion,fecha
                FROM comentarios
                WHERE id LIKE %s OR id_cliente LIKE %s OR id_producto LIKE %s OR comentario LIKE %s OR valoracion LIKE %s OR fecha LIKE %s
                """
                cursor.execute(query, ("%"+termino_busqueda+"%", "%"+termino_busqueda+"%", "%"+termino_busqueda+"%", "%"+termino_busqueda+"%", "%"+termino_busqueda+"%", "%"+termino_busqueda+"%"))
                comentarios = cursor.fetchall()

                cursor.close()
                self.conexion.close()

                for item in self.tree_lista_comentarios.get_children():
                    self.tree_lista_comentarios.delete(item)

                for comentario in comentarios:
                    self.tree_lista_comentarios.insert("", "end", values=comentario)

            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Error al conectar a la base de datos: {e}")
        else:
            self.cargar_comentarios()

    #--------------------------------------------------------------------
    #PROVEEDORES

    def ventana_proveedores(self):
        self.frame_lista_proveedores = Frame(self.frame_center)
        self.frame_lista_proveedores.grid(row=0, column=0, columnspan=2, padx=15, pady=15, sticky=NSEW)

        self.lblframe_botones_proveedores = LabelFrame(self.frame_lista_proveedores)
        self.lblframe_botones_proveedores.grid(row=0, column=0, padx=15, pady=15, sticky=NSEW)

        # Botones para nuevo, modificar y eliminar proveedores
        btn_nuevo_proveedor = tb.Button(self.lblframe_botones_proveedores, text="Nuevo", width=20, bootstyle="success", command=self.agregar_proveedor)
        btn_nuevo_proveedor.grid(row=0, column=0, padx=10, pady=10)

        btn_modificar_proveedor = ttk.Button(self.lblframe_botones_proveedores, text="Modificar", width=20, command=self.editar_proveedor)
        btn_modificar_proveedor.grid(row=0, column=1, padx=10, pady=10)

        btn_eliminar_proveedor = tb.Button(self.lblframe_botones_proveedores, text="Eliminar", width=20, bootstyle="danger", command=self.eliminar_proveedor)
        btn_eliminar_proveedor.grid(row=0, column=2, padx=10, pady=10)

        # Búsqueda de proveedores existentes
        self.lblframe_busqueda_proveedores = LabelFrame(self.frame_lista_proveedores, text="Buscar Proveedores")
        self.lblframe_busqueda_proveedores.grid(row=1, column=0, padx=15, pady=15, sticky=NSEW)

        self.txt_busqueda_proveedores = ttk.Entry(self.lblframe_busqueda_proveedores, width=150)
        self.txt_busqueda_proveedores.grid(row=0, column=0, padx=(10,0), pady=10, sticky=W)

        btn_buscar_proveedor = tb.Button(self.lblframe_busqueda_proveedores, text="🔍", width=3, command=self.buscar_proveedores)
        btn_buscar_proveedor.grid(row=0, column=1, padx=(0, 10), pady=10)


        # Vista de árbol para mostrar la lista de proveedores
        self.lblframe_tree_proveedores = LabelFrame(self.frame_lista_proveedores)
        self.lblframe_tree_proveedores.grid(row=2, column=0, sticky=NSEW)

        # Definición de las columnas manualmente acorde a la tabla de proveedores
        columnas = ("id", "nombre", "correo", "telefono")

        self.tree_lista_proveedores = tb.Treeview(self.lblframe_tree_proveedores, columns=columnas, height=75, show="headings", bootstyle="dark")
        self.tree_lista_proveedores.grid(row=0, column=0, sticky=NSEW)

        # Títulos de cada una de las columnas
        self.tree_lista_proveedores.heading("id", text="Id", anchor=W)
        self.tree_lista_proveedores.heading("nombre", text="Nombre", anchor=W)
        self.tree_lista_proveedores.heading("correo", text="Correo", anchor=W)
        self.tree_lista_proveedores.heading("telefono", text="Teléfono", anchor=W)
        # Configurar el ancho de cada columna
        self.tree_lista_proveedores.column("id", width=50, minwidth=50)
        self.tree_lista_proveedores.column("nombre", width=150, minwidth=100)
        self.tree_lista_proveedores.column("correo", width=300, minwidth=200)
        self.tree_lista_proveedores.column("telefono", width=100, minwidth=50)
        # Crear el scrollbar
        tree_scroll_proveedores = tb.Scrollbar(self.lblframe_tree_proveedores, bootstyle='round-dark', orient=VERTICAL, command=self.tree_lista_proveedores.yview)
        tree_scroll_proveedores.grid(row=0, column=1, sticky=NSEW)

        # Configuración del scroll
        self.tree_lista_proveedores.config(yscrollcommand=tree_scroll_proveedores.set)

        # Configuración de la expansión de columnas para utilizar todo el ancho disponible
        self.lblframe_tree_proveedores.columnconfigure(0, weight=1)  # Ajustar el tamaño del Treeview

        # Cargar los proveedores
        self.cargar_proveedores()

    def agregar_proveedor(self):
        self.ventana_nuevo_proveedor = Toplevel(self)
        self.ventana_nuevo_proveedor.title("Nuevo Proveedor")

        lbl_nombre = tk.Label(self.ventana_nuevo_proveedor, text="Nombre:")
        lbl_nombre.pack(pady=5)
        self.entry_nombre_proveedor = tk.Entry(self.ventana_nuevo_proveedor)
        self.entry_nombre_proveedor.pack(pady=5)

        lbl_correo = tk.Label(self.ventana_nuevo_proveedor, text="Correo:")
        lbl_correo.pack(pady=5)
        self.entry_correo_proveedor = tk.Entry(self.ventana_nuevo_proveedor)
        self.entry_correo_proveedor.pack(pady=5)

        lbl_telefono = tk.Label(self.ventana_nuevo_proveedor, text="Teléfono:")
        lbl_telefono.pack(pady=5)
        self.entry_telefono_proveedor = tk.Entry(self.ventana_nuevo_proveedor)
        self.entry_telefono_proveedor.pack(pady=5)

        btn_guardar = ttk.Button(self.ventana_nuevo_proveedor, text="Guardar", command=self.guardar_proveedor)
        btn_guardar.pack(pady=10)

    def guardar_proveedor(self):
        nombre = self.entry_nombre_proveedor.get()
        correo = self.entry_correo_proveedor.get()
        telefono = self.entry_telefono_proveedor.get()

        if nombre and correo and telefono:
            try:
                self.conexion = mysql.connector.connect(
                    host="127.0.0.1",
                    user="root",
                    password="",
                    database="lasuertedelaolla",
                    port=3306
                )

                cursor = self.conexion.cursor()
                query = "INSERT INTO proveedor (nombre, correo, telefono) VALUES (%s, %s, %s)"
                cursor.execute(query, (nombre, correo, telefono))

                self.conexion.commit()
                # Guardar el mensaje en la tabla de registros
                mensaje = "Proveedor añadido exitosamente."
                query_registro = "INSERT INTO registros (mensaje) VALUES (%s)"
                cursor.execute(query_registro, (mensaje,))
                self.conexion.commit()

                cursor.close()
                self.conexion.close()
                

                messagebox.showinfo("Nuevo Proveedor", "Proveedor agregado exitosamente.")
                self.ventana_nuevo_proveedor.destroy()
                self.cargar_proveedores()

            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Error al conectar a la base de datos: {e}")
        else:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")

    def editar_proveedor(self):
        selected_item = self.tree_lista_proveedores.selection()
        if selected_item:
            item = self.tree_lista_proveedores.item(selected_item)
            values = item['values']

            self.ventana_editar_proveedores = Toplevel(self)
            self.ventana_editar_proveedores.title("Editar Proveedor")

            lbl_nombre = tk.Label(self.ventana_editar_proveedores, text="Nombre:")
            lbl_nombre.pack(pady=5)
            self.entry_nombre_editar_proveedor = tk.Entry(self.ventana_editar_proveedores)
            self.entry_nombre_editar_proveedor.pack(pady=5)
            self.entry_nombre_editar_proveedor.insert(0, values[1])

            lbl_correo = tk.Label(self.ventana_editar_proveedores, text="Correo:")
            lbl_correo.pack(pady=5)
            self.entry_correo_editar_proveedor = tk.Entry(self.ventana_editar_proveedores)
            self.entry_correo_editar_proveedor.pack(pady=5)
            self.entry_correo_editar_proveedor.insert(0, values[2])

            lbl_telefono = tk.Label(self.ventana_editar_proveedores, text="Teléfono:")
            lbl_telefono.pack(pady=5)
            self.entry_telefono_editar_proveedor = tk.Entry(self.ventana_editar_proveedores)
            self.entry_telefono_editar_proveedor.pack(pady=5)
            self.entry_telefono_editar_proveedor.insert(0, values[3])

            btn_guardar = ttk.Button(self.ventana_editar_proveedores, text="Guardar", command=lambda: self.actualizar_proveedor(values[0]))
            btn_guardar.pack(pady=10)
        else:
            messagebox.showwarning("Advertencia", "Seleccione un proveedor para editar")

    def actualizar_proveedor(self, proveedor_id):
        nombre = self.entry_nombre_editar_proveedor.get()
        correo= self.entry_correo_editar_proveedor.get()
        telefono = self.entry_telefono_editar_proveedor.get()

        if nombre and correo and telefono:
            try:
                self.conexion = mysql.connector.connect(
                    host="127.0.0.1",
                    user="root",
                    password="",
                    database="lasuertedelaolla",
                    port=3306
                )

                cursor = self.conexion.cursor()
                query = "UPDATE proveedor SET nombre=%s, correo=%s, telefono=%s WHERE id=%s"
                cursor.execute(query, (nombre, correo, telefono, proveedor_id))

                self.conexion.commit()
                # Guardar el mensaje en la tabla de registros
                mensaje = "Proveedor actualizado exitosamente."
                query_registro = "INSERT INTO registros (mensaje) VALUES (%s)"
                cursor.execute(query_registro, (mensaje,))
                self.conexion.commit()

                cursor.close()
                self.conexion.close()
                
                messagebox.showinfo("Proveedor", "Proveedor actualizado exitosamente.")
                self.ventana_editar_proveedores.destroy()
                self.cargar_proveedores()

            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Error al conectar a la base de datos: {e}")
        else:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")

    def eliminar_proveedor(self):
        selected_item = self.tree_lista_proveedores.selection()
        if selected_item:
            item = self.tree_lista_proveedores.item(selected_item)
            proveedor_id = item['values'][0]

            confirmar = messagebox.askyesno("Confirmar Eliminación", "¿Está seguro de que desea eliminar este proveedor?")
            if confirmar:
                try:
                    self.conexion = mysql.connector.connect(
                        host="127.0.0.1",
                        user="root",
                        password="",
                        database="lasuertedelaolla",
                        port=3306
                    )

                    cursor = self.conexion.cursor()
                    query = "DELETE FROM proveedor WHERE id=%s"
                    cursor.execute(query, (proveedor_id,))

                    self.conexion.commit()
                    # Guardar el mensaje en la tabla de registros
                    mensaje = "Proveedor eliminado exitosamente."
                    query_registro = "INSERT INTO registros (mensaje) VALUES (%s)"
                    cursor.execute(query_registro, (mensaje,))
                    self.conexion.commit()

                    cursor.close()
                    self.conexion.close()
                

                    messagebox.showinfo("Proveedor", "Proveedor eliminado exitosamente.")
                    self.tree_lista_proveedores.delete(selected_item)
                    self.cargar_proveedores()

                except mysql.connector.Error as e:
                    messagebox.showerror("Error", f"Error al conectar a la base de datos: {e}")
        else:
            messagebox.showwarning("Advertencia", "Seleccione un proveedor para eliminar")

    def cargar_proveedores(self):
        try:
            self.conexion = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="",
                database="lasuertedelaolla",
                port=3306
            )

            cursor = self.conexion.cursor()
            query = "SELECT id, nombre, correo, telefono FROM proveedor"
            cursor.execute(query)
            proveedores = cursor.fetchall()

            cursor.close()
            self.conexion.close()

            for item in self.tree_lista_proveedores.get_children():
                self.tree_lista_proveedores.delete(item)

            for proveedor in proveedores:
                self.tree_lista_proveedores.insert("", "end", values=proveedor)

        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Error al conectar a la base de datos: {e}")

    def buscar_proveedores(self):
        termino_busqueda = self.txt_busqueda_proveedores.get().strip()
        if termino_busqueda:
            try:
                self.conexion = mysql.connector.connect(
                    host="127.0.0.1",
                    user="root",
                    password="",
                    database="lasuertedelaolla",
                    port=3306
                )

                cursor = self.conexion.cursor()
                query = """
                SELECT id, nombre, correo, telefono
                FROM proveedor 
                WHERE id LIKE %s OR nombre LIKE %s OR correo LIKE %s OR telefono LIKE %s
                """
                cursor.execute(query, ("%"+termino_busqueda+"%", "%"+termino_busqueda+"%", "%"+termino_busqueda+"%", "%"+termino_busqueda+"%"))
                proveedores = cursor.fetchall()

                cursor.close()
                self.conexion.close()

                for item in self.tree_lista_proveedores.get_children():
                    self.tree_lista_proveedores.delete(item)

                for proveedor in proveedores:
                    self.tree_lista_proveedores.insert("", "end", values=proveedor)

            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Error al conectar a la base de datos: {e}")
        else:
            self.cargar_proveedores()

    #---------------------------------------------------------------------
    #MESAS 
    def ventana_mesas(self):
        self.frame_lista_mesas = Frame(self.frame_center)
        self.frame_lista_mesas.grid(row=0, column=0, columnspan=2, padx=15, pady=15, sticky=NSEW)

        self.lblframe_botones_mesas = LabelFrame(self.frame_lista_mesas)
        self.lblframe_botones_mesas.grid(row=0, column=0, padx=15, pady=15, sticky=NSEW)

        # Botones para nueva, modificar y eliminar mesas
        btn_nueva_mesa = tb.Button(self.lblframe_botones_mesas, text="Nueva", width=20, bootstyle="success", command=self.nueva_mesa)
        btn_nueva_mesa.grid(row=0, column=0, padx=10, pady=10)

        btn_modificar_mesa = ttk.Button(self.lblframe_botones_mesas, text="Modificar", width=20, command=self.modificar_mesa)
        btn_modificar_mesa.grid(row=0, column=1, padx=10, pady=10)

        btn_eliminar_mesa = tb.Button(self.lblframe_botones_mesas, text="Eliminar", width=20, bootstyle="danger", command=self.eliminar_mesa)
        btn_eliminar_mesa.grid(row=0, column=2, padx=10, pady=10)

        # Búsqueda de mesas existentes
        self.lblframe_busqueda_mesas = LabelFrame(self.frame_lista_mesas, text="Buscar Mesas")
        self.lblframe_busqueda_mesas.grid(row=1, column=0, padx=15, pady=15, sticky=NSEW)

        self.txt_busqueda_mesas = ttk.Entry(self.lblframe_busqueda_mesas, width=150)
        self.txt_busqueda_mesas.grid(row=0, column=0, padx=(10,0), pady=10, sticky=W)

        btn_buscar_mesa = tb.Button(self.lblframe_busqueda_mesas, text="🔍", width=3, command=self.buscar_mesas)
        btn_buscar_mesa.grid(row=0, column=1, padx=(0, 10), pady=10)

        # Vista de árbol para mostrar la lista de mesas
        self.lblframe_tree_mesas = LabelFrame(self.frame_lista_mesas)
        self.lblframe_tree_mesas.grid(row=2, column=0, sticky=NSEW)

        # Definición de las columnas manualmente acorde a la tabla de mesas
        columnas = ("id", "descripcion", "capacidad", "estado")

        self.tree_lista_mesas = tb.Treeview(self.lblframe_tree_mesas, columns=columnas, height=75, show="headings", bootstyle="dark")
        self.tree_lista_mesas.grid(row=0, column=0, sticky=NSEW)

        # Títulos de cada una de las columnas
        self.tree_lista_mesas.heading("id", text="Id", anchor=W)
        self.tree_lista_mesas.heading("descripcion", text="Descripción", anchor=W)
        self.tree_lista_mesas.heading("capacidad", text="Capacidad", anchor=W)
        self.tree_lista_mesas.heading("estado", text="Estado", anchor=W)

        # Configurar el ancho de cada columna
        self.tree_lista_mesas.column("id", width=50, minwidth=50)
        self.tree_lista_mesas.column("descripcion", width=150, minwidth=100)
        self.tree_lista_mesas.column("capacidad", width=300, minwidth=200)
        self.tree_lista_mesas.column("estado", width=150, minwidth=100)

        # Crear el scrollbar
        tree_scroll_mesas = tb.Scrollbar(self.lblframe_tree_mesas, bootstyle='round-dark', orient=VERTICAL, command=self.tree_lista_mesas.yview)
        tree_scroll_mesas.grid(row=0, column=1, sticky=NSEW)

        # Configuración del scroll
        self.tree_lista_mesas.config(yscrollcommand=tree_scroll_mesas.set)

        # Configuración de la expansión de columnas para utilizar todo el ancho disponible
        self.lblframe_tree_mesas.columnconfigure(0, weight=1)  # Ajustar el tamaño del Treeview

        # Cargar las mesas
        self.cargar_mesas()

    def nueva_mesa(self):
        self.ventana_nueva_mesa = Toplevel(self)
        self.ventana_nueva_mesa.title("Nueva Mesa")

        lbl_descripcion = tk.Label(self.ventana_nueva_mesa, text="Descripción:")
        lbl_descripcion.pack(pady=5)
        self.entry_descripcion_mesa = tk.Entry(self.ventana_nueva_mesa)
        self.entry_descripcion_mesa.pack(pady=5)

        lbl_capacidad = tk.Label(self.ventana_nueva_mesa, text="Capacidad:")
        lbl_capacidad.pack(pady=5)
        self.entry_capacidad_mesa = tk.Entry(self.ventana_nueva_mesa)
        self.entry_capacidad_mesa.pack(pady=5)

        lbl_estado = tk.Label(self.ventana_nueva_mesa, text="Estado:")
        lbl_estado.pack(pady=5)
        self.entry_estado_mesa = tk.Entry(self.ventana_nueva_mesa)
        self.entry_estado_mesa.pack(pady=5)

        btn_guardar = ttk.Button(self.ventana_nueva_mesa, text="Guardar", command=self.guardar_mesa)
        btn_guardar.pack(pady=10)

    def guardar_mesa(self):
        descripcion = self.entry_descripcion_mesa.get()
        capacidad = self.entry_capacidad_mesa.get()
        estado = self.entry_estado_mesa.get()

        if descripcion and capacidad and estado:
            if estado.lower() not in ["libre", "ocupado"]:
                messagebox.showwarning("Advertencia", "El estado debe ser 'libre' o 'ocupado'.")
                return

            try:
                self.conexion = mysql.connector.connect(
                    host="127.0.0.1",
                    user="root",
                    password="",
                    database="lasuertedelaolla",
                    port=3306
                )

                cursor = self.conexion.cursor()
                query = "INSERT INTO mesa (descripcion, capacidad, estado) VALUES (%s, %s, %s)"
                cursor.execute(query, (descripcion, capacidad, estado))

                self.conexion.commit()
                # Guardar el mensaje en la tabla de registros
                mensaje = "Mesa añadida exitosamente."
                query_registro = "INSERT INTO registros (mensaje) VALUES (%s)"
                cursor.execute(query_registro, (mensaje,))
                self.conexion.commit()

                cursor.close()
                self.conexion.close()
                
                messagebox.showinfo("Nueva Mesa", "Mesa agregada exitosamente.")
                self.ventana_nueva_mesa.destroy()
                self.cargar_mesas()

            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Error al conectar a la base de datos: {e}")
        else:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")

    def modificar_mesa(self):
        selected_item = self.tree_lista_mesas.selection()
        if selected_item:
            item = self.tree_lista_mesas.item(selected_item)
            values = item['values']

            self.ventana_editar_mesa = Toplevel(self)
            self.ventana_editar_mesa.title("Editar Mesa")

            lbl_descripcion = tk.Label(self.ventana_editar_mesa, text="Descripción:")
            lbl_descripcion.pack(pady=5)
            self.entry_descripcion_editar_mesa = tk.Entry(self.ventana_editar_mesa)
            self.entry_descripcion_editar_mesa.pack(pady=5)
            self.entry_descripcion_editar_mesa.insert(0, values[1])

            lbl_capacidad = tk.Label(self.ventana_editar_mesa, text="Capacidad:")
            lbl_capacidad.pack(pady=5)
            self.entry_capacidad_editar_mesa = tk.Entry(self.ventana_editar_mesa)
            self.entry_capacidad_editar_mesa.pack(pady=5)
            self.entry_capacidad_editar_mesa.insert(0, values[2])

            lbl_estado = tk.Label(self.ventana_editar_mesa, text="Estado:")
            lbl_estado.pack(pady=5)
            self.entry_estado_editar_mesa = tk.Entry(self.ventana_editar_mesa)
            self.entry_estado_editar_mesa.pack(pady=5)
            self.entry_estado_editar_mesa.insert(0, values[3])

            btn_guardar = ttk.Button(self.ventana_editar_mesa, text="Guardar", command=lambda: self.actualizar_mesa(values[0]))
            btn_guardar.pack(pady=10)
        else:
            messagebox.showwarning("Advertencia", "Seleccione una mesa para editar")

    def actualizar_mesa(self, mesa_id):
        descripcion = self.entry_descripcion_editar_mesa.get()
        capacidad = self.entry_capacidad_editar_mesa.get()
        estado = self.entry_estado_editar_mesa.get()

        if descripcion and capacidad and estado:
            if estado.lower() not in ["libre", "ocupado"]:
                messagebox.showwarning("Advertencia", "El estado debe ser 'libre' o 'ocupado'.")
                return

            try:
                self.conexion = mysql.connector.connect(
                    host="127.0.0.1",
                    user="root",
                    password="",
                    database="lasuertedelaolla",
                    port=3306
                )

                cursor = self.conexion.cursor()
                query = "UPDATE mesa SET descripcion=%s, capacidad=%s, estado=%s WHERE id=%s"
                cursor.execute(query, (descripcion, capacidad, estado, mesa_id))

                self.conexion.commit()
                # Guardar el mensaje en la tabla de registros
                mensaje = "Mesa actualizada exitosamente."
                query_registro = "INSERT INTO registros (mensaje) VALUES (%s)"
                cursor.execute(query_registro, (mensaje,))
                self.conexion.commit()

                cursor.close()
                self.conexion.close()

                messagebox.showinfo("Mesa", "Mesa actualizada exitosamente.")
                self.ventana_editar_mesa.destroy()
                self.cargar_mesas()

            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Error al conectar a la base de datos: {e}")
        else:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")

    def eliminar_mesa(self):
        selected_item = self.tree_lista_mesas.selection()
        if selected_item:
            item = self.tree_lista_mesas.item(selected_item)
            mesa_id = item['values'][0]

            confirmar = messagebox.askyesno("Confirmar Eliminación", "¿Está seguro de que desea eliminar esta mesa?")
            if confirmar:
                try:
                    self.conexion = mysql.connector.connect(
                        host="127.0.0.1",
                        user="root",
                        password="",
                        database="lasuertedelaolla",
                        port=3306
                    )

                    cursor = self.conexion.cursor()
                    query = "DELETE FROM mesa WHERE id=%s"
                    cursor.execute(query, (mesa_id,))

                    self.conexion.commit()
                    # Guardar el mensaje en la tabla de registros
                    mensaje = "Mesa eliminada exitosamente."
                    query_registro = "INSERT INTO registros (mensaje) VALUES (%s)"
                    cursor.execute(query_registro, (mensaje,))
                    self.conexion.commit()

                    cursor.close()
                    self.conexion.close()
                

                    messagebox.showinfo("Mesa", "Mesa eliminada exitosamente.")
                    self.tree_lista_mesas.delete(selected_item)
                    self.cargar_mesas()

                except mysql.connector.Error as e:
                    messagebox.showerror("Error", f"Error al conectar a la base de datos: {e}")
        else:
            messagebox.showwarning("Advertencia", "Seleccione una mesa para eliminar")

    def cargar_mesas(self):
        try:
            self.conexion = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="",
                database="lasuertedelaolla",
                port=3306
            )

            cursor = self.conexion.cursor()
            query = "SELECT id, descripcion, capacidad, estado FROM mesa"
            cursor.execute(query)
            mesas = cursor.fetchall()

            cursor.close()
            self.conexion.close()

            for item in self.tree_lista_mesas.get_children():
                self.tree_lista_mesas.delete(item)

            for mesa in mesas:
                self.tree_lista_mesas.insert("", "end", values=mesa)

        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Error al conectar a la base de datos: {e}")

    def buscar_mesas(self):
        termino_busqueda = self.txt_busqueda_mesas.get().strip()
        if termino_busqueda:
            try:
                self.conexion = mysql.connector.connect(
                    host="127.0.0.1",
                    user="root",
                    password="",
                    database="lasuertedelaolla",
                    port=3306
                )

                cursor = self.conexion.cursor()
                query = """
                SELECT id, descripcion, capacidad, estado 
                FROM mesa 
                WHERE id LIKE %s OR descripcion LIKE %s OR capacidad LIKE %s OR estado LIKE %s
                """
                cursor.execute(query, ("%"+termino_busqueda+"%", "%"+termino_busqueda+"%", "%"+termino_busqueda+"%", "%"+termino_busqueda+"%"))
                mesas = cursor.fetchall()

                cursor.close()
                self.conexion.close()

                for item in self.tree_lista_mesas.get_children():
                    self.tree_lista_mesas.delete(item)

                for mesa in mesas:
                    self.tree_lista_mesas.insert("", "end", values=mesa)

            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Error al conectar a la base de datos: {e}")
        else:
            self.cargar_mesas()

    #----------------------------------------------------------------------
    #RESERVAS

    def ventana_reservas(self):
        self.frame_lista_reservas = Frame(self.frame_center)
        self.frame_lista_reservas.grid(row=0, column=0, columnspan=2, padx=15, pady=15, sticky=NSEW)

        self.lblframe_botones_reservas = LabelFrame(self.frame_lista_reservas)
        self.lblframe_botones_reservas.grid(row=0, column=0, padx=15, pady=15, sticky=NSEW)

        # Botones para nueva, modificar y eliminar reservas
        btn_nueva_reserva = tb.Button(self.lblframe_botones_reservas, text="Nueva", width=20, bootstyle="success", command=self.nueva_reserva)
        btn_nueva_reserva.grid(row=0, column=0, padx=10, pady=10)

        btn_modificar_reserva = ttk.Button(self.lblframe_botones_reservas, text="Modificar", width=20, command=self.modificar_reserva)
        btn_modificar_reserva.grid(row=0, column=1, padx=10, pady=10)

        btn_eliminar_reserva = tb.Button(self.lblframe_botones_reservas, text="Eliminar", width=20, bootstyle="danger", command=self.eliminar_reserva)
        btn_eliminar_reserva.grid(row=0, column=2, padx=10, pady=10)

        # Búsqueda de reservas existentes
        self.lblframe_busqueda_reservas = LabelFrame(self.frame_lista_reservas, text="Buscar Reservas")
        self.lblframe_busqueda_reservas.grid(row=1, column=0, padx=15, pady=15, sticky=NSEW)

        self.txt_busqueda_reservas = ttk.Entry(self.lblframe_busqueda_reservas, width=150)
        self.txt_busqueda_reservas.grid(row=0, column=0, padx=(10, 0), pady=10, sticky=W)


        btn_buscar_reserva = tb.Button(self.lblframe_busqueda_reservas, text="🔍", width=3, command=self.buscar_reserva)
        btn_buscar_reserva.grid(row=0, column=1, padx=(0, 10), pady=10)

        # Vista de árbol para mostrar la lista de reservas
        self.lblframe_tree_reservas = LabelFrame(self.frame_lista_reservas)
        self.lblframe_tree_reservas.grid(row=2, column=0, sticky=NSEW)

        # Definición de las columnas manualmente acorde a la tabla de reservas
        columnas = ("id", "id_cliente", "id_mesa", "fecha", "cantidad_personas")

        self.tree_lista_reservas = tb.Treeview(self.lblframe_tree_reservas, columns=columnas, height=75, show="headings", bootstyle="dark")
        self.tree_lista_reservas.grid(row=0, column=0, sticky=NSEW)

        # Títulos de cada una de las columnas
        self.tree_lista_reservas.heading("id", text="Id", anchor=W)
        self.tree_lista_reservas.heading("id_cliente", text="Id cliente", anchor=W)
        self.tree_lista_reservas.heading("id_mesa", text="Id mesa", anchor=W)
        self.tree_lista_reservas.heading("fecha", text="Fecha", anchor=W)
        self.tree_lista_reservas.heading("cantidad_personas", text="Cantidad personas", anchor=W)
        # Configurar el ancho de cada columna
        self.tree_lista_reservas.column("id", width=50, minwidth=50)
        self.tree_lista_reservas.column("id_cliente", width=150, minwidth=100)
        self.tree_lista_reservas.column("id_mesa", width=100, minwidth=50)
        self.tree_lista_reservas.column("fecha", width=100, minwidth=50)
        self.tree_lista_reservas.column("cantidad_personas", width=50, minwidth=50)
        # Crear el scrollbar
        tree_scroll_reservas = tb.Scrollbar(self.lblframe_tree_reservas, bootstyle='round-dark', orient=VERTICAL, command=self.tree_lista_reservas.yview)
        tree_scroll_reservas.grid(row=0, column=1, sticky=NSEW)

        # Configuración del scroll
        self.tree_lista_reservas.config(yscrollcommand=tree_scroll_reservas.set)

        # Configuración de la expansión de columnas para utilizar todo el ancho disponible
        self.lblframe_tree_reservas.columnconfigure(0, weight=1)  # Ajustar el tamaño del Treeview

        # Cargar las reservas
        self.cargar_reservas()

    def nueva_reserva(self):
        self.ventana_nueva_reserva = Toplevel(self)
        self.ventana_nueva_reserva.title("Nueva Reserva")

        lbl_id_cliente = tk.Label(self.ventana_nueva_reserva, text="Id Cliente:")
        lbl_id_cliente.pack(pady=5)
        self.entry_id_cliente_reserva = tk.Entry(self.ventana_nueva_reserva)
        self.entry_id_cliente_reserva.pack(pady=5)

        lbl_id_mesa = tk.Label(self.ventana_nueva_reserva, text="Id Mesa:")
        lbl_id_mesa.pack(pady=5)
        self.entry_id_mesa_reserva = tk.Entry(self.ventana_nueva_reserva)
        self.entry_id_mesa_reserva.pack(pady=5)

        lbl_fecha = tk.Label(self.ventana_nueva_reserva, text="Fecha:")
        lbl_fecha.pack(pady=5)
        self.entry_fecha_reserva = tk.Entry(self.ventana_nueva_reserva)
        self.entry_fecha_reserva.pack(pady=5)

        lbl_cantidad_personas = tk.Label(self.ventana_nueva_reserva, text="Cantidad de Personas:")
        lbl_cantidad_personas.pack(pady=5)
        self.entry_cantidad_personas_reserva = tk.Entry(self.ventana_nueva_reserva)
        self.entry_cantidad_personas_reserva.pack(pady=5)

        btn_guardar = ttk.Button(self.ventana_nueva_reserva, text="Guardar", command=self.guardar_reserva)
        btn_guardar.pack(pady=10)

    def guardar_reserva(self):
        id_cliente = self.entry_id_cliente_reserva.get()
        id_mesa = self.entry_id_mesa_reserva.get()
        fecha = self.entry_fecha_reserva.get()
        cantidad_personas = self.entry_cantidad_personas_reserva.get()

        if id_cliente and id_mesa and fecha and cantidad_personas:
            try:
                self.conexion = mysql.connector.connect(
                    host="127.0.0.1",
                    user="root",
                    password="",
                    database="lasuertedelaolla",
                    port=3306
                )

                cursor = self.conexion.cursor()
                query = "INSERT INTO reserva (id_cliente, id_mesa, fecha, cantidad_personas) VALUES (%s, %s, %s, %s)"
                cursor.execute(query, (id_cliente, id_mesa, fecha, cantidad_personas))

                self.conexion.commit()
                # Guardar el mensaje en la tabla de registros
                mensaje = "Reserva añadida exitosamente."
                query_registro = "INSERT INTO registros (mensaje) VALUES (%s)"
                cursor.execute(query_registro, (mensaje,))
                self.conexion.commit()

                cursor.close()
                self.conexion.close()
                

                messagebox.showinfo("Nueva Reserva", "Reserva agregada exitosamente.")
                self.ventana_nueva_reserva.destroy()
                self.cargar_reservas()

            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Error al conectar a la base de datos: {e}")
        else:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")

    def modificar_reserva(self):
        selected_item = self.tree_lista_reservas.selection()
        if selected_item:
            item = self.tree_lista_reservas.item(selected_item)
            values = item['values']

            self.ventana_editar_reserva = Toplevel(self)
            self.ventana_editar_reserva.title("Editar Reserva")

            lbl_id_cliente = tk.Label(self.ventana_editar_reserva, text="Id Cliente:")
            lbl_id_cliente.pack(pady=5)
            self.entry_id_cliente_editar_reserva = tk.Entry(self.ventana_editar_reserva)
            self.entry_id_cliente_editar_reserva.pack(pady=5)
            self.entry_id_cliente_editar_reserva.insert(0, values[1])

            lbl_id_mesa = tk.Label(self.ventana_editar_reserva, text="Id Mesa:")
            lbl_id_mesa.pack(pady=5)
            self.entry_id_mesa_editar_reserva = tk.Entry(self.ventana_editar_reserva)
            self.entry_id_mesa_editar_reserva.pack(pady=5)
            self.entry_id_mesa_editar_reserva.insert(0, values[2])

            lbl_fecha = tk.Label(self.ventana_editar_reserva, text="Fecha:")
            lbl_fecha.pack(pady=5)
            self.entry_fecha_editar_reserva = tk.Entry(self.ventana_editar_reserva)
            self.entry_fecha_editar_reserva.pack(pady=5)
            self.entry_fecha_editar_reserva.insert(0, values[3])

            lbl_cantidad_personas = tk.Label(self.ventana_editar_reserva, text="Cantidad de Personas:")
            lbl_cantidad_personas.pack(pady=5)
            self.entry_cantidad_personas_editar_reserva = tk.Entry(self.ventana_editar_reserva)
            self.entry_cantidad_personas_editar_reserva.pack(pady=5)
            self.entry_cantidad_personas_editar_reserva.insert(0, values[4])

            btn_guardar = ttk.Button(self.ventana_editar_reserva, text="Guardar", command=lambda: self.actualizar_reserva(values[0]))
            btn_guardar.pack(pady=10)
        else:
            messagebox.showwarning("Advertencia", "Seleccione una reserva para editar")

    def actualizar_reserva(self, reserva_id):
        id_cliente = self.entry_id_cliente_editar_reserva.get()
        id_mesa = self.entry_id_mesa_editar_reserva.get()
        fecha = self.entry_fecha_editar_reserva.get()
        cantidad_personas = self.entry_cantidad_personas_editar_reserva.get()

        if id_cliente and id_mesa and fecha and cantidad_personas:
            try:
                self.conexion = mysql.connector.connect(
                    host="127.0.0.1",
                    user="root",
                    password="",
                    database="lasuertedelaolla",
                    port=3306
                )

                cursor = self.conexion.cursor()
                query = "UPDATE reserva SET id_cliente=%s, id_mesa=%s, fecha=%s, cantidad_personas=%s WHERE id=%s"
                cursor.execute(query, (id_cliente, id_mesa, fecha, cantidad_personas, reserva_id))

                self.conexion.commit()
                # Guardar el mensaje en la tabla de registros
                mensaje = "Reserva modificada exitosamente."
                query_registro = "INSERT INTO registros (mensaje) VALUES (%s)"
                cursor.execute(query_registro, (mensaje,))
                self.conexion.commit()

                cursor.close()
                self.conexion.close()
                
                messagebox.showinfo("Reserva", "Reserva actualizada exitosamente.")
                self.ventana_editar_reserva.destroy()
                self.cargar_reservas()

            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Error al conectar a la base de datos: {e}")
        else:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")

    def eliminar_reserva(self):
        selected_item = self.tree_lista_reservas.selection()
        if selected_item:
            item = self.tree_lista_reservas.item(selected_item)
            reserva_id = item['values'][0]

            confirmar = messagebox.askyesno("Confirmar Eliminación", "¿Está seguro de que desea eliminar esta reserva?")
            if confirmar:
                try:
                    self.conexion = mysql.connector.connect(
                        host="127.0.0.1",
                        user="root",
                        password="",
                        database="lasuertedelaolla",
                        port=3306
                    )

                    cursor = self.conexion.cursor()
                    query = "DELETE FROM reserva WHERE id=%s"
                    cursor.execute(query, (reserva_id,))

                    self.conexion.commit()
                    # Guardar el mensaje en la tabla de registros
                    mensaje = "Reserva eliminada exitosamente."
                    query_registro = "INSERT INTO registros (mensaje) VALUES (%s)"
                    cursor.execute(query_registro, (mensaje,))
                    self.conexion.commit()

                    cursor.close()
                    self.conexion.close()
                    

                    messagebox.showinfo("Reserva", "Reserva eliminada exitosamente.")
                    self.tree_lista_reservas.delete(selected_item)
                    self.cargar_reservas()

                except mysql.connector.Error as e:
                    messagebox.showerror("Error", f"Error al conectar a la base de datos: {e}")
        else:
            messagebox.showwarning("Advertencia", "Seleccione una reserva para eliminar")

    def cargar_reservas(self):
        try:
            self.conexion = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="",
                database="lasuertedelaolla",
                port=3306
            )

            cursor = self.conexion.cursor()
            query = "SELECT id, id_cliente, id_mesa, fecha, cantidad_personas FROM reserva"
            cursor.execute(query)
            reservas = cursor.fetchall()

            cursor.close()
            self.conexion.close()

            for item in self.tree_lista_reservas.get_children():
                self.tree_lista_reservas.delete(item)

            for reserva in reservas:
                self.tree_lista_reservas.insert("", "end", values=reserva)

        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Error al conectar a la base de datos: {e}")

    def buscar_reserva(self):
        termino_busqueda = self.txt_busqueda_reservas.get().strip()
        if termino_busqueda:
            try:
                self.conexion = mysql.connector.connect(
                    host="127.0.0.1",
                    user="root",
                    password="",
                    database="lasuertedelaolla",
                    port=3306
                )

                cursor = self.conexion.cursor()
                query = """
                SELECT id, id_cliente, id_mesa, fecha, cantidad_personas 
                FROM reserva 
                WHERE id_cliente LIKE %s OR id_mesa LIKE %s OR fecha LIKE %s OR cantidad_personas LIKE %s
                """
                cursor.execute(query, ("%"+termino_busqueda+"%", "%"+termino_busqueda+"%", "%"+termino_busqueda+"%", "%"+termino_busqueda+"%"))
                reservas = cursor.fetchall()

                cursor.close()
                self.conexion.close()

                for item in self.tree_lista_reservas.get_children():
                    self.tree_lista_reservas.delete(item)

                for reserva in reservas:
                    self.tree_lista_reservas.insert("", "end", values=reserva)

            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Error al conectar a la base de datos: {e}")
        else:
            self.cargar_reservas()  # Cargar todas las reservas si no hay término de búsqueda

    #---------------------------------------------------------------------
    #PROMOCIONES

    def ventana_promociones(self):
        self.frame_lista_promociones = Frame(self.frame_center)
        self.frame_lista_promociones.grid(row=0, column=0, columnspan=2, padx=15, pady=15, sticky=NSEW)

        self.lblframe_botones_promociones = LabelFrame(self.frame_lista_promociones)
        self.lblframe_botones_promociones.grid(row=0, column=0, padx=15, pady=15, sticky=NSEW)

        btn_nuevo_promociones = tb.Button(self.lblframe_botones_promociones, text="Nuevo", width=20, bootstyle="success", command=self.nueva_promocion)
        btn_nuevo_promociones.grid(row=0, column=0, padx=10, pady=10)

        btn_modificar_promociones = tb.Button(self.lblframe_botones_promociones, text="Modificar", width=20, bootstyle="info", command=self.modificar_promocion)
        btn_modificar_promociones.grid(row=0, column=1, padx=10, pady=10)

        btn_eliminar_promociones = tb.Button(self.lblframe_botones_promociones, text="Eliminar", width=20, bootstyle="danger", command=self.eliminar_promocion)
        btn_eliminar_promociones.grid(row=0, column=2, padx=10, pady=10)

        self.lblframe_busqueda_promociones = LabelFrame(self.frame_lista_promociones, text="Buscar Promociones")
        self.lblframe_busqueda_promociones.grid(row=1, column=0, padx=15, pady=15, sticky=NSEW)

        self.txt_busqueda_promociones = ttk.Entry(self.lblframe_busqueda_promociones, width=150)
        self.txt_busqueda_promociones.grid(row=0, column=0,padx=(10,0), pady=10, sticky=W)

        btn_buscar_promocion = tb.Button(self.lblframe_busqueda_promociones, text="🔍", width=3, command=self.buscar_promociones)
        btn_buscar_promocion.grid(row=0, column=1, padx=(0, 10), pady=10)


        self.lblframe_tree_promociones = LabelFrame(self.frame_lista_promociones)
        self.lblframe_tree_promociones.grid(row=2, column=0, sticky=NSEW)

        columnas = ("id", "nombre", "descripcion", "descuento", "fecha_inicio", "fecha_fin")
        total_width = self.lblframe_tree_promociones.winfo_width()  

        column_widths = {
            "id": int(total_width * 0.1),
            "nombre": int(total_width * 0.2),
            "descripcion": int(total_width * 0.3),
            "descuento": int(total_width * 0.1),
            "fecha_inicio": int(total_width * 0.15),
            "fecha_fin": int(total_width * 0.15)
        }

        self.tree_lista_promociones = tb.Treeview(self.lblframe_tree_promociones, columns=columnas, height=175, show="headings", bootstyle="dark")
        self.tree_lista_promociones.grid(row=0, column=0, sticky=NSEW)

        self.tree_lista_promociones.heading("id", text="ID", anchor=W)
        self.tree_lista_promociones.heading("nombre", text="Nombre", anchor=W)
        self.tree_lista_promociones.heading("descripcion", text="Descripción", anchor=W)
        self.tree_lista_promociones.heading("descuento", text="Descuento (%)", anchor=W)
        self.tree_lista_promociones.heading("fecha_inicio", text="Fecha de Inicio", anchor=W)
        self.tree_lista_promociones.heading("fecha_fin", text="Fecha de Fin", anchor=W)

        self.tree_lista_promociones['displaycolumns'] = ("id", "nombre", "descripcion", "descuento", "fecha_inicio", "fecha_fin")

        for col, width in column_widths.items():
            self.tree_lista_promociones.column(col, width=width, minwidth=50)

        tree_scroll_promociones = tb.Scrollbar(self.lblframe_tree_promociones, bootstyle='round-dark', orient=VERTICAL, command=self.tree_lista_promociones.yview)
        tree_scroll_promociones.grid(row=0, column=1, sticky=NSEW)

        self.tree_lista_promociones.config(yscrollcommand=tree_scroll_promociones.set)

        self.lblframe_tree_promociones.columnconfigure(0, weight=1)

        self.cargar_promociones()

    def nueva_promocion(self):
        # Crear una nueva ventana para ingresar los datos de la nueva promoción
        self.ventana_nueva_promocion = Toplevel(self)
        self.ventana_nueva_promocion.title("Nueva Promoción")
        
        # Campos para ingresar los datos de la nueva promoción
        lbl_nombre = Label(self.ventana_nueva_promocion, text="Nombre:")
        lbl_nombre.grid(row=0, column=0, padx=10, pady=10)
        self.txt_nombre = Entry(self.ventana_nueva_promocion, width=30)
        self.txt_nombre.grid(row=0, column=1, padx=10, pady=10)
        
        lbl_descripcion = Label(self.ventana_nueva_promocion, text="Descripción:")
        lbl_descripcion.grid(row=1, column=0, padx=10, pady=10)
        self.txt_descripcion = Entry(self.ventana_nueva_promocion, width=30)
        self.txt_descripcion.grid(row=1, column=1, padx=10, pady=10)
        
        lbl_descuento = Label(self.ventana_nueva_promocion, text="Descuento (%):")
        lbl_descuento.grid(row=2, column=0, padx=10, pady=10)
        self.txt_descuento = Entry(self.ventana_nueva_promocion, width=30)
        self.txt_descuento.grid(row=2, column=1, padx=10, pady=10)
        
        lbl_fecha_inicio = Label(self.ventana_nueva_promocion, text="Fecha de Inicio (YYYY-MM-DD):")
        lbl_fecha_inicio.grid(row=3, column=0, padx=10, pady=10)
        self.txt_fecha_inicio = Entry(self.ventana_nueva_promocion, width=30)
        self.txt_fecha_inicio.grid(row=3, column=1, padx=10, pady=10)
        
        lbl_fecha_fin = Label(self.ventana_nueva_promocion, text="Fecha de Fin (YYYY-MM-DD):")
        lbl_fecha_fin.grid(row=4, column=0, padx=10, pady=10)
        self.txt_fecha_fin = Entry(self.ventana_nueva_promocion, width=30)
        self.txt_fecha_fin.grid(row=4, column=1, padx=10, pady=10)

        # Botón para guardar la nueva promoción
        btn_guardar = ttk.Button(self.ventana_nueva_promocion, text="Guardar", command=self.guardar_nueva_promocion)
        btn_guardar.grid(row=5, column=0, columnspan=2, padx=10, pady=10)
    
    def guardar_nueva_promocion(self):
        # Obtener los valores de los campos de la nueva promoción
        nombre = self.txt_nombre.get()
        descripcion = self.txt_descripcion.get()
        descuento = self.txt_descuento.get()
        fecha_inicio = self.txt_fecha_inicio.get()
        fecha_fin = self.txt_fecha_fin.get()

        # Validar que todos los campos estén completos
        if nombre and descripcion and descuento and fecha_inicio and fecha_fin:
            try:
                # Conectar a la base de datos
                conexion = mysql.connector.connect(
                    host="127.0.0.1",
                    user="root",
                    password="",
                    database="lasuertedelaolla", 
                    port=3306
                )
                
                cursor = conexion.cursor()

                # Insertar la nueva promoción en la base de datos
                query = "INSERT INTO promocion (nombre, descripcion, descuento, fecha_inicio, fecha_fin) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(query, (nombre, descripcion, descuento, fecha_inicio, fecha_fin))
                
                conexion.commit()
                # Guardar el mensaje en la tabla de registros
                mensaje = "Promoción añadida exitosamente."
                query_registro = "INSERT INTO registros (mensaje) VALUES (%s)"
                cursor.execute(query_registro, (mensaje,))
                conexion.commit()

                cursor.close()
                conexion.close()
                
                # Mostrar mensaje de éxito
                messagebox.showinfo("Nueva Promoción", "Promoción creada exitosamente.")
                
                # Cerrar la ventana de nueva promoción
                self.ventana_nueva_promocion.destroy()
                
                # Actualizar la lista de promociones
                self.cargar_promociones()

            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Error al conectar a la base de datos: {e}")
        else:
            # Mostrar mensaje de advertencia si no se completaron todos los campos
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")

    def modificar_promocion(self):
        # Crear una nueva ventana para seleccionar la promoción a modificar
        self.ventana_modificar_promocion = Toplevel(self)
        self.ventana_modificar_promocion.title("Modificar Promoción")
        
        # Etiqueta y campo de entrada para seleccionar la promoción por su ID
        lbl_id = Label(self.ventana_modificar_promocion, text="ID de la Promoción:")
        lbl_id.grid(row=0, column=0, padx=10, pady=10)
        
        self.txt_id_modificar = Entry(self.ventana_modificar_promocion, width=30)
        self.txt_id_modificar.grid(row=0, column=1, padx=10, pady=10)
        
        # Botón para buscar la promoción por ID
        btn_buscar = ttk.Button(self.ventana_modificar_promocion, text="Buscar", command=self.buscar_promocion_modificar)
        btn_buscar.grid(row=0, column=2, padx=10, pady=10)
        
        # Campos de entrada para modificar los datos de la promoción
        lbl_nombre_nuevo = Label(self.ventana_modificar_promocion, text="Nuevo Nombre:")
        lbl_nombre_nuevo.grid(row=1, column=0, padx=10, pady=10)
        self.txt_nombre_nuevo = Entry(self.ventana_modificar_promocion, width=30)
        self.txt_nombre_nuevo.grid(row=1, column=1, padx=10, pady=10)
        
        lbl_descripcion_nueva = Label(self.ventana_modificar_promocion, text="Nueva Descripción:")
        lbl_descripcion_nueva.grid(row=2, column=0, padx=10, pady=10)
        self.txt_descripcion_nueva = Entry(self.ventana_modificar_promocion, width=30)
        self.txt_descripcion_nueva.grid(row=2, column=1, padx=10, pady=10)
        
        lbl_descuento_nuevo = Label(self.ventana_modificar_promocion, text="Nuevo Descuento (%):")
        lbl_descuento_nuevo.grid(row=3, column=0, padx=10, pady=10)
        self.txt_descuento_nuevo = Entry(self.ventana_modificar_promocion, width=30)
        self.txt_descuento_nuevo.grid(row=3, column=1, padx=10, pady=10)
        
        lbl_fecha_inicio_nueva = Label(self.ventana_modificar_promocion, text="Nueva Fecha de Inicio (YYYY-MM-DD):")
        lbl_fecha_inicio_nueva.grid(row=4, column=0, padx=10, pady=10)
        self.txt_fecha_inicio_nueva = Entry(self.ventana_modificar_promocion, width=30)
        self.txt_fecha_inicio_nueva.grid(row=4, column=1, padx=10, pady=10)
        
        lbl_fecha_fin_nueva = Label(self.ventana_modificar_promocion, text="Nueva Fecha de Fin (YYYY-MM-DD):")
        lbl_fecha_fin_nueva.grid(row=5, column=0, padx=10, pady=10)
        self.txt_fecha_fin_nueva = Entry(self.ventana_modificar_promocion, width=30)
        self.txt_fecha_fin_nueva.grid(row=5, column=1, padx=10, pady=10)
        
        # Botón para guardar los cambios
        btn_guardar = ttk.Button(self.ventana_modificar_promocion, text="Guardar Cambios", command=self.guardar_modificacion_promocion)
        btn_guardar.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

    def buscar_promocion_modificar(self):
        # Obtener el ID de la promoción a modificar desde la entrada
        id_promocion = self.txt_id_modificar.get()
        
        # Validar que el ID de la promoción no esté vacío
        if id_promocion:
            try:
                # Conectar a la base de datos
                conexion = mysql.connector.connect(
                    host="127.0.0.1",
                    user="root",
                    password="",
                    database="lasuertedelaolla",  
                    port=3306
                )
                
                cursor = conexion.cursor()
                
                # Consultar la promoción en la base de datos
                query = "SELECT nombre, descripcion, descuento, fecha_inicio, fecha_fin FROM promocion WHERE id = %s"
                cursor.execute(query, (id_promocion,))
                
                # Obtener el resultado de la consulta
                promocion = cursor.fetchone()
                
                if promocion:
                    # Mostrar los datos de la promoción encontrada en los campos de entrada
                    self.txt_nombre_nuevo.delete(0, END)
                    self.txt_nombre_nuevo.insert(0, promocion[0])  # Nombre
                    self.txt_descripcion_nueva.delete(0, END)
                    self.txt_descripcion_nueva.insert(0, promocion[1])  # Descripción
                    self.txt_descuento_nuevo.delete(0, END)
                    self.txt_descuento_nuevo.insert(0, promocion[2])  # Descuento
                    self.txt_fecha_inicio_nueva.delete(0, END)
                    self.txt_fecha_inicio_nueva.insert(0, promocion[3])  # Fecha de Inicio
                    self.txt_fecha_fin_nueva.delete(0, END)
                    self.txt_fecha_fin_nueva.insert(0, promocion[4])  # Fecha de Fin
                else:
                    messagebox.showwarning("Promoción no encontrada", f"No se encontró ninguna promoción con el ID '{id_promocion}'.")
                
                cursor.close()
                conexion.close()
                
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Error al conectar a la base de datos: {e}")
        else:
            messagebox.showwarning("ID de Promoción vacío", "Por favor ingresa el ID de la promoción a modificar.")
    
    def guardar_modificacion_promocion(self):
        # Obtener los valores modificados de la promoción desde los campos de entrada
        nombre_nuevo = self.txt_nombre_nuevo.get()
        descripcion_nueva = self.txt_descripcion_nueva.get()
        descuento_nuevo = self.txt_descuento_nuevo.get()
        fecha_inicio_nueva = self.txt_fecha_inicio_nueva.get()
        fecha_fin_nueva = self.txt_fecha_fin_nueva.get()
        
        # Obtener el ID original de la promoción desde el campo de búsqueda
        id_promocion = self.txt_id_modificar.get()
        
        # Validar que todos los campos estén completos
        if nombre_nuevo and descuento_nuevo and fecha_inicio_nueva and fecha_fin_nueva and id_promocion:
            try:
                # Conectar a la base de datos
                conexion = mysql.connector.connect(
                    host="127.0.0.1",
                    user="root",
                    password="",
                    database="lasuertedelaolla",  
                    port=3306
                )
                
                cursor = conexion.cursor()
                
                # Actualizar la promoción en la base de datos
                query = "UPDATE promocion SET nombre = %s, descripcion = %s, descuento = %s, fecha_inicio = %s, fecha_fin = %s WHERE id = %s"
                cursor.execute(query, (nombre_nuevo, descripcion_nueva, descuento_nuevo, fecha_inicio_nueva, fecha_fin_nueva, id_promocion))
                
                conexion.commit()
                # Guardar el mensaje en la tabla de registros
                mensaje = "Promoción modificada exitosamente."
                query_registro = "INSERT INTO registros (mensaje) VALUES (%s)"
                cursor.execute(query_registro, (mensaje,))
                conexion.commit()

                cursor.close()
                conexion.close()
                
                # Mostrar mensaje de éxito
                messagebox.showinfo("Modificar Promoción", "Promoción modificada exitosamente.")
                
                # Cerrar la ventana de modificar promoción
                self.modificar_promocion.destroy()
                
                # Actualizar la lista de promociones
                self.cargar_promociones()
                
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Error al conectar a la base de datos: {e}")
        else:
            # Mostrar mensaje de advertencia si no se completaron todos los campos
            messagebox.showwarning("Campos Incompletos", "Todos los campos son obligatorios para guardar los cambios.")
  
    def eliminar_promocion(self):
        # Crear una nueva ventana para eliminar la promoción por su ID
        self.ventana_eliminar_promocion = Toplevel(self)
        self.ventana_eliminar_promocion.title("Eliminar Promoción")
        
        # Etiqueta y campo de entrada para ingresar el ID de la promoción a eliminar
        lbl_id_eliminar = Label(self.ventana_eliminar_promocion, text="ID de la Promoción:")
        lbl_id_eliminar.grid(row=0, column=0, padx=10, pady=10)
        
        self.txt_id_eliminar = Entry(self.ventana_eliminar_promocion, width=30)
        self.txt_id_eliminar.grid(row=0, column=1, padx=10, pady=10)
        
        # Botón para confirmar la eliminación de la promoción
        btn_eliminar = ttk.Button(self.ventana_eliminar_promocion, text="Eliminar", command=self.confirmar_eliminar_promocion)
        btn_eliminar.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    def confirmar_eliminar_promocion(self):
        # Obtener el ID de la promoción a eliminar desde la entrada
        id_promocion = self.txt_id_eliminar.get()
        
        # Validar que el ID de la promoción no esté vacío
        if id_promocion:
            if messagebox.askyesno("Confirmar Eliminación", f"¿Estás seguro de eliminar la promoción con ID '{id_promocion}'?"):
                try:
                    # Conectar a la base de datos
                    conexion = mysql.connector.connect(
                        host="127.0.0.1",
                        user="root",
                        password="",
                        database="lasuertedelaolla",  
                        port=3306
                    )
                    
                    cursor = conexion.cursor()
                    
                    # Eliminar la promoción de la base de datos
                    query = "DELETE FROM promocion WHERE id = %s"
                    cursor.execute(query, (id_promocion,))
                    
                    conexion.commit()
                    
                    # Guardar el mensaje en la tabla de registros
                    mensaje = "Promoción eliminada exitosamente."
                    query_registro = "INSERT INTO registros (mensaje) VALUES (%s)"
                    cursor.execute(query_registro, (mensaje,))
                    conexion.commit()

                    cursor.close()
                    conexion.close()
                    
                    # Mostrar mensaje de éxito
                    messagebox.showinfo("Eliminar Promoción", f"Promoción con ID '{id_promocion}' eliminada correctamente.")
                    
                    # Cerrar la ventana de eliminar promoción
                    self.ventana_eliminar_promocion.destroy()
                    
                    # Actualizar la lista de promociones
                    self.cargar_promociones()
                    
                except mysql.connector.Error as e:
                    messagebox.showerror("Error", f"Error al conectar a la base de datos: {e}")
        else:
            messagebox.showwarning("ID de Promoción vacío", "Por favor ingresa el ID de la promoción a eliminar.")

   
    def eliminar_promocion_bd(self):
        # Obtener el ID de la promoción a eliminar desde la entrada
        id_promocion = self.txt_id_eliminar.get()
        
        # Validar que el ID de la promoción no esté vacío
        if id_promocion:
            try:
                # Conectar a la base de datos
                conexion = mysql.connector.connect(
                    host="127.0.0.1",
                    user="root",
                    password="",
                    database="lasuertedelaolla",
                    port=3306
                )
                
                cursor = conexion.cursor()
                
                # Eliminar la promoción de la base de datos
                query = "DELETE FROM promocion WHERE id = %s"
                cursor.execute(query, (id_promocion,))
                
                conexion.commit()  

                cursor.close()
                conexion.close()

                
                # Mostrar mensaje de éxito
                messagebox.showinfo("Promoción Eliminada", f"Promoción con ID {id_promocion} eliminada correctamente.")
                
                # Cerrar la ventana de confirmar eliminar promoción
                self.ventana_eliminar_promocion.destroy()  # Cambiado a self.ventana_eliminar_promocion
                
                # Recargar la lista de promociones
                self.cargar_promociones()
                
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error al eliminar la promoción: {err}")
        else:
            messagebox.showwarning("ID de Promoción Vacío", "Por favor ingresa el ID de la promoción a eliminar.")


    def cargar_promociones(self):
        try:
            # Conectar a la base de datos MySQL
            conexion = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="",
                database="lasuertedelaolla",
                port=3306
            )
            cursor = conexion.cursor()
            cursor.execute("SELECT id, nombre, descripcion, descuento, fecha_inicio, fecha_fin FROM promocion")
    
            # Limpiar el Treeview
            for row in self.tree_lista_promociones.get_children():
                self.tree_lista_promociones.delete(row)
    
            # Insertar los datos en el Treeview
            for (id, nombre, descripcion, descuento, fecha_inicio, fecha_fin) in cursor:
                self.tree_lista_promociones.insert("", "end", values=(id, nombre, descripcion, descuento, fecha_inicio, fecha_fin))
    
            cursor.close()
            conexion.close()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
    
    def buscar_promociones(self):
        termino_busqueda = self.txt_busqueda_promociones.get().strip()
        if termino_busqueda:
            try:
                self.conexion = mysql.connector.connect(
                    host="127.0.0.1",
                    user="root",
                    password="",
                    database="lasuertedelaolla",
                    port=3306
                )

                cursor = self.conexion.cursor()
                query = """
                SELECT id,nombre,descripcion,descuento,fecha_inicio,fecha_fin
                FROM promocion 
                WHERE id LIKE %s OR nombre LIKE %s OR descripcion LIKE %s OR descuento LIKE %s OR fecha_inicio LIKE %s OR fecha_fin LIKE %s
                """
                cursor.execute(query, ("%"+termino_busqueda+"%", "%"+termino_busqueda+"%", "%"+termino_busqueda+"%", "%"+termino_busqueda+"%", "%"+termino_busqueda+"%", "%"+termino_busqueda+"%"))
                promociones = cursor.fetchall()

                cursor.close()
                self.conexion.close()

                for item in self.tree_lista_promociones.get_children():
                    self.tree_lista_promociones.delete(item)

                for promocion in promociones:
                    self.tree_lista_promociones.insert("", "end", values=promocion)

            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Error al conectar a la base de datos: {e}")
        else:
            self.cargar_promociones()

    #--------------------------------------------------------------------
    #ACTUALIZAR BD
    #---------------------------------------------------------------------
    #CENTRAR LA VENTANA 

    def center_window(self):
        # Obtener el tamaño de la pantalla
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calcular la posición x e y
        position_x = (screen_width - self.img_width) // 2
        position_y = (screen_height - self.img_height) // 2

        # Establecer la geometría de la ventana centrada
        self.geometry(f"{self.img_width}x{self.img_height}+{position_x}+{position_y}")


def main():
    app = Venta()
    app.title('La Suerte de la Olla')

    tb.Style('superhero')

    app.mainloop()

if __name__ == '__main__':
    main()
    