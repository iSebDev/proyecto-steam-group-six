from microbit import *
import os
import radio

# =========================================================
# CONFIGURACION INALAMBRICA
# =========================================================

RADIO_GRUPO = 25
CLAVE = "MICRO123"

MI_ID = "RGB01"

AUTORIZADOS = [
    "CTRL01"
]

PROTOCOLO = "RGB1"

ultima_secuencia = ""

# =========================================================
# RADIO
# =========================================================

radio.config(
    group=RADIO_GRUPO,
    length=251,
    queue=10
)

radio.on()

# =========================================================
# CARGAR CONFIGURACION
# =========================================================

if "color.txt" not in os.listdir():
    with open("color.txt", "w") as f:
        f.write("0,0,0")

f = open("color.txt", "r")
color_text = f.read().split(",")
f.close()

colors = [
    int(color_text[0]),
    int(color_text[1]),
    int(color_text[2])
]

# =========================================================
# LED RGB
# =========================================================

leds = [
    pin0,
    pin1,
    pin2
]

led_names = ["R", "G", "B"]

# =========================================================
# VARIABLES LOCALES
# =========================================================

setting_color = False
selected_color = 0

STEP = 20
LOGO_INTERVAL = 150
BLINK_TIME = 1000

touches = 0

# =========================================================
# LED
# =========================================================

def update_leds():
    pin0.write_analog(colors[0])
    pin1.write_analog(colors[1])
    pin2.write_analog(colors[2])

def turn_off_led():
    pin0.write_analog(0)
    pin1.write_analog(0)
    pin2.write_analog(0)

# =========================================================
# PANTALLA
# =========================================================

def show_value():
    value = colors[selected_color]

    pixels = (value * 25 + 511) // 1023

    display.clear()

    for i in range(pixels):
        x = i % 5
        y = i // 5

        display.set_pixel(
            x,
            y,
            9
        )

def show_radio():
    display.clear()
    display.show(Image.YES)
    sleep(500)
    display.clear()

def show_error():
    display.show(Image.NO)
    sleep(500)
    display.clear()

# =========================================================
# GUARDAR
# =========================================================

def save_colors():
    f = open("color.txt", "w")

    f.write(
        str(colors[0]) + "," +
        str(colors[1]) + "," +
        str(colors[2])
    )

    f.close()

# =========================================================
# CAMBIAR COLOR LOCAL
# =========================================================

def change_left():
    global selected_color

    selected_color -= 1

    if selected_color < 0:
        selected_color = 2

    show_value()

def change_right():
    global selected_color

    selected_color += 1

    if selected_color > 2:
        selected_color = 0

    show_value()

# =========================================================
# AUMENTAR COLOR LOCAL
# =========================================================

def increase_color():
    global touches

    value = colors[selected_color]

    if value < 1023:
        value += STEP

        if value > 1023:
            value = 1023

        colors[selected_color] = value

    else:
        touches += 1

        if touches >= 5:
            colors[selected_color] = 0
            touches = 0

    update_leds()
    show_value()

# =========================================================
# LOGO
# =========================================================

def load_logo():
    if not setting_color:
        return

    if pin_logo.is_touched():
        increase_color()

        sleep(LOGO_INTERVAL)

        while pin_logo.is_touched():
            if not setting_color:
                break

            increase_color()
            sleep(LOGO_INTERVAL)

# =========================================================
# RADIO - CONSTRUIR MENSAJE
# =========================================================

def send_message(destino, secuencia, comando):
    mensaje = (
        PROTOCOLO + "|" +
        CLAVE + "|" +
        MI_ID + "|" +
        destino + "|" +
        secuencia + "|" +
        comando
    )

    radio.send(mensaje)

def send_state(destino, secuencia):
    comando = (
        "STATE:" +
        str(colors[0]) + ":" +
        str(colors[1]) + ":" +
        str(colors[2])
    )

    send_message(
        destino,
        secuencia,
        comando
    )

# =========================================================
# AUTORIZACION
# =========================================================

def autorizado(origen):
    for dispositivo in AUTORIZADOS:
        if origen == dispositivo:
            return True

    return False

# =========================================================
# PROCESAR RADIO
# =========================================================

def process_radio():
    global ultima_secuencia

    mensaje = radio.receive()

    if mensaje is None:
        return

    partes = mensaje.split("|")

    if len(partes) != 6:
        return

    protocolo = partes[0]
    clave = partes[1]
    origen = partes[2]
    destino = partes[3]
    secuencia = partes[4]
    comando = partes[5]

    if protocolo != PROTOCOLO:
        return

    if clave != CLAVE:
        return

    if destino != MI_ID and destino != "*":
        return

    if not autorizado(origen):
        return

    if secuencia == ultima_secuencia:
        return

    ultima_secuencia = secuencia

    # -----------------------------------------------------
    # PING
    # -----------------------------------------------------

    if comando == "PING":
        send_message(
            origen,
            secuencia,
            "PONG"
        )

        show_radio()
        return

    # -----------------------------------------------------
    # GETSTATE
    # -----------------------------------------------------

    if comando == "GETSTATE":
        send_state(
            origen,
            secuencia
        )

        return

    # -----------------------------------------------------
    # SAVE
    # -----------------------------------------------------

    if comando == "SAVE":
        save_colors()

        send_message(
            origen,
            secuencia,
            "SAVED"
        )

        show_radio()
        return

    # -----------------------------------------------------
    # CAMBIAR COLOR
    # -----------------------------------------------------

    if comando.startswith("CHANGESETT:COLOR:"):

        datos = comando.split(":")

        if len(datos) != 4:
            send_message(
                origen,
                secuencia,
                "ERROR:FORMAT"
            )
            return

        color = datos[2]

        try:
            valor = int(datos[3])
        except:
            send_message(
                origen,
                secuencia,
                "ERROR:VALUE"
            )
            return

        if valor < 0:
            valor = 0

        if valor > 1023:
            valor = 1023

        if color == "RED":
            colors[0] = valor

        elif color == "GREEN":
            colors[1] = valor

        elif color == "BLUE":
            colors[2] = valor

        else:
            send_message(
                origen,
                secuencia,
                "ERROR:COLOR"
            )
            return

        update_leds()

        send_message(
            origen,
            secuencia,
            "ACK:" + comando
        )

        show_value()
        return

# =========================================================
# BOTONES LOCALES
# =========================================================

def load_menu_buttons():
    global setting_color

    if button_a.is_pressed() and button_b.is_pressed():

        sleep(200)

        if setting_color:
            save_colors()

            setting_color = False

            display.clear()
            turn_off_led()

        else:
            setting_color = True

            update_leds()
            show_value()

        while button_a.is_pressed() or button_b.is_pressed():
            sleep(10)

        return

    if button_a.was_pressed():
        if setting_color:
            change_left()

    if button_b.was_pressed():
        if setting_color:
            change_right()

# =========================================================
# PARPADEO
# =========================================================

def blink():
    update_leds()

    for i in range(100):

        process_radio()

        if setting_color:
            return

        load_menu_buttons()
        sleep(10)

    turn_off_led()

    for i in range(100):

        process_radio()

        if setting_color:
            return

        load_menu_buttons()
        sleep(10)

# =========================================================
# INICIO
# =========================================================

update_leds()
show_value()

# =========================================================
# LOOP
# =========================================================

while True:

    process_radio()

    if setting_color:
        load_menu_buttons()
        load_logo()
        sleep(10)

    else:
        blink()
