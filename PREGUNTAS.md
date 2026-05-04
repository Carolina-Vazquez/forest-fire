Pregunta 1: ¿Por qué el endpoint /api/simulations/{id}/step/ usa POST en lugar de GET?

Los GET se utilizan para consultar datos, pero estos datos nunca cambian, es decir da igual cuantas veces hagas el GET que el dato nunca va a cambiar. Esto se llama propiedad de idempotencia, que como ya he explicado significa repetir la misma petición y el resultado siempre debe ser el mismo, sin cambiar nada.

En el caso de nuestro endpoint cuando llamamos a /step/ la simulación avanza un paso, es decir las celdas en la base de datos cambian, al igual que el histograma y el contador de pasos. Esto quiere decir que en cada llamada los datos si se están modificando. 

Por todo esto mencionado, utilizamos POST, para no violar la propiedad de idempotencia antes mencionada. 


Pregunta 2: ¿Dónde debería vivir el estado de la simulación, en el servidor o en el navegador?

En mi proyecto he decidido poner el estado de simulación en el servidor que es la BBDD de Django. Esta decisión la he tomado porque el enunciado del ejercicio pedia acumular estadísticas e histograma a lo largo de la vida de la simulación, lo cual requiere persistencia. 

El hecho de que el estado este en el servidor hace que se guarde el estado de la cuadricula en la BBDD y cada vez que mandamos la petición POST mencionada en la pregunta 1, el servidor puede calcular el nuevo estado, guardarlo y devolverlo. 

Esto se traduce en que la simulación persiste aunque cierres el navegador y las estadísticas e histograma se acumulan a lo largo del tiempo. También varios usuarios pueden acceder a la misma simulación y la lógica se mantiene centralizada y es más fácil de controlar. 

En el caso de que hubiesemos puesto el estado en el navegador, la cuadricula estaria en JavaScript, en la memoria del navegador. Hubiesemos tenido la ventaja de que sería mucho mas rápido, ya que no tiene latencia, no necesitariamos servidor porque no habria base de datos ni peticiones en red para cada paso, por lo que se podrían ejecutar miles de pasos por segundo. La razón de no utilizarlo es porque no acumularia las estadisticas a largo plazo y si cierras el navegador se pierde todo. 


Pregunta 3: ¿Qué ocurre con el tamaño medio de los incendios si aumentas p manteniendo f constante? ¿Y si mantienes constante el cociente p/f pero aumentas ambos proporcionalmente?

Al aumentar p manteniendo f constante hay mas árboles haciendo el bosque más denso y el fuego se propaga más por lo que los incendios son cada vez más grandes. 

Al mantener p/f constante pero subir ambos, la densidad del bosque baja un poco porque al poner f más alta provoca más rayos que queman árboles antes de que crezcan. 

Así quedarían los datos de las 3 simulaciones realizadas:

p = 0,05 f = 0,001 Densidad = 39,9% (Incendios variados, muchos pequeños y algunos grandes)
p = 0,10 f = 0,001 Densidad = 41,8% (Más árboles e incendios más grandes)
p = 0,10 f = 0,002 Densidad = 40,60 % (Densidad baja respecto a los casos anteriores, incendios más frecuentes)

Pregunta 4: ¿Dónde validaste el parámetro size (entero entre 20 y 200) y por qué elegiste ese lugar? Describe al menos dos lugares alternativos.

En mi proyecto lo he validado en el archivo serializers.py, concretamente en CreateSimulationSerializer, en la siguiente linea de código;

size = serializers.IntegerField(min_value=20, max_value=200)

La razón de haber escogido serializers para la validación, es porque su función es recibir datos externos y comprobar que sean correctos antes de procesarlos. Si hay algun error lo devuelve al cliente sin llegar a guardarlo en la BBDD. Esto centraliza la validación, genera los errores en un JSON automáticamente y mantiene el código limpio y separdo. 

Otro lugar alternativo donde podría validarse, sería en el archivo models.py añandiendo un validar de Django al campo size. La desventaja de esto es que la validación ocurre muy tarde, justo antes de guardarlo en la base de datos y esto implica que si hay algun error ya se habrá ejecutado código innecesario.

También se puede validar en el archivo views.py con un if manual en el método post. Funciona pero se mezclan lógica de validación con lógica de negocio, lo que hace el código más dificil de mantener y de reutilizar. Si luego otro endpoint necesita crear simulaciones, tendriamos que repetir la validación. 

Pregunta 5: ¿Qué ventaja tiene uv con pyproject.toml frente a requirements.txt con pip freeze? Explica la diferencia entre dependencias directas y transitivas.

Las dependencias directas son aquellas que yo elijo instalar explicitamente porque las necesita mi proyecto.

Las dependencias transitivas, se instalan automáticamente poque las dependencias directas las necesitan, es decir se instalan solas. 

Por ejemplo en mi proyecto yo instalé Django, Djangorestframework, etc... que son las dependencias directas, pero django necesita asgiref y sqlparse, que son las dependencias transitivas que se intalaron solas. 

En cuanto a que ventaja tiene utilizar uv frente a pip freeze, es que el problema de usar pip freeze es que este genera una lista de absolutamente todos los paquetes instalados ya sean directos o transitivos y todo con versiones fijas. No sabes cuales has instalado tu directamente o cuales son las dependencias transitivas. Además si el proyecto lo instalasemos en otro SO por ejemplo Linux, puede que algunas de las dependencias transitivas sean diferentes, porque estas dependen del SO,con lo que podría resultar en que el proyecto no funcione igual.

En cambio, uv con pyproject.toml contiene solo las dependencias directas, manteniendolo limpio y claro y por otro lado uv.lock guarda las versiones exactas de todo para que sea usable en cualquier ordenador independientemente de su SO. Otra ventaja de uv es que es muchisimo más rapido que pip instalando paquetes. 
