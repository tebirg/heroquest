#Inicio del juego
#Aqui se encontrarán las funciones de apertura de partidas, guardado de partidas y todo lo referente a cosas genéricas del juego
from colorama import init, Fore, Back
from reto import Reto
import os

os.system("clear")
print ("\n")
print ("\n")
print (Fore.YELLOW+"#>The tErMinAl rOl gaMe") 
#print (Fore.GREEN+ "   ▄█    █▄       ▄████████    ▄████████  ▄██████▄  ████████▄   ███    █▄     ▄████████    ▄████████     ███    ") 
#print (Fore.GREEN+ "  ███    ███     ███    ███   ███    ███ ███    ███ ███    ███  ███    ███   ███    ███   ███    ███ ▀█████████▄") 
#print (Fore.GREEN+ "  ███    ███     ███    █▀    ███    ███ ███    ███ ███    ███  ███    ███   ███    █▀    ███    █▀     ▀███▀▀██") 
#print (Fore.GREEN+ " ▄███▄▄▄▄███▄▄  ▄███▄▄▄      ▄███▄▄▄▄██▀ ███    ███ ███    ███  ███    ███  ▄███▄▄▄       ███            ███   ▀") 
#print (Fore.YELLOW+"▀▀███▀▀▀▀███▀  ▀▀███▀▀▀     ▀▀███▀▀▀▀▀   ███    ███ ███    ███  ███    ███ ▀▀███▀▀▀     ▀███████████     ███    ")  
#print (Fore.YELLOW+"  ███    ███     ███    █▄  ▀███████████ ███    ███ ███    ███  ███    ███   ███    █▄           ███     ███    ")  
#print (Fore.YELLOW+"  ███    ███     ███    ███   ███    ███ ███    ███ ███  ▀ ███  ███    ███   ███    ███    ▄█    ███     ███    ")  
#print (Fore.YELLOW+"  ███    █▀      ██████████   ███    ███  ▀██████▀   ▀██████▀▄█ ████████▀    ██████████  ▄████████▀     ▄████▀  ")  
#print (Fore.YELLOW+"                              ███    ███                                                                        ")
print (Fore.RED+"-------------------------------------------------------------------------------------    ")
print (Fore.RED+"|"+Fore.YELLOW+"    █    █▄    ▄█████▄  ████████ ██████▄ ██████▄   ▄   ▄   ▄██████   ████          "+Fore.RED+"| ")
print (Fore.RED+"|"+Fore.YELLOW+"   ██    ██    ██   ██   ██   ██ ██   ██ ██   ██  ██   ██  ██  ███  ██ ██ ▀██████▄ "+Fore.RED+"| ")
print (Fore.RED+"|"+Fore.YELLOW+"   ██    ██    ██   █▀   ██   ██ ██   ██ ██   ██  ██   ██  ██  █▀   ██ █▀   ▀██▀██ "+Fore.RED+"| ")
print (Fore.RED+"|"+Fore.GREEN+ "  ▄██▄▄▄▄██▄▄ ▄██▄▄▄    ▄██▄▄▄█▀ ██   ██ ██   ██  ██   ██  ██▄▄     ██       ██  ▀ "+Fore.RED+"| ")
print (Fore.RED+"|"+Fore.GREEN+ " ▀▀██▀▀▀▀██▀  ▀██▀▀▀    ▀██▀▀▀▀▀ ██   ██ ██   ██  ██   ██ ▀██▀▀    ▀█████    ██    "+Fore.RED+"| ")
print (Fore.RED+"|"+Fore.GREEN+ "   ██    ██    ██   █▄ ▀████████ ██   ██ ██ █ ██  ██   ██  ██  █▄      ██    ██    "+Fore.RED+"| ")
print (Fore.RED+"|"+Fore.GREEN+ "   ██    ██    ██   ██   ██   ██ ██   ██ ██  ███  ██   ██  ██  ███ ▄█  ██    ██    "+Fore.RED+"| ")
print (Fore.RED+"|"+Fore.YELLOW+"   ██    █▀    ███████   ██   ██ ▀████▀  ▀██████ ▄███████▀ ███████▄██████▀ ▄████▀  "+Fore.RED+"| ")
#print (Fore.YELLOW+"|                                                                                   "+Fore.RED+"| ")
print (Fore.RED+"-------------------------------------------------------------------------------------    ")
print (Fore.LIGHTRED_EX+"                              ©Esteban Rodriguez                                    "+Fore.RED+"| ")
print (Fore.RED+"-------------------------------------------------------------------------------------    ")
print ("\n")

init()

print (Fore.WHITE+" Escoge una opción:    ")
print (Fore.WHITE+"-----------------------")
print (Fore.WHITE+" 1 . Ayuda              ")
print (Fore.WHITE+" 2 . Cargar partida     ")
print (Fore.WHITE+" 3 . Nueva partida      ")
print (Fore.WHITE+" 99. Salir              ")
print ("\n")


while True:
	try:
		opcion = int(input(Fore.WHITE+"#>>"))
		break
	except ValueError:
		print ("\n Opción no válida\n")

if opcion==1:
	print (Fore.WHITE+"Manual de usuario Heroquest")
	print (Fore.WHITE+"---------------------------") 
	print ("\n")
	
elif opcion==2:
	print ("Aun no programado cho..")
	print ("\n")
	
elif opcion==3:
	os.system("clear")
	print ("\n")
	print (" Elige uno de los retos  ")
	print ("_________________________")
	print ("  1 . La furia de Ragnar ")
#	print ("  2 . El mal nos persigue") Añadir los mapas deseados
	print ("\n")
	opcion = int(input("#>>"))
	
	_reto = Reto(1,3,'') # Al objeto Reto se le pasa el nro del reto, si es carga o nueva (opcion) y el ultimo parámetro es para cargar un reto ya iniciado.
	print ("\n")
	_reto.iniciar_partida()
elif opcion==99: print("bye, bye..")
