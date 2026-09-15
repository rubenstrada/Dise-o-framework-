# Requisitos de datos antes de modelar

## Motivo

El caso no proporciona tablas, columnas ni registros. Esta ausencia no se corrige inventando un dataset. Se convierte en una lista de información que Lumina debe solicitar y validar con Red Comercial Boreal.

## Inventario de fuentes

Por cada archivo, tabla o consulta se requiere:

- nombre y ubicación de la fuente;
- sistema que la genera;
- responsable funcional y técnico;
- frecuencia y hora de actualización;
- cobertura histórica;
- formato, codificación y zona horaria;
- reglas de acceso y retención.

## Diccionario de datos

Cada campo debe documentar:

- nombre exacto;
- significado de negocio;
- tipo físico y tipo lógico;
- unidad de medida y moneda;
- valores permitidos;
- significado de cero y de valor faltante;
- fecha desde la que es confiable;
- momento en que está disponible para decidir.

## Unidad de observación y llave

Se debe confirmar qué representa una fila. Producto por sucursal por semana es una hipótesis procedente del Avance 1, no una definición confirmada. También debe acordarse la llave que hace única cada observación y el tratamiento de correcciones tardías.

## Tiempo

La organización debe identificar la fecha del evento, la fecha de registro, la zona horaria y la frecuencia real. El tiempo de reabasto y la frecuencia de pedido determinan el horizonte. Cuatro semanas permanece como hipótesis y no debe fijarse antes de consultar la operación.

## Ventas demanda e inventario

Venta observada no siempre equivale a demanda. Si una sucursal agotó un producto, una venta baja puede significar falta de disponibilidad. Se requieren señales de inventario inicial, movimientos, devoluciones, ajustes, quiebres de stock y demanda no atendida para decidir qué objetivo es defendible.

## Promociones precios y disponibilidad futura

Solo pueden utilizarse como predictores los precios y promociones conocidos en el momento real de la decisión. Una campaña registrada después de la fecha de corte produciría fuga de información.

## Objetivo y decisión

Antes de entrenar debe contestarse:

1. ¿Qué decisión cambiará con la predicción?
2. ¿Quién toma esa decisión?
3. ¿Qué entidad recibe una predicción?
4. ¿Qué periodo futuro se desea anticipar?
5. ¿Cómo se observará después el resultado real?
6. ¿Cuánto cuesta un faltante frente a un sobrante?
7. ¿Cuál es la regla simple que actuará como línea base?

El contrato de configuración conserva `prediction_horizon: null` hasta que
este periodo se confirme; el modelado permanece bloqueado mientras siga vacío.

## Plan de exploración

Cuando existan fuentes autorizadas se revisará:

1. forma y tipos;
2. cobertura y continuidad temporal;
3. faltantes por campo y patrón;
4. duplicados exactos y de llave;
5. categorías y cardinalidad;
6. estadísticos descriptivos;
7. valores imposibles y atípicos;
8. integridad entre ventas, devoluciones e inventario;
9. censura de ventas por desabasto;
10. tasa base y estabilidad del objetivo propuesto.

## Visualizaciones previstas

| Gráfica | Campos lógicos | Pregunta de negocio |
|---|---|---|
| Serie temporal | Fecha, entidad y medida | ¿Existen tendencia, estacionalidad o rupturas? |
| Mapa de calor | Dos dimensiones y medida | ¿Dónde se concentra la disponibilidad o el riesgo? |
| Histograma y caja | Medida y segmento | ¿Hay asimetrías o valores atípicos por grupo? |
| Real contra pronóstico | Fecha, real y predicción | ¿El modelo mejora el baseline y dónde falla? |

Estas visualizaciones son propuestas. No se generarán resultados empresariales hasta que existan las columnas y observaciones requeridas.

## Criterio de aceptación

El análisis puede comenzar cuando la fuente abre de forma reproducible, el diccionario cubre los campos críticos, la llave no es ambigua, el tiempo está ordenado y la diferencia entre venta y demanda está documentada. El modelado requiere además objetivo, horizonte, fecha de corte, baseline y métrica acordados.
