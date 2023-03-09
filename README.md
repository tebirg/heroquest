# Heroquest
Juego de rol por consola que emula al heroquest. Permitirá crear retos propios y tendrá un
mapa interactivo por el cual el heroe se moverá. inicialmente está creado para un solo jugador contra
la máquina que hará las veces de Malvado Brujo.

Pantalla principal:

![image](https://user-images.githubusercontent.com/96789961/224074946-05559389-dbb8-44bb-baf8-9e93a4b0fd47.png)

Ejemplo de Reto:

![image](https://user-images.githubusercontent.com/96789961/224075140-095d9996-f79b-44c3-96f3-25044b1609c4.png)


El mapa se verá de la siguiente forma:

![image](https://user-images.githubusercontent.com/96789961/224062504-345311c8-8bdc-4d4a-993f-d623ec30efc9.png)

La simbología dentro del mapa es:

                # * El heroe
                
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

                # ® Tesoro

                # g Enemigo Goblin
                # o Enemigo Orco
                # f Enemigo Fimir
                # m Enemigo Momia
                # e Enemigo Esqueleto
                # b Enemigo Malbado brujo
                # G Enemigo Gargola
                
                #[] Escaleras
                
                # Resto Mobiliario
                
#Instalacion en linux debian:

sudo apt install git

sudo apt install python3

sudo apt install pip

sudo apt install libcairo2-dev libxt-dev libgirepository1.0-dev

pip install pycairo PyGObject

sudo apt-get install gstreamer-1.0

sudo git clone https://github.com/tebirg/heroquest



