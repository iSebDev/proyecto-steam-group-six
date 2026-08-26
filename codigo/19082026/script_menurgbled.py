import microbit
from microbit import pin0, pin1, pin2
from microbit import button_a, button_b, pin_logo
from microbit import sleep

import os

# Cargar configuracion

if "color.txt" not in os.listdir():
    with open("color.txt", 'w') as f:
        f.write("0,0,0")

f = open("color.txt", 'r')

color_text = f.read().split(',')

f.close()

colors = [
    int(color_text[0]),
    int(color_text[1]),
    int(color_text[2])
]

# ==========================================
# LED RGB
# ==========================================

# P0 = Rojo
# P1 = Verde
# P2 = Azul

leds = [
    pin0,
    pin1,
    pin2
]

led_names = ["R", "G", "B"]


# ==========================================
# VARIABLES
# ==========================================

setting_color = False

# 0 = R
# 1 = G
# 2 = B
selected_color = 0

# Valores RGB
# 0 - 1023

colors = [
    int(color_text[0]) or 0,      # R
    int(color_text[1]) or 0,      # G
    int(color_text[2]) or 0       # B
]

# Cuánto aumenta cada vez
STEP = 20

# Velocidad al mantener tocado el logo
LOGO_INTERVAL = 150

# Parpadeo
BLINK_TIME = 1000


# ==========================================
# LED RGB
# ==========================================

def update_leds():

    pin0.write_analog(colors[0])
    pin1.write_analog(colors[1])
    pin2.write_analog(colors[2])


def turn_off_led():

    pin0.write_analog(0)
    pin1.write_analog(0)
    pin2.write_analog(0)


# ==========================================
# BARRA DE 25 PIXELES
# ==========================================

def show_value():

    # Valor actual del color seleccionado
    value = colors[selected_color]

    # Convertir 0-1023 a 0-25
    pixels = (value * 25 + 511) // 1023

    # Limpiar matriz
    microbit.display.clear()

    # Dibujar barra
    for i in range(pixels):

        x = i % 5
        y = i // 5

        microbit.display.set_pixel(
            x,
            y,
            9
        )


# ==========================================
# CAMBIAR COLOR
# ==========================================

def change_left():

    global selected_color

    selected_color -= 1

    # Si estamos en R y vamos a la izquierda:
    # R -> B
    if selected_color < 0:
        selected_color = 2

    show_value()


def change_right():

    global selected_color

    selected_color += 1

    # Si estamos en B y vamos a la derecha:
    # B -> R
    if selected_color > 2:
        selected_color = 0

    show_value()


# ==========================================
# AUMENTAR VALOR
# ==========================================

touches = 0

def increase_color():

    global touches

    value = colors[selected_color]

    # --------------------------------------
    # Si todavía no llegó al máximo
    # --------------------------------------

    if value < 1023:

        value += STEP

        # No permitir pasar de 1023
        if value > 1023:
            value = 1023

        colors[selected_color] = value

    # --------------------------------------
    # Si ya estaba en 1023
    # --------------------------------------

    else:
        touches += 1
        if touches >= 5:
            # Volver a 0
            colors[selected_color] = 0
            touches = 0

    # Cambiar LED inmediatamente
    update_leds()

    # Actualizar barra inmediatamente
    show_value()


# ==========================================
# LOGO
# ==========================================

def load_logo():

    if not setting_color:
        return

    # --------------------------------------
    # Primer toque
    # --------------------------------------

    if pin_logo.is_touched():
        
        increase_color()

        sleep(LOGO_INTERVAL)

        # ----------------------------------
        # Mantener tocado
        # ----------------------------------

        while pin_logo.is_touched():

            # Si salió del modo configuración
            # dejamos de aumentar
            if not setting_color:
                break

            increase_color()

            sleep(LOGO_INTERVAL)


# ==========================================
# GUARDAR / ENTRAR
# ==========================================

def load_menu_buttons():

    global setting_color

    # ======================================
    # A + B
    # ======================================

    if button_a.is_pressed() and button_b.is_pressed():
    
        sleep(200)
    
        if setting_color:
    
            # Guardar configuración
            f = open("color.txt", 'w')
            f.write(",".join(map(str, colors)))
            f.close()
    
            setting_color = False
    
            microbit.display.clear()
            turn_off_led()
    
        else:
    
            setting_color = True
    
            update_leds()
            show_value()
    
        while button_a.is_pressed() or button_b.is_pressed():
            sleep(10)

        return



    # ======================================
    # A = izquierda
    # ======================================

    if button_a.was_pressed():

        if setting_color:

            change_left()


    # ======================================
    # B = derecha
    # ======================================

    if button_b.was_pressed():

        if setting_color:

            change_right()


# ==========================================
# PARPADEO
# ==========================================

def blink():

    # --------------------------------------
    # Encender
    # --------------------------------------

    update_leds()

    # Esperar 1 segundo,
    # pero seguir comprobando A+B
    for i in range(100):

        if setting_color:
            return

        load_menu_buttons()

        sleep(10)


    # --------------------------------------
    # Apagar
    # --------------------------------------

    turn_off_led()

    # Esperar 1 segundo
    for i in range(100):

        if setting_color:
            return

        load_menu_buttons()

        sleep(10)


# ==========================================
# INICIO
# ==========================================

update_leds()
show_value()


# ==========================================
# LOOP PRINCIPAL
# ==========================================

while True:

    # --------------------------------------
    # MODO CONFIGURACIÓN
    # --------------------------------------

    if setting_color:

        load_menu_buttons()

        load_logo()

        sleep(10)

    # --------------------------------------
    # MODO NORMAL
    # --------------------------------------

    else:

        blink()
