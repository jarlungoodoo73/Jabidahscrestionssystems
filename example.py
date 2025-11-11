#!/usr/bin/env python3
"""
Example usage of the Task Management System

This script demonstrates how to use the Task and TaskManager classes
programmatically. It creates sample tasks, manipulates them, and displays
the results.

Author: Jabidah Systems
Date: 2025-11-11
"""

from src.task_manager import TaskManager


def main():
    """
    Demonstrate the basic functionality of the Task Management System.
    
    This function shows examples of:
    - Creating tasks with different priorities
    - Marking tasks as complete
    - Listing and filtering tasks
    - Getting statistics
    - Updating and deleting tasks
    """
    print("=" * 60)
    print("Jabidah Task Management System - Example Usage")
    print("=" * 60)
    
    # Create a new task manager instance
    print("\n1. Creating a new Task Manager...")
    manager = TaskManager()
    
    # Create several example tasks
    print("\n2. Creating sample tasks...")
    
    # High priority task
    task1 = manager.create_task(
        title="Fix critical bug in production",
        description="Users are experiencing login issues on the main site",
        priority="high"
    )
    print(f"   Created: {task1}")
    
    # Medium priority task (default)
    task2 = manager.create_task(
        title="Update documentation",
        description="Add examples to the API documentation",
        priority="medium"
    )
    print(f"   Created: {task2}")
    
    # Low priority task
    task3 = manager.create_task(
        title="Refactor old code",
        description="Clean up deprecated methods in utils module",
        priority="low"
    )
    print(f"   Created: {task3}")
    
    # Another task
    task4 = manager.create_task(
        title="Write unit tests",
        description="Add tests for the new authentication module",
        priority="high"
    )
    print(f"   Created: {task4}")
    
    # List all tasks
    print("\n3. Listing all tasks:")
    all_tasks = manager.list_tasks()
    for task in all_tasks:
        print(f"   {task}")
    
    # Mark some tasks as complete
    print("\n4. Completing some tasks...")
    task1.mark_complete()
    print(f"   Marked complete: {task1}")
    task3.mark_complete()
    print(f"   Marked complete: {task3}")
    
    # List pending tasks only
    print("\n5. Listing pending tasks:")
    pending_tasks = manager.list_tasks(completed=False)
    for task in pending_tasks:
        print(f"   {task}")
    
    # List completed tasks only
    print("\n6. Listing completed tasks:")
    completed_tasks = manager.list_tasks(completed=True)
    for task in completed_tasks:
        print(f"   {task}")
    
    # Filter by priority
    print("\n7. Listing high priority tasks:")
    high_priority = manager.list_tasks(priority="high")
    for task in high_priority:
        print(f"   {task}")
    
    # Get statistics
    print("\n8. Task statistics:")
    stats = manager.get_stats()
    print(f"   Total tasks: {stats['total']}")
    print(f"   Completed: {stats['completed']}")
    print(f"   Pending: {stats['pending']}")
    print(f"   High priority: {stats['by_priority']['high']}")
    print(f"   Medium priority: {stats['by_priority']['medium']}")
    print(f"   Low priority: {stats['by_priority']['low']}")
    
    # Update a task
    print("\n9. Updating a task...")
    print(f"   Before: {task2}")
    task2.update(
        title="Update API documentation",
        priority="high"
    )
    print(f"   After: {task2}")
    
    # Delete a task
    print("\n10. Deleting a task...")
    print(f"    Deleting task #{task4.task_id}")
    deleted = manager.delete_task(task4.task_id)
    if deleted:
        print(f"    ✓ Task deleted successfully")
    
    # Show remaining tasks
    print("\n11. Final task list:")
    remaining_tasks = manager.list_tasks()
    for task in remaining_tasks:
        print(f"    {task}")
    
    # Clear completed tasks
    print("\n12. Clearing completed tasks...")
    cleared = manager.clear_completed()
    print(f"    Cleared {cleared} completed task(s)")
    
    # Final statistics
    print("\n13. Final statistics:")
    final_stats = manager.get_stats()
    print(f"    Total tasks remaining: {final_stats['total']}")
    print(f"    Completed: {final_stats['completed']}")
    print(f"    Pending: {final_stats['pending']}")
    
    print("\n" + "=" * 60)
    print("Example completed successfully!")
    print("=" * 60)


# Run the example when this script is executed
if __name__ == "__main__":
    main()
