def on_button_pressed_a():
    global menu
    menu += 1
    if menu > 3:
        menu = 1
    dibujarMenu()
input.on_button_pressed(Button.A, on_button_pressed_a)

def dibujarMenu():
    OLED.clear()
    if menu == 1:
        OLED.write_string_new_line("Prueba 1")
    elif menu == 2:
        OLED.write_string_new_line("Prueba 2")
    elif menu == 3:
        OLED.write_string_new_line("Prueba 3")
    else:
        OLED.write_string_new_line("Error")
menu = 0
menu = 1
OLED.init(128, 64)
dibujarMenu()
