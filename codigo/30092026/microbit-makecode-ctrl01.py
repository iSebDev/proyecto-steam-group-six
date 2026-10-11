ID = "CTRL01"
CLAVE = "MICRO123"
GROUP_INICIAL = 25

conexion = False
conectado_a = "NONE"
conectando_a = "NONE"
respuesta_buffer = ""

radio.set_group(GROUP_INICIAL)
radio.set_transmit_power(5)


def enviar_mensaje(mensaje: str):
    partes = mensaje.split("|")

    for parte in partes:
        if parte != "":
            radio.send_string(parte + "|")
            basic.pause(100)

    radio.send_string(";;")


def on_button_pressed_a():
    global conectando_a, respuesta_buffer

    if not conexion:
        conectando_a = "BUSCANDO"
        respuesta_buffer = ""

        enviar_mensaje("PING|" + CLAVE + "|" + ID + "|RGB*")
        basic.show_icon(IconNames.CHESSBOARD)

input.on_button_pressed(Button.A, on_button_pressed_a)


def procesar_respuesta(mensaje):
    global conexion, conectado_a, conectando_a

    serial.write_line("MENSAJE COMPLETO: " + mensaje)

    partes = mensaje.split("|")

    if len(partes) >= 4:
        comando = partes[0]
        clave = partes[1]
        origen = partes[2]
        destino = partes[3]

        if comando == "PONG" and clave == CLAVE and destino == ID:
            if origen.substr(0, 3) == "RGB":
                conectado_a = origen
                conectando_a = "NONE"
                conexion = True

                serial.write_line("CONECTADO A: " + conectado_a)
                basic.show_icon(IconNames.YES)


def on_received_string(r):
    global respuesta_buffer

    serial.write_line("RX: " + r)

    if r == ";;":
        mensaje = respuesta_buffer
        respuesta_buffer = ""
        procesar_respuesta(mensaje)
    else:
        respuesta_buffer += r

radio.on_received_string(on_received_string)

basic.show_icon(IconNames.DIAMOND)
