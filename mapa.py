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
					# Si el caracter de linea es el tercero antes del final miramos si está visible la siguiente
					# casilla para saber si es fin de linea.
					if k<=133:
						if int(linea[k+3])==0:
							salto="\n"
						else: 
							salto=""
					# Si estamos en la ultima casilla ha de ser fin de linea.
					elif k==136:
						 salto="\n"

					# Pintamos los diferentes caracteres del mapa que estén visibles
					if linea[k]=='■' and int(linea[k+1])==1:
						print (Fore.BLUE+linea[k], end=salto)

					elif linea[k]=='*' and int(linea[k+1])==1:
						print (Fore.YELLOW+linea[k], end=salto)
					elif linea[k]=='¥' and int(linea[k+1])==1:
						print (Fore.WHITE+linea[k], end=salto)
					elif linea[k]=='º'  :
						if int(linea[k+1])==1:   # Para cosas escondidas el 1 significa que no lo ha encontrado y mostramos pasillo
							print (Fore.BLUE+"■", end=salto)
						elif int(linea[k+1])==2: # Para cosas escondidas el 2 significa que lo ha encontrado
							print (Fore.RED+"º", end=salto)
					elif linea[k]=='®'  :
						if int(linea[k+1])==1:   # Para cosas escondidas el 1 significa que no lo ha encontrado y mostramos pasillo
							print (Fore.BLUE+"■", end=salto)
						elif int(linea[k+1])==2: # Para cosas escondidas el 2 significa que lo ha encontrado
							print (Fore.RED+"®", end=salto)
					elif k<=135 :
						if linea[k+1].isdigit()== True:
							if int(linea[k+1])==1:
								print (Fore.RED+linea[k], end=salto)

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
		# ¥ Puerta (ALT 190)
		# ^ Puerta secreta
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

						if (situacion_obj['Tipo'] == self.pos_hero['Tipo'] and self.pos_hero['Tipo']!="pasillo"):
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

		if fila==10  and columna==1 			:
			situacion = {'Tipo':'pasillo','Horizontal':1,'Vertical':1}	#interseccion
		elif fila==10  and columna==137 			:
			situacion = {'Tipo':'pasillo','Horizontal':1,'Vertical':4} 	#interseccion
		elif fila==23 and columna==1 			:
			situacion = {'Tipo':'pasillo','Horizontal':10,'Vertical':1}	#interseccion
		elif fila==23 and columna==137 			:
			situacion = {'Tipo':'pasillo','Horizontal':10,'Vertical':4}	#interseccion
		elif fila==23 and columna==49 			:
			situacion = {'Tipo':'pasillo','Horizontal':10,'Vertical':2}	#interseccion
		elif fila==19  and columna==49 			:
			situacion = {'Tipo':'pasillo','Horizontal':9,'Vertical':2}	#interseccion
		elif fila==19  and columna==87 			:
			situacion = {'Tipo':'pasillo','Horizontal':9,'Vertical':3}	#interseccion
		elif fila==23 and columna==87 			:
			situacion = {'Tipo':'pasillo','Horizontal':10,'Vertical':3}	#interseccion
		elif fila==28 and columna==49 			:
			situacion = {'Tipo':'pasillo','Horizontal':11,'Vertical':2}	#interseccion
		elif fila==28 and columna==87 			:
			situacion = {'Tipo':'pasillo','Horizontal':11,'Vertical':3}	#interseccion
		elif fila==35 and columna==1 			:
			situacion = {'Tipo':'pasillo','Horizontal':18,'Vertical':1}	#interseccion
		elif fila==35 and columna==137 			:
			situacion = {'Tipo':'pasillo','Horizontal':18,'Vertical':4}	#interseccion
		elif fila==10					:
			situacion = {'Tipo':'pasillo','Horizontal':1,'Vertical':0}
		elif fila==12  and (columna>=61 and columna<=71)	:
			situacion = {'Tipo':'pasillo','Horizontal':2,'Vertical':0}
		elif fila==13  and (columna>=61 and columna<=71)	:
			situacion = {'Tipo':'pasillo','Horizontal':3,'Vertical':0}
		elif fila==14  and (columna>=61 and columna<=71)	:
			situacion = {'Tipo':'pasillo','Horizontal':4,'Vertical':0}
		elif fila==15  and (columna>=61 and columna<=71)	:
			situacion = {'Tipo':'pasillo','Horizontal':5,'Vertical':0}
		elif fila==16  and (columna>=61 and columna<=71)	:
			situacion = {'Tipo':'pasillo','Horizontal':6,'Vertical':0}
		elif fila==17  and (columna>=61 and columna<=71)	:
			situacion = {'Tipo':'pasillo','Horizontal':7,'Vertical':0}
		elif fila==18  and (columna>=61 and columna<=71)	:
			situacion = {'Tipo':'pasillo','Horizontal':8,'Vertical':0}
		elif fila==19  and (columna>=51 and columna<=85)	:
			situacion = {'Tipo':'pasillo','Horizontal':9,'Vertical':0}
		elif fila==23 and (columna>=3  and columna<=47)	:
			situacion = {'Tipo':'pasillo','Horizontal':10,'Vertical':0}
		elif fila==28 and (columna>=51 and columna<=85)	:
			situacion = {'Tipo':'pasillo','Horizontal':11,'Vertical':0}
		elif fila==29 and (columna>=61 and columna<=71)	:
			situacion = {'Tipo':'pasillo','Horizontal':12,'Vertical':0}
		elif fila==30 and (columna>=61 and columna<=71)	:
			situacion = {'Tipo':'pasillo','Horizontal':13,'Vertical':0}
		elif fila==31 and (columna>=61 and columna<=71)	:
			situacion = {'Tipo':'pasillo','Horizontal':14,'Vertical':0}
		elif fila==32 and (columna>=61 and columna<=71)	:
			situacion = {'Tipo':'pasillo','Horizontal':15,'Vertical':0}
		elif fila==33 and (columna>=61 and columna<=71)	:
			situacion = {'Tipo':'pasillo','Horizontal':16,'Vertical':0}
		elif fila==34 and (columna>=61 and columna<=71)	:
			situacion = {'Tipo':'pasillo','Horizontal':17,'Vertical':0}
		elif fila==35 					:
			situacion = {'Tipo':'pasillo','Horizontal':18,'Vertical':0}
		elif columna==1 					:
			situacion = {'Tipo':'pasillo','Horizontal':0,'Vertical':1}
		elif columna==49 					:
			situacion = {'Tipo':'pasillo','Horizontal':0,'Vertical':2}
		elif columna==87 					:
			situacion = {'Tipo':'pasillo','Horizontal':0,'Vertical':3}
		elif columna==137 					:
			situacion = {'Tipo':'pasillo','Horizontal':0,'Vertical':4}

		#----------------------- habitaciones superiores -----------------------------
		elif ((fila>=13 and fila<=16) & (columna>=5 and columna<=21)):
			situacion = {'Tipo':'habitacion1','Horizontal':fila,'Vertical':columna}
		elif ((fila>=13 and fila<=16) & (columna>=27 and columna<=45)):
			situacion = {'Tipo':'habitacion2','Horizontal':fila,'Vertical':columna}
		elif ((fila>=13 and fila<=17) & (columna>=47 and columna<=57)):
			situacion = {'Tipo':'habitacion3','Horizontal':fila,'Vertical':columna}
		elif ((fila>=13 and fila<=17) & (columna>=75 and columna<=87)):
			situacion = {'Tipo':'habitacion4','Horizontal':fila,'Vertical':columna}
		elif ((fila>=13 and fila<=17) & (columna>=91 and columna<=101)):
			situacion = {'Tipo':'habitacion5','Horizontal':fila,'Vertical':columna}			
		elif ((fila>=13 and fila<=16) & (columna>=105 and columna<=133)):
			situacion = {'Tipo':'habitacion6','Horizontal':fila,'Vertical':columna}
		elif ((fila>=18 and fila<=21) & (columna>=5 and columna<=21)):
			situacion = {'Tipo':'habitacion7','Horizontal':fila,'Vertical':columna}	
		elif (((fila>=19 and fila<=21) & (columna>=27 and columna<=45))or (fila==8 and(columna>=27 and columna<=43))):
			situacion = {'Tipo':'habitacion8','Horizontal':fila,'Vertical':columna}		
		elif ((fila>=19 and fila<=21) & (columna>=91 and columna<=99)):
			situacion = {'Tipo':'habitacion9','Horizontal':fila,'Vertical':columna}
		elif ((fila>=19 and fila<=21) & (columna>=103 and columna<=111)):
			situacion = {'Tipo':'habitacion10','Horizontal':fila,'Vertical':columna}
		elif ((fila>=18 and fila<=21) & (columna>=115 and columna<=123)):
			situacion = {'Tipo':'habitacion11','Horizontal':fila,'Vertical':columna}
		elif ((fila>=18 and fila<=21) & (columna>=127 and columna<=133)):
			situacion = {'Tipo':'habitacion12','Horizontal':fila,'Vertical':columna}
			
		# --------- habitacion central -------------------------------------------------
		elif ((fila>=21 and fila<=26) & (columna>=53 and columna<=83)):
			situacion = {'Tipo':'habitacion13','Horizontal':fila,'Vertical':columna}
			
		#----------------------- habitaciones inferiores -----------------------------		
		elif ((fila>=25 and fila<=28) & (columna>=5 and columna<=21)):
			situacion = {'Tipo':'habitacion14','Horizontal':fila,'Vertical':columna}
		elif ((fila>=25 and fila<=28) & (columna>=25 and columna<=45)):
			situacion = {'Tipo':'habitacion15','Horizontal':fila,'Vertical':columna}		
		elif ((fila>=25 and fila<=29) & (columna>=91 and columna<=101)):
			situacion = {'Tipo':'habitacion16','Horizontal':fila,'Vertical':columna}
		elif ((fila>=25 and fila<=29) & (columna>=105 and columna<=133)):
			situacion = {'Tipo':'habitacion17','Horizontal':fila,'Vertical':columna}
		elif ((fila>=28 and fila<=32) & (columna>=5 and columna<=21)):
			situacion = {'Tipo':'habitacion18','Horizontal':fila,'Vertical':columna}
		elif ((fila>=28 and fila<=32) & (columna>=25 and columna<=45)):
			situacion = {'Tipo':'habitacion19','Horizontal':fila,'Vertical':columna}
		elif ((fila>=28 and fila<=32) & (columna>=29 and columna<=57)):
			situacion = {'Tipo':'habitacion20','Horizontal':fila,'Vertical':columna}
		elif ((fila>=28 and fila<=32) & (columna>=75 and columna<=87)):
			situacion = {'Tipo':'habitacion21','Horizontal':fila,'Vertical':columna}
		elif ((fila>=29 and fila<=32) & (columna>=91 and columna<=111)):
			situacion = {'Tipo':'habitacion22','Horizontal':fila,'Vertical':columna}
		elif ((fila>=29 and fila<=32) & (columna>=115 and columna<=133)):
			situacion = {'Tipo':'habitacion23','Horizontal':fila,'Vertical':columna}
		else:
			situacion = {'Tipo':'muro','Horizontal':fila,'Vertical':columna}

		return(situacion)
			

	#-----------------------------------------------------------------------------------------------------------------------------------------------------	
	# Esta funcion buscará moverá al personaje
	#-----------------------------------------------------------------------------------------------------------------------------------------------------	
	def heroe_se_mueve(self,movimiento):

		fila	=0 # Será la fila de retorno
		columna	=0 #será la columna de retorno

		posicion_actual = self.pos_hero

		# Quitamos de la lectura la parte del texto inicial del reto.
		for t in range(len(self.mapa_reto)):
			linea=self.mapa_reto[t].strip()
			if linea=="fin_texto_reto": break

		# Comenzamos la lectura del mapa
		for i in range(t+2,len(self.mapa_reto)):

			linea=self.mapa_reto[i].strip()

			for k in range(len(linea)):

				if linea[k].isdigit()== False:
			# -------------- mueve izquierda ---------------------------
					if linea[k]=='*' and movimiento=="left":
						fila	=i
						columna	=k
						posicion_donde_mueve=self.esta_en(fila,columna-2)
						if lista[columna-2]== "■":
							pos_hero=self.esta_en(fila,(columna-2))
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
						elif posicion_donde_mueve["Tipo"]=="muro" and lista[columna-2]!= "¥":
							print("Parece que te has dado un golpe contra estas viejas paredes.\n Camina con cuidado.\n")
							break
						elif posicion_donde_mueve["Tipo"]!=posicion_actual["Tipo"]:
							self.activa_exploracion(posicion_donde_mueve)
							self.muestra_mapa_explorado()
							if lista[columna-2]== "¥":
								lista[columna-4]= "*" # Esto es para cruzar la puerta
							else:
								lista[columna-2]= "*"

							linea= "".join(lista)
							self.mapa_reto[i]=linea
							self.muestra_mapa_explorado()
							print('\n')
							break

			# -------------- mueve derecha  ------------------------------
					elif linea[k]=='*' and movimiento=="right":
						fila	=i
						columna	=k
						pos_hero=self.esta_en(i,(k+2))
						lista = list(linea)
						lista[k+2]= "*"			      # Es +2 porque pese a moverse una posicion en la linea tenemos números para las visualizaciones en el mapa.
						lista[k]= "■"
						linea= "".join(lista)
						self.mapa_reto[i]=linea
						self.muestra_mapa_explorado()
						print('\n')
						break

	def activa_exploracion(posicion_donde_mueve):
		print("Se ha movido a:"+posicion_donde_mueve["Tipo"])
