Preinscripción del experimento — Reto 5 · La política que se queda clavada

Fecha:11-sep-2026

1. Diagnóstico (por qué se queda clavada)

La ávida pura, en cuanto un brazo le da una recompensa buena, deja de mirar los
demás y se queda tirando de ese mismo brazo. El problema es que ese brazo se
agota: en Meridiano, "tirar del brazo k" es practicar la habilidad k, y una vez
el estudiante ya la domina, seguir practicándola no enseña nada más. La ávida
se queda cobrando de un pozo seco — sigue eligiendo el brazo que antes le dio
la mejor recompensa, sin darse cuenta de que ya no le da nada nuevo.

La prueba está en la propia tabla del reto: de la ronda 100 a la 1500, la
ávida no mejora ni una milésima y toca solo 2 o 3 brazos de 20.

2. Hipótesis

Usaremos UCB1 porque, a diferencia de la ávida (que deja de explorar por
completo) y de epsilon-ávida (que explora al azar sin criterio), UCB1
prioriza probar los brazos de los que tiene menos información acumulada. Eso
debería traducirse en repartir las tiradas entre muchos brazos al principio, y
solo concentrarse cuando ya hay evidencia sólida de cuál es mejor — evitando
el estancamiento de la ávida.

3. Métricas

- Ganancia media a 500 rondas, contra las dos líneas base que mide el
  propio arnés: la ávida pura (+0,0160) y tirar al azar.
- Brazos distintos usados, sobre 20 brazos seria un buen número de ganancia tocando
  solo 2-3 brazos no cuenta como solución.

4. Criterio de decisión

Abandonamos UCB1 si a 500 rondas no supera +0,1400 de ganancia, o si toca
menos de 15 de los 20 brazos. En ese caso, probamos Thompson sampling en su
lugar.

5. Predicción antes de ejecutar

Predecimos que UCB1 alcanzará una ganancia ≥ +0,19 a 500 rondas y tocará
al menos 18 de 20 brazos, basándonos en el valor de referencia que trae
este mismo documento (+0,1933 a 500 rondas) y en que UCB1 explora en función
de la incertidumbre, no al azar fijo.

Si el resultado real quedara muy por debajo de +0,14 a pesar de repartir bien
los brazos, la conclusión sería que el problema no está en la falta de
exploración, sino en algo puntual del cálculo de la ganancia o del criterio
de selección mas no en la elección de UCB1 como familia de política.