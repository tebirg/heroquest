#importamos clase colorama para poder tener colores por consola
#Esta clase realizará busquedas en el mapa y todo lo referente a este.
from colorama import init, Fore, Back

class Mapa():

	#-----------------------------------------------------------------------------------------------------------------------------------------------------
	## Inicialmente cargamos el mapa del juego desde un fichero txt. Este nos lo pasará la clase main donde elegirán ddcho mapa, ya sea cargado o nuevo.
	#-----------------------------------------------------------------------------------------------------------------------------------------------------
	def __init__(self,nombre):
		self.nombre=nombre
		mapa_reto=[]
		self.pos_hero={'Tipo':'inicio','Horizontal':0,'Vertical':0}

		fichero= open("mapas/"+self.nombre+".txt",'r')
		self.mapa_reto=fichero.readlines()

	#-----------------------------------------------------------------------------------------------------------------------------------------------------
	# Dibuja el mapa base, util para la ayuda inicial
	#-----------------------------------------------------------------------------------------------------------------------------------------------------
	def dibujar_mapa_base(self):
		print ("Imprimiendo mapa",self.nombre)
		print ("____________________________")

		init() #Para reiniciar colorama

		for i in range(len(self.mapa_reto)):
			linea=self.mapa_reto[i].strip()
			for k in range(len(linea)):
				if k==68:
					salto="\n"
				else:
					salto=""

				if linea[k]=='■':
					print (Fore.BLUE+linea[k], end=salto)
				else:
					print (Fore.RED+linea[k], end=salto)

	#-----------------------------------------------------------------------------------------------------------------------------------------------------
	# Muestra las casillas exploradas del mapa
	# El valor a la derecha de las casillas indica su estado:
	#	- 0 --> No explorado y por tanto no visible
	#	- 1 --> Explorado pero contiene una trampa o tesoro aun no descubierto
	#	- 2 --> Explorado contiene una trampa o tesoro descubierto
	#-----------------------------------------------------------------------------------------------------------------------------------------------------
	def muestra_mapa_explorado(self):
		init() #Para reiniciar colorama

		for t in range(len(self.mapa_reto)):
			linea=self.mapa_reto[t].strip()
			if linea=="fin_texto_reto": break

		for i in range(t+2,len(self.mapa_reto)):

			linea=self.mapa_reto[i].strip()
			
			for k in range(len(linea)):

				if linea[k].isdigit()== False:
					# Si estamos en la ultima casilla ha de ser fin de linea.
					if k==136:
						salto="\n"
					else:
						salto=""

					# Pintamos los diferentes caracteres del mapa que estén visibles
					if linea[k]=='■':
						if int(linea[k+1])==1:
							print (Fore.BLUE+linea[k],end=salto)
						else:
							print(Fore.BLACK+" ",end=salto)
							
					elif linea[k]=='*':
						if int(linea[k+1])==1:
							print (Fore.YELLOW+linea[k],end=salto)
						else:
							print(Fore.BLACK+" ",end=salto)
					elif linea[k]=='¥':
						if int(linea[k+1])==1:
							print (Fore.WHITE+linea[k],end=salto)
						else:
							print(Fore.BLACK+" ",end=salto)
					elif linea[k]=='º'  :
						if int(linea[k+1])==1:   # Para cosas escondidas el 1 significa que no lo ha encontrado y mostramos pasillo
							print (Fore.BLUE+"■",end=salto)
						elif int(linea[k+1])==2: # Para cosas escondidas el 2 significa que lo ha encontrado
							print (Fore.RED+"º",end=salto)
						else:
							print(Fore.BLACK+" ",end=salto)	
					elif linea[k]=='®'  :
						if int(linea[k+1])==1:   # Para cosas escondidas el 1 significa que no lo ha encontrado y mostramos pasillo
							print (Fore.BLUE+"■",end=salto)
						elif int(linea[k+1])==2: # Para cosas escondidas el 2 significa que lo ha encontrado
							print (Fore.RED+"®",end=salto)
						else:
							print(Fore.BLACK+" ",end=salto)
					#Enemigos
					# g Enemigo Goblin
					# o Enemigo Orco
					# f Enemigo Fimir
					# m Enemigo Momia
					# e Enemigo Esqueleto
					# b Enemigo Malbado brujo
					# G Enemigo Gargola
					elif ((linea[k]=='g' or linea[k]=='o' or linea[k]=='f' or linea[k]=='m' or linea[k]=='e' or linea[k]=='b' or linea[k]=='G')):
						if int(linea[k+1])==1:
							print (Fore.GREEN+linea[k],end=salto)
						else:
							print(Fore.BLACK+" ",end=salto)	
					elif k<=135 :
						if linea[k+1].isdigit()== True:
							if int(linea[k+1])==1:
								print (Fore.RED+linea[k],end=salto)
							else:
								print(Fore.BLACK+" ",end=salto)
					else:
						print(Fore.BLACK+" ",end=salto)


	#-----------------------------------------------------------------------------------------------------------------------------------------------------
	# Muestra la historia del mapa. El mapa ha de contener "fin_texto_reto" para sabe donde termina.
	#-----------------------------------------------------------------------------------------------------------------------------------------------------	
	def muestra_historia(self):
		init() #Para reiniciar colorama

		for i in range(len(self.mapa_reto)):
			linea=self.mapa_reto[i].strip()
			if linea=="fin_texto_reto": break
			print (Fore.YELLOW+linea)

	#-----------------------------------------------------------------------------------------------------------------------------------------------------	
	# Esta funcion buscará cualquier objeto en el mapa que se encuentre a la vista del personaje.
	#-----------------------------------------------------------------------------------------------------------------------------------------------------	
	def heroe_busca(self,objeto):
	#El mapa ha de comenzar siempre en fila 11
	
		fila	=0 # Será la fila de retorno
		columna	=0 #será la columna de retorno

		# ■ Pasillo (Alt 220)
		# ^ Puerta secreta
		# ¥ Puerta

		# ║ Pared Lateral (Alt 186)
		# ═ Pared Horizontal (Alt 205)
		# ╩ Pared esquina1 (Alt 202)
		# ╝ Pared esquina2 (Alt 188)
		# ╚ Pared esquina3 (Alt 200)
		# ╦ Pared esquina4 (Alt 203)
		# ╣ Pared esquina5 (Alt 185)
		# ╠ Pared esquina6 (Alt 204)

		# Ç Trampa de roca caida
		# º  trampa de abismo (ALT 176)
		# > Trampa flechas
		
		# # Mobiliario
		
		# ® Tesoro
		
		# g Enemigo Goblin
		# o Enemigo Orco
		# f Enemigo Fimir
		# m Enemigo Momia
		# e Enemigo Esqueleto
		# b Enemigo Malbado brujo
		# G Enemigo Gargola

		# Quitamos de la lectura la parte del texto inicial del reto.
		for t in range(len(self.mapa_reto)):
			linea=self.mapa_reto[t].strip()
			if linea=="fin_texto_reto": break

		# Comenzamos la lectura del mapa
		for i in range(t+2,len(self.mapa_reto)):

			linea=self.mapa_reto[i].strip()

			for k in range(len(linea)):

				if linea[k].isdigit()== False:
					# Del mapa ya explorado buscamos su objeto.

					if (linea[k]==objeto and int(linea[k+1])==1)and linea[k]!='*' :
						# Una vez encontrado miramos si está a la vista
						situacion_obj=self.esta_en(i,k)
						if (situacion_obj['Tipo'] == self.pos_hero['Tipo']):
							fila	=i
							columna	=k
							lista = list(linea)
							lista[k+1]= "2"
							linea= "".join(lista)
							self.mapa_reto[i]=linea

					elif (linea[k]=='*' and objeto=='*'): # Esto retorna la posicion del heroe
						fila	=i
						columna	=k
						self.pos_hero=self.esta_en(i,k)


		if fila!=0 and columna!=0:
			return True
		else:
			return False

	#-----------------------------------------------------------------------------------------------------------------------------------------------------	
	# Esta funcion devuelve la situación del personaje, monstruo u objeto, asi podremos saber que puede ver y que no.
	#	hab1	-->  Comenzando de arriiba a la izd. [Tenemos un total de 23 habitaciones]
	#	Pas1H	--> Seria pasillo 1 horizontal comenzando por arriba [18 pasillos horizontales]
	#	Pas1V	--> Seria pasillo 1 vertical comenzando por la izqd. [4 pasillos verticales   ]
	#	Pas1H1V	--> Interseccion primer pasillo vertical con primero horizontal
	#-----------------------------------------------------------------------------------------------------------------------------------------------------	
	def esta_en(self,fila,columna):


		#situacion = {'Tipo':'pasillo','Horizontal':0,'Vertical':0}
		#print(Fore.WHITE+"Devolver posicion para fila:"+str(fila)+" y columna:"+str(columna))

		if fila==10  and columna==0 			:
			situacion = {'Tipo':'pasillo','Horizontal':1,'Vertical':1}	#interseccion
		elif fila==10  and columna==136 			:
			situacion = {'Tipo':'pasillo','Horizontal':1,'Vertical':4} 	#interseccion
		elif fila==23 and columna==0 			:
			situacion = {'Tipo':'pasillo','Horizontal':10,'Vertical':1}	#interseccion
		elif fila==23 and columna==136 			:
			situacion = {'Tipo':'pasillo','Horizontal':10,'Vertical':4}	#interseccion
		elif fila==23 and columna==48 			:
			situacion = {'Tipo':'pasillo','Horizontal':10,'Vertical':2}	#interseccion
		elif fila==19  and columna==48 			:
			situacion = {'Tipo':'pasillo','Horizontal':9,'Vertical':2}	#interseccion
		elif fila==19  and columna==86 			:
			situacion = {'Tipo':'pasillo','Horizontal':9,'Vertical':3}	#interseccion
		elif fila==23 and columna==86 			:
			situacion = {'Tipo':'pasillo','Horizontal':10,'Vertical':3}	#interseccion
		elif fila==28 and columna==48 			:
			situacion = {'Tipo':'pasillo','Horizontal':11,'Vertical':2}	#interseccion
		elif fila==28 and columna==86 			:
			situacion = {'Tipo':'pasillo','Horizontal':11,'Vertical':3}	#interseccion
		elif fila==35 and columna==0 			:
			situacion = {'Tipo':'pasillo','Horizontal':18,'Vertical':1}	#interseccion
		elif fila==35 and columna==136 			:
			situacion = {'Tipo':'pasillo','Horizontal':18,'Vertical':4}	#interseccion
		elif fila==10					:
			situacion = {'Tipo':'pasillo','Horizontal':1,'Vertical':0}
		elif fila==12  and (columna>=60 and columna<=70)	:
			situacion = {'Tipo':'pasillo','Horizontal':2,'Vertical':0}
		elif fila==13  and (columna>=60 and columna<=70)	:
			situacion = {'Tipo':'pasillo','Horizontal':3,'Vertical':0}
		elif fila==14  and (columna>=60 and columna<=70)	:
			situacion = {'Tipo':'pasillo','Horizontal':4,'Vertical':0}
		elif fila==15  and (columna>=60 and columna<=70)	:
			situacion = {'Tipo':'pasillo','Horizontal':5,'Vertical':0}
		elif fila==16  and (columna>=60 and columna<=70)	:
			situacion = {'Tipo':'pasillo','Horizontal':6,'Vertical':0}
		elif fila==17  and (columna>=60 and columna<=70)	:
			situacion = {'Tipo':'pasillo','Horizontal':7,'Vertical':0}
		elif fila==18  and (columna>=60 and columna<=70)	:
			situacion = {'Tipo':'pasillo','Horizontal':8,'Vertical':0}
		elif fila==19  and (columna>=50 and columna<=84)	:
			situacion = {'Tipo':'pasillo','Horizontal':9,'Vertical':0}
		elif fila==23 and (columna>=2  and columna<=46)	:
			situacion = {'Tipo':'pasillo','Horizontal':10,'Vertical':0}
		elif fila==27 and (columna>=50 and columna<=84)	:
			situacion = {'Tipo':'pasillo','Horizontal':11,'Vertical':0}
		elif fila==28 and (columna>=60 and columna<=70)	:
			situacion = {'Tipo':'pasillo','Horizontal':12,'Vertical':0}
		elif fila==29 and (columna>=60 and columna<=70)	:
			situacion = {'Tipo':'pasillo','Horizontal':13,'Vertical':0}
		elif fila==30 and (columna>=60 and columna<=70)	:
			situacion = {'Tipo':'pasillo','Horizontal':14,'Vertical':0}
		elif fila==31 and (columna>=60 and columna<=70)	:
			situacion = {'Tipo':'pasillo','Horizontal':15,'Vertical':0}
		elif fila==32 and (columna>=60 and columna<=70)	:
			situacion = {'Tipo':'pasillo','Horizontal':16,'Vertical':0}
		elif fila==33 and (columna>=60 and columna<=70)	:
			situacion = {'Tipo':'pasillo','Horizontal':17,'Vertical':0}
		elif fila==34 					:
			situacion = {'Tipo':'pasillo','Horizontal':18,'Vertical':0}
		elif columna==0 					:
			situacion = {'Tipo':'pasillo','Horizontal':0,'Vertical':1}
		elif columna==48 					:
			situacion = {'Tipo':'pasillo','Horizontal':0,'Vertical':2}
		elif columna==86 					:
			situacion = {'Tipo':'pasillo','Horizontal':0,'Vertical':3}
		elif columna==136 					:
			situacion = {'Tipo':'pasillo','Horizontal':0,'Vertical':4}

		#----------------------- habitaciones superiores -----------------------------
		elif ((fila>=12 and fila<=15) & (columna>=4 and columna<=20)):
			situacion = {'Tipo':'habitacion1','Horizontal':fila,'Vertical':columna}
		elif ((fila>=12 and fila<=15) & (columna>=26 and columna<=44)):
			situacion = {'Tipo':'habitacion2','Horizontal':fila,'Vertical':columna}
		elif ((fila>=12 and fila<=16) & (columna>=46 and columna<=56)):
			situacion = {'Tipo':'habitacion3','Horizontal':fila,'Vertical':columna}
		elif ((fila>=12 and fila<=16) & (columna>=74 and columna<=86)):
			situacion = {'Tipo':'habitacion4','Horizontal':fila,'Vertical':columna}
		elif ((fila>=12 and fila<=16) & (columna>=90 and columna<=100)):
			situacion = {'Tipo':'habitacion5','Horizontal':fila,'Vertical':columna}			
		elif ((fila>=12 and fila<=15) & (columna>=104 and columna<=132)):
			situacion = {'Tipo':'habitacion6','Horizontal':fila,'Vertical':columna}
		elif ((fila>=17 and fila<=20) & (columna>=4 and columna<=20)):
			situacion = {'Tipo':'habitacion7','Horizontal':fila,'Vertical':columna}	
		elif (((fila>=18 and fila<=20) & (columna>=26 and columna<=44))or (fila==17 and(columna>=27 and columna<=43))):
			situacion = {'Tipo':'habitacion8','Horizontal':fila,'Vertical':columna}		
		elif ((fila>=18 and fila<=20) & (columna>=90 and columna<=98)):
			situacion = {'Tipo':'habitacion9','Horizontal':fila,'Vertical':columna}
		elif ((fila>=18 and fila<=20) & (columna>=102 and columna<=110)):
			situacion = {'Tipo':'habitacion10','Horizontal':fila,'Vertical':columna}
		elif ((fila>=17 and fila<=20) & (columna>=114 and columna<=122)):
			situacion = {'Tipo':'habitacion11','Horizontal':fila,'Vertical':columna}
		elif ((fila>=17 and fila<=20) & (columna>=126 and columna<=132)):
			situacion = {'Tipo':'habitacion12','Horizontal':fila,'Vertical':columna}
			
		# --------- habitacion central -------------------------------------------------
		elif ((fila>=20 and fila<=25) & (columna>=52 and columna<=82)):
			situacion = {'Tipo':'habitacion13','Horizontal':fila,'Vertical':columna}
			
		#----------------------- habitaciones inferiores -----------------------------		
		elif ((fila>=24 and fila<=27) & (columna>=4 and columna<=20)):
			situacion = {'Tipo':'habitacion14','Horizontal':fila,'Vertical':columna}
		elif ((fila>=24 and fila<=27) & (columna>=24 and columna<=44)):
			situacion = {'Tipo':'habitacion15','Horizontal':fila,'Vertical':columna}		
		elif ((fila>=24 and fila<=28) & (columna>=90 and columna<=100)):
			situacion = {'Tipo':'habitacion16','Horizontal':fila,'Vertical':columna}
		elif ((fila>=24 and fila<=28) & (columna>=104 and columna<=132)):
			situacion = {'Tipo':'habitacion17','Horizontal':fila,'Vertical':columna}
		elif ((fila>=29 and fila<=32) & (columna>=4 and columna<=20)):
			situacion = {'Tipo':'habitacion18','Horizontal':fila,'Vertical':columna}
		elif ((fila>=29 and fila<=32) & (columna>=24 and columna<=44)):
			situacion = {'Tipo':'habitacion19','Horizontal':fila,'Vertical':columna}
		elif ((fila>=29 and fila<=32) & (columna>=28 and columna<=56)):
			situacion = {'Tipo':'habitacion20','Horizontal':fila,'Vertical':columna}
		elif ((fila>=29 and fila<=32) & (columna>=74 and columna<=86)):
			situacion = {'Tipo':'habitacion21','Horizontal':fila,'Vertical':columna}
		elif ((fila>=30 and fila<=32) & (columna>=90 and columna<=110)):
			situacion = {'Tipo':'habitacion22','Horizontal':fila,'Vertical':columna}
		elif ((fila>=30 and fila<=32) & (columna>=114 and columna<=132)):
			situacion = {'Tipo':'habitacion23','Horizontal':fila,'Vertical':columna}
		else:
			situacion = {'Tipo':'muro','Horizontal':fila,'Vertical':columna}
		
		#print(situacion)
		return(situacion)
			

	#-----------------------------------------------------------------------------------------------------------------------------------------------------	
	# Esta funcion buscará moverá al personaje
	#-----------------------------------------------------------------------------------------------------------------------------------------------------	
	def heroe_se_mueve(self,movimiento):

		fila	=0 # Será la fila de retorno
		columna	=0 #será la columna de retorno
		sw=True
		mensaje=''
		self.heroe_busca("*") #Actualizamos la nueva posicion de nuestro heroe
		posicion_actual = self.pos_hero
						
		# Quitamos de la lectura la parte del texto inicial del reto.
		for t in range(len(self.mapa_reto)):
			linea=self.mapa_reto[t].strip()
			if linea=="fin_texto_reto": break

		# Comenzamos la lectura de las filas del mapa, ojo los contadores inician en 0
		for i in range(t+2,len(self.mapa_reto)):

			linea=self.mapa_reto[i].strip()

		# Comenzamos la lectura de las columnas del mapa, ojo los contadores inician en 0	
			for k in range(len(linea)):
				if linea[k].isdigit()== False:
			# -------------- mueve arriba ---------------------------
					
					if linea[k]=='*' and movimiento=="up" and sw==True:				
						fila	=i
						columna	=k
						
						posicion_donde_mueve=self.esta_en(i-1,columna)
						
						lista = list(linea)
						lista[columna]= "■"
						
						linea= "".join(lista)
						self.mapa_reto[i]=linea

						linea=self.mapa_reto[i-1].strip() #Avanzamos una linea abajo
						lista = list(linea)
												
						if lista[columna]=='■':
							lista[columna]= "*"
							linea= "".join(lista)
							self.mapa_reto[i-1]=linea
							self.muestra_mapa_explorado()
						elif linea[columna]== "g":
							mensaje="Este Goblin no tiene pinta de dejarte pasar..\n Yo que tu lo esquivaría.\n"
							# No se podrá mover por tanto dejamos la linea como estaba, con el heroe en su posicion
							linea=self.mapa_reto[i].strip()
							lista = list(linea)
							lista[columna]= "*"		
							linea= "".join(lista)
							self.mapa_reto[i]=linea
							break
						# o Enemigo Orco
						elif linea[columna]== "o":
							mensaje="¿En serio te crees que un Orco va ha dejarte pasar..? \n Yo que tu lo esquivaría.\n"
							# No se podrá mover por tanto dejamos la linea como estaba, con el heroe en su posicion
							linea=self.mapa_reto[i].strip()
							lista = list(linea)
							lista[columna]= "*"		
							linea= "".join(lista)
							self.mapa_reto[i]=linea

							break

						# f Enemigo Fimir
						elif linea[columna]== "f":
							mensaje="Los Firmir no son muy amistosos.. \n Yo que tu lo esquivaría.\n"
							# No se podrá mover por tanto dejamos la linea como estaba, con el heroe en su posicion
							linea=self.mapa_reto[i].strip()
							lista = list(linea)
							lista[columna]= "*"		
							linea= "".join(lista)
							self.mapa_reto[i]=linea

							break

						# m Enemigo Momia
						elif linea[columna]== "m":
							mensaje="Con el vendaje de esa momia podrías curar muchas heridas pero, \n yo que tu la esquivaría.\n"
							# No se podrá mover por tanto dejamos la linea como estaba, con el heroe en su posicion
							linea=self.mapa_reto[i].strip()
							lista = list(linea)
							lista[columna]= "*"		
							linea= "".join(lista)
							self.mapa_reto[i]=linea

							break

						# e Enemigo Esqueleto
						elif linea[columna]== "e":
							mensaje="No te vas a colar entre los huesos de este esqueleto, \n yo que tu lo esquivaría.\n"
							# No se podrá mover por tanto dejamos la linea como estaba, con el heroe en su posicion
							linea=self.mapa_reto[i].strip()
							lista = list(linea)
							lista[columna]= "*"		
							linea= "".join(lista)
							self.mapa_reto[i]=linea

							break

						# b Enemigo Malbado brujo
						elif linea[columna]== "b":
							mensaje="Si hay un malo entre los malos ese es Malbado Brujo, \n yo que tu lo esquivaría.\n"
							# No se podrá mover por tanto dejamos la linea como estaba, con el heroe en su posicion
							linea=self.mapa_reto[i].strip()
							lista = list(linea)
							lista[columna]= "*"		
							linea= "".join(lista)
							self.mapa_reto[i]=linea

							break

						# G Enemigo Gargola
						elif linea[columna]== "G":
							mensaje="Esta Gárgola no tiene cara de buenos amigos..\n Yo que tu lo esquivaría.\n"
							# No se podrá mover por tanto dejamos la linea como estaba, con el heroe en su posicion
							linea=self.mapa_reto[i].strip()
							lista = list(linea)
							lista[columna]= "*"		
							linea= "".join(lista)
							self.mapa_reto[i]=linea

							break

						#Muebles
						elif linea[columna]== "[" or linea[columna]== "]" or linea[columna]== "#":
							mensaje="Parece que te has dado un golpe contra el mobiliario.\nCamina con cuidado guerrero.\n"
							# No se podrá mover por tanto dejamos la linea como estaba, con el heroe en su posicion
							linea=self.mapa_reto[i].strip()
							lista = list(linea)
							lista[columna]= "*"		
							linea= "".join(lista)
							self.mapa_reto[i]=linea

							break
						elif posicion_donde_mueve["Tipo"]=="muro" and linea[columna]!= "¥":
							mensaje="Parece que te has dado un golpe contra estas viejas paredes.\nCamina con cuidado.\n"
							# No se podrá mover por tanto dejamos la linea como estaba, con el heroe en su posicion
							linea=self.mapa_reto[i].strip()
							lista = list(linea)
							lista[columna]= "*"		
							linea= "".join(lista)
							self.mapa_reto[i]=linea

							break
						elif posicion_donde_mueve["Tipo"]!=posicion_actual["Tipo"]:
							
							if linea[columna]== "¥":
								linea=self.mapa_reto[i-2].strip() #Avanzamos una linea abajo
								lista = list(linea)
								lista[columna]='*'
								linea= "".join(lista)
								self.mapa_reto[i-2]=linea
								posicion_donde_mueve=self.esta_en(i-2,columna)
								lista=self.activa_exploracion(posicion_donde_mueve,lista)
								self.muestra_mapa_explorado()
							else: #CaMBIA DE PASILLO
								lista = list(linea)
								lista[columna]='*'
								linea= "".join(lista)
								self.mapa_reto[i-2]=linea
								posicion_donde_mueve=self.esta_en(i-2,columna)
								lista=self.activa_exploracion(posicion_donde_mueve,lista)
								self.muestra_mapa_explorado()

						sw=False
						print('\n')
						break
			# -------------- mueve abajo ---------------------------
					if linea[k]=='*' and movimiento=="down" and sw==True:				
						fila	=i
						columna	=k
						posicion_donde_mueve=self.esta_en(i+1,columna)
						lista = list(linea)
						
						lista[columna]= "■"
						
						linea= "".join(lista)
						self.mapa_reto[i]=linea

						linea=self.mapa_reto[i+1].strip() #Avanzamos una linea abajo
						lista = list(linea)
						
						if lista[columna]=='■':
							lista[columna]= "*"
							linea= "".join(lista)
							self.mapa_reto[i+1]=linea
							self.muestra_mapa_explorado()
						elif linea[columna]== "g":
							print(Fore.YELLOW+"Este Goblin no tiene pinta de dejarte pasar..\nYo que tu lo esquivaría.\n")
							# No se podrá mover por tanto dejamos la linea como estaba, con el heroe en su posicion
							linea=self.mapa_reto[i].strip()
							lista = list(linea)
							lista[columna]= "*"		
							linea= "".join(lista)
							self.mapa_reto[i]=linea

							break
						# o Enemigo Orco
						elif linea[columna]== "o":
							print(Fore.YELLOW+"¿En serio te crees que un Orco va ha dejarte pasar..? \nYo que tu lo esquivaría.\n")
							# No se podrá mover por tanto dejamos la linea como estaba, con el heroe en su posicion
							linea=self.mapa_reto[i].strip()
							lista = list(linea)
							lista[columna]= "*"		
							linea= "".join(lista)
							self.mapa_reto[i]=linea

							break

						# f Enemigo Fimir
						elif linea[columna]== "f":
							print(Fore.YELLOW+"Los Firmir no son muy amistosos.. \nYo que tu lo esquivaría.\n")
							# No se podrá mover por tanto dejamos la linea como estaba, con el heroe en su posicion
							linea=self.mapa_reto[i].strip()
							lista = list(linea)
							lista[columna]= "*"		
							linea= "".join(lista)
							self.mapa_reto[i]=linea

							break

						# m Enemigo Momia
						elif linea[columna]== "m":
							print(Fore.YELLOW+"Con el vendaje de esa momia podrías curar muchas heridas pero, \nyo que tu la esquivaría.\n")
							# No se podrá mover por tanto dejamos la linea como estaba, con el heroe en su posicion
							linea=self.mapa_reto[i].strip()
							lista = list(linea)
							lista[columna]= "*"		
							linea= "".join(lista)
							self.mapa_reto[i]=linea

							break

						# e Enemigo Esqueleto
						elif linea[columna]== "e":
							print(Fore.YELLOW+"No te vas a colar entre los huesos de este esqueleto, \nyo que tu lo esquivaría.\n")
							# No se podrá mover por tanto dejamos la linea como estaba, con el heroe en su posicion
							linea=self.mapa_reto[i].strip()
							lista = list(linea)
							lista[columna]= "*"		
							linea= "".join(lista)
							self.mapa_reto[i]=linea

							break

						# b Enemigo Malbado brujo
						elif linea[columna]== "b":
							print(Fore.YELLOW+"Si hay un malo entre los malos ese es Malbado Brujo, \nyo que tu lo esquivaría.\n")
							# No se podrá mover por tanto dejamos la linea como estaba, con el heroe en su posicion
							linea=self.mapa_reto[i].strip()
							lista = list(linea)
							lista[columna]= "*"		
							linea= "".join(lista)
							self.mapa_reto[i]=linea

							break

						# G Enemigo Gargola
						elif linea[columna]== "G":
							print(Fore.YELLOW+"Esta Gárgola no tiene cara de buenos amigos..\nYo que tu lo esquivaría.\n")
							# No se podrá mover por tanto dejamos la linea como estaba, con el heroe en su posicion
							linea=self.mapa_reto[i].strip()
							lista = list(linea)
							lista[columna]= "*"		
							linea= "".join(lista)
							self.mapa_reto[i]=linea

							break

						#Muebles
						elif linea[columna]== "[" or linea[columna]== "]" or linea[columna]== "#":
							print(Fore.YELLOW+"Parece que te has dado un golpe contra el mobiliario.\nCamina con cuidado guerrero.\n")
							# No se podrá mover por tanto dejamos la linea como estaba, con el heroe en su posicion
							linea=self.mapa_reto[i].strip()
							lista = list(linea)
							lista[columna]= "*"		
							linea= "".join(lista)
							self.mapa_reto[i]=linea

							break
						elif posicion_donde_mueve["Tipo"]=="muro" and linea[columna]!= "¥":
							print(Fore.YELLOW+"Parece que te has dado un golpe contra estas viejas paredes.\nCamina con cuidado.\n")
							# No se podrá mover por tanto dejamos la linea como estaba, con el heroe en su posicion
							linea=self.mapa_reto[i].strip()
							lista = list(linea)
							lista[columna]= "*"		
							linea= "".join(lista)
							self.mapa_reto[i]=linea

							break
						elif posicion_donde_mueve["Tipo"]!=posicion_actual["Tipo"]:
							
							if linea[columna]== "¥":
								linea=self.mapa_reto[i+2].strip() #Avanzamos una linea abajo
								lista = list(linea)
								lista[columna]='*'
								linea= "".join(lista)
								self.mapa_reto[i+2]=linea
								posicion_donde_mueve=self.esta_en(i+2,columna)
								lista=self.activa_exploracion(posicion_donde_mueve,lista)
								self.muestra_mapa_explorado()
							else: #CaMBIA DE PASILLO
								lista = list(linea)
								lista[columna]='*'
								linea= "".join(lista)
								self.mapa_reto[i+2]=linea
								posicion_donde_mueve=self.esta_en(i+2,columna)
								lista=self.activa_exploracion(posicion_donde_mueve,lista)
								self.muestra_mapa_explorado()

						sw=False
						print('\n')
						break
						
			# -------------- mueve izquierda ---------------------------
					if linea[k]=='*' and movimiento=="left":
						fila	=i
						columna	=k
						
						posicion_donde_mueve=self.esta_en(fila,columna-2)

						if linea[columna-2]== "■":
							self.pos_hero=self.esta_en(fila,(columna-2))
							lista = list(linea)
							lista[columna-2]= "*"                        # Es +2 porque pese a moverse una posicion en la linea tenemos números para las visualizaciones en el mapa.
							lista[columna]= "■"
												     # Tenemos la anterior posición y la nueva del heroe. Haremos diversas comprobaciones
							linea= "".join(lista)
							self.mapa_reto[i]=linea
							self.muestra_mapa_explorado()
							print('\n')
							break
						#aki poner elif si trampa o monstruo u mueble
						# g Enemigo Goblin
						elif linea[columna-2]== "g":
							print(Fore.YELLOW+"Este Goblin no tiene pinta de dejarte pasar..\n Yo que tu lo esquivaría.\n")
							break
						# o Enemigo Orco
						elif linea[columna-2]== "o":
							print(Fore.YELLOW+"¿En serio te crees que un Orco va ha dejarte pasar..? \n Yo que tu lo esquivaría.\n")
							break

						# f Enemigo Fimir
						elif linea[columna-2]== "f":
							print(Fore.YELLOW+"Los Firmir no son muy amistosos.. \n Yo que tu lo esquivaría.\n")
							break

						# m Enemigo Momia
						elif linea[columna-2]== "m":
							print(Fore.YELLOW+"Con el vendaje de esa momia podrías curar muchas heridas pero, \n yo que tu la esquivaría.\n")
							break

						# e Enemigo Esqueleto
						elif linea[columna-2]== "e":
							print(Fore.YELLOW+"No te vas a colar entre los huesos de este esqueleto, \n yo que tu lo esquivaría.\n")
							break

						# b Enemigo Malbado brujo
						elif linea[columna-2]== "b":
							print(Fore.YELLOW+"Si hay un malo entre los malos ese es Malbado Brujo, \n yo que tu lo esquivaría.\n")
							break

						# G Enemigo Gargola
						elif linea[columna-2]== "G":
							print(Fore.YELLOW+"Esta Gárgola no tiene cara de buenos amigos..\n Yo que tu lo esquivaría.\n")
							break
						#Muebles
						elif linea[columna-2]== "[" or linea[columna-2]== "]" or linea[columna-2]== "#":
							print(Fore.YELLOW+"Parece que te has dado un golpe contra el mobiliario.\n Camina con cuidado guerrero.\n")
							break
						elif posicion_donde_mueve["Tipo"]=="muro" and linea[columna-2]!= "¥":
							print(Fore.YELLOW+"Parece que te has dado un golpe contra estas viejas paredes.\n Camina con cuidado.\n")
							break
						elif posicion_donde_mueve["Tipo"]!=posicion_actual["Tipo"]:
														
							if linea[columna-2]== "¥":
								lista = list(linea)
								self.pos_hero=self.esta_en(fila,(columna-4))
								posicion_donde_mueve=self.esta_en(fila,columna-4) #Actualizamos donde mueve pues ha cruzado una puerta y aqui suma +4 para cruzarla
								lista=self.activa_exploracion(posicion_donde_mueve,lista)
								lista[columna-4]= "*" # Esto es para cruzar la puerta
								lista[columna]="■"
							else:
								lista = list(linea)
								self.pos_hero=self.esta_en(fila,(columna-2))
								lista=self.activa_exploracion(posicion_donde_mueve,lista)
								lista[columna]="■"
								lista[columna-2]= "*"
							
							self.muestra_mapa_explorado()

							linea= "".join(lista)
							self.mapa_reto[i]=linea
							self.muestra_mapa_explorado()
							print('\n')
							break
			# -------------- mueve derecha ---------------------------
					elif linea[k]=='*' and movimiento=="right":
						fila	=i
						columna	=k
						
						posicion_donde_mueve=self.esta_en(fila,columna+2)

						if linea[columna+2]== "■":
							self.pos_hero=self.esta_en(fila,(columna+2))
							lista = list(linea)
							lista[columna+2]= "*"                        # Es +2 porque pese a moverse una posicion en la linea tenemos números para las visualizaciones en el mapa.
							lista[columna]= "■"
												     # Tenemos la anterior posición y la nueva del heroe. Haremos diversas comprobaciones
							linea= "".join(lista)
							self.mapa_reto[i]=linea
							self.muestra_mapa_explorado()
							print('\n')
							break
						#aki poner elif si trampa o monstruo u mueble
						# g Enemigo Goblin
						elif linea[columna+2]== "g":
							print(Fore.YELLOW+"Este Goblin no tiene pinta de dejarte pasar..\n Yo que tu lo esquivaría.\n")
							break
						# o Enemigo Orco
						elif linea[columna+2]== "o":
							print(Fore.YELLOW+"¿En serio te crees que un Orco va ha dejarte pasar..? \n Yo que tu lo esquivaría.\n")
							break

						# f Enemigo Fimir
						elif linea[columna+2]== "f":
							print(Fore.YELLOW+"Los Firmir no son muy amistosos.. \n Yo que tu lo esquivaría.\n")
							break

						# m Enemigo Momia
						elif linea[columna+2]== "m":
							print(Fore.YELLOW+"Con el vendaje de esa momia podrías curar muchas heridas pero, \n yo que tu la esquivaría.\n")
							break

						# e Enemigo Esqueleto
						elif linea[columna+2]== "e":
							print(Fore.YELLOW+"No te vas a colar entre los huesos de este esqueleto, \n yo que tu lo esquivaría.\n")
							break

						# b Enemigo Malbado brujo
						elif linea[columna+2]== "b":
							print(Fore.YELLOW+"Si hay un malo entre los malos ese es Malbado Brujo, \n yo que tu lo esquivaría.\n")
							break

						# G Enemigo Gargola
						elif linea[columna+2]== "G":
							print(Fore.YELLOW+"Esta Gárgola no tiene cara de buenos amigos..\n Yo que tu lo esquivaría.\n")
							break

						#Muebles
						elif linea[columna+2]== "[" or linea[columna+2]== "]" or linea[columna+2]== "#":
							print(Fore.YELLOW+"Parece que te has dado un golpe contra el mobiliario.\n Camina con cuidado guerrero.\n")
							break
						elif posicion_donde_mueve["Tipo"]=="muro" and linea[columna+2]!= "¥":
							print(Fore.YELLOW+"Parece que te has dado un golpe contra estas viejas paredes.\n Camina con cuidado.\n")
							break
						elif posicion_donde_mueve["Tipo"]!=posicion_actual["Tipo"]:
														
							if linea[columna+2]== "¥":
								lista = list(linea)
								self.pos_hero=self.esta_en(fila,(columna-4))
								posicion_donde_mueve=self.esta_en(fila,columna+4) #Actualizamos donde mueve pues ha cruzado una puerta y aqui suma +4 para cruzarla
								lista=self.activa_exploracion(posicion_donde_mueve,lista)
								lista[columna+4]= "*" # Esto es para cruzar la puerta
								lista[columna]="■"
							else:
								lista = list(linea)
								lista=self.activa_exploracion(posicion_donde_mueve,lista)
								self.pos_hero=self.esta_en(fila,(columna+2))
								lista[columna]="■"
								lista[columna+2]= "*"
							
							self.muestra_mapa_explorado()

							linea= "".join(lista)
							self.mapa_reto[i]=linea
							self.muestra_mapa_explorado()
							print('\n')
							break
		return(mensaje)


	def activa_exploracion(self,posicion_donde_mueve,lista):

		
		if posicion_donde_mueve["Tipo"]== "habitacion23":
			#((fila>=29 and fila<=32) & (columna>=114 and columna<=132))
			# Quitamos de la lectura la parte del texto inicial del reto.
			for t in range(len(self.mapa_reto)):
				linea=self.mapa_reto[t].strip()
				if linea=="fin_texto_reto": break
			# Comenzamos la lectura de las filas del mapa, ojo los contadores inician en 0
			for i in range(t+2,len(self.mapa_reto)):
				linea=self.mapa_reto[i].strip()
			# Comenzamos la lectura de las columnas del mapa, ojo los contadores inician en 0	
				for k in range(len(linea)):
					if linea[k].isdigit()== False:
						if ((i>=29 and i<=33) & (k>=114 and k<=134)): #Si estamos en la habitación mostramos el contenido hasta 134 por el muro
							if posicion_donde_mueve["Horizontal"]==i:
								lista = list(linea)
								lista[k+1]="1"
								linea= "".join(lista)
							else:
								lista_aux = list(linea)
								lista_aux[k+1]="1"
								linea= "".join(lista_aux)
								
							self.mapa_reto[i]=linea
		elif (posicion_donde_mueve["Tipo"]=="pasillo" and  posicion_donde_mueve["Horizontal"]==18 and posicion_donde_mueve["Vertical"]==0):
			#fila==35
			# Quitamos de la lectura la parte del texto inicial del reto.
			for t in range(len(self.mapa_reto)):
				linea=self.mapa_reto[t].strip()
				if linea=="fin_texto_reto": break
			# Comenzamos la lectura de las filas del mapa, ojo los contadores inician en 0
			for i in range(t+2,len(self.mapa_reto)):
				linea=self.mapa_reto[i].strip()
			# Comenzamos la lectura de las columnas del mapa, ojo los contadores inician en 0	
				for k in range(len(linea)):
					if linea[k].isdigit()== False:
						if ((i==34 and (k>=0 and k<=137)) or (i==33 and((k>=2 and k<=58)or (k>=72 and k<=135)))): #Si estamos en la habitación mostramos el contenido hasta 134 por el muro
							if posicion_donde_mueve["Horizontal"]==i:
								lista = list(linea)
								if lista[k+1]=="0":
									lista[k+1]="1"
								linea= "".join(lista)
							else:
								lista_aux = list(linea)
								if lista[k+1]=="0":
									lista_aux[k+1]="1"
								linea= "".join(lista_aux)
							self.mapa_reto[i]=linea
								
		
		#Debemos actualizar la linea actual del movimiento y devolversela aquien nos llama.
		return(lista)
										

				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
