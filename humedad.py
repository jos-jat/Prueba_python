#import Adafruit_DHT
import datetime
import subprocess
import telegram_send
from time import sleep
import os
#from plotear_datos import crear_grafica

############################################################
#OBTENER LOS DATOS DEL SENSOR
############################################################
#DHT_SENSOR = Adafruit_DHT.DHT11
#DHT_PIN = 23
#humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
humidity, temperature = 80, 20
############################################################
#OBTENER FECHAS Y NOMBRES DE ARCHIVOS
############################################################
#print("Obteniendo fechas y nombres de archivos ...")
ahora_dt = datetime.datetime(2023,1,27,0,0)
#ahora_dt = datetime.datetime.now()

ahora_str = ahora_dt.strftime("%Y%m%d_%H%M%S")
ayer_dt = ahora_dt - datetime.timedelta(days=1)
ayer_str = ayer_dt.strftime("%Y%m%d")
#obtener el string de la fecha anterior
n_anterior = "datos_" + ayer_str
archivo_datos = 'datos.txt'
archivo_ayer_humedad = "hum_{}.jpg".format(ayer_str)
archivo_ayer_temperatura = "temp_{}.jpg".format(ayer_str)

############################################################
#cuando sean las 0 horas, hacer la grafica del archivo datos.txt
#se daran 10 minutos de gracia ...
if ahora_dt.hour == 0 and ahora_dt.minute < 10 and (not os.path.isfile(n_anterior + ".txt")):
    #print("Creando grafica por ser media noche ...")
    #intentar hacer la grafica y luego renombrarla
    try:
        #humedad
        crear_grafica('humedad', 'Humedad relativa', "1", "2", "[10:100]", archivo_datos, archivo_ayer_humedad)
        #temperatura
        #print("Grafica de humedad creada correctamente...")
        crear_grafica('temperatura', 'Temperatura', "1", "3", "[0:40]", archivo_datos, archivo_ayer_temperatura)
        sleep(3)
        #print("Grafica de temperatura creada correctamente...")
    except:
        pass
    #esperar unos dos segundos a que se creen los archivos en la memoria
    #sleep(2)
    #enviar los archivos por telegram
    #print("Intentando enviar los archivos por telegram...")
    if os.path.isfile(archivo_ayer_temperatura):
        with open(archivo_ayer_temperatura, 'rb') as archivo:
            telegram_send.send(
                conf='tsunami_experimental.conf',
                #conf='santos_lic.conf',
                files=[archivo],
                captions=["Archivo Temperamento"]
            )
    if os.path.isfile(archivo_ayer_humedad):
        with open(archivo_ayer_humedad, 'rb') as archivo:
            telegram_send.send(
                conf='tsunami_experimental.conf',
                #conf='santos_lic.conf',
                files=[archivo],
                captions=["Archivo humedad..."]
            )
    #renombrar los archivos a la fecha del dia anterior
    #print("Cambiando nombre al archivo de datos...")
    #try:
    #    subprocess.Popen(["mv", "datos.txt", n_anterior + ".txt"])
    #except FileNotFoundError:
    #    pass
print(ahora_str, humidity, temperature)
