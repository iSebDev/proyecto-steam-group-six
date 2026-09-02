def on_button_pressed_a():
    global menu
    if submenu == 0:
        menu += 1
        if menu > 3:
            menu = 1
        dibujarMenu()
    else:
        if submenu == 1 and menu == 1:
            OLED.write_num_new_line(Environment.read_noise(AnalogPin.P1))
        elif submenu == 1 and menu == 2:
            OLED.write_num_new_line(Environment.read_noise(AnalogPin.P1))
        elif submenu == 1 and menu == 3:
            OLED.write_num_new_line(Environment.read_noise(AnalogPin.P1))
        else:
            OLED.write_string_new_line("Error.")
input.on_button_pressed(Button.A, on_button_pressed_a)

def dibujarMenu():
    OLED.clear()
    if submenu == 0:
        if menu == 1:
            OLED.write_string_new_line("Opcion 1")
            OLED.write_string_new_line("A = cambiar opcion")
            OLED.write_string_new_line("B = seleccionar")
        elif menu == 2:
            OLED.write_string_new_line("Opcion 2")
            OLED.write_string_new_line("A = cambiar opcion")
            OLED.write_string_new_line("B = seleccionar")
        elif menu == 3:
            OLED.write_string_new_line("Opcion 3")
            OLED.write_string_new_line("A = cambiar opcion")
            OLED.write_string_new_line("B = seleccionar")
        else:
            OLED.write_string_new_line("Error")

def on_button_pressed_b():
    global submenu
    if submenu == 0:
        submenu = 1
        if menu == 1:
            OLED.clear()
            OLED.write_string_new_line("Test submenu 1")
            OLED.write_string_new_line("A = Ruido (db)")
            OLED.write_string_new_line("B = Atras")
        elif menu == 2:
            OLED.clear()
            OLED.write_string_new_line("Test submenu 2")
            OLED.write_string_new_line("A = Ruido (db)")
        elif menu == 3:
            OLED.clear()
            OLED.write_string_new_line("Test submenu 3")
            OLED.write_string_new_line("A = Ruido (db)")
            OLED.write_string_new_line("B = Atras")
    else:
        submenu = 0
        OLED.clear()
        dibujarMenu()
input.on_button_pressed(Button.B, on_button_pressed_b)

submenu = 0
menu = 0
menu = 1
submenu = 0
OLED.init(128, 64)
dibujarMenu()
