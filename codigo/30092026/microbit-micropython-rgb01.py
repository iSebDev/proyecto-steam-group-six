import microbit
import radio

ID = "RGB01"
CLAVE = "MICRO123"
GROUP_RGB = 25

buffer = ""

radio.config(group=GROUP_RGB, power=5)
radio.on()

def radio_send_string(msg, group_id):
    dal_header = b'\x01' + group_id.to_bytes(1,'little') + b'\x01'
    packet_type = int('2').to_bytes(1,'little')
    time_stamp = microbit.running_time().to_bytes(4,'little')
    serial_num = int('0').to_bytes(4,'little')
    msg_bytes = bytes(str(msg), 'utf8')
    msg_length = len(msg_bytes).to_bytes(1,'little')
    raw_bytes = (dal_header +
                 packet_type +
                 time_stamp +
                 serial_num +
                 msg_length +
                 msg_bytes)
    radio.send_bytes(raw_bytes)

def enviar_mensaje(mensaje):
    partes = mensaje.split("|")

    for parte in partes:
        paquete = parte + "|"
        radio_send_string(paquete, GROUP_RGB)
        microbit.sleep(100)

    radio_send_string(";;", GROUP_RGB)
    print("TX: ;;")


def procesar_mensaje(mensaje):
    print("MENSAJE COMPLETO:", mensaje)

    if not mensaje.endswith("|"):
        print("Falta el separador final")
        return

    partes = mensaje.split("|")

    if len(partes) < 5:
        print("Mensaje incompleto")
        return

    comando = partes[0]
    clave = partes[1]
    origen = partes[2]
    destino = partes[3]

    if comando == "PING" and clave == CLAVE:
        if destino == "RGB*" or destino == ID:
            print("PING valido")

            respuesta = "PONG|" + CLAVE + "|" + ID + "|" + origen + "|"
            enviar_mensaje(respuesta)


while True:
    paquete = radio.receive_bytes()

    if paquete:
        # Extraer texto a partir de PING o de un campo posterior.
        inicio = paquete.find(b"PING|")

        if inicio >= 0:
            buffer = ""

        if inicio < 0 and not buffer:
            microbit.sleep(20)
            continue

        if inicio >= 0:
            texto = paquete[inicio:]
        else:
            texto = paquete[13:]

        texto = texto.replace(b"\x00", b"")

        try:
            texto = texto.decode("utf-8")
            buffer += texto

            if ";;" in buffer:
                mensaje, resto = buffer.split(";;", 1)
                buffer = resto
                procesar_mensaje(mensaje)

        except:
            print("Error al leer paquete")

    microbit.sleep(20)
