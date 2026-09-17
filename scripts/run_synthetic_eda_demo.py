"""Demostración reproducible del flujo EDA sin representar datos empresariales."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from lumina_framework.data import DataProfiler
from lumina_framework.visualization import EDAVisualizer


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "docs" / "evidencia_sintetica"

DISCLAIMER = (
    "Dataset sintético utilizado exclusivamente para validar técnicamente el "
    "funcionamiento del framework. No representa datos de Lúmina Datos "
    "Operativos, Red Comercial Boreal ni resultados empresariales reales."
)


def build_synthetic_dataset(seed: int = 20260916) -> pd.DataFrame:
    """Construye una tabla demostrativa con anomalías controladas."""
    rng = np.random.default_rng(seed)
    periods = 24
    entities_per_period = 3
    row_count = periods * entities_per_period

    period_index = np.repeat(np.arange(periods), entities_per_period)
    entity_index = np.tile(np.arange(entities_per_period), periods)
    category_index = (period_index + entity_index) % 3

    entity_effect = np.take(np.array([0.0, 5.0, -3.0]), entity_index)
    category_effect = np.take(np.array([2.5, -1.5, 4.0]), category_index)
    trend = period_index * 0.45
    noise = rng.normal(loc=0.0, scale=3.2, size=row_count)

    data = pd.DataFrame(
        {
            "fecha_demo": pd.to_datetime(
                np.repeat(
                    pd.date_range("2026-01-05", periods=periods, freq="W-MON"),
                    entities_per_period,
                )
            ),
            "entidad_demo": np.take(
                np.array(["ENTIDAD_DEMO_A", "ENTIDAD_DEMO_B", "ENTIDAD_DEMO_C"]),
                entity_index,
            ),
            "categoria_demo": np.take(
                np.array([
                    "CATEGORIA_DEMO_X",
                    "CATEGORIA_DEMO_Y",
                    "CATEGORIA_DEMO_Z",
                ]),
                category_index,
            ).astype(object),
            "valor_demo": np.round(
                50.0 + entity_effect + category_effect + trend + noise,
                2,
            ),
            "promocion_demo": rng.random(row_count) < 0.3,
        }
    )

    data.loc[[5, 23, 44], "categoria_demo"] = None
    data.loc[[7, 31, 52, 69], "valor_demo"] = np.nan

    duplicated_rows = data.iloc[[1, 10]].copy(deep=True)
    return pd.concat([data, duplicated_rows], ignore_index=True)


def _round_numeric_statistics(
    statistics: dict[str, dict[str, Any]],
) -> dict[str, dict[str, float]]:
    """Redondea la salida numérica para hacerla estable y legible."""
    return {
        column: {
            statistic: round(float(value), 6)
            for statistic, value in column_statistics.items()
        }
        for column, column_statistics in statistics.items()
    }


def build_summary(data: pd.DataFrame, *, seed: int) -> dict[str, Any]:
    """Ejecuta ``DataProfiler`` y serializa sus resultados sin interpretarlos."""
    profile = DataProfiler().profile(data)
    row_count = profile.row_count

    return {
        "warning": DISCLAIMER,
        "seed": seed,
        "shape": {
            "rows": profile.row_count,
            "columns": profile.column_count,
        },
        "columns": [str(column) for column in data.columns],
        "dtypes": profile.dtypes,
        "missing": {
            column: {
                "count": count,
                "percentage": round((count / row_count) * 100, 2)
                if row_count
                else 0.0,
            }
            for column, count in profile.missing_counts.items()
        },
        "exact_duplicates": profile.exact_duplicates,
        "categorical_cardinality": {
            column: profile.unique_counts[column]
            for column in (
                "entidad_demo",
                "categoria_demo",
                "promocion_demo",
            )
        },
        "numeric_statistics": _round_numeric_statistics(
            profile.numeric_statistics
        ),
        "visualizations": [
            "serie_temporal_demo.png",
            "distribucion_demo.png",
            "mapa_calor_demo.png",
        ],
    }


def _add_synthetic_notice(source: Path, destination: Path) -> None:
    """Añade una advertencia visible sin cambiar la API de ``EDAVisualizer``."""
    import matplotlib.pyplot as plt

    image = plt.imread(source)
    figure, axis = plt.subplots(figsize=(10, 6))
    axis.imshow(image)
    axis.axis("off")
    figure.suptitle(
        "DEMOSTRACIÓN SINTÉTICA — NO REPRESENTA DATOS DE LÚMINA",
        color="#9B1C1C",
        fontsize=13,
        fontweight="bold",
    )
    figure.text(
        0.5,
        0.025,
        "Semilla fija y campos *_demo; uso exclusivo para validar el framework.",
        ha="center",
        fontsize=9,
        color="#374151",
    )
    figure.savefig(destination, dpi=160, bbox_inches="tight", facecolor="white")
    plt.close(figure)
    source.unlink()


def _render_markdown(summary: dict[str, Any]) -> str:
    """Construye evidencia legible a partir del mismo resumen JSON."""
    missing_rows = "\n".join(
        f"| `{column}` | `{summary['dtypes'][column]}` | "
        f"{details['count']} | {details['percentage']:.2f}% |"
        for column, details in summary["missing"].items()
    )
    numeric_rows = "\n".join(
        f"| {statistic} | {value} |"
        for statistic, value in summary["numeric_statistics"][
            "valor_demo"
        ].items()
    )
    visualization_rows = "\n".join(
        f"- [`{filename}`]({filename})" for filename in summary["visualizations"]
    )

    return f"""# Evidencia de exploración sintética reproducible

> {summary['warning']}

## Ejecución

- Semilla fija: `{summary['seed']}`.
- Estructura: {summary['shape']['rows']} filas y {summary['shape']['columns']} columnas.
- Duplicados exactos detectados: {summary['exact_duplicates']}.
- La tabla se genera en memoria y se entrega directamente a `DataProfiler` y
  `EDAVisualizer`. No se crea un CSV artificial solo para forzar el uso de
  `DataLoader`; ese componente se valida por separado en las pruebas del framework.

## Estructura y valores faltantes

| Campo demostrativo | Tipo observado | Faltantes | Porcentaje |
|---|---:|---:|---:|
{missing_rows}

## Estadística descriptiva de `valor_demo`

| Estadístico | Resultado |
|---|---:|
{numeric_rows}

Estos resultados solo comprueban que el framework calcula estadísticas descriptivas
sobre un `DataFrame`. No describen ventas, clientes, operaciones ni resultados de
Lúmina o Red Comercial Boreal.

## Visualizaciones generadas con el framework

{visualization_rows}

- La serie temporal demuestra el procesamiento de una fecha y una medida.
- La distribución demuestra la comparación descriptiva por una categoría.
- El mapa de calor demuestra una agregación entre dos dimensiones.

Las preguntas reales de negocio, el esquema fuente, la variable objetivo y el
horizonte predictivo permanecen pendientes hasta recibir datos y definiciones reales.
"""


def run_demo(output_dir: Path, *, seed: int = 20260916) -> dict[str, Any]:
    """Ejecuta el perfilado y las visualizaciones sobre la tabla sintética."""
    output_dir.mkdir(parents=True, exist_ok=True)
    data = build_synthetic_dataset(seed=seed)
    summary = build_summary(data, seed=seed)

    visualizer = EDAVisualizer(output_dir)
    generated_paths = (
        visualizer.plot_time_series(data, "fecha_demo", "valor_demo"),
        visualizer.plot_distribution(data, "valor_demo", "categoria_demo"),
        visualizer.plot_heatmap(
            data,
            row_column="entidad_demo",
            column_column="categoria_demo",
            value_column="valor_demo",
        ),
    )
    destination_paths = tuple(
        output_dir / filename for filename in summary["visualizations"]
    )
    for source, destination in zip(
        generated_paths,
        destination_paths,
        strict=True,
    ):
        _add_synthetic_notice(source, destination)

    (output_dir / "resumen_demo.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (output_dir / "resumen_demo.md").write_text(
        _render_markdown(summary),
        encoding="utf-8",
    )
    return summary


def parse_args() -> argparse.Namespace:
    """Lee opciones mínimas para reproducir la demostración."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directorio donde se escribirá la evidencia.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=20260916,
        help="Semilla de NumPy para reproducir la tabla.",
    )
    return parser.parse_args()


def main() -> None:
    """Punto de entrada de la demostración."""
    args = parse_args()
    summary = run_demo(args.output_dir, seed=args.seed)
    print(DISCLAIMER)
    print(
        "Estructura generada: "
        f"{summary['shape']['rows']} filas x {summary['shape']['columns']} columnas"
    )
    print(f"Duplicados exactos: {summary['exact_duplicates']}")
    print(f"Evidencia guardada en: {args.output_dir.resolve()}")


if __name__ == "__main__":
    main()
