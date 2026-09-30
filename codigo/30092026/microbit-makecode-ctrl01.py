"""

Formato Comandos:

COMANDO|CLAVE|ORIGEN|DESTINO|DATOS

"""
"""

Boton A:

Para conectarnos al

microdispositivo en el grupo actual

"""
# Respuesta esperada:
# PONG|MICRO123|RGB01|CTRL01

def on_button_pressed_a():
    if not (conexion):
        radio.send_string("PING|MICRO123|CTRL01|RGB01")
input.on_button_pressed(Button.A, on_button_pressed_a)

def on_received_string(r):
    basic.show_string(r)
    serial.write_line("Respuesta " + r)
radio.on_received_string(on_received_string)

"""

Variables on Running

"""
"""

Tiene que poder acceder a cualquier dispositivo

con id que sea = RGB[Numero]

"""
conexion = 0
# Parametros
ID = "CTRL01"
CLAVE = "MICRO123"
GROUP_INICIAL = 25
# Importamos el sistema de radio
radio.set_group(GROUP_INICIAL)
radio.set_transmit_power(5)
radio.on()
conectado_a = "NONE"
