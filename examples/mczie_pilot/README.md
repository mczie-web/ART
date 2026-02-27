# McZie Pilot Agents (ART)

Primer grupo piloto de agentes para adopción de ART en McZie.

## Objetivo
Entrenar un conjunto inicial de agentes comerciales que mejoren:
1. calidad de próxima acción,
2. priorización de riesgo,
3. disciplina de seguimiento.

## Grupo piloto (v1)
- **agent-next-action**: propone próxima acción (verbo + owner + fecha).
- **agent-risk-sentinel**: puntúa riesgo comercial (0-100) y explica causa.
- **agent-forecast-keeper**: valida higiene de datos para forecast (monto, etapa, fecha, owner).

## Estructura
- `pilot_agents.yaml`: definición del grupo piloto.
- `opportunities_seed.json`: lote inicial de oportunidades para entrenamiento.
- `train_pilot.py`: bucle inicial con ART (ServerlessBackend) para entrenar recomendaciones.

## Requisitos
- Python 3.11+
- `openpipe-art`
- Variable `WANDB_API_KEY` configurada (si usas ServerlessBackend)

## Ejecución (piloto)
```bash
cd examples/mczie_pilot
python train_pilot.py
```

## Métricas meta (fase 1)
- -25% oportunidades sin próxima acción válida.
- -20% tareas vencidas sin seguimiento.
- +10pp avance de etapa en cuentas at-risk.

## Nota
Este piloto está diseñado para iterar rápido. Antes de producción:
- validar reward con comité comercial,
- fijar dataset de evaluación offline,
- activar aprobación humana obligatoria para acciones externas.
