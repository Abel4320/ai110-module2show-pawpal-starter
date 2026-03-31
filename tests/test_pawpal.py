from pawpal_system import Task, Pet, Priority, TaskType


def test_task_mark_complete():
    task = Task("Walk", 20, Priority.HIGH, TaskType.WALK)
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_pet_add_task():
    pet = Pet("Buddy", "dog", 3)
    assert len(pet.tasks) == 0
    pet.add_task(Task("Walk", 20, Priority.HIGH, TaskType.WALK))
    assert len(pet.tasks) == 1
