# =========================================================
# VARIABLES
# =========================================================

menu = 1
submenu = 0

secuencia = 0

conectado = False

color = 1

# =========================================================
# CONFIGURACION
# =========================================================

radio.set_group(25)
radio.set_transmit_power(7)

OLED.init(128, 64)


# =========================================================
# RADIO
# =========================================================

def enviar(comando):
    global secuencia

    secuencia += 1

    mensaje = (
        "RGB1|MICRO123|CTRL01|RGB01|" +
        str(secuencia) +
        "|" +
        comando
    )

    radio.send_string(mensaje)


def on_received_string(mensaje):

    global conectado

    partes = mensaje.split("|")

    if len(partes) != 6:
        return

    if partes[0] != "RGB1":
        return

    if partes[1] != "MICRO123":
        return

    if partes[2] != "RGB01":
        return

    if partes[3] != "CTRL01":
        return

    comando = partes[5]

    # -----------------------------------------------------
    # PONG
    # -----------------------------------------------------

    if comando == "PONG":

        conectado = True

        OLED.clear()
        OLED.write_string_new_line("CONECTADO")
        basic.pause(1000)

        dibujar_menu()

    # -----------------------------------------------------
    # STATE
    # -----------------------------------------------------

    elif comando.startswith("STATE:"):

        conectado = True

        OLED.clear()
        OLED.write_string_new_line("ESTADO RGB")

        datos = comando.split(":")

        if len(datos) == 4:

            OLED.write_string_new_line("R: " + datos[1])
            OLED.write_string_new_line("G: " + datos[2])
            OLED.write_string_new_line("B: " + datos[3])

        basic.pause(1500)

        dibujar_menu()

    # -----------------------------------------------------
    # SAVED
    # -----------------------------------------------------

    elif comando == "SAVED":

        conectado = True

        OLED.clear()
        OLED.write_string_new_line("GUARDADO")

        basic.pause(1000)

        dibujar_menu()

    # -----------------------------------------------------
    # ACK
    # -----------------------------------------------------

    elif comando.startswith("ACK:"):

        conectado = True

        OLED.clear()
        OLED.write_string_new_line("CAMBIO OK")

        basic.pause(1000)

        dibujar_menu()

    # -----------------------------------------------------
    # ERROR
    # -----------------------------------------------------

    elif comando.startswith("ERROR:"):

        OLED.clear()
        OLED.write_string_new_line("ERROR")
        OLED.write_string_new_line(comando)

        basic.pause(1500)

        dibujar_menu()


radio.on_received_string(on_received_string)


# =========================================================
# MENU PRINCIPAL
# =========================================================

def dibujar_menu():

    OLED.clear()

    if menu == 1:

        OLED.write_string_new_line("CONEXION")
        OLED.write_string_new_line("A = probar")
        OLED.write_string_new_line("B = siguiente")

    elif menu == 2:

        OLED.write_string_new_line("CAMBIAR")
        OLED.write_string_new_line("A = entrar")
        OLED.write_string_new_line("B = siguiente")

    elif menu == 3:

        OLED.write_string_new_line("GUARDAR")
        OLED.write_string_new_line("A = guardar")
        OLED.write_string_new_line("B = volver")


# =========================================================
# BOTON A
# =========================================================

def on_button_pressed_a():

    global menu
    global submenu
    global color

    # =====================================================
    # MENU PRINCIPAL
    # =====================================================

    if submenu == 0:

        # -------------------------------------------------
        # CONEXION
        # -------------------------------------------------

        if menu == 1:

            OLED.clear()
            OLED.write_string_new_line("CONECTANDO...")

            enviar("PING")

        # -------------------------------------------------
        # CAMBIAR
        # -------------------------------------------------

        elif menu == 2:

            if not conectado:

                OLED.clear()
                OLED.write_string_new_line("SIN CONEXION")
                OLED.write_string_new_line("Conecte primero")

                basic.pause(1500)

                dibujar_menu()

            else:

                submenu = 1
                color = 1

                dibujar_cambio()

        # -------------------------------------------------
        # GUARDAR
        # -------------------------------------------------

        elif menu == 3:

            if not conectado:

                OLED.clear()
                OLED.write_string_new_line("SIN CONEXION")
                OLED.write_string_new_line("Conecte primero")

                basic.pause(1500)

                dibujar_menu()

            else:

                OLED.clear()
                OLED.write_string_new_line("GUARDANDO...")

                enviar("SAVE")


    # =====================================================
    # SUBMENU CAMBIAR
    # =====================================================

    elif submenu == 1:

        if color == 1:

            enviar("CHANGESETT:COLOR:RED:500")

        elif color == 2:

            enviar("CHANGESETT:COLOR:GREEN:500")

        elif color == 3:

            enviar("CHANGESETT:COLOR:BLUE:500")


input.on_button_pressed(Button.A, on_button_pressed_a)


# =========================================================
# BOTON B
# =========================================================

def on_button_pressed_b():

    global menu
    global submenu
    global color

    # =====================================================
    # MENU PRINCIPAL
    # =====================================================

    if submenu == 0:

        menu += 1

        if menu > 3:
            menu = 1

        dibujar_menu()

    # =====================================================
    # SUBMENU CAMBIAR
    # =====================================================

    elif submenu == 1:

        color += 1

        if color > 3:
            color = 1

        dibujar_cambio()


input.on_button_pressed(Button.B, on_button_pressed_b)


# =========================================================
# MENU CAMBIAR
# =========================================================

def dibujar_cambio():

    OLED.clear()

    if color == 1:

        OLED.write_string_new_line("CAMBIAR ROJO")
        OLED.write_string_new_line("A = aplicar")
        OLED.write_string_new_line("B = siguiente")

    elif color == 2:

        OLED.write_string_new_line("CAMBIAR VERDE")
        OLED.write_string_new_line("A = aplicar")
        OLED.write_string_new_line("B = siguiente")

    elif color == 3:

        OLED.write_string_new_line("CAMBIAR AZUL")
        OLED.write_string_new_line("A = aplicar")
        OLED.write_string_new_line("B = siguiente")


# =========================================================
# INICIO
# =========================================================

OLED.clear()
OLED.write_string_new_line("CONTROL RGB")

basic.pause(1000)

dibujar_menu()


# =========================================================
# LOOP
# =========================================================

while True:

    basic.pause(100)
