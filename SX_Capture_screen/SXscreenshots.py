#!/usr/bin/python
# -*- coding: utf-8 -*-

from configparser import ConfigParser
import time
import sys
import os
from datetime import datetime
from datetime import timedelta
from selenium import webdriver
import pyautogui

config = ConfigParser()
config.read("./parametros.cfg")

#print(config.sections())
# Recursos:
# https://blog.carreralinux.com.ar/2017/09/archivos-de-configuracion-acceso-desde-python/
# https://python-para-impacientes.blogspot.com/2015/01/gestionar-la-configuracion-de-un.html
# http://docs.python.org/library/datetime.html#timedelta-objects

try:
    while True:
        def ok():
            Sopciones = config['OPCIONES']
            cap_web_esc = Sopciones['Capturar_pagina_y_escritorio']
            cap_web_pos_esc = Sopciones["Capturar_pagina_c_posicion_y_escritorio"]
            cap_web = Sopciones["Capturar_solo_pagina"]
            cap_web_pos = Sopciones["Capturar_solo_pagina_c_posiciom"]
            cap_desktop = Sopciones["Capturar_solo_escritorio"]

            Sdelay = config['DELAY']
            cwe = int(Sdelay['CPag_esc'])
            cwpe = int(Sdelay['CPag_pos_esc'])
            cw = int(Sdelay['CPag'])
            cwp = int(Sdelay['CPag_pos'])
            cd = int(Sdelay['CEsc'])

            Stiempo = config['TIEMPO']
            num_caps = int(Stiempo['Capturas_por_ciclo'])
            minutos = float(Stiempo['Tiempo_del_ciclo'])

            Sadicionales = config['ADICIONALES']
            pos_scroll = int(Sadicionales['Posicion'])
            DRIVER = Sadicionales['Ruta_controlador']
            op3 = Sadicionales['Sitio']

            segundos = (minutos * 60)

            print("La primera vez que lo abres, el programa trabajará en el horario indicado y tomará su primer captura cumpliendo el mismo")
            print("Para interrumpir la ejecución, Presione CTRL+C")

            print("El proceso se ejecutará cada:", minutos, "minutos")
            hora = (datetime.now().strftime("%H:%M:%S"))
            print("Hora de ejecución: ", hora)
            nueva_hora = datetime.now() + timedelta(minutes=minutos)
            print("Siguiente ejecución " + nueva_hora.strftime("%H:%M:%S"))
            print("seg: ", segundos)

            while True:
                hora = (datetime.now().strftime("%H:%M:%S"))
                sys.stdout.write("\r")  # Regresa a la primer línea
                sys.stdout.write(hora)
                sys.stdout.flush()
                time.sleep(1)
                if hora == nueva_hora.strftime("%H:%M:%S"):
                    break

            for i in range(0, 1, num_caps):
                if cap_web_esc == "Y":
                    time.sleep(1)  # Capturar pantalla sitio web + escritorio
                    driver = webdriver.Chrome(DRIVER)
                    driver.maximize_window()
                    driver.get('http://%s' % op3)
                    time.sleep(cwe)
                    now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
                    pyautogui.screenshot("./screenshots/%s-Scsh_web_desktop.png" % now)
                    driver.quit()

                if cap_web_pos_esc == "Y":
                    time.sleep(1)  # Capturar pantalla sitio web con posicion + escritorio
                    driver = webdriver.Chrome(DRIVER)
                    driver.maximize_window()
                    driver.get('http://%s' % op3)
                    time.sleep(1)
                    alturapag = int(driver.get_window_size()['height'])
                    print("\naltura de la página: ", alturapag)
                    pos_scroll += pos_scroll
                    driver.maximize_window()
                    driver.execute_script('window.scrollTo(0, %s)' % pos_scroll)
                    time.sleep(cwpe)
                    now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
                    pyautogui.screenshot("./screenshots/%s-Scsh_web_pos_desktop.png" % now)
                    driver.quit()

                if cap_web == "Y":
                    time.sleep(1)  # Capturar solo pantalla sitio web
                    driver = webdriver.Chrome(DRIVER)
                    driver.maximize_window()
                    driver.get('http://%s' % op3)
                    time.sleep(cw)
                    now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
                    driver.save_screenshot('./screenshots/%s-Scsh_web.png' % now)
                    driver.quit()


                if cap_web_pos == "Y":
                    time.sleep(1)  # Capturar solo pantalla sitio web con posicion
                    driver = webdriver.Chrome(DRIVER)
                    driver.maximize_window()
                    driver.get('http://%s' % op3)
                    time.sleep(1)
                    alturapag = int(driver.get_window_size()['height'])
                    print("\naltura de la página: ", alturapag)
                    pos_scroll = pos_scroll + alturapag
                    driver.execute_script('window.scrollTo(0, %s)' % pos_scroll)
                    time.sleep(cwp)
                    now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
                    driver.save_screenshot('./screenshots/%s-Scsh_web_pos.png' % now)
                    driver.quit()

                if cap_desktop == "Y":
                    time.sleep(cd)  # Solo capturar pantalla (escritorio)
                    now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
                    pyautogui.screenshot("./screenshots/%s-Scsh_desktop.png" % now)

            print("Proceso de captura número", i + 1, "de", num_caps, " completada")
            print("Se han guardado con éxito, siguiente ciclo...")
            time.sleep(2)
            os.system('cls')
            print("nuevo")
        ok()

except KeyboardInterrupt:
    pass






