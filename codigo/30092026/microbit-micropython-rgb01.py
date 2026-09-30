# Parametros 
ID = "RGB01"
CLAVE = "MICRO123"
GROUP_RGB = 25

"""
Tiene que poder acceder a cualquier dispositivo
con id que sea = RGB[Numero]
"""

# Importamos el sistema de radio
import radio
import microbit

conexion = False
controlador = "NONE"

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

while True:
    msg = radio.receive_bytes()
    if msg and not conexion:
        print(msg, len(msg))
        try:
            radio_send_string("PONG|MICRO123|RGB01|CTRL01", GROUP_RGB)
        except Exception as e:
            print("ERR", e)
    microbit.sleep(50)
