#importamos clase colorama para poder tener colores por consola
"""Esta clase llevará el control del juego"""
from colorama import init, Fore, Back
from mapa import Mapa
import random
import sys, tty, termios
import os

class Reto():

	def __init__(self,nro_reto,opcion_carga,usuario):
	
		self.nro_reto 		= nro_reto
		self.opcion_carga 	= opcion_carga
		self.usuario		= usuario
		
		self.nombre_mapa =''
				
		if self.nro_reto==1:
			self.nombre_mapa="la_furia_de_ragnar"
#		elif self.nro_reto==2:                        # Agregar los mapas deseados
#			self.nombre_mapa="El mal nos persigue"
		
	def iniciar_partida(self):

		mapa_reto = Mapa(self.nombre_mapa)
		
		os.system("clear")
		
		mapa_reto.muestra_historia()
		mapa_reto.heroe_busca('*')
		
		input("#>>") # Elusuario irá avanzando según desee

		os.system("clear")

		mapa_reto.muestra_mapa_explorado()
		
		opcion=0
		
		while opcion!=99:
		
			init()
		
			print (Fore.WHITE+'\n ¿Que deseas hacer?')
			print ("____________________________")
			print (  "1. Buscar puertas secretas" ) 
			print (  "2. Buscar trampas" )
			print (  "3. Buscar tesoros" )		
			print (  "4. Moverte" )
			print (  "5. Atacar" )
			print (  "6. Defenderte" )
			print (  "7. Salvar partida" )
			print (  "8. Texto de misión" )
			print (  "99. Salir\n" )

			while True:
				try:
					opcion = int(input(Fore.WHITE+"#>>"))
					break
				except ValueError:
					print ("\n Opción no válida\n")

			#-------------------------------------------------------
			#                 BUSCAR PUERTAS SECRETAS 
			#-------------------------------------------------------
			if opcion == 1 :

				hay_puerta = mapa_reto.heroe_busca('^') 
				
				if hay_puerta==True:
					print (Fore.YELLOW+"\n Te apoyas por error en un candelabro y las rocas de la pared se abren como por arte de mágia.\n ¡Es un pasadizo secreto!")		
				else:
					print (Fore.WHITE+"\n Tu búsqueda ha sido en vano. No has encontrado nada.")
					
				print ('\n')
				input(Fore.WHITE+"#>>") # Elusuario irá avanzando según desee
				os.system("clear")
				mapa_reto.muestra_mapa_explorado()			
				
			#-------------------------------------------------------
			#                 BUSCAR TRAMPAS 
			#-------------------------------------------------------
			if opcion == 2 :

				hay_trampa 	= mapa_reto.heroe_busca('º') #abismo
				
				if hay_trampa==True:
					print (Fore.YELLOW+"\n ¡Mira que eres astut@! \n Efectivamente había un abismo oculto que has salvado en un hábil movimiento.")
				else:
					print (Fore.WHITE+"\n No hay ningún abismo por aquí.")

				hay_trampa=False
				hay_trampa = mapa_reto.heroe_busca('>')	#felchas
				
				if (hay_trampa==True):
					print (Fore.YELLOW+"\n ¡Esos reflejos son admirables! \n Pisas una baldosa floja que activa una trampa de flechas, pero en un hábil\n movimiento logras esquivarlas.")
				else:
					print (Fore.WHITE+"\n Te has librado pues no hay trampas de flechas  a la vista.")
				
				hay_trampa=False
				hay_trampa = mapa_reto.heroe_busca('Ç') #roca caida

				if (hay_trampa==True):
					print (Fore.YELLOW+"\n ¡El techo se derrumba! \n Por los pelos mi audaz guerrer@. Por esta vez solo ha sido un chichon y te salvas de una buena.")
				else:
					print (Fore.WHITE+"\n El techo está en buen estado. Esta vez no te caerá ninguna roca en la cabeza..")
				
				

				print ('\n')
				input(Fore.WHITE+"#>>") # Elusuario irá avanzando según desee
				os.system("clear")
				mapa_reto.muestra_mapa_explorado()

			#-------------------------------------------------------
			#                 BUSCAR TESOROS 
			#-------------------------------------------------------
			if opcion == 3 :
				
				hay_tesoro = mapa_reto.heroe_busca('®') #Tesoro
				
				
				if hay_tesoro==True:
					print (Fore.YELLOW+"\n ¡Eres una persona con suerte! \n Buscando bajo un empolvado armario has encontrado un tesoro.\n")
				else:
					print (Fore.WHITE+"\n Tu búsqueda ha sido en vano. No has encontrado nada.")

				print ('\n')
				input(Fore.WHITE+"#>>") # Elusuario irá avanzando según desee
				os.system("clear")
				mapa_reto.muestra_mapa_explorado()
				
			#-------------------------------------------------------
			#                      MOVERSE 
			#-------------------------------------------------------
			if opcion == 4 :
				init()	
				os.system("clear")
				print (Fore.WHITE+'Has tirado los dados.. \n')	
				
				#tirada = random.randrange(2,12,1)
				tirada=20
				
				print (Fore.WHITE+ '  _____             ')
				print (Fore.YELLOW+' /\ .  \    _____   ')
				print (Fore.WHITE+ '/. \____\  / .  /\  ')
				print (Fore.YELLOW+'\. / .  / /____/..\ ')
				print (Fore.WHITE+ ' \/____/  \.  .\  / ')
				print (Fore.YELLOW+'           \.__.\/  ')
				
				print (Fore.YELLOW+"\n Has sacado un "+str(tirada))
				input(Fore.WHITE+"#>>") # El usuario irá avanzando según desee
				os.system("clear")
				mapa_reto.muestra_mapa_explorado()
				print (Fore.WHITE+"Toca "+str(tirada)+" veces el pad de flechas para moverte:")
				
				print(Fore.WHITE+"muevete #>>")
				movimiento=0		
				while movimiento<tirada:
					
					k = self.captura_tecla()
					if k==1072:  # Arriba
						mensaje=mapa_reto.heroe_se_mueve("up")
					if k==1080:  # Abajo
						mensaje=mapa_reto.heroe_se_mueve("down")
					if k==1075:  # Izquierda
						mensaje=mapa_reto.heroe_se_mueve("left")
					if k==1077:  # Derecha
						mensaje=mapa_reto.heroe_se_mueve("right")
					else:print("")
					movimiento+=1
					
					
					os.system("clear")
					mapa_reto.muestra_mapa_explorado()
					print(Fore.YELLOW+mensaje)
			#---------------------------------------------------------------------
			#                      Imprime por pantalla el texto de la mision 
			#---------------------------------------------------------------------
			if opcion == 8 :
				init()	
				os.system("clear")
				mapa_reto.muestra_historia()


		os.system("clear")


				
	def captura_tecla(self):
			
				fd = sys.stdin.fileno()
				old_settings = termios.tcgetattr(fd)
				a=[0,0,0,0,0,0]
				try:
					tty.setraw(sys.stdin.fileno())
					a[0]=ord(sys.stdin.read(1))
					if a[0]==27:
						a[1]=ord(sys.stdin.read(1))
					if a[1]==91:
						a[2]=ord(sys.stdin.read(1))
					if (a[2]>=49 and a[2]<=54) or a[2]==91:
						a[3]=ord(sys.stdin.read(1))
					if a[3]>=48 and a[3]<=57:
						a[4]=ord(sys.stdin.read(1))
				finally:
					termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
				
				if   a==[ 10,  0,  0,   0,   0, 0]: k=  13   # Enter
				elif a==[ 27, 27,  0,   0,   0, 0]: k=  27   # Esc (double press)
				elif a==[ 27, 91, 91,  65,   0, 0]: k=1059   # F1
				elif a==[ 27, 91, 91,  66,   0, 0]: k=1060   # F2
				elif a==[ 27, 91, 91,  67,   0, 0]: k=1061   # F3
				elif a==[ 27, 91, 91,  68,   0, 0]: k=1062   # F4
				elif a==[ 27, 91, 91,  69,   0, 0]: k=1063   # F5
				elif a==[ 27, 91, 49,  55, 126, 0]: k=1064   # F6
				elif a==[ 27, 91, 49,  56, 126, 0]: k=1065   # F7
				elif a==[ 27, 91, 49,  57, 126, 0]: k=1066   # F8
				elif a==[ 27, 91, 50,  48, 126, 0]: k=1067   # F9
				elif a==[ 27, 91, 50,  49, 126, 0]: k=1068   # F10
				elif a==[ 27, 91, 50,  51, 126, 0]: k=1133   # F11
				elif a==[ 27, 91, 50,  52, 126, 0]: k=1134   # F12
				elif a==[ 27, 91, 50, 126,   0, 0]: k=1082   # Ins
				elif a==[ 27, 91, 51, 126,   0, 0]: k=1083   # Del
				elif a==[ 27, 91, 49, 126,   0, 0]: k=1071   # Home
				elif a==[ 27, 91, 52, 126,   0, 0]: k=1079   # End
				elif a==[ 27, 91, 53, 126,   0, 0]: k=1073   # Pg Up
				elif a==[ 27, 91, 54, 126,   0, 0]: k=1081   # Pg Dn
				elif a==[ 27, 91, 65,   0,   0, 0]: k=1072   # Up
				elif a==[ 27, 91, 66,   0,   0, 0]: k=1080   # Down
				elif a==[ 27, 91, 68,   0,   0, 0]: k=1075   # Left
				elif a==[ 27, 91, 67,   0,   0, 0]: k=1077   # Right
				elif a==[127,  0,  0,   0,   0, 0]: k=   8   # Backspace
				else:                               k=a[0]   # Ascii code

				return(k)




