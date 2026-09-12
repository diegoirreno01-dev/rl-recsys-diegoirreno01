"""Reto de la sesion 6 · Gane a dos lineas de codigo.

═══════════════════════════════════════════════════════════════════════════
QUE PASA
═══════════════════════════════════════════════════════════════════════════

Sobre los datos de ASSISTments, con particion TEMPORAL, esto es lo que sale:

    recomendador                 Recall@10   nDCG@10   cobertura
    repetir lo propio               0,7009    0,5880       0,973
    popularidad                     0,4121    0,2738       0,090
    kNN por items                   0,2613    0,1857       0,856
    al azar                         0,0990    0,0683       1,000
    novedad pura                    0,0949    0,0766       0,649

Lea la primera fila y la tercera. **El filtro colaborativo pierde contra una
linea base de dos lineas**, y por casi tres veces. Y «repetir lo propio» es
literalmente esto:

    los items que este usuario ya practico, el mas repetido primero,
    y despues los mas populares para rellenar

Lea tambien la ultima fila. «Novedad pura», que solo recomienda cosas que el
usuario NO ha hecho, saca menos que recomendar AL AZAR. La intuicion de que un
recomendador no debe repetir es, en estos datos, el error mas caro posible.

═══════════════════════════════════════════════════════════════════════════
QUE HAY QUE HACER
═══════════════════════════════════════════════════════════════════════════

Dos cosas, y la primera se entrega aunque la segunda no salga.

1. **El diagnostico, escrito en su bitacora antes de tocar el codigo.** Por que
   gana repetir. Que dice eso sobre estos datos. Y una prediccion: cuanto cree
   que va a sacar su recomendador.

Diagnostico (Antes de ejecutar el codigo):

Repetir lo propio gana porque el 70,6% de lo que un estudiante practica mañana
ya lo practicó antes, un dato medido en el Taller C que expusimos: en un dominio
donde repasar es literalmente cómo se aprende, "lo de siempre" es una predicción
excelente, y ningún algoritmo colaborativo necesita ser complejo para perder
frente a eso. El filtro kNN no está mal implementado; simplemente mide algo
distinto —qué hacen usuarios parecidos a mí— cuando lo que de verdad predice aquí
es qué he hecho yo mismo. Esto nos dice que en estos datos la señal más fuerte
no está en el comportamiento colectivo sino en el historial individual de cada
estudiante, así que cualquier recomendador que quiera superar a repetir lo
propio tiene que partir de ahí y no ignorarlo. Nuestra estrategia es reproducir
esa misma lógica de repetición por frecuencia, y aprovechar el espacio real de
mejora en el 30% restante: el tramo donde el estudiante prueba algo nuevo y 
"repetir lo propio" se rinde y rellena a ciegas con popularidad.
En lugar de ese relleno ciego, vamos a rellenar con kNN, que por sí solo ya
cubre 0,856 del catálogo, para no sacrificar cobertura mientras intentamos
superar el Recall. Predecimos un Recall@10 mayor o igual a 0,72, apenas por
encima de 0,7009, porque el 70% del problema ya lo resuelve la parte de repetición
y el margen de mejora real es angosto; y una cobertura mayor o igual a 0,80,
heredada del relleno con kNN. Si el resultado real queda muy por debajo de 0,7009,
la conclusión no sería que la idea de "repetir más relleno inteligente" está mal,
sino que el relleno de kNN está aportando menos de lo esperado en ese tramo específico.

2. **El recomendador.** Rellene ``mi_recomendador`` para superar a «repetir lo
   propio» sin encoger el catalogo. Tiene todo ``rlrs.recomendacion``
   disponible y puede escribir el suyo desde cero.

    uv run python scripts/reto6.py        mide y da el veredicto
    uv run pytest tests/test_reto6.py     comprueba el contrato

═══════════════════════════════════════════════════════════════════════════

Aviso: hay una forma facil de subir el Recall que consiste en recomendarle a
todo el mundo lo mismo. Por eso hay un criterio de cobertura, y por eso el
arnes le ensena las cuatro cifras y no una.
"""

from __future__ import annotations

from collections import Counter

from rlrs.recomendacion import (  # noqa: F401
    Particion,
    factorizacion_implicita,
    knn_items,
    por_popularidad,
    repetir_lo_propio,
)


def mi_recomendador(particion: Particion):
    """Repite lo propio primero (por frecuencia), y cuando eso se acaba,
    rellena con kNN en vez de con popularidad — para no perder cobertura
    en el relleno, que es donde 'repetir lo propio' se queda ciego.
    """
    recomendador_knn = knn_items(particion, vecinos=20)

    def recomendar(historial):
        # Parte personal: lo que el usuario ya practicó, más frecuente primero.
        # Esto reproduce a mano lo que hace "repetir lo propio" en su primera mitad.
        conteo = Counter(historial)
        propios = [item for item, _ in conteo.most_common()]

        # Parte de relleno: en vez de "lo más popular", usamos lo que kNN
        # cree que le gustaría a alguien parecido a este estudiante.
        vecinos = recomendador_knn(historial)

        vistos = set(propios)
        relleno = [item for item in vecinos if item not in vistos]

        return propios + relleno

    return recomendar


"""
Analisis de resultados (Despues de ejecutar):

Nuestro recomendador superó a "repetir lo propio" en Recall@10 (0,7217 contra 0,7009) sin encoger
el catálogo (cobertura 0,964 contra 0,973) — resultado coincidente con la predicción (≥0,72).
La decisión concreta que creemos que lo logró fue separar el problema en dos partes en vez
de tratarlo como una sola: dejamos intacta la lógica de repetición por frecuencia (que ya
resuelve el 70% del problema, tal como se midió en el Taller C) y solo intervinimos en
el tramo donde esa lógica se rinde — el relleno para ítems nuevos. Al reemplazar ahí
el relleno ciego por popularidad (que solo cubre 0,090 del catálogo) por un relleno
con kNN (que cubre 0,856), ganamos Recall en el tramo de exploración sin sacrificar
casi nada de cobertura en el tramo de repetición, porque nunca tocamos esa primera parte.
La novedad también subió (6,06 contra 5,38 de repetir lo propio), lo cual tiene sentido:
el relleno con kNN es más variado que el relleno con popularidad.
"""