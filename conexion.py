import mysql.connector 
from hashlib import md5
from tabulate import tabulate 
from os import system
from datetime import datetime




class Database:
    def __init__(self):
        self.conexion = mysql.connector.connect(
        user='root',
        password='ericocoro',
        host='localhost',
        database='hotel')
        self.cursor=self.conexion.cursor()

    def cerrarBD(self):
        self.cursor.close()
        self.conexion.close()
        
    def login_usuario(self):
        nombre_usuario=input('Ingrese nombre del usuario: ')
        password_usuario=input('Ingrese password: ')
        return nombre_usuario,password_usuario

    def login_admin(self):
        rut_admin='11111111-1'
        password_admin='123'
        sql1='insert into ADMINISTRADOR values('+repr(rut_admin)+','+repr(password_admin)+')'
        self.cursor.execute(sql1)
        return rut_admin,password_admin
    
    def Entra_usuario(self):
        db=Database()
        nombre_usuario,password_usuario=self.login_usuario()
        sql1='select * from ENCARGADO where USUARIO='+repr(nombre_usuario)+'and CONTRASEÑA_ENC='+repr(password_usuario)
        try:
            self.cursor.execute(sql1)
            result=self.cursor.fetchone()
            if result!=None and result[1]==nombre_usuario and result[2]==password_usuario:
                print('Bienvenido',nombre_usuario) 
                while True:
                    elige3=input('\nElige una opción:\n\
                    Registrar Habitacion (1)\n\
                    Registrar Pasajero (2)\n\
                    Ver tabla resumen de habitaciones (3)\n\
                    Ver tabla resumen de pasajeros (4)\n\
                    Eliminar Habitacion (5)\n\
                    Asignar Pasajero (6)\n\
                    Eliminar Pasajero(7)\n\
                    Ver Habitaciones eliminadas(8)\n\
                    Salir(s)\n=>')
                    if elige3=='1':
                        db.Registrar_Hab()
                    elif elige3=='2':
                        db.Registrar_pasajero()    
                    elif elige3=='3':
                        db.Tabla_resumen_Habitacion()
                    elif elige3=='4':
                       db.Tabla_resumen_Pasajero()
                    elif elige3=='5':
                        db.Eliminar_Habitacion()      
                    elif elige3=='6':
                        db.Asignacion()    
                    elif elige3=='7':
                        db.Eliminar_pasajero()
                    elif elige3=='8':
                        db.Hab_eliminadas()        
                    elif elige3=='s':
                        db.cerrarBD()      
                        system('cls')
                        break
            else:
                print('Acceso denegado')
                input('Presione Enter para continuar...')
                system('cls')
                db.cerrarBD()
        except Exception as err:
            self.conexion.rollback()
            print(err)
            
    
    def Entra_admin(self):
        db=Database()
        rut_admin=input('Ingrese rut del administrador: ')
        password_admin=input('Ingrese password del administrador: ')
        rut_admin,password_admin=self.login_admin()
        sql1='select * from ADMINISTRADOR where RUT_ADMIN='+repr(rut_admin)+'and CONTRASEÑA='+repr(password_admin)            
        try:
            self.cursor.execute(sql1)
            result=self.cursor.fetchone()
            if result[0]==rut_admin and result[1]==password_admin:
                while True:
                    print('---Menu de Administrador---')
                    elige2=input('\nElige una opción:\n\
                    Registrar nuevo usuario (1)\n\
                    Salir (s)\n=>')
                    if elige2=='1':
                        db.Registrar_usuario()
                    elif elige2=='s':
                        db.cerrarBD()
                        system('cls')
                        break
                    else:
                        ('Elige una opción valida')
            else:
                print('Acceso Denegado')
                input('Presione Enter para continuar...')    
                system('cls')
                db.cerrarBD()
        except Exception as err:
            self.conexion.rollback()
            print(err)
    
    
           
    def Registrar_usuario(self):
         nombre_usuario,password_usuario=self.login_usuario()
         rut_enc=input('Ingrese rut del nuevo usuario: ')
         sql1='select * from ENCARGADO where RUT_ENC='+repr(rut_enc)
         try:
             self.cursor.execute(sql1)
             result=self.cursor.fetchone()
             if result==None:
                 sql2='insert into ENCARGADO values('+repr(rut_enc)+','+repr(nombre_usuario)+','+repr(password_usuario)+')'
                 try:
                     self.cursor.execute(sql2)
                     self.conexion.commit()
                     print('Se ha creado un nuevo usuario')
                     input('Presione Enter para continuar...')
                     system('cls')
                 except Exception as err:
                     self.conexion.rollback()
                     print(err)
             else:
                 print('Ya existe un usuario con los datos ingresados')
                 input('Presione Enter para continuar...')
                 system('cls')
         except Exception as err:
             self.conexion.rollback()
             print(err)
    
    def Registrar_Hab(self):
        id = int(input('Ingrese ID para la habitación= '))
        Num_habitacion = int(input('Ingrese el número de la habitación: '))
        sql1 = 'SELECT ID_HABITACION and NUM_HABITACION FROM HABITACION WHERE ID_HABITACION = %s'
        try:
            self.cursor.execute(sql1, (id,))
            if self.cursor.fetchone() is None:
                cant_max = int(input('Ingrese el número máximo de pasajeros para la habitación: '))
                Orientacion = input('Ingrese la orientación de la habitación: ')
                sql2 = 'INSERT INTO HABITACION (ID_HABITACION, NUM_HABITACION, CANT_ADMITIDA, ORIENTACION) VALUES (%s, %s, %s, %s)'
                try:
                    self.cursor.execute(sql2, (id, Num_habitacion, cant_max, Orientacion))
                    self.conexion.commit()
                    print('Nueva habitación registrada')
                except Exception as err:
                    self.conexion.rollback()
                    print(f'Error al registrar la habitación: {err}')
            else:
                print('Ya existe una habitación con el ID o numero ingresado')
        except Exception as err:
            print(f'Error al verificar la habitación: {err}')
        input('Presione Enter para continuar...')
        system('cls')
        return Num_habitacion     
    
  
        
    def Registrar_pasajero(self):
        Rut_pasajero = input('Ingrese RUT del pasajero: ')
        sql1 = 'SELECT RUT_PASAJERO FROM PASAJERO WHERE RUT_PASAJERO = %s'
        try:
             self.cursor.execute(sql1, (Rut_pasajero,))
             if self.cursor.fetchone() is None:
                 Nombre_pasajero = input('Ingrese nombre del pasajero: ')
                 Tipo_habitacion = input('Ingrese tipo de habitación deseada: ')
                 Cantidad_pasajeros = int(input('Ingrese la cantidad de pasajeros a hospedar: '))
                 sql2 = 'INSERT INTO PASAJERO (RUT_PASAJERO, NOMBRE_PASAJERO, TIPO_HABITACION, CANT_PASAJEROS) VALUES (%s, %s, %s, %s)'
                 try:
                     self.cursor.execute(sql2, (Rut_pasajero, Nombre_pasajero, Tipo_habitacion, Cantidad_pasajeros))
                     self.conexion.commit()
                     print('Pasajero registrado')
                 except Exception as err:
                     self.conexion.rollback()
                     print(f'Error al registrar al pasajero: {err}')
             else:
                 print('Ya existe un pasajero con el RUT ingresado')
        except Exception as err:
            print(f'Error al verificar el pasajero: {err}')
        input('Presione Enter para continuar...')
        system('cls')
        return Cantidad_pasajeros
    
    
    def Eliminar_Habitacion(self):
        Id_habitacion = input('Escriba el id de la habitación que desea eliminar: ')
        
        # Verificar si la habitación existe
        sql1 = 'SELECT * FROM HABITACION WHERE ID_HABITACION = %s'
        try:
            self.cursor.execute(sql1, (Id_habitacion,))
            habitacion = self.cursor.fetchone()
            
            if habitacion is not None:
                # Verificar si hay un pasajero responsable asignado a esta habitación
                confirmar = 'SELECT PASAJERO_RESPONSABLE FROM HABITACION WHERE ID_HABITACION = %s'
                self.cursor.execute(confirmar, (Id_habitacion,))
                pasajero_responsable = self.cursor.fetchone()[0]
                
                # Transfiriendo datos a la tabla HAB_ELIMINADA
                datos_habitacion = (
                    habitacion[0],  # ID_HABITACION
                    habitacion[1],  # NUM_HABITACION
                    habitacion[3],  # ORIENTACION
                    habitacion[6]   # PASAJEROS_PASADOS
                )
                insertar_hab_eliminada = '''
                    INSERT INTO HAB_ELIMINADA (ID_HABITACION, NUM_HABITACION, ORIENTACION, PASAJEROS_PASADOS)
                    VALUES (%s, %s, %s, %s)
                '''
                self.cursor.execute(insertar_hab_eliminada, datos_habitacion)

                if pasajero_responsable is None:
                    # Eliminar la habitación
                    sql2 = 'DELETE FROM HABITACION WHERE ID_HABITACION = %s'
                    try:
                        self.cursor.execute(sql2, (Id_habitacion,))
                        self.conexion.commit()
                        print('Habitación eliminada y datos transferidos a HAB_ELIMINADA')
                    except Exception as err:
                        self.conexion.rollback()
                        print(f'Error al eliminar la habitación: {err}')
                else:
                    print('Existe un pasajero asignado a esta habitación, por lo tanto no se puede eliminar esta habitación')
            else:
                print('No existe habitación con el código ingresado')
            input('Presione cualquier tecla para continuar...')
            system('cls')
        except Exception as err:
            print(f'Error al eliminar la habitación: {err}')

  


    
    def Asignacion(self):
        fechaactual = datetime.now()
        Id_asignacion = int(input('Ingrese ID de asignación: '))
        sql1 = 'SELECT * FROM ASIGNACION WHERE ID_ASIGNACION = %s'
        try:
            self.cursor.execute(sql1, (Id_asignacion,))
            if self.cursor.fetchone() is None:
                Rut_pasajero = input('Ingrese el RUT del pasajero que desea asignar: ')
                Nombre_pasajero = input('Ingrese el nombre del pasajero: ')
                Id_habitacion = int(input('Ingrese el ID de la habitación que desea asignar: '))
                Num_habitacion = int(input('Ingrese el número de la habitación: '))
                Costo = int(input('Ingrese el costo de la habitación: '))
                # Validar que Id_habitacion, Num_habitacion y Costo sean mayores que 0
                if Id_habitacion <= 0 or Num_habitacion <= 0 or Costo <= 0:
                    print('Error: ID de habitación, número de habitación y costo deben ser mayores que 0.')
                    input('Presione Enter para continuar...')
                    system('cls')
                    return

                Fecha = fechaactual

                # Verificar si el RUT del pasajero está registrado en la tabla PASAJERO
                sql2 = 'SELECT CANT_PASAJEROS FROM PASAJERO WHERE RUT_PASAJERO = %s'
                self.cursor.execute(sql2, (Rut_pasajero,))
                resultado_pasajero = self.cursor.fetchone()
                if resultado_pasajero:
                    cant_pasejeros = resultado_pasajero[0]
                else:
                    print('El RUT del pasajero ingresado no está registrado.')
                    input('Presione Enter para continuar...')
                    system('cls')
                    return

                # Verificar si la habitación está ocupada
                sql3 = 'SELECT COUNT(*) FROM ASIGNACION WHERE ID_HABITACION = %s'
                self.cursor.execute(sql3, (Id_habitacion,))
                ocupacion_actual = self.cursor.fetchone()[0]

                if ocupacion_actual > 0:
                    print('La habitación ya tiene un pasajero asignado.')
                    input('Presione Enter para continuar...')
                    system('cls')
                    return

                # Verificar la capacidad máxima de la habitación
                sql4 = 'SELECT CANT_ADMITIDA FROM HABITACION WHERE ID_HABITACION = %s'
                self.cursor.execute(sql4, (Id_habitacion,))
                resultado_habitacion = self.cursor.fetchone()
                if resultado_habitacion:
                    cant_admitida = resultado_habitacion[0]

                    if cant_pasejeros != cant_admitida:
                        print(f'Error: La cantidad de pasajeros ({cant_pasejeros}) debe coincidir con la capacidad máxima ({cant_admitida}) de la habitación.')
                        input('Presione Enter para continuar...')
                        system('cls')
                        return

                    sql5 = '''
                    INSERT INTO ASIGNACION (ID_ASIGNACION, RUT_PASAJERO, PASAJERO_RESPONSABLE, ID_HABITACION, NUM_HABITACION, COSTO, FECHA)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    '''
                    try:
                        self.cursor.execute(sql5, (Id_asignacion, Rut_pasajero, Nombre_pasajero, Id_habitacion, Num_habitacion, Costo, Fecha))
                        self.conexion.commit()
                        print('Pasajero asignado')
                    except Exception as err:
                        self.conexion.rollback()
                        print(f'Error al realizar la asignación: {err}')

                    # Actualizar PASAJERO_RESPONSABLE y ESTADO en la tabla HABITACION
                    sql6 = 'UPDATE HABITACION SET PASAJERO_RESPONSABLE = %s, COSTO = %s, ESTADO = %s WHERE ID_HABITACION = %s'
                    try:
                        self.cursor.execute(sql6, (Nombre_pasajero, Costo, 'OCUPADO', Id_habitacion))
                        self.conexion.commit()
                    except Exception as err:
                        self.conexion.rollback()
                        print(f'Error al actualizar la habitación: {err}')
                else:
                    print('No existe una habitación con el ID ingresado.')
            else:
                print('Ya existe una asignación con esa ID')
        except Exception as err:
            print(f'Error al verificar la asignación: {err}')
        input('Presione Enter para continuar...')
        system('cls')

    

    
              
        
    def Tabla_resumen_Pasajero(self):
        query = "select ID_ASIGNACION, PASAJERO_RESPONSABLE,ID_HABITACION,NUM_HABITACION from ASIGNACION "
        self.cursor.execute(query)
        columnas = [desc[0] for desc in self.cursor.description]
        resultados = self.cursor.fetchall()
        print(tabulate(resultados, headers=columnas, tablefmt="pretty"))
        input('Presione Enter para continuar...')
        system('cls')
    
    def Tabla_resumen_Habitacion(self):
        query = "SELECT ID_HABITACION, NUM_HABITACION, ESTADO FROM HABITACION"
        self.cursor.execute(query)
        columnas = [desc[0] for desc in self.cursor.description]
        resultados = self.cursor.fetchall()
        print(tabulate(resultados, headers=columnas, tablefmt="pretty"))
        input('Presione Enter para continuar...')
        system('cls')
   

    
    
    def Eliminar_pasajero(self):
        # Mostrar las asignaciones actuales
        query = "SELECT ID_ASIGNACION, PASAJERO_RESPONSABLE, ID_HABITACION, NUM_HABITACION FROM ASIGNACION"
        self.cursor.execute(query)
        columnas = [desc[0] for desc in self.cursor.description]
        resultados = self.cursor.fetchall()
        print(tabulate(resultados, headers=columnas, tablefmt="pretty"))

        pasajero = input('Ingrese el nombre del pasajero que desea eliminar de la habitación: ')
        id_hab = int(input('Ingrese el ID de la habitación en la que desea eliminar el pasajero: '))

   
        sql1 = '''
        SELECT * FROM ASIGNACION WHERE PASAJERO_RESPONSABLE = %s AND ID_HABITACION = %s
        '''
        try:
            self.cursor.execute(sql1, (pasajero, id_hab))
            if self.cursor.fetchone() is not None:
          
                sql2 = '''
                UPDATE HABITACION
                SET PASAJEROS_PASADOS = CONCAT(COALESCE(PASAJEROS_PASADOS, ''), %s, ', ')
                WHERE ID_HABITACION = %s
                '''
                try:
                    self.cursor.execute(sql2, (pasajero, id_hab))
                    self.conexion.commit()
                except Exception as err:
                    self.conexion.rollback()
                    print(f'Error al actualizar PASAJEROS_PASADOS: {err}')
                    return  

          
                sql3 = '''
                DELETE FROM ASIGNACION WHERE PASAJERO_RESPONSABLE = %s AND ID_HABITACION = %s
                '''
                try:
                    self.cursor.execute(sql3, (pasajero, id_hab))
                    self.conexion.commit()
                except Exception as err:
                    self.conexion.rollback()
                    print(f'Error al eliminar el pasajero de ASIGNACION: {err}')
                    return


                sql4 = '''
                UPDATE HABITACION 
                SET PASAJERO_RESPONSABLE = NULL, ESTADO = %s
                WHERE ID_HABITACION = %s
                '''
                try:
                    self.cursor.execute(sql4, ('VACANTE', id_hab))
                    self.conexion.commit()
                    print('Pasajero eliminado')
                except Exception as err:
                    self.conexion.rollback()
                    print(f'Error al actualizar PASAJERO_RESPONSABLE y ESTADO en HABITACION: {err}')
            else:
                print('No existe el pasajero con el nombre solicitado en la habitación indicada.')
                input('Presione Enter para continuar...')
                system('cls')
        except Exception as err:
            print(f'Error en la consulta: {err}')

    def Hab_eliminadas(self):
        query = "SELECT ID_HABITACION, NUM_HABITACION,ORIENTACION, PASAJEROS_PASADOS FROM HAB_ELIMINADAS"
        self.cursor.execute(query)
        columnas = [desc[0] for desc in self.cursor.description]
        resultados = self.cursor.fetchall()
        print(tabulate(resultados, headers=columnas, tablefmt="pretty"))
        input('Presione Enter para continuar...')
        system('cls')
   
        
                    
                
        

      
            
   
        
    
                   
        
            
        
        
        
        
        
            
                    
                

            
                                
                
            
                                   