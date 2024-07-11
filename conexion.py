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
                    Salir(s)\n=>')
                    if elige3=='1':
                        db.Registrar_Hab()
                    elif elige3=='2':
                        db.Registrar_pasajero()    
                    # elif elige3==3:
                    #     db.Tabla_resumen_Habitacion()
                    # elif elige3==4:
                    #     db.Tabla_resumen_Pasajero()
                    elif elige3=='5':
                        db.Eliminar_Habitacion()      
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
                sql2='insert into HABITACION values('+repr(id)+','+repr(Num_habitacion)+','+repr(cant_max)+','+repr(Orientacion)+','+repr(None)+','+repr(None)+','+repr(None)+')'
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
                sql2='insert into PASAJERO values('+repr(Rut_pasajero)+','+repr(Nombre_pasajero)+','+repr(Tipo_habitacion)+')'
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
    

    def Eliminar_Habitacion(self):
        Id_habitacion=input('Escriba el id de la habitacion que desea eliminar: ')
        sql1='select * from HABITACION where ID_HABITACION='+repr(Id_habitacion)
        try:
            self.cursor.execute(sql1)
            if self.cursor.fetchone()!=None:
                try:
                    confirmar='select PASAJEROS_ACTUALES from HABITACION'
                    try:
                        self.cursor.execute(confirmar)
                        if self.cursor.fetchone()==None:
                            sql1='delete from HABITACION where ID_HABITACION='+repr(Id_habitacion)
                            print('Habitacion eliminada')
                            input('Presione Enter para continuar...')
                            system('cls')
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
    
    # def Tabla_resumen_Habitacion(self):
        
    
                   
        
            
        
        
        
        
        
            
                    
                

            
                                
                
            
                                   