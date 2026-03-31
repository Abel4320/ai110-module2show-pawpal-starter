from pawpal_system import Owner, Pet, Task, Priority, TaskType, Scheduler


def main():
    # Create owner
    alice = Owner(name="Alice", time_available=60)

    # Create pets
    buddy = Pet(name="Buddy", species="dog", age=3)
    whiskers = Pet(name="Whiskers", species="cat", age=5)

    # Add tasks to Buddy
    buddy.add_task(Task("Walk", 20, Priority.HIGH, TaskType.WALK))
    buddy.add_task(Task("Feeding", 10, Priority.MEDIUM, TaskType.FEEDING))
    buddy.add_task(Task("Grooming", 30, Priority.LOW, TaskType.GROOMING))

    # Add tasks to Whiskers
    whiskers.add_task(Task("Feeding", 10, Priority.HIGH, TaskType.FEEDING))
    whiskers.add_task(Task("Enrichment", 15, Priority.LOW, TaskType.ENRICHMENT))

    # Register pets with owner
    alice.add_pet(buddy)
    alice.add_pet(whiskers)

    # Generate schedule
    scheduler = Scheduler(alice)
    plans = scheduler.generate_schedule()

    # Print results
    print("=== Today's Schedule ===\n")
    for plan in plans:
        print(plan.get_summary())
        print()


if __name__ == "__main__":
    main()
