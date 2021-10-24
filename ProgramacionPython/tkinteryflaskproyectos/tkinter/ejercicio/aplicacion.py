from tkinter import ttk
from tkinter import *
import sqlite3

class Producto:
    
    db = 'database/producto.db'

    def __init__(self, root):
        self.ventana = root
        self.ventana.title("App Gestor de Produtos")
        self.ventana.resizable(1,1)
        self.ventana.wm_iconbitmap('recursos/icon.ico')
        
        
        # Creacion del contenedor 
        frame=LabelFrame(self.ventana, text = "Registrar un nuevo Producto")
        frame.grid(row = 0, column = 0, columnspan = 3, pady = 20) 
        
        # Label Nombre
        self.etiqueta_nombre = Label(frame, text="Nombre: ")  
        self.etiqueta_nombre.grid(row=1, column=0) 
        self.nombre = Entry(frame)  
        self.nombre.focus() 
        self.nombre.grid(row=1, column=1)
        # Label precio
        self.etiqueta_precio = Label(frame, text="Precio: ")  
        self.etiqueta_precio.grid(row=2, column=0) 
        self.precio = Entry(frame)  
        self.precio.focus() 
        self.precio.grid(row=2, column=1)
        
        # Boton Añadir Producto 
        self.boton_aniadir = ttk.Button(frame, text = "Guardar Producto",command=self.add_producto)
        self.boton_aniadir.grid(row = 3, columnspan = 2, sticky = W + E)
        # Mensaje informativo para el usuario
        self.mensaje = Label(text = '', fg = 'red')
        self.mensaje.grid(row = 3, column = 0, columnspan = 2, sticky = W + E)
        # Botones de Eliminar y Editar
        boton_eliminar = ttk.Button(text = 'ELIMINAR', command = self.del_producto)
        boton_eliminar.grid(row = 5, column = 0, sticky = W + E)
        boton_editar = ttk.Button(text='EDITAR',command = self.edit_producto)
        boton_editar.grid(row = 5, column = 1, sticky = W + E)
        
        #fotmateo
        style=ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=  0, font=('Calibri', 11))  # Se modifica la fuente de la 
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 13, 'bold'))  # Se modifica la fuente de las 
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])  # Eliminamos los bordes
         
         
        # Estructura de la tabla 
        self.tabla = ttk.Treeview(height = 20, columns = 2, style="mystyle.Treeview")
        self.tabla.grid(row = 4, column = 0, columnspan = 2) 
        self.tabla.heading('#0', text = 'Nombre', anchor = CENTER)
        # Encabezado 0
        self.tabla.heading('#1', text='Precio', anchor = CENTER) 
        self.get_productos()  
    def db_consulta(self, consulta, parametros = ()):    
        with sqlite3.connect(self.db) as   con: # Iniciamos una conexion con la base de datos (alias con)
            cursor = con.cursor() # Generamos un cursor de la conexion para poder operar en la base de datos
            resultado = cursor.execute(consulta, parametros) # Preparar la consulta SQL (con parametros si los hay)con.
            con.commit() # Ejecutar la consulta SQL preparada anteriormente   
        return resultado # Retornar el resultado de la consulta SQL
    
    def get_productos(self):
         registros_tabla = self.tabla.get_children() 
        # Obtener todos los datos de la tabla    
         for fila in registros_tabla:
             self.tabla.delete(fila)
           
         query = 'SELECT * FROM producto ORDER BY nombre DESC'    
         registros_db= self.db_consulta(query) # Se hace la llamada al metodo db_consultas 
         # Escribir los datos en pantalla    
         for fila in registros_db:
             print(fila) # print para verificar por consola los datos
             self.tabla.insert('', 0, text = fila[1], values = fila[2])
             
    def validacion_nombre(self):     
        nombre_introducido_por_usuario = self.nombre.get()    
        return len (nombre_introducido_por_usuario) != 0
    def validacion_precio(self):    
        precio_introducido_por_usuario = self.precio.get()    
        return len (precio_introducido_por_usuario) != 0
    def add_producto(self):  
        if self.validacion_nombre() and self.validacion_precio():
            query = 'INSERT INTO producto VALUES(NULL, ?, ?)' 
        # Consulta SQL (sin los datos)
            parametros = (self.nombre.get(), self.precio.get()) 
        # Parametros de la consulta 
            self.db_consulta(query, parametros)
            self.mensaje['text'] = 'Producto {} añadido con éxito'.format(self.nombre.get()) 
            # Label ubicado entre el boton y la 
            self.nombre.delete(0, END) 
            # Borrar el campo nombre del formulario
            self.precio.delete(0, END) 
            # Borrar el campo precio del formulario     
        elif self.validacion_nombre() and self.validacion_precio() == False:
            self.mensaje['text'] = 'El precio es obligatorio'   
        elif self.validacion_nombre() == False and self.validacion_precio():
            self.mensaje['text'] = 'El nombre es obligatorio' 
        else:
             self.mensaje['text'] = 'El nombre y el precio son obligatorios'
             
        self.get_productos()  
    def del_producto(self):    
        # Debug    
        # #print(self.tabla.item(self.tabla.selection()))    
        # #print(self.tabla.item(self.tabla.selection())['text'])   
        #  #print(self.tabla.item(self.tabla.selection())['values'])   
        #  #print(self.tabla.item(self.tabla.selection())['values'][0])   
          self.mensaje['text'] = '' # Mensaje inicialmente vacio    
         # Comprobacion de que se seleccione un producto para poder eliminarlo   
          try:
              self.tabla.item(self.tabla.selection())['text'][0]    
          except IndexError as e:
                   self.mensaje['text'] = 'Por favor, seleccione un producto'
                   return    
          self.mensaje['text'] = ''    
          nombre = self.tabla.item(self.tabla.selection())['text']   
          query = 'DELETE FROM producto WHERE nombre = ?' 
          # Consulta SQL    
          self.db_consulta(query, (nombre,)) 
          # Ejecutar la consulta    
          self.mensaje['text'] = 'Producto {} eliminado con éxito'.format(nombre)    
          self.get_productos() # Actualizar la tabla de productos   
          
    def edit_producto(self ):    
         self.mensaje['text'] = '' 
         # Mensaje inicialmente vacio    
         try:
            self.tabla.item(self.tabla.selection())['text'][0]     
         except IndexError as e: 
             self.mensaje['text'] = 'Por favor, seleccione un producto'
             return    
         nombre = self.tabla.item(self.tabla.selection())['text']    
         old_precio = self.tabla.item(self.tabla.selection())['values'][0] # El precio se encuentra dentro de una lista    
         self.ventana_editar = Toplevel() # Crear una ventana por delante de la principal    
         self.ventana_editar.title = "Editar Producto" # Titulo de la ventana   
         self.ventana_editar.resizable(1, 1)  # Activar la redimension de la ventana. Para desactivarla: (0,0)     
         self.ventana_editar.wm_iconbitmap('recursos/icon.ico') # Icono de la ventan 
         titulo = Label(self.ventana_editar, text='Edición de Productos', font=('Calibri', 50, 'bold'))
         titulo.grid(column=0, row=0) # Creacion del contenedor Frame de la ventana de Editar Producto
         frame_ep = LabelFrame(self.ventana_editar, text="Editar el siguiente Producto") # frame_ep: Frame Editar Producto
         frame_ep.grid(row=1, column=0, columnspan=20, pady=20) # Label Nombre antiguo
         self.etiqueta_nombre_anituguo = Label(frame_ep, text = "Nombre antiguo: ")  # Etiqueta de texto ubicada en el frame
         self.etiqueta_nombre_anituguo.grid(row=2, column=0)  # Posicionamiento a traves de grid# Entry Nombre antiguo (texto que no se podra modificar)
         self.input_nombre_antiguo = Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=nombre), state='readonly')
         self.input_nombre_antiguo.grid(row=2, column=1) # Label Nombre nuevo
         self.etiqueta_nombre_nuevo = Label(frame_ep, text="Nombre nuevo: ") 
         self.etiqueta_nombre_nuevo.grid(row=3, column=0) # Entry Nombre nuevo (texto que si se podra modificar)
         self.input_nombre_nuevo = Entry(frame_ep)
         self.input_nombre_nuevo.grid(row=3, column=1)
         self.input_nombre_nuevo.focus() # Para que el foco del raton vaya a este Entry al inicio# Label Precio antiguo
         self.etiqueta_precio_anituguo = Label(frame_ep,text="Precio antiguo: ")  # Etiqueta de texto ubicada en el frame
         self.etiqueta_precio_anituguo.grid(row=4, column=0)  # Posicionamiento a traves de grid# Entry Precio antiguo (texto que no se podra modificar)
         # Entry Precio antiguo (texto que no se podra modificar)
         self.input_precio_antiguo = Entry(frame_ep,
         textvariable=StringVar(self.ventana_editar, value=old_precio),state='readonly')
         self.input_precio_antiguo.grid(row=4, column=1) # Label Precio nuevo
         self.etiqueta_precio_nuevo = Label(frame_ep, text="Precio nuevo: ") 
         self.etiqueta_precio_nuevo.grid(row=5, column=0) # Entry Precio nuevo (texto que si se podra modificar)
         self.input_precio_nuevo = Entry(frame_ep)
         self.input_precio_nuevo.grid(row=5, column=1) # Boton Actualizar Producto
         self.boton_actualizar = ttk.Button(frame_ep, text="Actualizar Producto",
                                            command=lambda: 
         self.actualizar_productos(self.input_nombre_nuevo.get(),
         self.input_nombre_antiguo.get(),self.input_precio_nuevo.get(),self.input_precio_antiguo.get()))
         self.boton_actualizar.grid(row=6, columnspan=2, sticky=W + E)
    def actualizar_productos(self, nuevo_nombre, antiguo_nombre, nuevo_precio, antiguo_precio):    
        producto_modificado = False    
        query = 'UPDATE producto SET nombre = ?, precio = ? WHERE nombre = ? AND precio = ?'   
        if nuevo_nombre != '' and nuevo_precio != '':
             # Si el usuario escribe nuevo nombre y nuevo precio, se cambian ambos
             parametros = (nuevo_nombre, nuevo_precio, antiguo_nombre, antiguo_precio)
             producto_modificado = True    
        elif nuevo_nombre != '' and nuevo_precio == '':
            # Si el usuario deja vacio el nuevo precio, se mantiene el pecio anterior
            parametros = (nuevo_nombre, antiguo_precio, antiguo_nombre, antiguo_precio)
            producto_modificado = True    
        elif nuevo_nombre == '' and nuevo_precio != '':
            # Si el usuario deja vacio el nuevo nombre, se mantiene el nombre anterior
            parametros = (antiguo_nombre, nuevo_precio, antiguo_nombre, antiguo_precio)
            producto_modificado = True    
            
        if(producto_modificado):
            self.db_consulta(query, parametros)  # Ejecutar la consulta 
            self.ventana_editar.destroy() # Cerrar la ventana de edicion de productos
            self.mensaje['text'] = 'El producto {} ha sido actualizado con éxito'.format(antiguo_nombre) # Mostrar mensaje para el usuario
            self.get_productos() # Actualizar la tabla de productos    
        else: 
            self.ventana_editar.destroy()  # Cerrar la ventana de edicion de productos
            self.mensaje['text'] = 'El producto {} NO ha sido actualizado'.format(antiguo_nombre)

 
if __name__ =='__main__':   
    root=Tk()
    app=Producto(root)
    root.mainloop()#tiene la pantalla en un bucle
    
