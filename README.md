# Framework modular conceptual de Lumina

## Propósito

Este repositorio contiene la aproximación técnica preliminar del Avance de proyecto 2 de Programación para la inteligencia artificial. Organiza en módulos el flujo de carga, validación, limpieza, perfilado, visualización, preprocesamiento, entrenamiento, evaluación y reporte propuesto para Lumina Datos Operativos.

El caso de Red Comercial Boreal describe información general de ventas, inventarios, categorías, precios y promociones, pero no proporciona archivos, tablas, columnas, tipos, llaves ni variable objetivo. Por ello, este proyecto no incluye un dataset empresarial ni presenta estadísticas o métricas atribuidas a Lumina. Su primera salida válida es un diagnóstico de preparación que explica qué definiciones faltan.

## Estado y alcance

El framework está construido y probado como estructura preliminar configurable. Puede:

- diagnosticar si existen requisitos suficientes para perfilar o modelar;
- cargar archivos CSV sin cambiar sus encabezados;
- validar una tabla contra un contrato declarado;
- limpiar duplicados o renombrar columnas solo mediante una regla explícita;
- generar un perfil estructural sin exigir etiqueta;
- crear tres visualizaciones cuando las columnas necesarias están configuradas;
- separar entrenamiento y prueba respetando el tiempo;
- ajustar un estimador proporcionado externamente;
- evaluar regresión contra una línea base;
- producir perfiles y manifiestos trazables.

El proyecto no selecciona un algoritmo, no entrena un modelo de Boreal y no determina un horizonte de pronóstico. Esas decisiones requieren el contrato de datos y la validación operativa descritos en `docs/requisitos_de_datos.md`.

> **Alcance académico:** este repositorio demuestra la arquitectura y el comportamiento técnico del framework. No contiene una base de datos de Lumina, no define columnas reales y no presenta resultados de negocio.

## Organización

```text
lumina_avance_2/
├── config/
│   └── config.example.yaml
├── docs/
│   ├── arquitectura.md
│   └── requisitos_de_datos.md
├── src/lumina_framework/
│   ├── core/
│   ├── data/
│   ├── preprocessing/
│   ├── visualization/
│   ├── modeling/
│   ├── reporting/
│   ├── pipeline/
│   └── cli.py
├── tests/
├── artifacts/
└── pyproject.toml
```

La agrupación es por capacidad. `cli.py` solo recibe argumentos e inicia el diagnóstico; no contiene reglas de datos, gráficas ni modelos.

## Arquitectura visual

![Arquitectura preliminar del framework](docs/images/arquitectura_framework.png)

El diagrama completo de clases, contratos, entradas y salidas se encuentra en [`docs/arquitectura.md`](docs/arquitectura.md).

![Mapa de clases y responsabilidades](docs/images/mapa_clases.png)

## Componentes

| Componente | Responsabilidad |
|---|---|
| `FrameworkConfig` | Mantener rutas independientes del esquema |
| `DatasetContract` | Representar definiciones confirmadas por el cliente |
| `ReadinessChecker` | Informar requisitos ausentes antes de ejecutar |
| `RunContext` | Registrar identidad, eventos y artefactos de una corrida |
| `DataLoader` | Leer CSV sin transformaciones silenciosas |
| `DataValidator` | Comparar datos contra el contrato |
| `DataCleaner` | Aplicar únicamente reglas autorizadas y registrarlas |
| `DataProfiler` | Describir estructura y calidad básica |
| `EDAVisualizer` | Generar figuras cuando existen los campos requeridos |
| `DataPreprocessor` | Separar periodos y construir transformadores no ajustados |
| `ModelTrainer` | Ajustar el estimador recibido solo con entrenamiento |
| `ModelEvaluator` | Comparar el candidato contra una línea base |
| `ReportGenerator` | Persistir perfil y manifiesto |
| `LuminaPipeline` | Coordinar las etapas sin absorber su lógica |

## Instalación en Windows

Desde esta carpeta:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
```

## Diagnóstico conceptual

Ejecutar:

```powershell
.\.venv\Scripts\python.exe -m lumina_framework.cli --config config\config.example.yaml
```

La configuración de ejemplo conserva valores `null` y listas vacías de forma intencional. No son errores de programación ni espacios para completar al azar: representan definiciones que Boreal debe confirmar. La salida esperada informa:

```json
{
  "status": "blocked",
  "blocker_codes": [
    "missing_source",
    "missing_columns",
    "missing_target",
    "missing_prediction_horizon"
  ],
  "loaded_rows": null,
  "artifact_paths": []
}
```

## Pruebas

```powershell
.\.venv\Scripts\python.exe -m pytest -v
```

Los fixtures creados dentro de `tests` son tablas mínimas para comprobar contratos de software. No representan datos simulados de Lumina ni se utilizan para extraer conclusiones empresariales.

## Flujo previsto

```text
Configuración y contrato
          ↓
Diagnóstico de preparación
          ↓
Carga → Validación → Limpieza explícita → Perfilado
                                         ├→ Visualización
                                         └→ Preprocesamiento
                                               ↓
                                          Entrenamiento
                                               ↓
                                      Evaluación vs baseline
                                               ↓
                                            Reporte
```

Cada etapa comprueba sus condiciones de entrada. La falta de etiqueta bloquea el modelado, pero no impide un perfil estructural cuando sí existen fuente y columnas confirmadas.

## Librerías

- **Pandas:** lectura, validación y manipulación tabular.
- **NumPy:** validación numérica y cálculo de WAPE.
- **Matplotlib:** creación y exportación controlada de figuras.
- **Seaborn:** series, distribuciones y mapas de calor.
- **Scikit-learn:** transformadores, pipelines, modelos y métricas.
- **PyYAML:** configuración fuera del código.
- **Joblib:** persistencia futura del pipeline cuando exista un modelo válido.
- **Pytest:** pruebas automatizadas de comportamientos observables.

## Decisiones de calidad

- Una responsabilidad principal por módulo.
- Composición en lugar de una clase o archivo que haga todo.
- Configuración separada de la lógica.
- Objetos `dataclass` para contratos y resultados.
- Errores de dominio con mensajes accionables.
- Copias defensivas antes de limpiar o graficar.
- Registro de transformaciones y artefactos.
- Partición temporal cuando se declara una fecha.
- Ajuste del preprocesamiento solo con entrenamiento.
- Línea base obligatoria antes de recomendar un modelo.

## Uso de inteligencia artificial

Codex se utilizó como apoyo para organizar la arquitectura, redactar código, ejecutar pruebas y revisar la documentación. El estudiante debe leer, ejecutar, explicar y adaptar el contenido antes de entregarlo. La responsabilidad de validar las decisiones y declarar correctamente las limitaciones permanece en el estudiante.
