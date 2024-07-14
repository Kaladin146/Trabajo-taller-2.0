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
        nombre_usuario=input('Ingrese nombre del usuario=')
        password_usuario=input('Ingrese password=')
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
                    Salir(s)\n=>')
                    if elige3=='1':
                        db.Registrar_Hab()
                    elif elige3=='2':
                        db.Registrar_pasajero()    
                    # elif elige3==3:
                    #     db.Tabla_resumen_Habitacion()
                    elif elige3=='4':
                       db.Tabla_resumen_Pasajero()
                    elif elige3=='5':
                        db.Eliminar_Habitacion()      
                    elif elige3=='6':
                        db.Asignacion()    
                    elif elige3=='7':
                        db.Eliminar_pasajero()    
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
                    input('Presion Enter para continuar...')
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
        id=int(input('Ingrese ID para la habitación= '))
        sql1='select ID_HABITACION from HABITACION where ID_HABITACION='+repr(id)
        try:
            self.cursor.execute(sql1)
            if self.cursor.fetchone()==None:
                Num_habitacion=int(input('Ingrese el número de la habitación: '))
                cant_max=int(input('Ingrese el número máximo de pasajeros para la habitación: '))
                Orientacion=input('Ingrese la orientacion de la habitación: ')
                sql2='insert into HABITACION values('+repr(id)+','+repr(Num_habitacion)+','+repr(cant_max)+','+repr(Orientacion)+','+repr('')+','+repr('')+','+repr('')+')'
                try:
                    self.cursor.execute(sql2)
                    self.conexion.commit()
                    print('Nueva habitacion registrada')
                    input('Presione Enter para continuar...')
                    system('cls')
                except Exception as err:
                    self.conexion.rollback()
                    print(err)
            else:
                print('Ya existe una habitacion con el ID ingresado')
                input('Presione Enter para continuar...')
                system('cls')    
        except Exception as err:
            print(err)              
        return Num_habitacion        
    
    def Registrar_pasajero(self):
        Rut_pasajero=input('Ingrese rut del pasajero: ')
        sql1='select RUT_PASAJERO from PASAJERO where RUT_PASAJERO='+repr(Rut_pasajero)
        try:
            self.cursor.execute(sql1)
            if self.cursor.fetchone()==None:
                Nombre_pasajero=input('Ingrese nombre del pasajero: ')
                Tipo_habitacion=input('Ingrese tipo de habitacion deseada: ')
                Cantidad_pasajeros=int(input('Ingrese la cantidad de pasajeros a hospedar: '))
                sql2='insert into PASAJERO values('+repr(Rut_pasajero)+','+repr(Nombre_pasajero)+','+repr(Tipo_habitacion)+','+repr(Cantidad_pasajeros)+')'
                try:
                    self.cursor.execute(sql2)
                    self.conexion.commit()
                    print('Pasajero registrado')
                    input('Presione Enter para continuar...')
                    system('cls')
                except Exception as err:
                    self.conexion.rollback()
                    print(err)
            else:
                print('Ya existe un pasajero con el rut ingresado: ')
                input('Presione Enter para continuar...')
                system('cls')            
        except Exception as err:
            print(err)   
        return Nombre_pasajero    
            
    

    def Eliminar_Habitacion(self):
        Id_habitacion=input('Escriba el id de la habitacion que desea eliminar: ')
        sql1='select * from HABITACION where ID_HABITACION='+repr(Id_habitacion)
        try:
            self.cursor.execute(sql1)
            if self.cursor.fetchone()!=None:
                try:
                    confirmar='select PASAJERO_RESPONSABLE from HABITACION'
                    try:
                        self.cursor.execute(confirmar)
                        if self.cursor.fetchone()==None:
                            sql2='delete from HABITACION where ID_HABITACION='+repr(Id_habitacion)
                            try:
                                self.cursor.execute(sql2)
                                self.conexion.commit()
                                print('Habitacion eliminada')
                                input('Presione Enter para continuar...')
                                system('cls')
                            except Exception as err:
                                self.conexion.rollback()
                                print(err)    
                        else:
                            print('Existe un pasajero asignado a esta habitacion, por lo tanto no se puede eliminar esta habitacion')
                            input('Presione Enter para continuar...')
                            system('cls')
                    except Exception as err:
                        self.conexion.rollback()
                        print(err)           
                except Exception as err:
                    self.conexion.rollback()
                    print(err)
            else:
                print('No existe habitacion con el codigo ingresado')
                input('Presione Enter para continuar...')
                system('cls')
        except Exception as err:
            print(err)                    
    
                    
    def Asignacion(self):
        fechaactual = datetime.now()
        Id_asignacion = int(input('Ingrese id de asignacion: '))
        # Consulta para verificar si existe una asignación con el mismo ID
        sql1 = 'SELECT * FROM ASIGNACION WHERE ID_ASIGNACION = %s'
        try:
            self.cursor.execute(sql1, (Id_asignacion,))
            if self.cursor.fetchone() is None:
                Rut_pasajero = input('Ingrese el rut del pasajero que desea asignar: ')
                Nombre_pasajero=input('Ingrese el nombre del pasajero: ')
                Id_habitacion = int(input('Ingrese el ID de la habitacion que desea asignar: '))
                Num_habitacion=int(input('Ingrese el numero de la habitacion: '))
                Costo = int(input('Ingrese el costo de la habitacion: '))
                Fecha = fechaactual
                # Uso de parámetros en lugar de concatenar strings para evitar SQL Injection
                sql2 = '''
                INSERT INTO ASIGNACION (ID_ASIGNACION, RUT_PASAJERO,PASAJERO_RESPONSABLE, ID_HABITACION,NUM_HABITACION, COSTO, FECHA)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                '''
                try:
                    self.cursor.execute(sql2, (Id_asignacion, Rut_pasajero,Nombre_pasajero, Id_habitacion,Num_habitacion, Costo, Fecha))
                    self.conexion.commit()
                    print('Pasajero Asignado')
                except Exception as err:
                    self.conexion.rollback()
                    print(f'Error al realizar la asignación: {err}')
                input('Presione Enter para continuar...')
                system('cls')
                sql3='''update HABITACION set PASAJERO_RESPONSABLE =%s , COSTO=%s where ID_HABITACION=%s'''
                try:
                    self.cursor.execute(sql3,(Nombre_pasajero,Costo,Id_habitacion))
                    self.conexion.commit()
                except Exception as err:
                    self.conexion.rollback()
                    print('Error al añadir a habitacion')        
            else:
                print('Ya existe una asignación con esa ID')
                input('Presione Enter para continuar...')
                system('cls')
        except Exception as err:
            print(f'Error al verificar la asignación: {err}')                
        
    def Tabla_resumen_Pasajero(self):
        query = "select ID_ASIGNACION, PASAJERO_RESPONSABLE,ID_HABITACION,NUM_HABITACION from ASIGNACION "
        self.cursor.execute(query)
        columnas = [desc[0] for desc in self.cursor.description]
        resultados = self.cursor.fetchall()
        print(tabulate(resultados, headers=columnas, tablefmt="pretty"))
        self.cursor.close()
        self.conexion.close()

    def Tabla_resumen_Habitacion(self):
        query = "select ID_HABITACION,NUM_HABITACION from HABITACION "
        self.cursor.execute(query)
        columnas = [desc[0] for desc in self.cursor.description]
        resultados = self.cursor.fetchall()
        print(tabulate(resultados, headers=columnas, tablefmt="pretty"))
        self.cursor.close()
        self.conexion.close()
        
    
    
                        
    def Eliminar_pasajero(self):
            pasajero= input('Ingrese el nombre del pasajero que desea eliminar de la habitacion: ')
            id_hab = input('Ingrese el ID de la habitacion en la que desea eliminar el pasajero: ')
            
            # Verificar si el pasajero está asignado a la habitación
            sql1 = '''
            SELECT * FROM HABITACION WHERE PASAJERO_RESPONSABLE = %s AND ID_HABITACION = %s
            '''
            try:
                self.cursor.execute(sql1, (pasajero, id_hab))
                if self.cursor.fetchone() is not None:
                    # Actualizar el campo PASAJEROS_PASADOS en la habitación
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
                        return  # Salir de la función en caso de error

                    # Eliminar el pasajero responsable de la habitación
                    sql3 = '''
                    UPDATE HABITACION 
                    SET PASAJERO_RESPONSABLE = NULL 
                    WHERE ID_HABITACION = %s
                    '''
                    try:
                        self.cursor.execute(sql3, (id_hab,))
                        self.conexion.commit()
                        print('Pasajero eliminado')
                        input('Presione Enter para continuar...')
                        system('cls')  # O usa 'clear' en sistemas Unix/Linux
                    except Exception as err:
                        self.conexion.rollback()
                        print(f'Error al eliminar el pasajero: {err}')
                else:
                    print('No existe el pasajero con el nombre solicitado en la habitación indicada.')
                    input('Presione Enter para continuar...')
                    system('cls')  # O usa 'clear' en sistemas Unix/Linux
            except Exception as err:
                print(f'Error en la consulta: {err}')       
                    
                
        

      
            
   
        
    
                   
        
            
        
        
        
        
        
            
                    
                

            
                                
                
            
                                   