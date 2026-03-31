# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Smarter Scheduling

PawPal+ includes several features that make the scheduler more intelligent and flexible:

### Task Sorting
Tasks can be sorted before scheduling to control which ones get prioritized:
- **By priority** — HIGH tasks are always scheduled before MEDIUM and LOW
- **By duration** — shorter tasks are preferred when time is limited, fitting more tasks into the budget
- **By scheduled time** — tasks with a set `HH:MM` start time are ordered chronologically; unscheduled tasks appear last

### Filtering
Any task list can be filtered to narrow down what's displayed or scheduled:
- **By status** — show only completed or only pending tasks
- **By type** — isolate tasks of a specific category (e.g. MEDICATION, WALK)
- **By pet** — view tasks belonging to a single pet from a cross-pet task list

### Recurring Tasks
Tasks support a `frequency` field (`"once"`, `"daily"`, `"weekly"`). When a recurring task is marked complete via `pet.complete_task()`, the system automatically creates the next occurrence with an updated due date:
- Daily tasks roll forward by 1 day
- Weekly tasks roll forward by 7 days

### Conflict Detection
`Scheduler.detect_conflicts()` checks for problems before generating a schedule and returns plain-English warning strings:
- Total task time across all pets exceeds the owner's available time
- HIGH priority tasks alone exceed the time budget (flags critical tasks at risk)
- Two tasks from different pets have overlapping scheduled times

## Testing PawPal+

### Run the tests

```bash
python -m pytest tests/test_pawpal.py -v
```

### What the tests cover

| Area | Tests | What's verified |
|---|---|---|
| Core behavior | 2 | Task completion, adding tasks to a pet |
| Sorting | 5 | `sort_by_priority` returns HIGH before LOW; `sort_by_time` returns shortest first; neither mutates the original list |
| Recurring tasks | 6 | Daily tasks roll forward 1 day, weekly tasks roll forward 7 days; `"once"` tasks do not create a next occurrence; tasks without a due date are handled safely |
| Conflict detection | 5 | Budget overrun, HIGH-only overrun, cross-pet time overlap, and empty pet edge cases all produce correct warnings or empty results |

### Confidence level

★★★★☆ (4/5)

18 tests pass covering the core scheduling behaviors, sorting, recurrence, and conflict detection. The missing star reflects areas not yet tested: the Streamlit UI layer, `generate_schedule()` end-to-end across multiple pets, and edge cases like duplicate task names or zero-duration tasks.

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.
