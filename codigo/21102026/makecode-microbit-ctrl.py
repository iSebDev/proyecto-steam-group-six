# ==========================================
# CONFIGURACION
# ==========================================

ID = "CTRL01"
CLAVE = "MICRO123"

GROUP_INICIAL = 25
CANTIDAD_GRUPOS = 10
TIEMPO_POR_GRUPO = 500
TIEMPO_CONEXION = 1500

modo = "ESCANEANDO"
grupo_escucha = GROUP_INICIAL

dispositivos_nombres = [""]
dispositivos_nombres.pop()

dispositivos_grupos = [0]
dispositivos_grupos.pop()

seleccion = 0
conexion = False
conectado_a = "NONE"

configurando = False

respuesta_buffer = ""
inicio_conexion = 0


# ==========================================
# FUNCIONES AUXILIARES
# ==========================================

def nombre_esperado(grupo):
    numero = grupo - GROUP_INICIAL + 1

    if numero < 10:
        return "RGB0" + str(numero)

    return "RGB" + str(numero)


def enviar_mensaje(mensaje: str):
    partes = mensaje.split("|")

    for parte in partes:
        if parte != "":
            radio.send_string(parte + "|")
            basic.pause(100)

    radio.send_string(";;")


# ==========================================
# INTERFAZ OLED
# ==========================================

def dibujar_lista():
    OLED.clear()

    if modo == "ESCANEANDO":
        OLED.write_string_new_line("Buscando RGB...")
        OLED.write_string_new_line(
            "Grupo: " + str(grupo_escucha)
        )
        OLED.write_string_new_line("Espere...")
        return

    elif modo == "CONECTANDO":
        OLED.write_string_new_line("Conectando...")
        OLED.write_string_new_line(conectado_a)
        OLED.write_string_new_line("Esperando PONG")
        return

    elif modo == "CONECTADO":
        OLED.write_string_new_line("CONECTADO")
        OLED.write_string_new_line(conectado_a)
        OLED.write_string_new_line(
            "Grupo: " + str(grupo_escucha)
        )
        OLED.write_string_new_line("A: Buscar otra vez")
        OLED.write_string_new_line("B: Ir a configurar")
        return

    if len(dispositivos_nombres) == 0:
        OLED.write_string_new_line("Sin dispositivos")
        OLED.write_string_new_line("RGB disponibles: 0")
        OLED.write_string_new_line("A: Reintentar")
        return

    OLED.write_string_new_line(
        "RGB encontrados: " + str(len(dispositivos_nombres))
    )

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
# BUSQUEDA DE DISPOSITIVOS
# ==========================================

def buscar_cercanos():
    global modo
    global grupo_escucha
    global dispositivos_nombres
    global dispositivos_grupos
    global seleccion
    global conexion
    global conectado_a
    global respuesta_buffer

    conexion = False
    conectado_a = "NONE"

    dispositivos_nombres = [""]
    dispositivos_nombres.pop()

    dispositivos_grupos = [0]
    dispositivos_grupos.pop()

    seleccion = 0
    modo = "ESCANEANDO"

    dibujar_lista()

    for grupo in range(
        GROUP_INICIAL,
        GROUP_INICIAL + CANTIDAD_GRUPOS
    ):
        grupo_escucha = grupo
        respuesta_buffer = ""

        radio.set_group(grupo)

        # Esperar a que el grupo este configurado.
        basic.pause(50)

        # Descubrimiento, no conexion.
        enviar_mensaje(
            "HELLO|" + CLAVE + "|" + ID + "|RGB*"
        )

        # Ventana para recibir el BYE.
        basic.pause(TIEMPO_POR_GRUPO)

    modo = "LISTA"
    seleccion = 0

    dibujar_lista()


# ==========================================
# CONEXION CON EL DISPOSITIVO SELECCIONADO
# ==========================================

def conectar_seleccionado():
    global modo
    global grupo_escucha
    global conexion
    global conectado_a

    global inicio_conexion
    global respuesta_buffer

    if len(dispositivos_nombres) == 0:
        return

    conectado_a = dispositivos_nombres[seleccion]
    grupo_escucha = dispositivos_grupos[seleccion]

    conexion = False
    respuesta_buffer = ""

    modo = "CONECTANDO"
    dibujar_lista()

    radio.set_group(grupo_escucha)
    basic.pause(50)

    inicio_conexion = input.running_time()

    enviar_mensaje(
        "PING|"
        + CLAVE
        + "|"
        + ID
        + "|"
        + conectado_a
    )

    # El resultado se comprueba en el bucle principal.
    # No bloquear aqui esperando el PONG.


# ==========================================
# PROCESAMIENTO DE MENSAJES COMPLETOS
# ==========================================

def procesar_mensaje(mensaje):
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

    if clave != CLAVE:
        return

    # --------------------------------------
    # DESCUBRIMIENTO: BYE
    # BYE|MICRO123|RGB01|25
    # --------------------------------------

    if comando == "BYE":
        if modo != "ESCANEANDO":
            return

        if destino != str(grupo_escucha):
            return

        if origen != nombre_esperado(grupo_escucha):
            return

        if origen not in dispositivos_nombres:
            dispositivos_nombres.append(origen)
            dispositivos_grupos.append(grupo_escucha)

        return

    # OPTIMIZACION CABECERAS PARA LOS SIGUIENTES COMANDOS
    if origen != conectado_a:
        return

    if destino != ID:
        return

    # --------------------------------------
    # CONEXION: PONG
    # PONG|MICRO123|RGB01|CTRL01
    # --------------------------------------

    if comando == "PONG":
        if modo != "CONECTANDO":
            return

        conexion = True
    
    # --------------------------------------
    # CONFIGURACION: CONFIG
    # CONFIG|MICRO123|RGB01|CTRL01
    # --------------------------------------

    if comando == "CONFIG":
        if modo != "CONFIG":
            return
        
        configurando = True

# ==========================================
# RECEPCION DE RADIO
# ==========================================

def al_recibir_radio(mensaje):
    global respuesta_buffer

    # El emisor envia los campos por separado,
    # terminando cada mensaje con ;;.
    if mensaje == ";;":
        completo = respuesta_buffer
        respuesta_buffer = ""

        if completo != "":
            procesar_mensaje(completo)

    else:
        respuesta_buffer += mensaje

# ==========================================
# CONFIGURACION
# ==========================================

def menu_configuracion():
    global modo
    modo = "CONFIG"

    OLED.clear()

    enviar_mensaje(
        "CONFIG|"
        + CLAVE
        + "|"
        + ID
        + "|"
        + conectado_a
    )

    if not configurando:
        OLED.write_string_new_line("Abriendo menu...")
        return
        
    OLED.write_string_new_line("Menu de Configuracion")


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

    if modo == "CONECTADO":
        menu_configuracion()

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
# INICIO
# ==========================================

def bucle_principal():
    global modo
    global conexion
    
    if modo == "CONECTANDO":
        if conexion:
            modo = "CONECTADO"
            
            dibujar_lista()

        elif (input.running_time() - inicio_conexion >= TIEMPO_CONEXION):
            modo = "LISTA"
            
            dibujar_lista()
    elif modo == "CONFIG":
            menu_configuracion()

    basic.pause(50)


dibujar_lista()
basic.forever(bucle_principal)

# Iniciar busqueda despues de registrar callbacks.
buscar_cercanos()
