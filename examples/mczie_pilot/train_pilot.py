import asyncio
import json
from datetime import datetime
from pathlib import Path

import art
from art.serverless.backend import ServerlessBackend

BASE_MODEL = "OpenPipe/Qwen3-14B-Instruct"
TRAIN_STEPS = 5
ROLLOUTS_PER_STEP = 3

SYSTEM_PROMPT = (
    "Eres un agente comercial B2B. Devuelve JSON con: next_action, owner, due_date, "
    "risk_score (0-100), data_gaps[]. Sin texto adicional."
)


def load_seed() -> list[dict]:
    p = Path(__file__).parent / "opportunities_seed.json"
    return json.loads(p.read_text())


def score_output(raw: str) -> float:
    """Reward simple de arranque para el piloto.
    Ajustar en iteraciones siguientes con feedback real del equipo comercial.
    """
    reward = 0.0
    text = (raw or "").lower()
    if "next_action" in text:
        reward += 1.0
    if "owner" in text:
        reward += 1.0
    if "due_date" in text:
        reward += 1.0
    if "risk_score" in text:
        reward += 0.5
    if "data_gaps" in text:
        reward += 0.5
    if len(text) < 30:
        reward -= 1.0
    return reward


async def rollout(model: art.TrainableModel, opportunity: dict) -> art.Trajectory:
    traj = art.Trajectory(
        messages_and_choices=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": json.dumps(opportunity, ensure_ascii=False),
            },
        ],
        reward=0.0,
    )

    choice = (
        await model.openai_client().chat.completions.create(
            model=model.inference_model_name,
            messages=traj.messages(),
            max_completion_tokens=220,
            timeout=60,
        )
    ).choices[0]

    output = choice.message.content or ""
    traj.messages_and_choices.append(choice)
    traj.reward = score_output(output)
    return traj.finish()


async def main() -> None:
    seeds = load_seed()

    model = art.TrainableModel(
        name=f"mczie-pilot-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}",
        project="mczie-sales-pilot",
        base_model=BASE_MODEL,
    )

    backend = ServerlessBackend()
    await model.register(backend)

    for _ in range(await model.get_step(), TRAIN_STEPS):
        groups = await art.gather_trajectory_groups(
            [
                art.TrajectoryGroup(
                    rollout(model, seeds[i % len(seeds)]) for i in range(ROLLOUTS_PER_STEP)
                )
            ]
        )
        result = await backend.train(model, groups)
        await model.log(groups, metrics=result.metrics, step=result.step, split="train")
        print(f"Step {result.step} done")


if __name__ == "__main__":
    asyncio.run(main())
