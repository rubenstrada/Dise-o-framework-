# Guía breve para explicar el Avance 2

## Idea central en 30 segundos

El framework está organizado por responsabilidades. Cada módulo recibe una
entrada clara, hace una sola parte del proceso y devuelve un resultado tipado.
Como el caso no incluye datos, columnas, target ni horizonte, la configuración
de ejemplo conserva esos campos vacíos y el sistema responde `blocked`. Esto
evita aparentar resultados y deja preparado el flujo para cuando llegue la
fuente real.

## Clase, objeto, atributo y método

- Una **clase** define una responsabilidad. Ejemplo: `DataLoader` define cómo
  cargar una fuente.
- Un **objeto** es una instancia de esa clase utilizada durante una corrida.
- Un **atributo** conserva estado o configuración. Ejemplo: `source_path`.
- Un **método** realiza una acción. Ejemplo: `load()`, `validate()` o `clean()`.

## Por qué no se creó un dataset simulado

Los PDF solo mencionan tipos generales de información. No confirman nombres de
tablas, columnas, unidad de observación, target ni horizonte. Una simulación
podría resolver un problema distinto al real. La consigna permite presentar un
plan de exploración cuando todavía no hay datos, por lo que se eligió esa vía.

## Diferencia entre los módulos

- `DataLoader`: abre la fuente y no la corrige.
- `DataValidator`: observa problemas y no modifica la tabla.
- `DataCleaner`: aplica únicamente reglas autorizadas y registra cambios.
- `DataProfiler`: resume estructura, faltantes, duplicados y estadísticos.
- `EDAVisualizer`: genera gráficos solo con roles configurados.
- `DataPreprocessor`: divide por tiempo y construye transformaciones.
- `ModelTrainer`: recibe un estimador externo y lo ajusta con entrenamiento.
- `ModelEvaluator`: compara el candidato con una línea base.
- `ReportGenerator`: convierte resultados en archivos interpretables.
- `LuminaPipeline`: coordina el orden sin absorber la lógica de los demás.

## Tres decisiones que conviene poder defender

1. Se usó configuración YAML para no fijar nombres de columnas en el código.
2. Se separa pasado y futuro antes de ajustar transformaciones para evitar fuga
   de información.
3. Un modelo no se recomienda si no supera una línea base bajo las mismas
   observaciones.

## Evidencia real

- Hay 24 pruebas automatizadas aprobadas, incluida la reproducción de los tres visuales.
- Se detectó una inconsistencia entre el diagrama y el contrato respecto al
  horizonte. Primero se añadió una prueba que falló y después se corrigió el
  contrato, el YAML y el `ReadinessChecker`.
- Las figuras del documento son diagramas y bocetos conceptuales, no resultados
  empresariales.

## Preguntas probables

**¿Por qué no entrenaste un modelo?**  Porque no hay target, horizonte ni
observaciones. Entrenar requeriría inventar la definición del problema.

**¿Entonces sí hay código funcional?**  Sí. Los contratos, carga, validación,
limpieza, perfilado, visualización configurable, preprocesamiento, entrenamiento,
evaluación, reportes y orquestación tienen una primera implementación y pruebas.

**¿Qué se necesita para continuar?**  Fuente autorizada, diccionario, llave,
unidad de observación, fechas, target, horizonte, baseline y costo del error.
