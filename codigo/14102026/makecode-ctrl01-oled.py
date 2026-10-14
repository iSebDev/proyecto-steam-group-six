# ==========================================
# CONFIGURACION
# ==========================================

ID = "CTRL01"
CLAVE = "MICRO123"

GROUP_INICIAL = 25
CANTIDAD_GRUPOS = 10
TIEMPO_POR_GRUPO = 500

# Estados:
# ESCANEANDO
# LISTA
# CONECTANDO
# CONECTADO

modo = "ESCANEANDO"

grupo_escucha = GROUP_INICIAL

dispositivos_nombres = [""]
dispositivos_grupos = [0]
dispositivos_nombres.pop()
dispositivos_grupos.pop()

seleccion = 0
conexion = False
conectado_a = "NONE"


# ==========================================
# FUNCIONES AUXILIARES
# ==========================================

def nombre_esperado(grupo):
    numero = grupo - GROUP_INICIAL + 1

    if numero < 10:
        return "RGB0" + str(numero)

    return "RGB" + str(numero)


# ==========================================
# INTERFAZ OLED
# ==========================================

def dibujar_lista():
    global dispositivos_nombres

    OLED.clear()

    if modo == "ESCANEANDO":
        OLED.write_string_new_line("Buscando RGB...")
        OLED.write_string_new_line(
            "Grupo: " + str(grupo_escucha)
        )
        OLED.write_string_new_line("Espere...")
        return

    if modo == "CONECTANDO":
        OLED.write_string_new_line("Conectando...")
        OLED.write_string_new_line(conectado_a)
        OLED.write_string_new_line("Esperando PONG")
        return

    if modo == "CONECTADO":
        OLED.write_string_new_line("CONECTADO")
        OLED.write_string_new_line(conectado_a)
        OLED.write_string_new_line(
            "Grupo: " + str(grupo_escucha)
        )
        OLED.write_string_new_line("A: Buscar otra vez")
        return

    if len(dispositivos_nombres) == 0:
        OLED.write_string_new_line("Sin dispositivos")
        OLED.write_string_new_line("RGB disponibles: 0")
        OLED.write_string_new_line("A: Reintentar")
        return

    OLED.write_string_new_line(
        "RGB encontrados: " + str(len(dispositivos_nombres))
    )

    # Ventana de cinco elementos.
    inicio = seleccion - 2

    if inicio < 0:
        inicio = 0

    max_inicio = len(dispositivos_nombres) - 5

    if max_inicio < 0:
        max_inicio = 0

    if inicio > max_inicio:
        inicio = max_inicio

    fin = inicio + 5

    if fin > len(dispositivos_nombres):
        fin = len(dispositivos_nombres)

    for i in range(inicio, fin):
        marca = ">" if i == seleccion else " "

        OLED.write_string_new_line(
            marca
            + dispositivos_nombres[i]
            + " G"
            + str(dispositivos_grupos[i])
        )

    OLED.write_string_new_line("A:Arr B:Abj AB:OK")


# ==========================================
# GESTOR DE CONEXION
# ==========================================

def buscar_cercanos():
    global modo
    global grupo_escucha
    global dispositivos_nombres
    global dispositivos_grupos
    global seleccion
    global conexion
    global conectado_a

    conexion = False
    conectado_a = "NONE"

    dispositivos_nombres = []
    dispositivos_grupos = []

    seleccion = 0
    modo = "ESCANEANDO"

    dibujar_lista()

    # Escanear grupos 25 a 34.
    for grupo in range(
        GROUP_INICIAL,
        GROUP_INICIAL + CANTIDAD_GRUPOS
    ):
        grupo_escucha = grupo

        radio.set_group(grupo)

        # HELLO | clave | controlador | destino
        radio.send_string(
            "HELLO|" + CLAVE + "|" + ID + "|RGB*"
        )

        # Dar tiempo al dispositivo para responder BYE.
        basic.pause(TIEMPO_POR_GRUPO)

    modo = "LISTA"
    seleccion = 0

    dibujar_lista()


def conectar_seleccionado():
    global modo
    global grupo_escucha
    global conexion
    global conectado_a

    if len(dispositivos_nombres) == 0:
        return

    conectado_a = dispositivos_nombres[seleccion]
    grupo_escucha = dispositivos_grupos[seleccion]

    conexion = False
    modo = "CONECTANDO"

    dibujar_lista()

    # Volver al grupo del dispositivo elegido.
    radio.set_group(grupo_escucha)

    # Intentar la conexion real.
    radio.send_string(
        "PING|"
        + CLAVE
        + "|"
        + ID
        + "|"
        + conectado_a
    )

    # Esperar respuesta PONG.
    basic.pause(800)

    if conexion:
        modo = "CONECTADO"
        dibujar_lista()
    else:
        modo = "LISTA"

        OLED.clear()
        OLED.write_string_new_line("Sin respuesta PONG")
        OLED.write_string_new_line(conectado_a)

        basic.pause(1000)

        dibujar_lista()


# ==========================================
# RECEPCION DE RADIO
# ==========================================

def al_recibir_radio(mensaje):
    global conexion
    global conectado_a
    global dispositivos_nombres
    global dispositivos_grupos

    partes = mensaje.split("|")

    if len(partes) < 4:
        return

    comando = partes[0]
    clave = partes[1]
    origen = partes[2]
    destino = partes[3]

    # --------------------------------------
    # RESPUESTA AL DESCUBRIMIENTO
    # BYE | CLAVE | RGBxx | GRUPO
    # --------------------------------------

    if comando == "BYE":
        if modo != "ESCANEANDO":
            return

        if clave != CLAVE:
            return

        if destino != str(grupo_escucha):
            return

        if origen != nombre_esperado(grupo_escucha):
            return

        if origen not in dispositivos_nombres:
            dispositivos_nombres.append(origen)
            dispositivos_grupos.append(grupo_escucha)

        return

    # --------------------------------------
    # RESPUESTA A LA CONEXION
    # PONG | CLAVE | RGBxx | CTRL01
    # --------------------------------------

    if comando == "PONG":
        if modo != "CONECTANDO":
            return

        if clave != CLAVE:
            return

        if origen != conectado_a:
            return

        if destino != ID:
            return

        conexion = True


# ==========================================
# BOTONES
# ==========================================

def al_pulsar_a():
    global seleccion

    if modo == "CONECTADO":
        buscar_cercanos()
        return

    if modo != "LISTA":
        return

    if len(dispositivos_nombres) == 0:
        buscar_cercanos()
        return

    seleccion -= 1

    if seleccion < 0:
        seleccion = len(dispositivos_nombres) - 1

    dibujar_lista()


def al_pulsar_b():
    global seleccion

    if modo != "LISTA":
        return

    if len(dispositivos_nombres) == 0:
        return

    seleccion += 1

    if seleccion >= len(dispositivos_nombres):
        seleccion = 0

    dibujar_lista()


def al_pulsar_ab():
    if modo == "LISTA":
        conectar_seleccionado()


# ==========================================
# INICIALIZACION
# ==========================================

OLED.init(128, 64)

radio.set_group(GROUP_INICIAL)
radio.set_transmit_power(5)

radio.on_received_string(al_recibir_radio)

input.on_button_pressed(Button.A, al_pulsar_a)
input.on_button_pressed(Button.B, al_pulsar_b)
input.on_button_pressed(Button.AB, al_pulsar_ab)


# ==========================================
# INICIO AUTOMATICO DEL DESCUBRIMIENTO
# ==========================================

buscar_cercanos()


# ==========================================
# BUCLE PRINCIPAL
# ==========================================

def bucle_principal():
    basic.pause(50)


basic.forever(bucle_principal)
