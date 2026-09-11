"""Reto de la sesion 4 · Un agente que se rinde.

═══════════════════════════════════════════════════════════════════════════
QUE PASA
═══════════════════════════════════════════════════════════════════════════

El actor-critico de ``rlrs.pg`` colapsa en la mitad de las semillas. No
aprende despacio: **deja de aprender**. Lo viste en la parte 4 del
experimento:

    tramo             retorno medio   desviacion   llegan a la meta
    0 a 100                 -3.5056       0.9940                25 %
    200 a 300               -3.9776       0.2229                 1 %
    500 a 600               -4.0000       0.0000                 0 %

La columna que importa es la de la desviacion. Cuando llega a cero, todos los
episodios dan lo mismo, y un metodo que aprende comparando episodios se queda
sin nada que comparar.

═══════════════════════════════════════════════════════════════════════════
QUE HAY QUE HACER
═══════════════════════════════════════════════════════════════════════════

Dos cosas, y la primera se entrega aunque la segunda no salga.

1. **El diagnostico, escrito en tu bitacora antes de tocar el codigo.** Por
   que crees que pasa. Que cantidad se hace cero primero. Por que no se
   arregla con mas episodios.

Respuesta punto 1:
El agente deja de aprender porque la incertidumbre al elegir sus acciones cae 
a cero antes de tiempo, volviéndose completamente rígido y repitiendo exactamente
la misma ruta en cada intento. Lo primero que se hace cero es esa variedad o 
entropía en sus decisiones, provocando inmediatamente que la diferencia de 
resultados entre episodios caiga a cero; al ser todos los intentos idénticos, 
el agente pierde el contraste necesario para evaluar qué decisiones fueron mejores
o peores que el promedio. Este problema no se soluciona simplemente añadiendo
más episodios porque, cuando el agente está totalmente convencido de una sola 
acción, los ajustes matemáticos que le permiten corregir su comportamiento 
se vuelven nulos, dejándolo atrapado para siempre en el mismo circuito repetitivo.

2. **El arreglo.** Rellena ``mi_agente`` para que no colapse en ninguna
   semilla. Tienes todas las piezas de ``rlrs.pg`` disponibles y puedes mover
   lo que quieras: el metodo, la tasa de aprendizaje, la linea base, el
   tamano del lote, el termino de entropia.

    uv run python scripts/reto4.py        lo evalua con semillas que no ves
    uv run pytest tests/test_reto4.py     comprueba el contrato

Despues de ejecutar :
Logré superar el reto añadiéndole a mi agente una regla de flexibilidad que lo 
premia por no volverse terco antes de tiempo, obligándolo a mantener abiertas 
distintas opciones al decidir. Al evitar que se concentrara al 100 % en una 
sola ruta fija (manteniendo su concentración en un nivel saludable de entre 
0.74 y 0.86 en las seis semillas), mi agente nunca repitió episodios idénticos 
y siempre conservó el contraste necesario entre intentos para seguir corrigiendo 
su rumbo. Gracias a esto, evité que se rindiera en cualquiera de las semillas y 
superé el objetivo con un resultado medio de +0.5413.

═══════════════════════════════════════════════════════════════════════════

Una pista que no es una respuesta: el problema no esta en cuanto aprende, sino
en que deja de haber informacion que aprender. Cualquier arreglo tiene que
atacar eso.
"""

from __future__ import annotations

from rlrs.pg import EntrenamientoPG, actor_critico, reinforce  # noqa: F401


def mi_agente(env, phi, episodes: int, gamma: float, seed: int) -> EntrenamientoPG:
    """Entrena un agente de gradiente de política que no colapse.

    Tiene que devolver lo que devuelven ``actor_critico`` o ``reinforce``, es
    decir un ``EntrenamientoPG``.
    """
    # ── tu respuesta va aqui ──────────────────────────────────────────────
    return actor_critico(
        env,
        phi,
        episodes=episodes,
        gamma=gamma,
        seed=seed,
        entropia=0.01,     # Activa la regularización por entropía en español
        lr_actor=0.001,    # Tasa de aprendizaje suave para el actor
        lr_critico=0.005,  # Tasa de aprendizaje para el crítico
    )