# PawPal+ Project Reflection

## 1. System Design
**Core User Actions:**

1. **Add a Pet**: User enters their pet's information (name, species, age) and their own details (name, available time for pet care).

2. **Manage Care Tasks**: User creates, edits, or removes care tasks for their pet. Each task has a name, duration, priority level, and type (walk, feeding, medication, enrichment, grooming).

3. **Generate Daily Schedule**: User clicks to generate a daily care plan. The system creates a prioritized schedule that fits within the available time and explains why tasks were included or skipped.

**a. Initial design**

My initial UML design included six classes and two enumerations:

**Classes:**

1. **Owner**: Holds owner's name and available time for pet care. Responsible for managing the time constraint and storing a list of pets.

2. **Pet**: Stores pet details (name, species, age). Responsible for maintaining and managing its list of care tasks.

3. **Task**: Represents a single care activity with name, duration, priority, type, and completion status. Responsible for tracking whether it's done and comparing itself to other tasks by priority.

4. **Scheduler**: Takes an Owner and Pet as input. Responsible for running the scheduling algorithm that prioritizes tasks and respects time constraints.

5. **DailyPlan**: Holds the scheduling output—scheduled tasks, skipped tasks, total time used, and explanation text. Responsible for building and displaying the final plan summary.

**Enumerations:**

6. **Priority**: Defines task priority levels (HIGH, MEDIUM, LOW) for sorting.

7. **TaskType**: Defines valid task categories (WALK, FEEDING, MEDICATION, ENRICHMENT, GROOMING).

**Key Relationships:**
- Owner owns one or more Pets (1-to-many)
- Pet has zero or more Tasks (1-to-many)
- Scheduler uses Owner and Pet to create a DailyPlan

**b. Design changes**

Yes, my design changed significantly during implementation. Here are the key changes:

**1. Removed unused import**
- Dropped `from typing import Optional` — it was imported but never used, keeping the code clean.

**2. Task — added `pet_name` field**
- Added `pet_name: str = ""` so that any task appearing in `skipped_tasks` or `scheduled_tasks` carries its parent pet's identity with it. This was necessary because when viewing the final plan, I needed to know which pet each task belonged to.

**3. DailyPlan — three changes**
- Added `owner: Owner` and `pet: Pet` fields — a plan now knows who it belongs to instead of being anonymous. This makes the output more informative.
- Changed `explanation: str` → `explanation: list[str]` — one string entry per scheduling decision. This is easier to populate incrementally during scheduling and easier to test individual decisions.

**4. Scheduler — redesigned around the owner, not a single pet**
- `__init__` now takes only `Owner` (removed the single `pet` parameter). This allows scheduling across all of an owner's pets.
- Added `_time_remaining` — a shared budget counter across all pets so multiple pets don't each see the full time allowance.
- `generate_plan()` now returns `list[DailyPlan]` — one plan per pet instead of a single plan.
- Added `generate_plan_for_pet(_pet)` — schedules one pet at a time against the shared budget.
- `prioritize_tasks(_pet)` now takes a pet explicitly and filters to incomplete tasks only, preventing re-scheduling of `completed=True` tasks.
- Stub parameters prefixed with `_` to silence unused-parameter linter hints.

**Why these changes?**
The original design assumed one pet per owner, but real users often have multiple pets sharing the same time budget. Redesigning the Scheduler to work at the Owner level made the app more realistic and useful.



---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
