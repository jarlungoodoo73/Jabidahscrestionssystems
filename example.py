#!/usr/bin/env python3
"""
Example usage of the Task Management System and Agent Management System

This script demonstrates how to use the Task, TaskManager, Agent, and 
AgentManager classes programmatically. It creates sample tasks and agents,
assigns them, and displays the results.

Author: Jabidah Systems
Date: 2025-11-11
"""

from src.task_manager import TaskManager, AgentManager


def main():
    """
    Demonstrate the basic functionality of the Task and Agent Management Systems.
    
    This function shows examples of:
    - Creating tasks with different priorities
    - Creating agents with different positions
    - Assigning agents to tasks
    - Monitoring agent status
    - Marking tasks as complete
    - Listing and filtering tasks and agents
    - Getting statistics
    - Updating and deleting tasks and agents
    """
    print("=" * 60)
    print("Jabidah Task & Agent Management System - Example Usage")
    print("=" * 60)
    
    # Create a new task manager instance
    print("\n1. Creating Task Manager and Agent Manager...")
    manager = TaskManager()
    agent_manager = AgentManager()
    
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
    
    # Create agents
    print("\n3. Creating sample agents...")
    
    agent1 = agent_manager.create_agent(
        name="Alice Johnson",
        position="available"
    )
    print(f"   Created: {agent1}")
    
    agent2 = agent_manager.create_agent(
        name="Bob Smith",
        position="available"
    )
    print(f"   Created: {agent2}")
    
    agent3 = agent_manager.create_agent(
        name="Charlie Brown",
        position="offline"
    )
    print(f"   Created: {agent3}")
    
    # Assign agents to tasks
    print("\n4. Assigning agents to tasks...")
    agent_manager.assign_agent_to_task(agent1.agent_id, task1)
    print(f"   Assigned {agent1.name} to {task1.title}")
    
    agent_manager.assign_agent_to_task(agent1.agent_id, task4)
    print(f"   Assigned {agent1.name} to {task4.title}")
    
    agent_manager.assign_agent_to_task(agent2.agent_id, task2)
    print(f"   Assigned {agent2.name} to {task2.title}")
    
    # Monitor all agents
    print("\n5. Monitoring all agents:")
    monitoring_data = agent_manager.monitor_all_agents()
    for data in monitoring_data:
        print(f"   Agent #{data['agent_id']}: {data['name']} - Position: {data['position']}, Tasks: {data['task_count']}")
    
    # List all tasks
    print("\n6. Listing all tasks:")
    all_tasks = manager.list_tasks()
    for task in all_tasks:
        print(f"   {task}")
    
    # Mark some tasks as complete
    print("\n7. Completing some tasks...")
    task1.mark_complete()
    print(f"   Marked complete: {task1}")
    task3.mark_complete()
    print(f"   Marked complete: {task3}")
    
    # List pending tasks only
    print("\n8. Listing pending tasks:")
    pending_tasks = manager.list_tasks(completed=False)
    for task in pending_tasks:
        print(f"   {task}")
    
    # List completed tasks only
    print("\n9. Listing completed tasks:")
    completed_tasks = manager.list_tasks(completed=True)
    for task in completed_tasks:
        print(f"   {task}")
    
    # Filter by priority
    print("\n10. Listing high priority tasks:")
    high_priority = manager.list_tasks(priority="high")
    for task in high_priority:
        print(f"   {task}")
    
    # Get task statistics
    print("\n11. Task statistics:")
    stats = manager.get_stats()
    print(f"   Total tasks: {stats['total']}")
    print(f"   Completed: {stats['completed']}")
    print(f"   Pending: {stats['pending']}")
    print(f"   High priority: {stats['by_priority']['high']}")
    print(f"   Medium priority: {stats['by_priority']['medium']}")
    print(f"   Low priority: {stats['by_priority']['low']}")
    
    # Get agent statistics
    print("\n12. Agent statistics:")
    agent_stats = agent_manager.get_stats()
    print(f"   Total agents: {agent_stats['total']}")
    print(f"   Available: {agent_stats['available']}")
    print(f"   Busy: {agent_stats['busy']}")
    print(f"   Offline: {agent_stats['offline']}")
    print(f"   Total assignments: {agent_stats['total_assignments']}")
    
    # View agent's assigned tasks
    print("\n13. Viewing Agent 1's assigned tasks:")
    agent_tasks = agent_manager.get_agent_tasks(agent1.agent_id, manager)
    for task in agent_tasks:
        print(f"   {task}")
    
    # Update a task
    print("\n14. Updating a task...")
    print(f"   Before: {task2}")
    task2.update(
        title="Update API documentation",
        priority="high"
    )
    print(f"   After: {task2}")
    
    # Update agent position
    print("\n15. Updating agent position...")
    print(f"   Before: {agent3}")
    agent3.update_position("available")
    print(f"   After: {agent3}")
    
    # Delete a task
    print("\n16. Deleting a task...")
    print(f"    Deleting task #{task4.task_id}")
    deleted = manager.delete_task(task4.task_id)
    if deleted:
        print(f"    ✓ Task deleted successfully")
    
    # Show remaining tasks
    print("\n17. Final task list:")
    remaining_tasks = manager.list_tasks()
    for task in remaining_tasks:
        print(f"    {task}")
    
    # Show all agents
    print("\n18. Final agent list:")
    all_agents = agent_manager.list_agents()
    for agent in all_agents:
        print(f"    {agent}")
    
    # Clear completed tasks
    print("\n19. Clearing completed tasks...")
    cleared = manager.clear_completed()
    print(f"    Cleared {cleared} completed task(s)")
    
    # Final statistics
    print("\n20. Final task and agent statistics:")
    final_stats = manager.get_stats()
    print(f"    Tasks:")
    print(f"      Total tasks remaining: {final_stats['total']}")
    print(f"      Completed: {final_stats['completed']}")
    print(f"      Pending: {final_stats['pending']}")
    
    final_agent_stats = agent_manager.get_stats()
    print(f"    Agents:")
    print(f"      Total agents: {final_agent_stats['total']}")
    print(f"      Available: {final_agent_stats['available']}")
    print(f"      Busy: {final_agent_stats['busy']}")
    print(f"      Offline: {final_agent_stats['offline']}")
    
    print("\n" + "=" * 60)
    print("Example completed successfully!")
    print("=" * 60)


# Run the example when this script is executed
if __name__ == "__main__":
    main()
