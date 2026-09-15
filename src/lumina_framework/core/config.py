"""Configuración general y comprobación de preparación."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

from lumina_framework.core.contracts import (
    DatasetContract,
    ReadinessIssue,
    ReadinessResult,
)


@dataclass(frozen=True)
class FrameworkConfig:
    """Opciones independientes del esquema de un cliente."""

    source_path: Path | None = None
    output_dir: Path = Path("artifacts")


class ReadinessChecker:
    """Detecta información faltante sin inventar supuestos."""

    def check(
        self,
        config: FrameworkConfig,
        contract: DatasetContract,
    ) -> ReadinessResult:
        """Devuelve todos los bloqueos observables antes de ejecutar."""
        issues: list[ReadinessIssue] = []
        if config.source_path is None:
            issues.append(
                ReadinessIssue("missing_source", "Falta la fuente de datos.")
            )
        if not contract.columns:
            issues.append(
                ReadinessIssue(
                    "missing_columns",
                    "Falta el diccionario de columnas validado por el cliente.",
                )
            )
        if contract.target_column is None:
            issues.append(
                ReadinessIssue(
                    "missing_target",
                    "Falta definir la variable objetivo y su uso de negocio.",
                )
            )
        if contract.prediction_horizon is None:
            issues.append(
                ReadinessIssue(
                    "missing_prediction_horizon",
                    "Falta confirmar el horizonte de predicción.",
                )
            )
        return ReadinessResult(blockers=tuple(issues))


def load_yaml_configuration(
    path: Path,
) -> tuple[FrameworkConfig, DatasetContract]:
    """Carga configuración y contrato sin completar definiciones ausentes."""
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    dataset = raw.get("dataset") or {}
    source_value = raw.get("source_path")
    config = FrameworkConfig(
        source_path=None if source_value is None else Path(source_value),
        output_dir=Path(raw.get("output_dir", "artifacts")),
    )
    contract = DatasetContract(
        table_name=dataset.get("table_name"),
        columns=tuple(dataset.get("columns") or ()),
        identifier_columns=tuple(dataset.get("identifier_columns") or ()),
        date_column=dataset.get("date_column"),
        target_column=dataset.get("target_column"),
        prediction_horizon=dataset.get("prediction_horizon"),
        numeric_features=tuple(dataset.get("numeric_features") or ()),
        categorical_features=tuple(dataset.get("categorical_features") or ()),
    )
    return config, contract
