from conexion import *
from os import system

db=Database()

while True:
    print('---Menu Inicial---')
    elige1=input('\nElige una opción:\n\
    Ingresar como admin (1)\n\
    Ingresar como encargado (2)\n\
    Salir (s)\n=>')
    if elige1=='1':
        db.Entra_admin()
    elif elige1=='2':
        db.Entra_usuario()
    elif elige1=='s':
        db.cerrarBD()
        break    
    
        
                    
                
                
                
                                  
        