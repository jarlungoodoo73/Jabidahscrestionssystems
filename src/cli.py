"""
Command-Line Interface for Task Manager

This module provides a command-line interface to interact with the
Task Management System and Agent Management System. Users can create,
view, update, and delete tasks and agents through simple commands.

Author: Jabidah Systems
Date: 2025-11-11
"""

import sys
from typing import List
from src.task_manager import TaskManager, AgentManager


class CLI:
    """
    Command-Line Interface for the Task Management System.
    
    This class handles user input and provides a text-based menu system
    for interacting with tasks and agents.
    
    Attributes:
        manager (TaskManager): The task manager instance handling all tasks
        agent_manager (AgentManager): The agent manager instance handling all agents
        running (bool): Flag to control the main loop
    """
    
    def __init__(self):
        """Initialize the CLI with new TaskManager and AgentManager instances."""
        # Create a task manager to handle our tasks
        self.manager = TaskManager()
        # Create an agent manager to handle our agents
        self.agent_manager = AgentManager()
        # Flag to control whether the CLI should keep running
        self.running = True
    
    def display_menu(self) -> None:
        """
        Display the main menu options to the user.
        
        Shows all available commands that the user can execute.
        """
        print("\n" + "=" * 50)
        print("Task & Agent Management - Main Menu")
        print("=" * 50)
        print("TASK MANAGEMENT:")
        print("1. Create new task")
        print("2. List all tasks")
        print("3. List pending tasks")
        print("4. List completed tasks")
        print("5. View task details")
        print("6. Mark task as complete")
        print("7. Mark task as incomplete")
        print("8. Update task")
        print("9. Delete task")
        print("10. View task statistics")
        print("11. Clear completed tasks")
        print("\nAGENT MANAGEMENT:")
        print("12. Create new agent")
        print("13. List all agents")
        print("14. View agent details")
        print("15. Assign agent to task")
        print("16. Unassign agent from task")
        print("17. View agent statistics")
        print("18. Monitor all agents")
        print("19. Update agent position")
        print("20. Delete agent")
        print("\n0. Exit")
        print("=" * 50)
    
    def get_input(self, prompt: str, required: bool = True) -> str:
        """
        Get input from the user with optional validation.
        
        Args:
            prompt (str): The prompt message to display
            required (bool): Whether the input is required (non-empty)
        
        Returns:
            str: The user's input
        """
        while True:
            # Get user input
            user_input = input(prompt).strip()
            
            # If input is required, keep asking until we get something
            if required and not user_input:
                print("This field is required. Please try again.")
                continue
            
            return user_input
    
    def create_task_interactive(self) -> None:
        """
        Interactive process to create a new task.
        
        Prompts the user for task details and creates the task.
        """
        print("\n--- Create New Task ---")
        
        # Get task title (required)
        title = self.get_input("Enter task title: ", required=True)
        
        # Get task description (optional)
        description = self.get_input("Enter task description (optional): ", required=False)
        
        # Get priority level with validation
        while True:
            priority = self.get_input("Enter priority (low/medium/high, default: medium): ", required=False)
            
            # Use default if nothing entered
            if not priority:
                priority = "medium"
            
            # Validate priority
            if priority.lower() in ['low', 'medium', 'high']:
                priority = priority.lower()
                break
            else:
                print("Invalid priority. Please enter 'low', 'medium', or 'high'.")
        
        try:
            # Create the task
            task = self.manager.create_task(title, description, priority)
            print(f"\n✓ Task created successfully: {task}")
        except ValueError as e:
            # Handle any validation errors
            print(f"\n✗ Error creating task: {e}")
    
    def list_tasks(self, completed: bool = None) -> None:
        """
        Display a list of tasks with optional filtering.
        
        Args:
            completed (bool, optional): Filter by completion status.
                                       None shows all tasks.
        """
        # Get tasks based on filter
        tasks = self.manager.list_tasks(completed=completed)
        
        # Determine what we're showing
        if completed is None:
            print("\n--- All Tasks ---")
        elif completed:
            print("\n--- Completed Tasks ---")
        else:
            print("\n--- Pending Tasks ---")
        
        # Check if there are any tasks to display
        if not tasks:
            print("No tasks found.")
            return
        
        # Display each task
        for task in tasks:
            print(task)
            # Show description if it exists
            if task.description:
                print(f"    Description: {task.description}")
    
    def view_task_details(self) -> None:
        """
        Display detailed information about a specific task.
        
        Prompts for task ID and shows all task details.
        """
        print("\n--- View Task Details ---")
        
        try:
            # Get task ID from user
            task_id = int(self.get_input("Enter task ID: "))
            
            # Find the task
            task = self.manager.get_task(task_id)
            
            if task:
                # Display full task details
                print(f"\nTask #{task.task_id}")
                print(f"Title: {task.title}")
                print(f"Description: {task.description}")
                print(f"Priority: {task.priority}")
                print(f"Status: {'Completed' if task.completed else 'Pending'}")
                print(f"Created: {task.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
                if task.completed_at:
                    print(f"Completed: {task.completed_at.strftime('%Y-%m-%d %H:%M:%S')}")
            else:
                print(f"\n✗ Task #{task_id} not found.")
        
        except ValueError:
            print("\n✗ Invalid task ID. Please enter a number.")
    
    def mark_task_complete(self) -> None:
        """
        Mark a task as completed.
        
        Prompts for task ID and marks it as complete.
        """
        print("\n--- Mark Task Complete ---")
        
        try:
            # Get task ID from user
            task_id = int(self.get_input("Enter task ID: "))
            
            # Find the task
            task = self.manager.get_task(task_id)
            
            if task:
                # Mark it as complete
                task.mark_complete()
                print(f"\n✓ Task #{task_id} marked as complete.")
            else:
                print(f"\n✗ Task #{task_id} not found.")
        
        except ValueError:
            print("\n✗ Invalid task ID. Please enter a number.")
    
    def mark_task_incomplete(self) -> None:
        """
        Mark a task as incomplete (undo completion).
        
        Prompts for task ID and marks it as incomplete.
        """
        print("\n--- Mark Task Incomplete ---")
        
        try:
            # Get task ID from user
            task_id = int(self.get_input("Enter task ID: "))
            
            # Find the task
            task = self.manager.get_task(task_id)
            
            if task:
                # Mark it as incomplete
                task.mark_incomplete()
                print(f"\n✓ Task #{task_id} marked as incomplete.")
            else:
                print(f"\n✗ Task #{task_id} not found.")
        
        except ValueError:
            print("\n✗ Invalid task ID. Please enter a number.")
    
    def update_task_interactive(self) -> None:
        """
        Interactive process to update an existing task.
        
        Prompts for task ID and which fields to update.
        """
        print("\n--- Update Task ---")
        
        try:
            # Get task ID from user
            task_id = int(self.get_input("Enter task ID: "))
            
            # Find the task
            task = self.manager.get_task(task_id)
            
            if not task:
                print(f"\n✗ Task #{task_id} not found.")
                return
            
            # Show current task details
            print(f"\nCurrent task: {task}")
            
            # Get new values (leave empty to keep current)
            print("\nLeave fields empty to keep current values:")
            
            new_title = self.get_input(f"New title (current: {task.title}): ", required=False)
            new_description = self.get_input(f"New description (current: {task.description}): ", required=False)
            
            # Get new priority with validation
            new_priority = None
            priority_input = self.get_input(f"New priority (current: {task.priority}): ", required=False)
            if priority_input and priority_input.lower() in ['low', 'medium', 'high']:
                new_priority = priority_input.lower()
            elif priority_input:
                print("Invalid priority. Keeping current value.")
            
            # Update the task
            task.update(
                title=new_title if new_title else None,
                description=new_description if new_description else None,
                priority=new_priority
            )
            
            print(f"\n✓ Task updated successfully: {task}")
        
        except ValueError:
            print("\n✗ Invalid input. Please try again.")
    
    def delete_task_interactive(self) -> None:
        """
        Delete a task after confirmation.
        
        Prompts for task ID and confirms before deletion.
        """
        print("\n--- Delete Task ---")
        
        try:
            # Get task ID from user
            task_id = int(self.get_input("Enter task ID: "))
            
            # Find the task to show what will be deleted
            task = self.manager.get_task(task_id)
            
            if not task:
                print(f"\n✗ Task #{task_id} not found.")
                return
            
            # Show task and ask for confirmation
            print(f"\nTask to delete: {task}")
            confirm = self.get_input("Are you sure? (yes/no): ", required=True)
            
            # Only delete if user confirms
            if confirm.lower() in ['yes', 'y']:
                self.manager.delete_task(task_id)
                print(f"\n✓ Task #{task_id} deleted successfully.")
            else:
                print("\n✓ Deletion cancelled.")
        
        except ValueError:
            print("\n✗ Invalid task ID. Please enter a number.")
    
    def show_statistics(self) -> None:
        """
        Display statistics about all tasks.
        
        Shows counts of tasks by various categories.
        """
        print("\n--- Task Statistics ---")
        
        # Get stats from the manager
        stats = self.manager.get_stats()
        
        # Display overall statistics
        print(f"\nTotal tasks: {stats['total']}")
        print(f"Completed: {stats['completed']}")
        print(f"Pending: {stats['pending']}")
        
        # Display breakdown by priority
        print("\nBy Priority:")
        print(f"  High: {stats['by_priority']['high']}")
        print(f"  Medium: {stats['by_priority']['medium']}")
        print(f"  Low: {stats['by_priority']['low']}")
    
    def clear_completed_interactive(self) -> None:
        """
        Clear all completed tasks after confirmation.
        
        Removes all completed tasks from the system.
        """
        print("\n--- Clear Completed Tasks ---")
        
        # Count how many tasks will be removed
        completed_count = len(self.manager.list_tasks(completed=True))
        
        if completed_count == 0:
            print("\nNo completed tasks to clear.")
            return
        
        # Ask for confirmation
        print(f"\nThis will delete {completed_count} completed task(s).")
        confirm = self.get_input("Are you sure? (yes/no): ", required=True)
        
        # Only clear if user confirms
        if confirm.lower() in ['yes', 'y']:
            removed = self.manager.clear_completed()
            print(f"\n✓ Cleared {removed} completed task(s).")
        else:
            print("\n✓ Operation cancelled.")
    
    def create_agent_interactive(self) -> None:
        """
        Interactive process to create a new agent.
        
        Prompts the user for agent details and creates the agent.
        """
        print("\n--- Create New Agent ---")
        
        # Get agent name (required)
        name = self.get_input("Enter agent name: ", required=True)
        
        # Get position with validation
        while True:
            position = self.get_input("Enter position (available/busy/offline, default: available): ", required=False)
            
            # Use default if nothing entered
            if not position:
                position = "available"
            
            # Validate position
            if position.lower() in ['available', 'busy', 'offline']:
                position = position.lower()
                break
            else:
                print("Invalid position. Please enter 'available', 'busy', or 'offline'.")
        
        try:
            # Create the agent
            agent = self.agent_manager.create_agent(name, position)
            print(f"\n✓ Agent created successfully: {agent}")
        except ValueError as e:
            # Handle any validation errors
            print(f"\n✗ Error creating agent: {e}")
    
    def list_agents(self, position: str = None) -> None:
        """
        Display a list of agents with optional filtering.
        
        Args:
            position (str, optional): Filter by position.
                                     None shows all agents.
        """
        # Get agents based on filter
        agents = self.agent_manager.list_agents(position=position)
        
        # Determine what we're showing
        if position is None:
            print("\n--- All Agents ---")
        else:
            print(f"\n--- Agents ({position}) ---")
        
        # Check if there are any agents to display
        if not agents:
            print("No agents found.")
            return
        
        # Display each agent
        for agent in agents:
            print(agent)
            # Show assigned tasks if any
            if len(agent.assigned_task_ids) > 0:
                print(f"    Assigned to tasks: {', '.join(f'#{tid}' for tid in agent.assigned_task_ids)}")
    
    def view_agent_details(self) -> None:
        """
        Display detailed information about a specific agent.
        
        Prompts for agent ID and shows all agent details including assigned tasks.
        """
        print("\n--- View Agent Details ---")
        
        try:
            # Get agent ID from user
            agent_id = int(self.get_input("Enter agent ID: "))
            
            # Find the agent
            agent = self.agent_manager.get_agent(agent_id)
            
            if agent:
                # Display full agent details
                print(f"\nAgent #{agent.agent_id}")
                print(f"Name: {agent.name}")
                print(f"Position: {agent.position}")
                print(f"Created: {agent.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"Assigned Tasks: {len(agent.assigned_task_ids)}")
                
                # Show assigned tasks details
                if len(agent.assigned_task_ids) > 0:
                    print("\nAssigned to:")
                    agent_tasks = self.agent_manager.get_agent_tasks(agent_id, self.manager)
                    for task in agent_tasks:
                        status = "✓" if task.completed else "○"
                        print(f"  [{status}] Task #{task.task_id}: {task.title}")
            else:
                print(f"\n✗ Agent #{agent_id} not found.")
        
        except ValueError:
            print("\n✗ Invalid agent ID. Please enter a number.")
    
    def assign_agent_to_task_interactive(self) -> None:
        """
        Assign an agent to a task.
        
        Prompts for agent ID and task ID and creates the assignment.
        """
        print("\n--- Assign Agent to Task ---")
        
        try:
            # Get agent ID
            agent_id = int(self.get_input("Enter agent ID: "))
            
            # Get task ID
            task_id = int(self.get_input("Enter task ID: "))
            
            # Find the agent and task
            agent = self.agent_manager.get_agent(agent_id)
            task = self.manager.get_task(task_id)
            
            if not agent:
                print(f"\n✗ Agent #{agent_id} not found.")
                return
            
            if not task:
                print(f"\n✗ Task #{task_id} not found.")
                return
            
            # Assign agent to task
            success = self.agent_manager.assign_agent_to_task(agent_id, task)
            
            if success:
                print(f"\n✓ Agent #{agent_id} ({agent.name}) assigned to Task #{task_id} ({task.title})")
            else:
                print(f"\n✗ Failed to assign agent to task.")
        
        except ValueError:
            print("\n✗ Invalid input. Please enter numbers for IDs.")
    
    def unassign_agent_from_task_interactive(self) -> None:
        """
        Unassign an agent from a task.
        
        Prompts for agent ID and task ID and removes the assignment.
        """
        print("\n--- Unassign Agent from Task ---")
        
        try:
            # Get agent ID
            agent_id = int(self.get_input("Enter agent ID: "))
            
            # Get task ID
            task_id = int(self.get_input("Enter task ID: "))
            
            # Find the agent and task
            agent = self.agent_manager.get_agent(agent_id)
            task = self.manager.get_task(task_id)
            
            if not agent:
                print(f"\n✗ Agent #{agent_id} not found.")
                return
            
            if not task:
                print(f"\n✗ Task #{task_id} not found.")
                return
            
            # Unassign agent from task
            success = self.agent_manager.unassign_agent_from_task(agent_id, task)
            
            if success:
                print(f"\n✓ Agent #{agent_id} ({agent.name}) unassigned from Task #{task_id} ({task.title})")
            else:
                print(f"\n✗ Agent was not assigned to this task.")
        
        except ValueError:
            print("\n✗ Invalid input. Please enter numbers for IDs.")
    
    def show_agent_statistics(self) -> None:
        """
        Display statistics about all agents.
        
        Shows counts of agents by various categories.
        """
        print("\n--- Agent Statistics ---")
        
        # Get stats from the manager
        stats = self.agent_manager.get_stats()
        
        # Display overall statistics
        print(f"\nTotal agents: {stats['total']}")
        print(f"Available: {stats['available']}")
        print(f"Busy: {stats['busy']}")
        print(f"Offline: {stats['offline']}")
        print(f"Total task assignments: {stats['total_assignments']}")
    
    def monitor_all_agents_interactive(self) -> None:
        """
        Monitor all agents and their current status.
        
        Displays a comprehensive view of all agents for monitoring purposes.
        """
        print("\n--- Agent Monitoring Dashboard ---")
        
        # Get monitoring data
        monitoring_data = self.agent_manager.monitor_all_agents()
        
        if not monitoring_data:
            print("\nNo agents to monitor.")
            return
        
        # Display monitoring information for each agent
        print(f"\nMonitoring {len(monitoring_data)} agent(s):\n")
        for data in monitoring_data:
            print(f"Agent #{data['agent_id']}: {data['name']}")
            print(f"  Position: {data['position']}")
            print(f"  Tasks Assigned: {data['task_count']}")
            if data['task_count'] > 0:
                print(f"  Task IDs: {', '.join(f'#{tid}' for tid in data['assigned_tasks'])}")
            print()
    
    def update_agent_position_interactive(self) -> None:
        """
        Update an agent's position/status.
        
        Prompts for agent ID and new position.
        """
        print("\n--- Update Agent Position ---")
        
        try:
            # Get agent ID
            agent_id = int(self.get_input("Enter agent ID: "))
            
            # Find the agent
            agent = self.agent_manager.get_agent(agent_id)
            
            if not agent:
                print(f"\n✗ Agent #{agent_id} not found.")
                return
            
            # Show current position
            print(f"\nCurrent position: {agent.position}")
            
            # Get new position with validation
            while True:
                new_position = self.get_input("New position (available/busy/offline): ", required=True)
                
                if new_position.lower() in ['available', 'busy', 'offline']:
                    new_position = new_position.lower()
                    break
                else:
                    print("Invalid position. Please enter 'available', 'busy', or 'offline'.")
            
            # Update position
            agent.update_position(new_position)
            print(f"\n✓ Agent #{agent_id} position updated to '{new_position}'")
        
        except ValueError:
            print("\n✗ Invalid input. Please enter a valid agent ID.")
    
    def delete_agent_interactive(self) -> None:
        """
        Delete an agent after confirmation.
        
        Prompts for agent ID and confirms before deletion.
        """
        print("\n--- Delete Agent ---")
        
        try:
            # Get agent ID from user
            agent_id = int(self.get_input("Enter agent ID: "))
            
            # Find the agent to show what will be deleted
            agent = self.agent_manager.get_agent(agent_id)
            
            if not agent:
                print(f"\n✗ Agent #{agent_id} not found.")
                return
            
            # Show agent and ask for confirmation
            print(f"\nAgent to delete: {agent}")
            if len(agent.assigned_task_ids) > 0:
                print(f"Warning: This agent is assigned to {len(agent.assigned_task_ids)} task(s).")
            confirm = self.get_input("Are you sure? (yes/no): ", required=True)
            
            # Only delete if user confirms
            if confirm.lower() in ['yes', 'y']:
                self.agent_manager.delete_agent(agent_id)
                print(f"\n✓ Agent #{agent_id} deleted successfully.")
            else:
                print("\n✓ Deletion cancelled.")
        
        except ValueError:
            print("\n✗ Invalid agent ID. Please enter a number.")
    
    def run(self) -> None:
        """
        Run the main CLI loop.
        
        Continuously displays the menu and processes user commands
        until the user chooses to exit.
        """
        print("\nWelcome to Jabidah Task & Agent Management System!")
        
        # Main program loop
        while self.running:
            # Show menu to user
            self.display_menu()
            
            # Get user's choice
            choice = self.get_input("\nEnter your choice: ", required=True)
            
            # Process the user's choice
            if choice == "1":
                self.create_task_interactive()
            elif choice == "2":
                self.list_tasks(completed=None)
            elif choice == "3":
                self.list_tasks(completed=False)
            elif choice == "4":
                self.list_tasks(completed=True)
            elif choice == "5":
                self.view_task_details()
            elif choice == "6":
                self.mark_task_complete()
            elif choice == "7":
                self.mark_task_incomplete()
            elif choice == "8":
                self.update_task_interactive()
            elif choice == "9":
                self.delete_task_interactive()
            elif choice == "10":
                self.show_statistics()
            elif choice == "11":
                self.clear_completed_interactive()
            elif choice == "12":
                self.create_agent_interactive()
            elif choice == "13":
                self.list_agents(position=None)
            elif choice == "14":
                self.view_agent_details()
            elif choice == "15":
                self.assign_agent_to_task_interactive()
            elif choice == "16":
                self.unassign_agent_from_task_interactive()
            elif choice == "17":
                self.show_agent_statistics()
            elif choice == "18":
                self.monitor_all_agents_interactive()
            elif choice == "19":
                self.update_agent_position_interactive()
            elif choice == "20":
                self.delete_agent_interactive()
            elif choice == "0":
                # Exit the program
                print("\nThank you for using Jabidah Task & Agent Management System!")
                self.running = False
            else:
                # Invalid choice
                print("\n✗ Invalid choice. Please try again.")


def main():
    """
    Main entry point for the application.
    
    Creates a CLI instance and starts the interactive loop.
    """
    try:
        # Create and run the CLI
        cli = CLI()
        cli.run()
    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        print("\n\nProgram interrupted. Goodbye!")
        sys.exit(0)
    except Exception as e:
        # Handle unexpected errors
        print(f"\n✗ An unexpected error occurred: {e}")
        sys.exit(1)


# This code only runs if this file is executed directly (not imported)
if __name__ == "__main__":
    main()
