## ACTUALIZACIÓN [12102026] - El problema que tuvimos con la radio entre Makecode y Micropython

El problema principal era el limite de bytes que había al enviar un mensaje por radio.
Y es verdad que Makecode requiere unos encabezados que tienen que ser enviados desde Micropython para poder recibir el mensaje correctamente

> [!IMPORTANT]
> Supuse que sería un problema de un limite de bytes, pero en la [documentación de micro:bit radio](https://microbit-micropython.readthedocs.io/en/latest/radio.html#examples) nos figura que hay un limite de mas de 200 bytes para una comunicación estable.

Pero no entendemos el porque el controlador ([ctrl01](https://github.com/iSebDev/proyecto-steam-group-six/blob/main/codigo/30092026/microbit-makecode-ctrl01.py)) al enviar un mensaje a nuestro dispositivo RGB ([rgb01](https://github.com/iSebDev/proyecto-steam-group-six/blob/main/codigo/30092026/microbit-micropython-rgb01.py)) este al devolvernos el mensaje parecia como si se quedara en el aire, no puedo comprender eso hasta ahora.

