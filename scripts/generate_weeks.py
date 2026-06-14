from __future__ import annotations

import datetime as dt
import json

import generate_week as base


WEEK_COUNT = 52


def build_plan(today: dt.date) -> dict:
    previous = json.loads(base.PLAN_JSON.read_text(encoding="utf-8")) if base.PLAN_JSON.exists() else None
    start = base.plan_monday(today)
    if (
        previous
        and previous.get("weekStart") == start.isoformat()
        and len(previous.get("weeks", [])) == WEEK_COUNT
    ):
        return previous

    analysis = base.analyze_previous(previous)
    weeks = []
    for offset in range(WEEK_COUNT):
        week_start = start + dt.timedelta(weeks=offset)
        week = {
            "weekStart": week_start.isoformat(),
            "weekEnd": (week_start + dt.timedelta(days=4)).isoformat(),
            "analysis": analysis["summary"],
            **base.build_mode("normal", week_start, analysis),
        }
        weeks.append(week)
        analysis = base.analyze_previous(week)

    # Keep the first week at the top level so older cached app.js versions still work.
    return {
        "generatedAt": today.isoformat(),
        **weeks[0],
        "weeks": weeks,
    }


def main() -> None:
    base.DATA_DIR.mkdir(exist_ok=True)
    plan = build_plan(dt.date.today())
    base.PLAN_JSON.write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")
    base.DATA_JS.write_text(
        "window.MEAL_PLAN_DATA = " + json.dumps(plan, ensure_ascii=False, indent=2) + ";\n",
        encoding="utf-8",
    )
    print(f"Generated {base.PLAN_JSON}")
    print(f"Generated {base.DATA_JS}")


if __name__ == "__main__":
    main()
