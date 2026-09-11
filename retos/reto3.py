"""Reto de la sesion 3 · Escriba usted la recompensa.

═══════════════════════════════════════════════════════════════════════════
QUE HAY QUE HACER
═══════════════════════════════════════════════════════════════════════════

El agente de la cuadricula tarda mucho en encontrar la meta porque durante
cientos de episodios no recibe ninguna senal util: solo el coste de cada paso.
Su trabajo es **darle una pista**, escribiendo una recompensa extra.

Rellene ``mi_moldeado``. Recibe tres cosas y devuelve un numero, que se suma a
la recompensa que el entorno ya entrega.

    anterior   la casilla donde estaba, como (fila, columna). Puede ser None
               en el primer paso.
    siguiente  la casilla a la que acaba de llegar.
    terminal   True si ``siguiente`` termina el episodio.

No hay ninguna restriccion sobre lo que puede escribir. Puede usar la
distancia a la meta, la fila, la columna, lo que se le ocurra.

═══════════════════════════════════════════════════════════════════════════
COMO SE SABE SI FUNCIONO
═══════════════════════════════════════════════════════════════════════════

    uv run python scripts/reto3.py        entrena y mide, e imprime el veredicto
    uv run pytest tests/test_reto3.py     comprueba el contrato

**Antes de ejecutar nada, escriba su prediccion en la bitacora.** Que espera
que haga su agente. Cuantos pasos va a tardar. Que retorno va a sacar.

Aviso, y va en serio: es muy probable que su primera version obtenga un
retorno estupendo y sea un desastre. Cuando eso pase, no lo arregle todavia.
Anotelo, que de eso trata la clase.
"""

#Antes de ejecutar el reto:
#Espero que el agente caiga en una trampa de incentivos y se quede dando
#vueltas en círculos al lado de la meta sin cruzarla jamás,
#pues descubrirá que le resulta más rentable seguir cobrando
#la pista de cercanía que terminar el juego. Debido a este
#comportamiento circular, el agente agotará el tiempo límite
#tardando 100 pasos por episodio y, aunque en su entrenamiento
#creerá tener miles de puntos acumulados, en la prueba real obtendrá
#un resultado pésimo de 0 % de éxito.


#Despues de ejecutar el reto:
#Antes de probar el código, esperaba que mi agente se quedara 
#dando vueltas en círculos sin cruzar nunca la meta y fallara por
#completo. Al ejecutarlo, me sorprendió ver que logró llegar al 
#final el 100 % de las veces, pero no de la forma esperada: en lugar
#de tomar el camino directo, aprendió una ruta llena de rodeos e 
#ineficiencias por todo el tablero, lo que hizo que se engañara creyendo
#que su desempeño era pésimo y dejara su resultado real muy lejos del óptimo.

from __future__ import annotations

# Estas dos las puede mover libremente.
GAMMA = 0.9      # tiene que ser el mismo descuento con el que se entrena
ESCALA = 0.5     # cuanto pesa su pista frente al coste del paso, que es -0,04

META = (0, 11)   # la esquina de arriba a la derecha de la sala de 8 x 12


def pasos_hasta_la_meta(pos: tuple[int, int]) -> int:
    """Cuantos pasos faltan hasta la meta, contando por la rejilla.

    Se la dejo hecha para que no pierda tiempo en esto. Usela o no la use.
    """
    return abs(pos[0] - META[0]) + abs(pos[1] - META[1])


# Primera prueba sin arreglar
#def mi_moldeado(
    #anterior: tuple[int, int] | None,
    #siguiente: tuple[int, int],
    #terminal: bool,
#) -> float:
    #"""La recompensa extra de una transicion. **Esto es lo que usted escribe.**"""
    # ── su respuesta va aqui ──────────────────────────────────────────────
    
    # Calculamos la distancia restante desde la casilla a la que acaba de llegar
    #distancia = pasos_hasta_la_meta(siguiente)
    
    # Le damos un premio que crece a medida que la distancia a la meta se reduce.
    # Usamos 20 como referencia de distancia máxima para que el premio siempre sea positivo.
    #recompensa_estar_cerca = (20 - distancia) * ESCALA
    
    #return recompensa_estar_cerca

# Arreglo de segunda prueba
def mi_moldeado(
    anterior: tuple[int, int] | None,
    siguiente: tuple[int, int],
    terminal: bool,
) -> float:
    """La recompensa extra de una transicion utilizando potenciales de Ng."""
    # Si es el primer paso, no hay estado anterior para calcular la diferencia
    if anterior is None:
        return 0.0
    
    # Definimos una función de potencial estrictamente positiva
    # phi(s) = 20 - pasos_hasta_la_meta(s)
    phi_anterior = 20 - pasos_hasta_la_meta(anterior)
    phi_siguiente = 20 - pasos_hasta_la_meta(siguiente)
    
    # Calculamos la diferencia de potencial descontada por el GAMMA del archivo
    recompensa_shaping = (GAMMA * phi_siguiente - phi_anterior) * ESCALA
    
    return recompensa_shaping
