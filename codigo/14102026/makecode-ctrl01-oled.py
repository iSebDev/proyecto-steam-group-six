# ==========================================
# CONFIGURACION
# ==========================================

ID = "CTRL01"
CLAVE = "MICRO123"
GROUP_INICIAL = 25
TIEMPO_BUSQUEDA = 10000

conexion = False
conectado_a = "NONE"
conectando_a = "NONE"
respuesta_buffer = ""

interfaz_pendiente = True


# ==========================================
# CLASE: GESTOR DE CONEXION
# ==========================================

class GestorConexion:
    def __init__(self):
        self.conexion = False
        self.conectado_a = "NONE"
        self.buscando = False
        self.respuesta_buffer = ""
        self.inicio_busqueda = 0

    def iniciar_busqueda(self):
        global interfaz_pendiente

        if self.conexion or self.buscando:
            return

        self.buscando = True
        self.respuesta_buffer = ""
        self.inicio_busqueda = input.running_time()

        interfaz_pendiente = True

        self.enviar_mensaje(
            "PING|" + CLAVE + "|" + ID + "|RGB*"
        )

    def enviar_mensaje(self, mensaje: str):
        partes = mensaje.split("|")

        for parte in partes:
            if parte != "":
                radio.send_string(parte + "|")
                basic.pause(100)

        radio.send_string(";;")

    def comprobar_tiempo(self):
        global interfaz_pendiente

        if not self.buscando:
            return

        transcurrido = (
            input.running_time() - self.inicio_busqueda
        )

        if transcurrido >= TIEMPO_BUSQUEDA:
            self.buscando = False
            interfaz_pendiente = True

    def recibir_fragmento(self, fragmento):
        if fragmento == ";;":
            mensaje = self.respuesta_buffer
            self.respuesta_buffer = ""
            self.procesar_respuesta(mensaje)
        else:
            self.respuesta_buffer += fragmento

    def procesar_respuesta(self, mensaje):
        global interfaz_pendiente

        if not self.buscando:
            return

        partes = mensaje.split("|")

        if len(partes) < 4:
            return

        comando = partes[0]
        clave = partes[1]
        origen = partes[2]
        destino = partes[3]

        if (comando == "PONG"
            and clave == CLAVE
            and destino == ID
            and origen.substr(0, 3) == "RGB"):

            self.conexion = True
            self.conectado_a = origen
            self.buscando = False

            interfaz_pendiente = True

            serial.write_line(
                "CONECTADO A: " + self.conectado_a
            )

    def buscar_cercanos(self):
        rango_maximo = 10
        desde = GROUP_INICIAL
        actual = desde
        nombre = "RGB"
        print("========")
        for i in range(rango_maximo):
            actual = desde + i
            n = i + 1
            serial.write_line("ACTUAL: GROUP" + actual)

            nombre = "RGB0" + n if n < 10 else "RGB" + n
            serial.write_line("BUSCANDO: " + nombre)

    def borrar_conexion(self):
        global interfaz_pendiente

        self.conexion = False
        self.conectado_a = "NONE"
        self.buscando = False
        self.respuesta_buffer = ""

        interfaz_pendiente = True


# ==========================================
# CLASE: MENU OLED
# ==========================================

class MenuOLED:
    def __init__(self, gestor: GestorConexion):
        self.gestor = gestor
        self.menu = 1

    def dibujar(self):
        OLED.clear()

        if not self.gestor.conexion:
            if self.gestor.buscando:
                OLED.write_string_new_line("Buscando RGB...")
                OLED.write_string_new_line("Maximo: 10 segundos")
            else:
                OLED.write_string_new_line("CONTROLADOR")
                OLED.write_string_new_line("Sin conexion")
                OLED.write_string_new_line("A: Buscar")
            return

        OLED.write_string_new_line("Conectado:")
        OLED.write_string_new_line(self.gestor.conectado_a)

        if self.menu == 1:
            OLED.write_string_new_line("> Borrar conexion")
            OLED.write_string_new_line("  Buscar cercanos")
        else:
            OLED.write_string_new_line("  Borrar conexion")
            OLED.write_string_new_line("> Buscar cercanos")

        OLED.write_string_new_line("A: Cambiar")
        OLED.write_string_new_line("B: Elegir")

    def boton_a(self):
        global interfaz_pendiente

        if not self.gestor.conexion:
            self.gestor.iniciar_busqueda()
            interfaz_pendiente = True
            return

        self.menu += 1

        if self.menu > 2:
            self.menu = 1

        interfaz_pendiente = True

    def boton_b(self):
        global interfaz_pendiente

        if not self.gestor.conexion:
            return

        if self.menu == 1:
            self.gestor.borrar_conexion()

        elif self.menu == 2:
            OLED.clear()
            OLED.write_string_new_line("Buscar cercanos")
            self.gestor.buscar_cercanos()
            OLED.write_string_new_line("A: Volver")

            # La busqueda de dispositivos cercanos
            # se implementara en una etapa posterior.


# ==========================================
# INICIALIZACION
# ==========================================

radio.set_group(GROUP_INICIAL)
radio.set_transmit_power(5)
OLED.init(128, 64)

gestor = GestorConexion()
interfaz = MenuOLED(gestor)


# ==========================================
# CALLBACKS GLOBALES
# ==========================================

def al_recibir_radio(r):
    gestor.recibir_fragmento(r)


def al_pulsar_a():
    interfaz.boton_a()


def al_pulsar_b():
    interfaz.boton_b()


radio.on_received_string(al_recibir_radio)
input.on_button_pressed(Button.A, al_pulsar_a)
input.on_button_pressed(Button.B, al_pulsar_b)


# ==========================================
# BUCLE PRINCIPAL
# ==========================================

def bucle_principal():
    global interfaz_pendiente

    gestor.comprobar_tiempo()

    if interfaz_pendiente:
        interfaz_pendiente = False
        interfaz.dibujar()

    basic.pause(50)


interfaz.dibujar()
basic.forever(bucle_principal)
