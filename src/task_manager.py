"""
Task Manager Module

This module provides a Task Management System for organizing and tracking tasks.
It includes functionality for creating, updating, deleting, and listing tasks.

Author: Jabidah Systems
Date: 2025-11-11
"""

from datetime import datetime
from typing import List, Optional, Dict


class Task:
    """
    Represents a single task in the system.
    
    This class encapsulates all the information about a task including its
    title, description, priority level, and completion status.
    
    Attributes:
        task_id (int): Unique identifier for the task
        title (str): Short title of the task
        description (str): Detailed description of what needs to be done
        priority (str): Priority level - 'low', 'medium', or 'high'
        completed (bool): Whether the task has been completed
        created_at (datetime): Timestamp when the task was created
        completed_at (Optional[datetime]): Timestamp when task was completed, None if not completed
    """
    
    def __init__(self, task_id: int, title: str, description: str = "", priority: str = "medium"):
        """
        Initialize a new Task object.
        
        Args:
            task_id (int): Unique identifier for this task
            title (str): The title/name of the task
            description (str, optional): Detailed description. Defaults to empty string.
            priority (str, optional): Priority level ('low', 'medium', 'high'). Defaults to 'medium'.
        
        Raises:
            ValueError: If priority is not one of the valid options
        """
        # Validate that priority is one of the allowed values
        valid_priorities = ['low', 'medium', 'high']
        if priority not in valid_priorities:
            raise ValueError(f"Priority must be one of {valid_priorities}")
        
        # Initialize task attributes
        self.task_id = task_id
        self.title = title
        self.description = description
        self.priority = priority
        self.completed = False
        self.created_at = datetime.now()
        self.completed_at: Optional[datetime] = None
    
    def mark_complete(self) -> None:
        """
        Mark this task as completed.
        
        Sets the completed flag to True and records the completion timestamp.
        If the task is already completed, this method has no effect.
        """
        if not self.completed:
            self.completed = True
            self.completed_at = datetime.now()
    
    def mark_incomplete(self) -> None:
        """
        Mark this task as incomplete (undo completion).
        
        Sets the completed flag to False and clears the completion timestamp.
        """
        self.completed = False
        self.completed_at = None
    
    def update(self, title: Optional[str] = None, description: Optional[str] = None, 
               priority: Optional[str] = None) -> None:
        """
        Update task attributes.
        
        Allows updating one or more task attributes. Only provided arguments
        will be updated; None values are ignored.
        
        Args:
            title (Optional[str]): New title for the task
            description (Optional[str]): New description for the task
            priority (Optional[str]): New priority level
        
        Raises:
            ValueError: If priority is provided but not valid
        """
        # Update title if provided
        if title is not None:
            self.title = title
        
        # Update description if provided
        if description is not None:
            self.description = description
        
        # Update priority if provided (with validation)
        if priority is not None:
            valid_priorities = ['low', 'medium', 'high']
            if priority not in valid_priorities:
                raise ValueError(f"Priority must be one of {valid_priorities}")
            self.priority = priority
    
    def to_dict(self) -> Dict:
        """
        Convert task to a dictionary representation.
        
        Useful for serialization or API responses.
        
        Returns:
            Dict: Dictionary containing all task attributes
        """
        return {
            'task_id': self.task_id,
            'title': self.title,
            'description': self.description,
            'priority': self.priority,
            'completed': self.completed,
            'created_at': self.created_at.isoformat(),
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }
    
    def __str__(self) -> str:
        """
        Return a human-readable string representation of the task.
        
        Returns:
            str: Formatted string showing task details
        """
        status = "✓" if self.completed else "○"
        return f"[{status}] Task #{self.task_id}: {self.title} (Priority: {self.priority})"
    
    def __repr__(self) -> str:
        """
        Return a detailed representation of the task for debugging.
        
        Returns:
            str: String representation including all task attributes
        """
        return f"Task(id={self.task_id}, title='{self.title}', priority='{self.priority}', completed={self.completed})"


class TaskManager:
    """
    Manages a collection of tasks.
    
    This class provides methods to create, read, update, and delete tasks.
    It maintains a list of tasks and provides various ways to query and
    manipulate them.
    
    Attributes:
        tasks (List[Task]): List of all tasks in the system
        next_id (int): Counter for generating unique task IDs
    """
    
    def __init__(self):
        """Initialize a new TaskManager with an empty task list."""
        # List to store all tasks
        self.tasks: List[Task] = []
        # Counter for assigning unique IDs to new tasks
        self.next_id = 1
    
    def create_task(self, title: str, description: str = "", priority: str = "medium") -> Task:
        """
        Create a new task and add it to the manager.
        
        Args:
            title (str): Title of the new task
            description (str, optional): Task description. Defaults to empty string.
            priority (str, optional): Priority level. Defaults to 'medium'.
        
        Returns:
            Task: The newly created task object
        
        Raises:
            ValueError: If title is empty or priority is invalid
        """
        # Validate that title is not empty
        if not title or not title.strip():
            raise ValueError("Task title cannot be empty")
        
        # Create the new task with auto-incremented ID
        task = Task(self.next_id, title, description, priority)
        
        # Add task to our collection
        self.tasks.append(task)
        
        # Increment ID counter for next task
        self.next_id += 1
        
        return task
    
    def get_task(self, task_id: int) -> Optional[Task]:
        """
        Retrieve a task by its ID.
        
        Args:
            task_id (int): The ID of the task to retrieve
        
        Returns:
            Optional[Task]: The task if found, None otherwise
        """
        # Search through all tasks to find matching ID
        for task in self.tasks:
            if task.task_id == task_id:
                return task
        
        # Return None if no task with this ID exists
        return None
    
    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task by its ID.
        
        Args:
            task_id (int): The ID of the task to delete
        
        Returns:
            bool: True if task was deleted, False if task was not found
        """
        # Find the task with matching ID
        task = self.get_task(task_id)
        
        # If task exists, remove it from the list
        if task:
            self.tasks.remove(task)
            return True
        
        # Task not found
        return False
    
    def list_tasks(self, completed: Optional[bool] = None, priority: Optional[str] = None) -> List[Task]:
        """
        List tasks with optional filtering.
        
        Args:
            completed (Optional[bool]): Filter by completion status. 
                                       None returns all tasks.
            priority (Optional[str]): Filter by priority level.
                                     None returns all priorities.
        
        Returns:
            List[Task]: List of tasks matching the filter criteria
        """
        # Start with all tasks
        filtered_tasks = self.tasks.copy()
        
        # Filter by completion status if specified
        if completed is not None:
            filtered_tasks = [t for t in filtered_tasks if t.completed == completed]
        
        # Filter by priority if specified
        if priority is not None:
            filtered_tasks = [t for t in filtered_tasks if t.priority == priority]
        
        return filtered_tasks
    
    def get_stats(self) -> Dict:
        """
        Get statistics about the tasks.
        
        Returns:
            Dict: Dictionary containing various statistics:
                - total: Total number of tasks
                - completed: Number of completed tasks
                - pending: Number of pending tasks
                - by_priority: Count of tasks for each priority level
        """
        # Calculate total counts
        total = len(self.tasks)
        completed = sum(1 for t in self.tasks if t.completed)
        pending = total - completed
        
        # Count tasks by priority level
        priority_counts = {
            'low': sum(1 for t in self.tasks if t.priority == 'low'),
            'medium': sum(1 for t in self.tasks if t.priority == 'medium'),
            'high': sum(1 for t in self.tasks if t.priority == 'high')
        }
        
        return {
            'total': total,
            'completed': completed,
            'pending': pending,
            'by_priority': priority_counts
        }
    
    def clear_completed(self) -> int:
        """
        Remove all completed tasks from the manager.
        
        Returns:
            int: Number of tasks that were removed
        """
        # Get list of completed tasks
        completed_tasks = [t for t in self.tasks if t.completed]
        
        # Remove each completed task
        for task in completed_tasks:
            self.tasks.remove(task)
        
        # Return count of removed tasks
        return len(completed_tasks)
