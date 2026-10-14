import microbit
import radio

ID = "RGB01"
CLAVE = "MICRO123"
GRUPO = 25

buffer = ""

radio.config(group=GRUPO, power=5)
radio.on()


# ==========================================
# ENVIO DE MENSAJES
# ==========================================

def enviar(mensaje):
    for parte in mensaje.split("|"):
        if parte:
            radio_send_string(parte + "|", GRUPO)
            microbit.sleep(100)

    radio_send_string(";;", GRUPO)


def radio_send_string(msg, grupo):
    datos = msg.encode("utf-8")

    paquete = (
        b"\x01" + bytes([grupo]) + b"\x01" +
        b"\x02" +
        microbit.running_time().to_bytes(4, "little") +
        b"\x00" * 4 +
        bytes([len(datos)]) +
        datos
    )

    radio.send_bytes(paquete)


# ==========================================
# PROCESAMIENTO DE MENSAJES
# ==========================================

def procesar(mensaje):
    print("MENSAJE:", mensaje)

    partes = mensaje.split("|")

    if len(partes) < 4:
        print("Mensaje incompleto")
        return

    comando, clave, origen, destino = partes[:4]

    if clave != CLAVE:
        print("Clave incorrecta")
        return

    if origen != "CTRL01":
        print("Origen no autorizado")
        return

    # --------------------------------------
    # DESCUBRIMIENTO: HELLO -> BYE
    # --------------------------------------

    if comando == "HELLO" and destino == "RGB*":
        print("HELLO valido")

        enviar(
            "BYE|"
            + CLAVE + "|"
            + ID + "|"
            + str(GRUPO) + "|"
        )

    # --------------------------------------
    # CONEXION: PING -> PONG
    # --------------------------------------

    elif comando == "PING" and destino in ("RGB*", ID):
        print("PING valido")

        enviar(
            "PONG|"
            + CLAVE + "|"
            + ID + "|"
            + origen + "|"
        )


# ==========================================
# BUCLE PRINCIPAL
# ==========================================

while True:
    paquete = radio.receive_bytes()
    if paquete:
        inicio = paquete.find(b"HELLO|")
        if inicio < 0:
            inicio = paquete.find(b"PING|")

        if inicio >= 0:
            buffer = ""

        if inicio >= 0 or buffer:
            texto = (
                paquete[inicio:]
                if inicio >= 0
                else paquete[13:]
            )

            buffer += texto.replace(
                b"\x00", b""
            ).decode("utf-8")
            if ";;" in buffer:
                mensaje, buffer = buffer.split(";;", 1)
                procesar(mensaje)

    microbit.sleep(20)
