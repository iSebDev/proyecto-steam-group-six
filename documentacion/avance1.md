# Informe de Avance 1: Agosto 2026

## 12/8/2026
Durante esta primera semana se realizó la definición y planificación inicial del proyecto, cuyo objetivo es desarrollar una alarma visual para personas sordas utilizando una micro:bit. El dispositivo busca detectar una situación que normalmente se identifica mediante un sonido y comunicarla mediante estímulos visuales, facilitando así la identificación de la alarma por parte del usuario.

En esta etapa, el equipo estuvo enfocado principalmente en analizar la viabilidad de la propuesta, investigar sus posibles casos de uso y determinar los recursos necesarios para llevarla a cabo. También se comenzó con la familiarización con los materiales y herramientas que serán utilizados durante el desarrollo, incluyendo la micro:bit y el repositorio del proyecto en GitHub.

### Tareas completadas
*  Se debatieron y analizaron diferentes propuestas de proyecto hasta seleccionar la idea de desarrollar una alarma visual para personas sordas.
*  Se realizó una investigación inicial sobre el proyecto seleccionado, considerando:
  *  Posibles casos de uso.
  *  Necesidad y utilidad de la solución.
  *  Viabilidad técnica del proyecto.
  *  Funcionamiento general esperado.
  *  Materiales y componentes necesarios.
*  Se investigaron los recursos necesarios para implementar el prototipo.
*  Se comenzó la familiarización con la micro:bit y los componentes que podrían utilizarse durante el desarrollo.
*  Se creó/realizó un fork del repositorio del proyecto en GitHub, con el objetivo de disponer de un espacio propio para trabajar y llevar un
  control de los cambios realizados.
*  Los integrantes del equipo comenzaron a distribuir y analizar las posibles tareas necesarias para las siguientes etapas.


### Problemas encontrados y soluciones/alternativas propuestas

Durante esta primera etapa no se presentaron problemas técnicos importantes, debido a que todavía no se comenzó con la implementación física o programación del prototipo. Sin embargo, uno de los principales desafíos identificados fue determinar cómo detectar de manera confiable el evento que debe activar la alarma visual. Como alternativa inicial, se consideró utilizar un sensor de sonido/micrófono conectado a la micro:bit, de manera que el dispositivo pueda detectar determinados niveles de sonido y activar una señal visual.
También será necesario evaluar durante las próximas etapas si los componentes seleccionados permiten alcanzar el funcionamiento esperado y si es necesario realizar ajustes en la sensibilidad del sensor para evitar activaciones falsas.

### Próximos pasos

Para la siguiente semana se propone:
*  Definir con mayor precisión el funcionamiento general del sistema.
*  Determinar los componentes definitivos que serán utilizados.
*  Realizar las primeras pruebas con la micro:bit y los sensores.
*  Investigar y probar la detección de sonidos mediante el sensor correspondiente.
*  Diseñar una primera versión del circuito.
*  Comenzar con la programación básica de la alarma visual.
*  Establecer una estructura inicial para el código y el repositorio de GitHub.
*  Realizar las primeras pruebas del prototipo y registrar los resultados.


### Imágenes o videos ilustrativos del avance
<img width="2160" height="3840" alt="IMG-20260819-WA0004" src="https://github.com/user-attachments/assets/7c00f7b0-8139-43fa-84a3-f68c92262ef8" />
<img width="1152" height="2048" alt="IMG-20260819-WA0018" src="https://github.com/user-attachments/assets/ac4eddc5-16ef-4b0f-9911-d02074e9dbdb" />

 


## 19/8/2026
Durante esta segunda semana se continuó con el desarrollo de la alarma visual para personas sordas utilizando una micro:bit, avanzando desde la etapa inicial de investigación hacia el prototipado y las primeras pruebas prácticas. El objetivo principal de esta etapa fue comprobar la capacidad de la micro:bit para detectar sonidos mediante un micrófono y utilizar el nivel de sonido registrado para generar una respuesta visual. Para ello, se desarrolló inicialmente un prototipo en Tinkercad y posteriormente se trasladó el circuito a componentes físicos reales.

Además, durante esta semana se comenzó a trabajar con el IoT Kit de Elecfreaks, investigando especialmente el funcionamiento del micrófono incorporado y de la pantalla del dispositivo. Como parte de estas pruebas, se desarrolló un primer prototipo de menú para mostrar información en la pantalla. Finalmente, se consiguió que el LED RGB respondiera correctamente a los sonidos detectados, pudiendo encenderse en diferentes colores dependiendo del nivel de sonido registrado, lo que representa un avance importante hacia el funcionamiento esperado de la alarma.


### Tareas completadas
*  Se continuó con la investigación y planificación iniciada durante la primera semana.
*  Se realizó un prototipo del circuito en Tinkercad.
*  Se planteó como primer objetivo detectar sonido y utilizar esta información para controlar un LED RGB.
*  Se trasladó el circuito diseñado en Tinkercad a componentes físicos reales.
*  Se realizaron pruebas con la micro:bit, el micrófono y el LED RGB.
*  Se logró detectar diferentes niveles de sonido mediante el micrófono.
*  Se consiguió que el LED RGB se encienda en diferentes colores según el nivel de sonido detectado.
*  Se comenzó a investigar el funcionamiento del IoT Kit de Elecfreaks, particularmente el micrófono incorporado.
*  Se realizaron pruebas para comprender cómo utilizar el micrófono del kit junto con la micro:bit.
*  Se desarrolló un prototipo inicial de menú para mostrar contenido en la pantalla del IoT Kit.
*  Se continuó con la revisión de la documentación correspondiente al proyecto y a los componentes utilizados.


### Problemas encontrados y soluciones/alternativas propuestas

- Uno de los principales inconvenientes encontrados durante esta semana fue la familiarización con el IoT Kit de Elecfreaks, ya que el equipo no había trabajado anteriormente con este dispositivo. Fue necesario investigar su funcionamiento, los componentes incluidos y la forma correcta de utilizarlos junto con la micro:bit.
- También se presentaron algunos contratiempos durante la implementación física del circuito previamente realizado en Tinkercad. Debido principalmente a la falta de experiencia del equipo con determinadas conexiones y componentes, fue necesario revisar el circuito y realizar diferentes pruebas hasta conseguir reproducir correctamente el funcionamiento esperado.
- Finalmente, se logró solucionar estos inconvenientes y obtener un resultado funcional: el sistema detecta el nivel de sonido y modifica el color del LED RGB en función de dicho nivel. Este resultado permitió comprobar que es posible utilizar la intensidad del sonido como criterio para generar diferentes niveles de alerta visual.


### Próximos pasos

Para la siguiente semana se propone:
*  Continuar experimentando con el micrófono del IoT Kit.
*  Determinar los rangos de sonido que corresponderá a cada nivel de alerta.
*  Ajustar la sensibilidad del sistema para evitar activaciones innecesarias.
*  Continuar desarrollando el menú de la pantalla del IoT Kit.
*  Integrar progresivamente el micrófono, la pantalla y los elementos visuales en un único sistema.
*  Definir qué colores representarán cada nivel de alerta.
*  Realizar pruebas con diferentes tipos y niveles de sonido.
*  Analizar posibles falsos positivos y buscar alternativas para mejorar la precisión.
*  Continuar documentando los avances y las dificultades encontradas durante el desarrollo.


### Imágenes o videos ilustrativos del avance
<img width="2048" height="1432" alt="IMG-20260819-WA0022" src="https://github.com/user-attachments/assets/7afd73eb-09f8-4fbe-94d8-0742ca70f96b" />
<img width="2048" height="1152" alt="IMG-20260819-WA0021" src="https://github.com/user-attachments/assets/149f11f3-e8bd-4df7-ac6f-f2001adf3437" />


## 26/8/2026
Durante esta tercera semana se continuó con el proceso de desarrollo e integración de los diferentes componentes del proyecto de alarma visual para personas sordas mediante micro:bit. El trabajo se enfocó principalmente en mejorar la interacción con el dispositivo y avanzar en la organización del código, desarrollando un menú inicial en la pantalla del IoT Kit de ELECFREAKS compuesto por tres opciones navegables. Si bien las opciones ya pueden visualizarse e interactuarse mediante los controles del dispositivo, su funcionalidad específica todavía se encuentra pendiente de implementación.

También se realizaron mejoras en el sistema de control de los LED RGB, incorporando un mecanismo para guardar configuraciones de colores que permita posteriormente establecer diferentes colores para los distintos niveles de alerta. Paralelamente, se comenzó el proceso de integración de la comunicación por radio entre diferentes micro:bit, con el objetivo de que un dispositivo pueda transmitir información a otro cuando se detecte un evento. Finalmente, se realizaron modificaciones en la conexión física de los componentes, buscando mejorar la organización y el funcionamiento del circuito y facilitar las próximas etapas de integración.

### Tareas completadas
*  Se desarrolló un menú inicial en la pantalla del IoT Kit de ELECFREAKS.
*  Se incorporaron tres opciones dentro del menú.
*  Se implementó la interacción básica con las opciones mediante los botones del dispositivo.
*  Se dejó preparada la estructura del menú para incorporar las funcionalidades correspondientes en próximas etapas.
*  Se realizaron mejoras en el código encargado de controlar los LED RGB.
*  Se implementó un sistema inicial para guardar configuraciones de colores, permitiendo establecer qué color utilizará el dispositivo para las diferentes condiciones de alerta.
*  Se comenzó el proceso de integración de la comunicación por radio entre diferentes micro:bit.
*  Se realizaron las primeras pruebas y preparaciones necesarias para permitir el intercambio de información entre dispositivos.
*  Se realizaron cambios en la conexión física de los componentes, buscando mejorar la distribución y estabilidad del circuito.
*  Se continuó con la revisión y organización del código para facilitar la incorporación de nuevas funcionalidades.


### Problemas encontrados y soluciones/alternativas propuestas
Durante esta semana, uno de los principales desafíos estuvo relacionado con la integración de las diferentes funcionalidades del proyecto. A medida que se incorporaron nuevas características, como el menú, el almacenamiento de configuraciones y la comunicación por radio, fue necesario reorganizar parte del código para evitar conflictos entre los distintos componentes del sistema.

También fue necesario realizar modificaciones en las conexiones físicas de los componentes, con el objetivo de adaptar el circuito a los nuevos requerimientos del proyecto y mejorar su organización. Estos cambios permitieron preparar el dispositivo para una futura integración de todas las funcionalidades.

En cuanto a la comunicación por radio, durante esta semana se comenzó a trabajar en la estructura necesaria para que diferentes micro:bit puedan intercambiar información. Esta funcionalidad todavía se encuentra en proceso de desarrollo, por lo que las próximas pruebas estarán orientadas a comprobar la correcta transmisión y recepción de los datos.


### Próximos pasos

Para la siguiente semana se propone:

- Implementar las funcionalidades correspondientes a las tres opciones del menú.
- Incorporar al menú la posibilidad de modificar las configuraciones del dispositivo.
- Continuar mejorando el sistema de almacenamiento de los colores de alerta.
- Definir los diferentes niveles de alerta y sus respectivos colores.
- Finalizar la integración de la comunicación por radio entre las diferentes micro:bit.
- Determinar qué información será enviada entre los dispositivos.
- Realizar pruebas de comunicación a diferentes distancias.
- Continuar reorganizando y optimizando el código a medida que se integren nuevas funcionalidades.
- Continuar realizando pruebas con el circuito físico y ajustar las conexiones según sea necesario.
- Avanzar hacia una primera versión en la que los distintos componentes funcionen de manera integrada.

### Imágenes o videos ilustrativos del avance
<img width="1500" height="2000" alt="IMG-20260826-WA0009" src="https://github.com/user-attachments/assets/7d5dfe7f-964b-4d74-98a6-6e79fdbb45ea" />
