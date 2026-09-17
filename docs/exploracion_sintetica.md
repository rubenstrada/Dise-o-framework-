# Exploración sintética ejecutada con Python

> **Advertencia:** dataset sintético utilizado exclusivamente para validar
> técnicamente el funcionamiento del framework. No representa datos de Lumina
> Datos Operativos, Red Comercial Boreal ni resultados empresariales reales.

Esta página permite revisar en GitHub la secuencia completa entre datos, código y
resultado visual. Las figuras no son capturas dibujadas manualmente. Se crearon al
ejecutar Python sobre el `DataFrame` sintético y se guardaron como PNG para que
GitHub pueda mostrarlas.

**No se utilizó generación de imágenes mediante inteligencia artificial.** Las
gráficas son salidas nativas de Matplotlib y Seaborn.

## Reproducir la exploración

Desde la raíz del repositorio:

```powershell
python scripts/run_synthetic_eda_demo.py
```

El script completo y comentado se encuentra en
[`scripts/run_synthetic_eda_demo.py`](../scripts/run_synthetic_eda_demo.py). La
implementación reutilizada para las gráficas está en
[`src/lumina_framework/visualization/eda.py`](../src/lumina_framework/visualization/eda.py).

## 1. Generación de la tabla

La semilla fija permite obtener la misma estructura, valores faltantes y duplicados
en cada ejecución:

```python
from scripts.run_synthetic_eda_demo import build_synthetic_dataset

data = build_synthetic_dataset(seed=20260916)
print(data.shape)
print(data.columns.tolist())
print(data.dtypes)
```

Pandas conserva los nombres y tipos de los campos dentro del `DataFrame`. NumPy se
utiliza dentro del generador para producir valores reproducibles; no se convierte
toda la tabla en un arreglo que elimine sus etiquetas.

## 2. Perfilado ejecutado

La tabla se entrega al componente real del framework, sin reimplementar manualmente
los cálculos:

```python
from lumina_framework.data import DataProfiler

profile = DataProfiler().profile(data)

print(profile.row_count, profile.column_count)
print(profile.dtypes)
print(profile.missing_counts)
print(profile.exact_duplicates)
print(profile.unique_counts)
print(profile.numeric_statistics)
```

Los valores producidos por esa ejecución se guardan automáticamente en dos formatos:

- [`resumen_demo.json`](evidencia_sintetica/resumen_demo.json), para comprobar la
  estructura calculada por el programa.
- [`resumen_demo.md`](evidencia_sintetica/resumen_demo.md), para leer en GitHub los
  faltantes, porcentajes, duplicados y estadísticos descriptivos.

## 3. Matplotlib y Seaborn

`EDAVisualizer` importa explícitamente ambas librerías:

```python
import matplotlib.pyplot as plt
import seaborn as sns
```

La demostración crea el visualizador y ejecuta sus tres métodos sobre el mismo
`DataFrame` perfilado:

```python
from pathlib import Path

from lumina_framework.visualization import EDAVisualizer

output_dir = Path("docs/evidencia_sintetica")
visualizer = EDAVisualizer(output_dir)

visualizer.plot_time_series(data, "fecha_demo", "valor_demo")
visualizer.plot_distribution(data, "valor_demo", "categoria_demo")
visualizer.plot_heatmap(
    data,
    row_column="entidad_demo",
    column_column="categoria_demo",
    value_column="valor_demo",
)
```

Dentro del visualizador, Seaborn construye las representaciones estadísticas y
Matplotlib controla la figura y su exportación:

```python
sns.lineplot(data=plot_data, x=date_column, y=value_column, marker="o")
sns.histplot(data=plot_data, x=value_column, hue=group_column, kde=True)
sns.heatmap(matrix, annot=True, fmt=".2f", cmap="YlGnBu")

plt.tight_layout()
plt.savefig(path, dpi=160, bbox_inches="tight")
plt.close()
```

| Librería o componente | Uso verificable en esta exploración |
|---|---|
| Pandas | Mantiene la tabla, fechas, categorías, faltantes y duplicados. |
| NumPy | Genera valores reproducibles mediante una semilla fija. |
| `DataProfiler` | Calcula estructura, calidad básica y estadísticos. |
| Seaborn | Construye la serie, el histograma con densidad y el mapa de calor. |
| Matplotlib | Configura, rotula y guarda cada figura como PNG. |

## 4. Salidas generadas por el código

### Serie temporal

![Serie temporal sintética generada con Seaborn y Matplotlib](evidencia_sintetica/serie_temporal_demo.png)

Comprueba técnicamente que el visualizador puede recibir una fecha y una medida. No
representa la evolución de una variable real de Lumina.

### Distribución

![Distribución sintética generada con Seaborn y Matplotlib](evidencia_sintetica/distribucion_demo.png)

Comprueba que el visualizador puede construir un histograma y distinguir grupos
declarados. No demuestra diferencias entre categorías empresariales reales.

### Mapa de calor

![Mapa de calor sintético generado con Seaborn y Matplotlib](evidencia_sintetica/mapa_calor_demo.png)

Comprueba que el visualizador puede agregar una medida entre dos dimensiones. Los
valores y nombres mostrados pertenecen solamente a la demostración.

## Trazabilidad

```text
Semilla fija
    ↓
Pandas DataFrame sintético
    ├─→ DataProfiler → JSON y Markdown
    └─→ EDAVisualizer → Seaborn + Matplotlib → tres PNG
```

Validar esta ejecución demuestra que el software funciona. La validación del esquema,
los patrones y las decisiones del negocio sigue requiriendo la fuente real autorizada.
