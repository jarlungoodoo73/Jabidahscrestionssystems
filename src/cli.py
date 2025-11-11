"""
Command-Line Interface for Task Manager

This module provides a command-line interface to interact with the
Task Management System. Users can create, view, update, and delete
tasks through simple commands.

Author: Jabidah Systems
Date: 2025-11-11
"""

import sys
from typing import List
from src.task_manager import TaskManager


class CLI:
    """
    Command-Line Interface for the Task Management System.
    
    This class handles user input and provides a text-based menu system
    for interacting with tasks.
    
    Attributes:
        manager (TaskManager): The task manager instance handling all tasks
        running (bool): Flag to control the main loop
    """
    
    def __init__(self):
        """Initialize the CLI with a new TaskManager instance."""
        # Create a task manager to handle our tasks
        self.manager = TaskManager()
        # Flag to control whether the CLI should keep running
        self.running = True
    
    def display_menu(self) -> None:
        """
        Display the main menu options to the user.
        
        Shows all available commands that the user can execute.
        """
        print("\n" + "=" * 50)
        print("Task Manager - Main Menu")
        print("=" * 50)
        print("1. Create new task")
        print("2. List all tasks")
        print("3. List pending tasks")
        print("4. List completed tasks")
        print("5. View task details")
        print("6. Mark task as complete")
        print("7. Mark task as incomplete")
        print("8. Update task")
        print("9. Delete task")
        print("10. View statistics")
        print("11. Clear completed tasks")
        print("0. Exit")
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
    
    def run(self) -> None:
        """
        Run the main CLI loop.
        
        Continuously displays the menu and processes user commands
        until the user chooses to exit.
        """
        print("\nWelcome to Jabidah Task Management System!")
        
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
            elif choice == "0":
                # Exit the program
                print("\nThank you for using Jabidah Task Management System!")
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
