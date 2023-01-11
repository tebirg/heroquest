#importamos clase colorama para poder tener colores por consola
#Esta clase realizará busquedas en el mapa y todo lo referente a este.
"""La calse mapa se encarga de las búsquedas de objetos y personajes, de los movimientos en dicho mapa etc. """
from colorama import init, Fore, Back

class Mapa():

	#-----------------------------------------------------------------------------------------------------------------------------------------------------
	## Inicialmente cargamos el mapa del juego desde un fichero txt. Este nos lo pasará la clase main donde elegirán ddcho mapa, ya sea cargado o nuevo.
	#-----------------------------------------------------------------------------------------------------------------------------------------------------
	def __init__(self,nombre):
		self.nombre=nombre
		mapa_reto=[]
		self.pos_hero={'Tipo':'inicio','Horizontal':0,'Vertical':0}

		fichero= open("mapas/"+self.nombre+"/"+self.nombre+".txt",'r')
		self.mapa_reto=fichero.readlines()

	#-----------------------------------------------------------------------------------------------------------------------------------------------------
	# Dibuja el mapa base, util para la ayuda inicial
	#-----------------------------------------------------------------------------------------------------------------------------------------------------
	def dibujar_mapa_base(self):
		init() #Para reiniciar colorama

		for i in range(len(self.mapa_reto)):
			linea=self.mapa_reto[i].strip()

			for k in range(len(linea)):
				if k==136:
					salto="\n"
				else:
					salto=""

				if linea[k]=='■':
					print (Fore.BLUE+linea[k], end=salto)
				elif linea[k].isnumeric()==True: pass
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
		#print(self.mapa_reto)
		print('\n\n')
		
		for i in range(len(self.mapa_reto)):

			linea=self.mapa_reto[i].strip()

			for k in range(len(linea)):

				if (linea[k].isdigit()== False and k<137 and linea[k]!='-' and linea[k]!='|') :
					# Si estamos en la ultima casilla ha de ser fin de linea.
					if k==136:
						salto="\n"
					else:
						salto=""

					# Pintamos los diferentes caracteres del mapa que estén visibles
					if linea[k]=='■':
						if int(linea[k+1])==1 :
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
					elif linea[k]=='^'  :
						if int(linea[k+1])==1:   # Para cosas escondidas el 1 significa que no lo ha encontrado y mostramos pasillo
							print (Fore.BLUE+"■",end=salto)
						elif int(linea[k+1])==2: # Para cosas escondidas el 2 significa que lo ha encontrado
							print (Fore.RED+"^",end=salto)
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
	# Muestra la historia del mapa.
	#-----------------------------------------------------------------------------------------------------------------------------------------------------	
	def muestra_historia(self):
		init() #Para reiniciar colorama
		print('\n')

		texto_reto= open("mapas/"+self.nombre+"/"+self.nombre+"_historia.txt",'r')
		
		for linea in texto_reto:
			print(Fore.LIGHTYELLOW_EX+linea,end='')
		

	#-----------------------------------------------------------------------------------------------------------------------------------------------------	
	# Esta funcion buscará cualquier objeto en el mapa que se encuentre a la vista del personaje.
	#-----------------------------------------------------------------------------------------------------------------------------------------------------	
	def heroe_busca(self,objeto):
	#El mapa ha de comenzar siempre en fila 11

		fila	=0 # Será la fila de retorno
		columna	=0 #será la columna de retorno

		# ■ Pasillo 
		# ^ Puerta secreta
		# ¥ Puerta

		# ║ Pared Lateral 
		# ═ Pared Horizontal
		# ╩ Pared esquina1 
		# ╝ Pared esquina2 
		# ╚ Pared esquina3 
		# ╦ Pared esquina4 
		# ╣ Pared esquina5 
		# ╠ Pared esquina6 

		# Ç Trampa de roca caida
		# º  trampa de abismo
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

		# Comenzamos la lectura del mapa
		for i in range(len(self.mapa_reto)):

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
							break

					elif (linea[k]=='*' and objeto=='*'): # Esto retorna la posicion del heroe
						fila	=i
						columna	=k
						self.pos_hero=self.esta_en(i,k)
						break


		if fila!=0 and columna!=0:
			return True
		else:
			return False

	#-----------------------------------------------------------------------------------------------------------------------------------------------------	
	# Esta funcion buscará moverá al personaje
	#-----------------------------------------------------------------------------------------------------------------------------------------------------	
	def heroe_se_mueve(self,movimiento):
		#print("heroe se mueve..")
		fila	=0 # Será la fila de retorno
		columna	=0 #será la columna de retorno
		sw=True
		mensaje=''
		self.heroe_busca("*") #Actualizamos la nueva posicion de nuestro heroe
		posicion_actual = self.pos_hero

		# Comenzamos la lectura de las filas del mapa, ojo los contadores inician en 0
		for i in range(len(self.mapa_reto)):

			linea=self.mapa_reto[i].strip()

		# Comenzamos la lectura de las columnas del mapa, ojo los contadores inician en 0
			for k in range(len(linea)):
				if linea[k].isdigit()== False and sw==True:
			# -------------- mueve arriba ---------------------------

					if linea[k]=='*' and movimiento=="up" and i>=1 and sw==True:
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
							if(posicion_donde_mueve["Tipo"]==posicion_actual["Tipo"] or ((posicion_actual["Tipo"]=="intersec" or posicion_donde_mueve["Tipo"]=="intersec") and (posicion_actual["Vertical"]== posicion_donde_mueve["Vertical"] or posicion_actual["Horizontal"]== posicion_donde_mueve["Horizontal"]))):
								lista[columna]= "*"
								linea= "".join(lista)
								self.mapa_reto[i-1]=linea
								if (posicion_actual["Tipo"]=="intersec" or posicion_donde_mueve["Tipo"]=="intersec"):
									lista=self.activa_exploracion(posicion_donde_mueve,lista)								
									self.muestra_mapa_explorado()

								sw=False
								break
						
						# Ç Trampa de roca caida
						# º  trampa de abismo (ALT 176)
						# > Trampa flechas
						elif lista[columna]=='>' or lista[columna]=='º' or lista[columna]=='Ç':

							if lista[columna + 1]== "2" :
								mensaje="Por aqui no puedes pasar amigo.\n Yo que tu lo esquivaría.\n"	
								# No se podrá mover por tanto dejamos la linea como estaba, con el heroe en su posicion
								linea=self.mapa_reto[i].strip()
								lista = list(linea)
								lista[columna]= "*"		
								linea= "".join(lista)
								self.mapa_reto[i]=linea
								sw=False
								break
							elif lista[columna + 1]== "1" : #En este caso activa la trampa
								if lista[columna]=='>': mensaje=" Una cordel que no has visto y el cual cruzaba el pasillo a activado el certero tiro de una ballesta.\nDeberás luchar por sobrevivir.."
								if lista[columna]=='º': mensaje=" ¡El suelo bajo tus pies se derrumba y te ves atrapado!\nDeberás luchar por sobrevivir.."
								if lista[columna]=='Ç': mensaje=" ¡Este viejo castillo no durará mucho en pie, ahora ves como el techo se derummba!\nDeberás luchar por sobrevivir.."
								lista[columna]= "*"
								linea= "".join(lista)
								self.mapa_reto[i-1]=linea
#								self.muestra_mapa_explorado()
								sw=False
								break
						# ^ Puerta secreta
						# ® Tesoro
						elif lista[columna]=='®' or lista[columna]=='^':
							if lista[columna + 1]== "2" :
								mensaje="Por aqui no puedes pasar amigo.\n Yo que tu lo esquivaría.\n"	
								# No se podrá mover por tanto dejamos la linea como estaba, con el heroe en su posicion
								linea=self.mapa_reto[i].strip()
								lista = list(linea)
								lista[columna]= "*"		
								linea= "".join(lista)
								self.mapa_reto[i]=linea
								sw=False
								break
							elif lista[columna + 1]== "1" : #hay q ver como restaurar el tesoro que había.. o lo que hubiese.. quizas con un 3 para indicar que se ha de leer del original
								lista[columna]= "*"
								lista[columna + 1]="3"
								linea= "".join(lista)
								self.mapa_reto[i-1]=linea
#								self.muestra_mapa_explorado()
								sw=False
								break
						
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
#								self.muestra_mapa_explorado()
								sw=False
								break
							else: #CaMBIA DE PASILLO
								lista = list(linea)
								lista[columna]='*'
								linea= "".join(lista)
								self.mapa_reto[i-2]=linea
								posicion_donde_mueve=self.esta_en(i-2,columna)
								lista=self.activa_exploracion(posicion_donde_mueve,lista)
#								self.muestra_mapa_explorado()
								sw=False
								break

						sw=False
						print('\n')
						break
			# -------------- mueve abajo -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
			# -------------- mueve abajo -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
			# -------------- mueve abajo -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
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
							if(posicion_donde_mueve["Tipo"]==posicion_actual["Tipo"] or ((posicion_actual["Tipo"]=="intersec" or posicion_donde_mueve["Tipo"]=="intersec") and (posicion_actual["Vertical"]== posicion_donde_mueve["Vertical"] or posicion_actual["Horizontal"]== posicion_donde_mueve["Horizontal"]))) :
								lista[columna]= "*"
								linea= "".join(lista)
								self.mapa_reto[i+1]=linea
								if (posicion_actual["Tipo"]=="intersec" or posicion_donde_mueve["Tipo"]=="intersec"):
									lista=self.activa_exploracion(posicion_donde_mueve,lista)								
									self.muestra_mapa_explorado()

								sw=False
								break
						
						# Ç Trampa de roca caida
						# º  trampa de abismo (ALT 176)
						# > Trampa flechas
						elif lista[columna]=='>' or lista[columna]=='º' or lista[columna]=='Ç':
							
							if lista[columna + 1]== "2" :
								mensaje="Por aqui no puedes pasar amigo.\n Yo que tu lo esquivaría.\n"	
								# No se podrá mover por tanto dejamos la linea como estaba, con el heroe en su posicion
								linea=self.mapa_reto[i].strip()
								lista = list(linea)
								lista[columna]= "*"		
								linea= "".join(lista)
								self.mapa_reto[i]=linea
								sw=False
								break
								
							elif lista[columna + 1]== "1" : #Ha caido en una trampa
								if lista[columna]=='>': 
									mensaje=" Un cordel que no has visto y el cual cruzaba el pasillo a activado el certero tiro de una ballesta.\nDeberás luchar por sobrevivir.."
								if lista[columna]=='º': 
									mensaje=" ¡El suelo bajo tus pies se derrumba y te ves atrapado!\nDeberás luchar por sobrevivir.."
								if lista[columna]=='Ç': 
									mensaje=" ¡Este viejo castillo no durará mucho en pie, ahora ves como el techo se derummba!\nDeberás luchar por sobrevivir.."
								lista[columna]= "*"
								linea= "".join(lista)
								self.mapa_reto[i+1]=linea
#								self.muestra_mapa_explorado()
								sw=False
								break
						# ^ Puerta secreta
						# ® Tesoro
						elif lista[columna]=='®' or lista[columna]=='^':
							if lista[columna + 1]== "2" :
								mensaje="Por aqui no puedes pasar amigo.\n Yo que tu lo esquivaría.\n"	
								# No se podrá mover por tanto dejamos la linea como estaba, con el heroe en su posicion
								linea=self.mapa_reto[i].strip()
								lista = list(linea)
								lista[columna]= "*"		
								linea= "".join(lista)
								self.mapa_reto[i]=linea
								sw=False
								break
							elif lista[columna + 1]== "1" : #hay q ver como restaurar el tesoro que había.. o lo que hubiese.. quizas con un 3 para indicar que se ha de leer del original
								lista[columna]= "*"
								lista[columna + 1]="3"
								linea= "".join(lista)
								self.mapa_reto[i+1]=linea
#								self.muestra_mapa_explorado()
								sw=False
								break
						
						elif linea[columna]== "g":
							mensaje="Este Goblin no tiene pinta de dejarte pasar..\nYo que tu lo esquivaría.\n"
							# No se podrá mover por tanto dejamos la linea como estaba, con el heroe en su posicion
							linea=self.mapa_reto[i].strip()
							lista = list(linea)
							lista[columna]= "*"		
							linea= "".join(lista)
							self.mapa_reto[i]=linea
							sw=False
							break

						# o Enemigo Orco
						elif linea[columna]== "o":
							mensaje="¿En serio te crees que un Orco va ha dejarte pasar..? \nYo que tu lo esquivaría.\n"
							# No se podrá mover por tanto dejamos la linea como estaba, con el heroe en su posicion
							linea=self.mapa_reto[i].strip()
							lista = list(linea)
							lista[columna]= "*"		
							linea= "".join(lista)
							self.mapa_reto[i]=linea
							sw=False
							break

						# f Enemigo Fimir
						elif linea[columna]== "f":
							mensaje="Los Firmir no son muy amistosos.. \nYo que tu lo esquivaría.\n"
							# No se podrá mover por tanto dejamos la linea como estaba, con el heroe en su posicion
							linea=self.mapa_reto[i].strip()
							lista = list(linea)
							lista[columna]= "*"		
							linea= "".join(lista)
							self.mapa_reto[i]=linea
							sw=False
							break

						# m Enemigo Momia
						elif linea[columna]== "m":
							mensaje="Con el vendaje de esa momia podrías curar muchas heridas pero, \nyo que tu la esquivaría.\n"
							# No se podrá mover por tanto dejamos la linea como estaba, con el heroe en su posicion
							linea=self.mapa_reto[i].strip()
							lista = list(linea)
							lista[columna]= "*"		
							linea= "".join(lista)
							self.mapa_reto[i]=linea
							sw=False
							break

						# e Enemigo Esqueleto
						elif linea[columna]== "e":
							mensaje="No te vas a colar entre los huesos de este esqueleto, \nyo que tu lo esquivaría.\n"
							# No se podrá mover por tanto dejamos la linea como estaba, con el heroe en su posicion
							linea=self.mapa_reto[i].strip()
							lista = list(linea)
							lista[columna]= "*"		
							linea= "".join(lista)
							self.mapa_reto[i]=linea
							sw=False
							break

						# b Enemigo Malbado brujo
						elif linea[columna]== "b":
							mensaje="Si hay un malo entre los malos ese es Malbado Brujo, \nyo que tu lo esquivaría.\n"
							# No se podrá mover por tanto dejamos la linea como estaba, con el heroe en su posicion
							linea=self.mapa_reto[i].strip()
							lista = list(linea)
							lista[columna]= "*"		
							linea= "".join(lista)
							self.mapa_reto[i]=linea
							sw=False
							break

						# G Enemigo Gargola
						elif linea[columna]== "G":
							mensaje="Esta Gárgola no tiene cara de buenos amigos..\nYo que tu lo esquivaría.\n"
							# No se podrá mover por tanto dejamos la linea como estaba, con el heroe en su posicion
							linea=self.mapa_reto[i].strip()
							lista = list(linea)
							lista[columna]= "*"		
							linea= "".join(lista)
							self.mapa_reto[i]=linea
							sw=False
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
							sw=False
							break
						elif posicion_donde_mueve["Tipo"]=="muro" and linea[columna]!= "¥":
							mensaje="Parece que te has dado un golpe contra estas viejas paredes.\nCamina con cuidado.\n"
							# No se podrá mover por tanto dejamos la linea como estaba, con el heroe en su posicion
							linea=self.mapa_reto[i].strip()
							lista = list(linea)
							lista[columna]= "*"		
							linea= "".join(lista)
							self.mapa_reto[i]=linea
							sw=False
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
#								self.muestra_mapa_explorado()
								sw=False
								break
							else: #CaMBIA DE PASILLO
								lista = list(linea)
								lista[columna]='*'
								linea= "".join(lista)
								self.mapa_reto[i+2]=linea
								posicion_donde_mueve=self.esta_en(i+2,columna)
								lista=self.activa_exploracion(posicion_donde_mueve,lista)
#								self.muestra_mapa_explorado()
								sw=False
								break

						sw=False
						print('\n')
						break
						
			# -------------- mueve izquierda ---------------------------
#					if linea[k]=='*' and movimiento=="left" and k>=2 and i>0 and sw==True:
					if linea[k]=='*' and movimiento=="left" and k>0 and sw==True:
						fila	=i
						columna	=k
					
						posicion_donde_mueve=self.esta_en(fila,columna-2)

						if linea[columna-2]== "■":
							if(posicion_donde_mueve["Tipo"]==posicion_actual["Tipo"] or ((posicion_actual["Tipo"]=="intersec" or posicion_donde_mueve["Tipo"]=="intersec") and (posicion_actual["Vertical"]== posicion_donde_mueve["Vertical"] or posicion_actual["Horizontal"]== posicion_donde_mueve["Horizontal"]))) :
								self.pos_hero=self.esta_en(fila,(columna-2))
								lista = list(linea)
								lista[columna-2]= "*"                        # Es -2 porque pese a moverse una posicion en la linea tenemos números para las visualizaciones en el mapa.
								lista[columna]= "■"
												     # Tenemos la anterior posición y la nueva del heroe. Haremos diversas comprobaciones
								linea= "".join(lista)
								self.mapa_reto[i]=linea
								if (posicion_actual["Tipo"]=="intersec" or posicion_donde_mueve["Tipo"]=="intersec"):
									lista=self.activa_exploracion(posicion_donde_mueve,lista)								
									self.muestra_mapa_explorado()
								print('\n')
								sw=False
								break

						# ^ Puerta secreta
						# Ç Trampa de roca caida
						# º  trampa de abismo (ALT 176)
						# > Trampa flechas
						# ® Tesoro
						elif linea[columna-2]=='®' or linea[columna-2]=='>' or linea[columna-2]=='º' or linea[columna-2]=='Ç' or linea[columna-2]=='^':
							if linea[columna - 3]== "2" :
								mensaje="Por aqui no puedes pasar amigo.\n Yo que tu lo esquivaría.\n"	
								sw=False
								break
							elif linea[columna - 3]== "1" : #hay q ver como restaurar el tesoro que había.. o lo que hubiese.. quizas con un 3 para indicar que se ha de leer del original
								self.pos_hero=self.esta_en(fila,(columna-2))
								lista = list(linea)
								lista[columna-2]= "*"
								lista[columna - 3]== "3"
								lista[columna]= "■"
								linea= "".join(lista)
								self.mapa_reto[i]=linea
								if (posicion_actual["Tipo"]=="intersec" or posicion_donde_mueve["Tipo"]=="intersec"):
									lista=self.activa_exploracion(posicion_donde_mueve,lista)								
									self.muestra_mapa_explorado()

								sw=False
								break
		
						# g Enemigo Goblin
						elif linea[columna-2]== "g":
							mensaje="Este Goblin no tiene pinta de dejarte pasar..\n Yo que tu lo esquivaría.\n"
							sw=False
							break
						# o Enemigo Orco
						elif linea[columna-2]== "o":
							mensaje="¿En serio te crees que un Orco va ha dejarte pasar..? \n Yo que tu lo esquivaría.\n"
							sw=False
							break

						# f Enemigo Fimir
						elif linea[columna-2]== "f":
							mensaje="Los Firmir no son muy amistosos.. \n Yo que tu lo esquivaría.\n"
							sw=False
							break

						# m Enemigo Momia
						elif linea[columna-2]== "m":
							mensaje="Con el vendaje de esa momia podrías curar muchas heridas pero, \n yo que tu la esquivaría.\n"
							sw=False
							break

						# e Enemigo Esqueleto
						elif linea[columna-2]== "e":
							mensaje="No te vas a colar entre los huesos de este esqueleto, \n yo que tu lo esquivaría.\n"
							sw=False
							break

						# b Enemigo Malbado brujo
						elif linea[columna-2]== "b":
							mensaje="Si hay un malo entre los malos ese es Malbado Brujo, \n yo que tu lo esquivaría.\n"
							sw=False
							break

						# G Enemigo Gargola
						elif linea[columna-2]== "G":
							mensaje="Esta Gárgola no tiene cara de buenos amigos..\n Yo que tu lo esquivaría.\n"
							sw=False
							break
						#Muebles
						elif linea[columna-2]== "[" or linea[columna-2]== "]" or linea[columna-2]== "#":
							mensaje="Parece que te has dado un golpe contra el mobiliario.\n Camina con cuidado guerrero.\n"
							sw=False
							break
						elif posicion_donde_mueve["Tipo"]=="muro" and linea[columna-2]!= "¥":
							mensaje="Parece que te has dado un golpe contra estas viejas paredes.\n Camina con cuidado.\n"
							sw=False
							break
						elif posicion_donde_mueve["Tipo"]!=posicion_actual["Tipo"]:
														
							if linea[columna-2]== "¥":
								lista = list(linea)
								self.pos_hero=self.esta_en(fila,(columna-4))
								posicion_donde_mueve=self.esta_en(fila,columna-4) #Actualizamos donde mueve pues ha cruzado una puerta y aqui suma +4 para cruzarla
								lista=self.activa_exploracion(posicion_donde_mueve,lista)
								lista[columna-4]= "*" # Esto es para cruzar la puerta
								lista[columna]="■"
								sw=False
								linea= "".join(lista)
								self.mapa_reto[i]=linea
								self.muestra_mapa_explorado()
								break
							else:
								lista = list(linea)
								self.pos_hero=self.esta_en(fila,(columna-2))
								lista=self.activa_exploracion(posicion_donde_mueve,lista)
								lista[columna]="■"
								lista[columna-2]= "*"
								linea= "".join(lista)
								self.mapa_reto[i]=linea
								sw=False
								self.muestra_mapa_explorado()
								break
							
			# -------------- mueve derecha ---------------------------
					elif linea[k]=='*' and movimiento=="right" and k<=135 and i<35 and sw==True:
						fila	=i
						columna	=k
						
						posicion_donde_mueve=self.esta_en(fila,columna+2)
						lista = list(linea)
						
						if linea[columna+2]== "■":
							if(posicion_donde_mueve["Tipo"]==posicion_actual["Tipo"] or ((posicion_actual["Tipo"]=="intersec" or posicion_donde_mueve["Tipo"]=="intersec") and (posicion_actual["Vertical"]== posicion_donde_mueve["Vertical"] or posicion_actual["Horizontal"]== posicion_donde_mueve["Horizontal"]))) :
								self.pos_hero=self.esta_en(fila,(columna+2))
								lista[columna+2]= "*"                        # Es +2 porque pese a moverse una posicion en la linea tenemos números para las visualizaciones en el mapa.
								lista[columna]= "■"
								sw=False
												     # Tenemos la anterior posición y la nueva del heroe. Haremos diversas comprobaciones
								linea= "".join(lista)
								self.mapa_reto[i]=linea
								if (posicion_actual["Tipo"]=="intersec" or posicion_donde_mueve["Tipo"]=="intersec"):
									lista=self.activa_exploracion(posicion_donde_mueve,lista)								
									self.muestra_mapa_explorado()
								print('\n')
								break

						# ^ Puerta secreta
						# Ç Trampa de roca caida
						# º  trampa de abismo (ALT 176)
						# > Trampa flechas
						# ® Tesoro
						elif lista[columna+2]=='®' or lista[columna+2]=='>' or lista[columna+2]=='º' or lista[columna+2]=='Ç' or lista[columna+2]=='^':
							
							if lista[columna + 3]== "2" :
								mensaje="Por aqui no puedes pasar amigo.\n Yo que tu lo esquivaría.\n"	
								sw=False
								break
							elif lista[columna + 3]== "1" : #hay q ver como restaurar el tesoro que había.. o lo que hubiese.. quizas con un 3 para indicar que se ha de leer del original
								self.pos_hero=self.esta_en(fila,(columna+2))
								lista[columna+2]= "*"
								lista[columna + 3]== "3"
								lista[columna]= "■"
								linea= "".join(lista)
								self.mapa_reto[i]=linea
								sw=False
#								self.muestra_mapa_explorado()
								break
						# g Enemigo Goblin
						elif linea[columna+2]== "g":
							mensaje="Este Goblin no tiene pinta de dejarte pasar..\n Yo que tu lo esquivaría.\n"
							sw=False
							break
						# o Enemigo Orco
						elif linea[columna+2]== "o":
							mensaje="¿En serio te crees que un Orco va ha dejarte pasar..? \n Yo que tu lo esquivaría.\n"
							sw=False
							break

						# f Enemigo Fimir
						elif linea[columna+2]== "f":
							mensaje="Los Firmir no son muy amistosos.. \n Yo que tu lo esquivaría.\n"
							sw=False
							break

						# m Enemigo Momia
						elif linea[columna+2]== "m":
							mensaje="Con el vendaje de esa momia podrías curar muchas heridas pero, \n yo que tu la esquivaría.\n"
							sw=False
							break

						# e Enemigo Esqueleto
						elif linea[columna+2]== "e":
							mensaje="No te vas a colar entre los huesos de este esqueleto, \n yo que tu lo esquivaría.\n"
							sw=False
							break

						# b Enemigo Malbado brujo
						elif linea[columna+2]== "b":
							mensaje="Si hay un malo entre los malos ese es Malbado Brujo, \n yo que tu lo esquivaría.\n"
							sw=False
							break

						# G Enemigo Gargola
						elif linea[columna+2]== "G":
							mensaje="Esta Gárgola no tiene cara de buenos amigos..\n Yo que tu lo esquivaría.\n"
							sw=False
							break

						#Muebles
						elif linea[columna+2]== "[" or linea[columna+2]== "]" or linea[columna+2]== "#":
							mensaje="Parece que te has dado un golpe contra el mobiliario.\n Camina con cuidado guerrero.\n"
							sw=False
							break
						elif posicion_donde_mueve["Tipo"]=="muro" and linea[columna+2]!= "¥":
							mensaje="Parece que te has dado un golpe contra estas viejas paredes.\n Camina con cuidado.\n"
							sw=False
							break
						elif posicion_donde_mueve["Tipo"]!=posicion_actual["Tipo"] and sw==True:
							
							#print("Entra en es distinto.."+str(columna))					
							if linea[columna+2]== "¥":
								lista = list(linea)
								self.pos_hero=self.esta_en(fila,(columna+4))
								posicion_donde_mueve=self.esta_en(fila,columna+4) #Actualizamos donde mueve pues ha cruzado una puerta y aqui suma +4 para cruzarla
								lista=self.activa_exploracion(posicion_donde_mueve,lista)
								lista[columna+4]= "*" # Esto es para cruzar la puerta
								lista[columna]="■"
								linea= "".join(lista)
								self.mapa_reto[i]=linea
								self.muestra_mapa_explorado()
								sw=False
								break
							else:
								lista = list(linea)
								
								lista=self.activa_exploracion(posicion_donde_mueve,lista)
								self.pos_hero=self.esta_en(fila,(columna+2))
								lista[columna]="■"
								lista[columna+2]= "*"
								linea= "".join(lista)
								self.mapa_reto[i]=linea
								self.muestra_mapa_explorado()
								sw=False
								break
							
							

							print('\n')
							sw=False
							break
							
					elif (linea[k]=='*' and movimiento=="right" and k>135) or (linea[k]=='*' and movimiento=="left" and k<2) :
						mensaje="Parece que te has dado un golpe contra estas viejas paredes.\n Camina con cuidado.\n"
						sw=False
						break
							
		return(mensaje)

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



		if fila==0  and columna==0 			:
			situacion = {'Tipo':'intersec','Horizontal':1,'Vertical':1}		#interseccion
		elif fila==0  and columna==136 			:
			situacion = {'Tipo':'intersec','Horizontal':1,'Vertical':4} 	#interseccion
		elif fila==12 and columna==0 			:
			situacion = {'Tipo':'intersec','Horizontal':10,'Vertical':1}	#interseccion
		elif fila==12 and columna==136 			:
			situacion = {'Tipo':'intersec','Horizontal':10,'Vertical':4}	#interseccion
		elif fila==12 and columna==48 			:
			situacion = {'Tipo':'intersec','Horizontal':10,'Vertical':2}	#interseccion
		elif fila==12 and columna==86 			:
			situacion = {'Tipo':'intersec','Horizontal':10,'Vertical':3}	#interseccion
		elif fila==8  and columna==48 			:
			situacion = {'Tipo':'intersec','Horizontal':9,'Vertical':2}		#interseccion
		elif fila==8  and columna==86 			:
			situacion = {'Tipo':'intersec','Horizontal':9,'Vertical':3}		#interseccion
		elif fila==8  and columna>=59 and columna<=70 			:
			situacion = {'Tipo':'intersec','Horizontal':9,'Vertical':0}		#interseccion passllo superior a hab central
		elif fila==17 and columna==48 			:
			situacion = {'Tipo':'intersec','Horizontal':11,'Vertical':2}	#interseccion
		elif fila==17 and columna==86 			:
			situacion = {'Tipo':'intersec','Horizontal':11,'Vertical':3}	#interseccion
		elif fila==24 and columna==0 			:
			situacion = {'Tipo':'intersec','Horizontal':18,'Vertical':1}	#interseccion
		elif fila==24 and columna==136 			:
			situacion = {'Tipo':'intersec','Horizontal':18,'Vertical':4}	#interseccion
		elif fila==0 and (columna>=60 or columna<=70)			:
			situacion = {'Tipo':'intersec','Horizontal':1,'Vertical':0}		#interseccion pasillo central superior
		elif fila==0					:
			situacion = {'Tipo':'pasillo','Horizontal':1,'Vertical':0}
		elif fila==1  and (columna>=60 and columna<=70)	:
			situacion = {'Tipo':'pasillo','Horizontal':2,'Vertical':0}
		elif fila==2  and (columna>=60 and columna<=70)	:
			situacion = {'Tipo':'pasillo','Horizontal':3,'Vertical':0}
		elif fila==3  and (columna>=60 and columna<=70)	:
			situacion = {'Tipo':'pasillo','Horizontal':4,'Vertical':0}
		elif fila==4  and (columna>=60 and columna<=70)	:
			situacion = {'Tipo':'pasillo','Horizontal':5,'Vertical':0}
		elif fila==5  and (columna>=60 and columna<=70)	:
			situacion = {'Tipo':'pasillo','Horizontal':6,'Vertical':0}
		elif fila==6  and (columna>=60 and columna<=70)	:
			situacion = {'Tipo':'pasillo','Horizontal':7,'Vertical':0}
		elif fila==7  and (columna>=60 and columna<=70)	:
			situacion = {'Tipo':'pasillo','Horizontal':8,'Vertical':0}
		elif fila==8  and (columna>=50 and columna<=84)	:
			situacion = {'Tipo':'pasillo','Horizontal':9,'Vertical':0}
		elif fila==12 and ((columna>=2  and columna<=46) or (columna>=87  and columna<=134))	:
			situacion = {'Tipo':'pasillo','Horizontal':10,'Vertical':0}
		elif fila==17 and (columna>=50 and columna<=84)	:
			situacion = {'Tipo':'pasillo','Horizontal':11,'Vertical':0}
		elif fila==18 and (columna>=60 and columna<=70)	:
			situacion = {'Tipo':'pasillo','Horizontal':12,'Vertical':0}
		elif fila==19 and (columna>=60 and columna<=70)	:
			situacion = {'Tipo':'pasillo','Horizontal':13,'Vertical':0}
		elif fila==20 and (columna>=60 and columna<=70)	:
			situacion = {'Tipo':'pasillo','Horizontal':14,'Vertical':0}
		elif fila==21 and (columna>=60 and columna<=70)	:
			situacion = {'Tipo':'pasillo','Horizontal':15,'Vertical':0}
		elif fila==22 and (columna>=60 and columna<=70)	:
			situacion = {'Tipo':'pasillo','Horizontal':16,'Vertical':0}
		elif fila==23 and (columna>=60 and columna<=70)	:
			situacion = {'Tipo':'pasillo','Horizontal':17,'Vertical':0}
		elif fila==24 					:
			situacion = {'Tipo':'pasillo','Horizontal':18,'Vertical':0}
		elif columna==0 					:
			situacion = {'Tipo':'pasillo','Horizontal':0,'Vertical':1}
		elif columna==48 					:
			situacion = {'Tipo':'pasillo','Horizontal':0,'Vertical':2}
		elif columna==86 and (fila not in(18,23,7,1,2,3,4,5,6,19,20,21,22) )					:
			situacion = {'Tipo':'pasillo','Horizontal':0,'Vertical':3}
		elif columna==136 and (fila not in(35,0,12)) 					:
			situacion = {'Tipo':'pasillo','Horizontal':0,'Vertical':4}

		#----------------------- habitaciones superiores -----------------------------
		elif ((fila>=2 and fila<=5) & (columna>=4 and columna<=20)):
			situacion = {'Tipo':'habitacion1','Horizontal':fila,'Vertical':columna}
		elif ((fila>=2 and fila<=5) & (columna>=26 and columna<=44)):
			situacion = {'Tipo':'habitacion2','Horizontal':fila,'Vertical':columna}
		elif ((fila>=2 and fila<=6) & (columna>=46 and columna<=56)):
			situacion = {'Tipo':'habitacion3','Horizontal':fila,'Vertical':columna}
		elif ((fila>=2 and fila<=6) & (columna>=74 and columna<=86)):
			situacion = {'Tipo':'habitacion4','Horizontal':fila,'Vertical':columna}
		elif ((fila>=2 and fila<=6) & (columna>=90 and columna<=100)):
			situacion = {'Tipo':'habitacion5','Horizontal':fila,'Vertical':columna}			
		elif ((fila>=2 and fila<=5) & (columna>=114 and columna<=132)):
			situacion = {'Tipo':'habitacion6','Horizontal':fila,'Vertical':columna}
		elif ((fila>=7 and fila<=10) & (columna>=4 and columna<=20)):
			situacion = {'Tipo':'habitacion7','Horizontal':fila,'Vertical':columna}	
		elif (((fila>=8 and fila<=10) & (columna>=26 and columna<=44))or (fila==7 and(columna>=27 and columna<=43))):
			situacion = {'Tipo':'habitacion8','Horizontal':fila,'Vertical':columna}		
		elif ((fila>=8 and fila<=10) & (columna>=90 and columna<=98)):
			situacion = {'Tipo':'habitacion9','Horizontal':fila,'Vertical':columna}
		elif ((fila>=8 and fila<=10) & (columna>=102 and columna<=110)):
			situacion = {'Tipo':'habitacion10','Horizontal':fila,'Vertical':columna}
		elif ((fila>=7 and fila<=10) & (columna>=114 and columna<=122)):
			situacion = {'Tipo':'habitacion11','Horizontal':fila,'Vertical':columna}
		elif ((fila>=7 and fila<=10) & (columna>=126 and columna<=132)):
			situacion = {'Tipo':'habitacion12','Horizontal':fila,'Vertical':columna}
			
		# --------- habitacion central -------------------------------------------------
		elif ((fila>=10 and fila<=15) & (columna>=52 and columna<=82)):
			situacion = {'Tipo':'habitacion13','Horizontal':fila,'Vertical':columna}
			
		#----------------------- habitaciones inferiores -----------------------------		
		elif ((fila>=14 and fila<=17) & (columna>=4 and columna<=20)):
			situacion = {'Tipo':'habitacion14','Horizontal':fila,'Vertical':columna}
		elif ((fila>=14 and fila<=17) & (columna>=24 and columna<=44)):
			situacion = {'Tipo':'habitacion15','Horizontal':fila,'Vertical':columna}		
		elif ((fila>=14 and fila<=18) & (columna>=90 and columna<=100)):
			situacion = {'Tipo':'habitacion16','Horizontal':fila,'Vertical':columna}
		elif ((fila>=14 and fila<=18) & (columna>=104 and columna<=132)):
			situacion = {'Tipo':'habitacion17','Horizontal':fila,'Vertical':columna}
		elif ((fila>=19 and fila<=22) & (columna>=4 and columna<=20)):
			situacion = {'Tipo':'habitacion18','Horizontal':fila,'Vertical':columna}
		elif ((fila>=19 and fila<=22) & (columna>=24 and columna<=44)):
			situacion = {'Tipo':'habitacion19','Horizontal':fila,'Vertical':columna}
		elif ((fila>=19 and fila<=22) & (columna>=28 and columna<=56)):
			situacion = {'Tipo':'habitacion20','Horizontal':fila,'Vertical':columna}
		elif ((fila>=19 and fila<=22) & (columna>=74 and columna<=86)):
			situacion = {'Tipo':'habitacion21','Horizontal':fila,'Vertical':columna}
		elif ((fila>=20 and fila<=22) & (columna>=90 and columna<=110)):
			situacion = {'Tipo':'habitacion22','Horizontal':fila,'Vertical':columna}
		elif ((fila>=20 and fila<=22) & (columna>=114 and columna<=132)):
			situacion = {'Tipo':'habitacion23','Horizontal':fila,'Vertical':columna}
		else:
			situacion = {'Tipo':'muro','Horizontal':fila,'Vertical':columna}

		return(situacion)

	def activa_exploracion(self,posicion_donde_mueve,lista):

		if posicion_donde_mueve["Tipo"]== "habitacion1":
			# Comenzamos la lectura de las filas del mapa, ojo los contadores inician en 0
			for i in range(len(self.mapa_reto)):
				linea=self.mapa_reto[i].strip()
			# Comenzamos la lectura de las columnas del mapa, ojo los contadores inician en 0	
				for k in range(len(linea)):
					if linea[k].isdigit()== False:
						if ((i>=1 and i<=6) & (k>=2 and k<=24)): #Si estamos en la habitación mostramos el contenido
							if posicion_donde_mueve["Horizontal"]==i:
								lista = list(linea)
								lista[k+1]="1"
								linea= "".join(lista)
							else:
								lista_aux = list(linea)
								lista_aux[k+1]="1"
								linea= "".join(lista_aux)	
							self.mapa_reto[i]=linea

		if posicion_donde_mueve["Tipo"]== "habitacion2":
			# Comenzamos la lectura de las filas del mapa, ojo los contadores inician en 0
			for i in range(len(self.mapa_reto)):
				linea=self.mapa_reto[i].strip()
			# Comenzamos la lectura de las columnas del mapa, ojo los contadores inician en 0	
				for k in range(len(linea)):
					if linea[k].isdigit()== False:
						if ((i>=1 and i<=6) & (k>=24 and k<=44)): #Si estamos en la habitación mostramos el contenido
							if posicion_donde_mueve["Horizontal"]==i:
								lista = list(linea)
								lista[k+1]="1"
								linea= "".join(lista)
							else:
								lista_aux = list(linea)
								lista_aux[k+1]="1"
								linea= "".join(lista_aux)	
							self.mapa_reto[i]=linea

		if posicion_donde_mueve["Tipo"]== "habitacion3":
			# Comenzamos la lectura de las filas del mapa, ojo los contadores inician en 0
			for i in range(len(self.mapa_reto)):
				linea=self.mapa_reto[i].strip()
			# Comenzamos la lectura de las columnas del mapa, ojo los contadores inician en 0	
				for k in range(len(linea)):
					if linea[k].isdigit()== False:
						if ((i>=1 and i<=7) & (k>=44 and k<=58)): #Si estamos en la habitación mostramos el contenido
							if posicion_donde_mueve["Horizontal"]==i:
								lista = list(linea)
								lista[k+1]="1"
								linea= "".join(lista)
							else:
								lista_aux = list(linea)
								lista_aux[k+1]="1"
								linea= "".join(lista_aux)	
							self.mapa_reto[i]=linea

		if posicion_donde_mueve["Tipo"]== "habitacion4":
			# Comenzamos la lectura de las filas del mapa, ojo los contadores inician en 0
			for i in range(len(self.mapa_reto)):
				linea=self.mapa_reto[i].strip()
			# Comenzamos la lectura de las columnas del mapa, ojo los contadores inician en 0	
				for k in range(len(linea)):
					if linea[k].isdigit()== False:
						if ((i>=1 and i<=7) & (k>=72 and k<=88)): #Si estamos en la habitación mostramos el contenido
							if posicion_donde_mueve["Horizontal"]==i:
								lista = list(linea)
								lista[k+1]="1"
								linea= "".join(lista)
							else:
								lista_aux = list(linea)
								lista_aux[k+1]="1"
								linea= "".join(lista_aux)	
							self.mapa_reto[i]=linea

		if posicion_donde_mueve["Tipo"]== "habitacion5":
			# Comenzamos la lectura de las filas del mapa, ojo los contadores inician en 0
			for i in range(len(self.mapa_reto)):
				linea=self.mapa_reto[i].strip()
			# Comenzamos la lectura de las columnas del mapa, ojo los contadores inician en 0	
				for k in range(len(linea)):
					if linea[k].isdigit()== False:
						if ((i>=1 and i<=7) & (k>=88 and k<=102)): #Si estamos en la habitación mostramos el contenido
							if posicion_donde_mueve["Horizontal"]==i:
								lista = list(linea)
								lista[k+1]="1"
								linea= "".join(lista)
							else:
								lista_aux = list(linea)
								lista_aux[k+1]="1"
								linea= "".join(lista_aux)	
							self.mapa_reto[i]=linea

		if posicion_donde_mueve["Tipo"]== "habitacion6":
			# Comenzamos la lectura de las filas del mapa, ojo los contadores inician en 0
			for i in range(len(self.mapa_reto)):
				linea=self.mapa_reto[i].strip()
			# Comenzamos la lectura de las columnas del mapa, ojo los contadores inician en 0	
				for k in range(len(linea)):
					if linea[k].isdigit()== False:
						if ((i>=1 and i<=6) & (k>=112 and k<=134)): #Si estamos en la habitación mostramos el contenido
							if posicion_donde_mueve["Horizontal"]==i:
								lista = list(linea)
								lista[k+1]="1"
								linea= "".join(lista)
							else:
								lista_aux = list(linea)
								lista_aux[k+1]="1"
								linea= "".join(lista_aux)	
							self.mapa_reto[i]=linea

		if posicion_donde_mueve["Tipo"]== "habitacion23":
			# Comenzamos la lectura de las filas del mapa, ojo los contadores inician en 0
			for i in range(len(self.mapa_reto)):
				linea=self.mapa_reto[i].strip()
			# Comenzamos la lectura de las columnas del mapa, ojo los contadores inician en 0	
				for k in range(len(linea)):
					if linea[k].isdigit()== False:
						if ((i>=19 and i<=23) & (k>=114 and k<=134)): #Si estamos en la habitación mostramos el contenido hasta 134 por el muro
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
			
			# Comenzamos la lectura de las filas del mapa, ojo los contadores inician en 0
			for i in range(len(self.mapa_reto)):
				linea=self.mapa_reto[i].strip()
			# Comenzamos la lectura de las columnas del mapa, ojo los contadores inician en 0	
				for k in range(len(linea)):
					if linea[k].isdigit()== False:
						if (((i==24 and (k>=0 and k<=137)) or (i==23 and((k>=2 and k<=58)or (k>=72 and k<=135))))and i<25): #Si estamos en la habitación mostramos el contenido hasta 134 por el muro
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

		elif (posicion_donde_mueve["Tipo"]=="intersec" and posicion_donde_mueve["Vertical"]==4 and posicion_donde_mueve["Horizontal"]!=10 and posicion_donde_mueve["Horizontal"]!=1):
			# Comenzamos la lectura de las filas del mapa, ojo los contadores inician en 0
			for i in range(len(self.mapa_reto)):
				linea=self.mapa_reto[i].strip()
			# Comenzamos la lectura de las columnas del mapa, ojo los contadores inician en 0	
				for k in range(len(linea)):
					
					if linea[k].isdigit()== False:
						if ((k>=134 and k<=136 and (i not in(12,24,0))) or (k==136)):
							lista = list(linea)
							if lista[k+1]=="0":
								lista[k+1]="1"
							linea= "".join(lista)
							self.mapa_reto[i]=linea

		# Interseccion del pasillo central ojo porque hay que mostrar tambien el vertical 4, es decir, dos pasillos					
		elif (posicion_donde_mueve["Tipo"]=="intersec" and posicion_donde_mueve["Vertical"]==4 and posicion_donde_mueve["Horizontal"]==10):
			# Comenzamos la lectura de las filas del mapa, ojo los contadores inician en 0
			for i in range(len(self.mapa_reto)):
				linea=self.mapa_reto[i].strip()
			# Comenzamos la lectura de las columnas del mapa, ojo los contadores inician en 0	
				for k in range(len(linea)):
					
					if linea[k].isdigit()== False:
						if ((k>=88 and k<=136 and i>=11 and i<=13) or (k>=84 and k<=86 and i==12) or (((k>=134 and k<=136 and (i not in(12,24,0))) or (k==136)))):
							lista = list(linea)
							if lista[k+1]=="0":
								lista[k+1]="1"
							linea= "".join(lista)
							self.mapa_reto[i]=linea

		elif (posicion_donde_mueve["Tipo"]=="intersec" and posicion_donde_mueve["Vertical"]==3 and posicion_donde_mueve["Horizontal"]==10):
			# Comenzamos la lectura de las filas del mapa, ojo los contadores inician en 0
			for i in range(len(self.mapa_reto)):
				linea=self.mapa_reto[i].strip()
			# Comenzamos la lectura de las columnas del mapa, ojo los contadores inician en 0	
				for k in range(len(linea)):
					
					if linea[k].isdigit()== False:
						if ( (k>=84 and k<=88 and i>8 and i<17) or (k>=86 and k<=88 and (i==7 or i==8 or i==17 or i==18)) or ((k>=84 and k<=136 and i>=11 and i<=13))):
							lista = list(linea)
							if lista[k+1]=="0":
								lista[k+1]="1"
							linea= "".join(lista)
							self.mapa_reto[i]=linea
		#Esquina superior derecha
		elif(posicion_donde_mueve["Tipo"]=="intersec" and  posicion_donde_mueve["Vertical"]==4 and posicion_donde_mueve["Horizontal"]==1):
			# Comenzamos la lectura de las filas del mapa, ojo los contadores inician en 0
			for i in range(len(self.mapa_reto)):
				linea=self.mapa_reto[i].strip()
			# Comenzamos la lectura de las columnas del mapa, ojo los contadores inician en 0	
				for k in range(len(linea)-1):
					
					if linea[k].isdigit()== False:
						if ((i>=0 and i<=1) or (i==1 and k not in(0,136,60,62,64,66,68,70) and k<=136) ):
							if i==1 and k in(0,60,62,64,66,68,70): pass
							else:
								lista = list(linea)
								if lista[k+1]=="0":
									lista[k+1]="1"
								linea= "".join(lista)
								self.mapa_reto[i]=linea
		#Pasillo central superior
		elif(posicion_donde_mueve["Tipo"]=="intersec" and  posicion_donde_mueve["Vertical"]==0 and posicion_donde_mueve["Horizontal"]==1):
			# Comenzamos la lectura de las filas del mapa, ojo los contadores inician en 0
			for i in range(len(self.mapa_reto)):
				linea=self.mapa_reto[i].strip()
			# Comenzamos la lectura de las columnas del mapa, ojo los contadores inician en 0	
				for k in range(len(linea)-1):
					#Muestra pasillo central
					if linea[k].isdigit()== False:
						if i>=1 and i<=9 and k>=58 and k<=72 :
							if (k==58 or k==72) and (i>=8 or i==0):pass
							else:
								lista = list(linea)
								if lista[k+1]=="0":
									lista[k+1]="1"
								linea= "".join(lista)
								self.mapa_reto[i]=linea
						#Muestra pasillo horizontal 1
						if ((i>=0 and i<=1) or (i==1 and k not in(0,136,60,62,64,66,68,70) and k<=136) ):
							if i==1 and k in(0,60,62,64,66,68,70): pass
							else:
								lista = list(linea)
								if lista[k+1]=="0":
									lista[k+1]="1"
								linea= "".join(lista)
								self.mapa_reto[i]=linea

		#Pasillo horizontal encima de la habitacion central
		elif(posicion_donde_mueve["Tipo"]=="intersec" and  posicion_donde_mueve["Vertical"]==0 and posicion_donde_mueve["Horizontal"]==9):
			# Comenzamos la lectura de las filas del mapa, ojo los contadores inician en 0
			for i in range(len(self.mapa_reto)):
				linea=self.mapa_reto[i].strip()
			# Comenzamos la lectura de las columnas del mapa, ojo los contadores inician en 0	
				for k in range(len(linea)-1):
					if linea[k].isdigit()== False:
						if i>=0 and i<=9 and k>=58 and k<=72 :
							if i==0 and (k==58 or k==72):pass
							else:
								lista = list(linea)
								if lista[k+1]=="0":
									lista[k+1]="1"
								linea= "".join(lista)
								self.mapa_reto[i]=linea
						if i>=7 and i<=9 and k>=46 and k<=88 :
							if (k==48 or k==86) and (i==9):pass
							elif (k>=60 and k<=70) and (i==7):pass
							else:
								lista = list(linea)
								if lista[k+1]=="0":
									lista[k+1]="1"
								linea= "".join(lista)
								self.mapa_reto[i]=linea
		#Pasillo horizontal encima de la habitacion central y lateral derecho
		elif(posicion_donde_mueve["Tipo"]=="intersec" and  posicion_donde_mueve["Vertical"]==3 and posicion_donde_mueve["Horizontal"]==9):
			# Comenzamos la lectura de las filas del mapa, ojo los contadores inician en 0
			for i in range(len(self.mapa_reto)):
				linea=self.mapa_reto[i].strip()
			# Comenzamos la lectura de las columnas del mapa, ojo los contadores inician en 0	
				for k in range(len(linea)-1):
					
					if linea[k].isdigit()== False:
						if i>=7 and i<=9 and k>=46 and k<=88 :
							if (k==48 or k==86) and (i==9):pass
							elif (k>=60 and k<=70) and (i==7):pass
							else:
								lista = list(linea)
								if lista[k+1]=="0":
									lista[k+1]="1"
								linea= "".join(lista)
								self.mapa_reto[i]=linea
						if k>=84 and k<=88 and i>=7 and i<=18:
							if ((i==12 and k==88) or(i==17 and k==84)):pass
							else:
								lista = list(linea)
								if lista[k+1]=="0":
									lista[k+1]="1"
								linea= "".join(lista)
								self.mapa_reto[i]=linea
							
								
		#print("sale activa exploracion..")
		#Debemos actualizar la linea actual del movimiento y devolversela aquien nos llama.
		return(lista)
										

				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				
