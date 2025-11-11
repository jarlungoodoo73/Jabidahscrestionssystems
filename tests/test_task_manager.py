"""
Unit Tests for Task Manager

This module contains comprehensive unit tests for the Task and TaskManager
classes. Tests verify that all functionality works correctly and handles
edge cases properly.

Author: Jabidah Systems
Date: 2025-11-11
"""

import unittest
from datetime import datetime
from src.task_manager import Task, TaskManager


class TestTask(unittest.TestCase):
    """
    Test cases for the Task class.
    
    Tests the creation, manipulation, and representation of individual tasks.
    """
    
    def test_task_creation(self):
        """Test that a task is created with correct default values."""
        # Create a simple task
        task = Task(1, "Test Task")
        
        # Verify attributes are set correctly
        self.assertEqual(task.task_id, 1)
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.description, "")
        self.assertEqual(task.priority, "medium")
        self.assertFalse(task.completed)
        self.assertIsNone(task.completed_at)
        self.assertIsInstance(task.created_at, datetime)
    
    def test_task_with_all_parameters(self):
        """Test task creation with all parameters specified."""
        task = Task(
            task_id=2,
            title="Important Task",
            description="This is a detailed description",
            priority="high"
        )
        
        # Verify all parameters are set correctly
        self.assertEqual(task.task_id, 2)
        self.assertEqual(task.title, "Important Task")
        self.assertEqual(task.description, "This is a detailed description")
        self.assertEqual(task.priority, "high")
    
    def test_invalid_priority(self):
        """Test that invalid priority raises ValueError."""
        # Attempt to create task with invalid priority
        with self.assertRaises(ValueError):
            Task(1, "Test", priority="invalid")
    
    def test_mark_complete(self):
        """Test marking a task as complete."""
        task = Task(1, "Test Task")
        
        # Initially not completed
        self.assertFalse(task.completed)
        self.assertIsNone(task.completed_at)
        
        # Mark as complete
        task.mark_complete()
        
        # Verify completion
        self.assertTrue(task.completed)
        self.assertIsInstance(task.completed_at, datetime)
    
    def test_mark_incomplete(self):
        """Test marking a completed task as incomplete."""
        task = Task(1, "Test Task")
        
        # Mark complete then incomplete
        task.mark_complete()
        task.mark_incomplete()
        
        # Verify it's back to incomplete state
        self.assertFalse(task.completed)
        self.assertIsNone(task.completed_at)
    
    def test_update_title(self):
        """Test updating task title."""
        task = Task(1, "Old Title")
        
        # Update title
        task.update(title="New Title")
        
        # Verify title changed
        self.assertEqual(task.title, "New Title")
    
    def test_update_priority(self):
        """Test updating task priority."""
        task = Task(1, "Test", priority="low")
        
        # Update priority
        task.update(priority="high")
        
        # Verify priority changed
        self.assertEqual(task.priority, "high")
    
    def test_update_invalid_priority(self):
        """Test that updating with invalid priority raises ValueError."""
        task = Task(1, "Test")
        
        # Attempt to update with invalid priority
        with self.assertRaises(ValueError):
            task.update(priority="invalid")
    
    def test_to_dict(self):
        """Test conversion of task to dictionary."""
        task = Task(1, "Test Task", "Description", "high")
        
        # Convert to dictionary
        task_dict = task.to_dict()
        
        # Verify dictionary contains correct keys and values
        self.assertEqual(task_dict['task_id'], 1)
        self.assertEqual(task_dict['title'], "Test Task")
        self.assertEqual(task_dict['description'], "Description")
        self.assertEqual(task_dict['priority'], "high")
        self.assertFalse(task_dict['completed'])
        self.assertIsNotNone(task_dict['created_at'])
        self.assertIsNone(task_dict['completed_at'])
    
    def test_str_representation(self):
        """Test string representation of task."""
        task = Task(1, "Test Task", priority="high")
        
        # Get string representation
        task_str = str(task)
        
        # Verify it contains expected information
        self.assertIn("Task #1", task_str)
        self.assertIn("Test Task", task_str)
        self.assertIn("high", task_str)
        self.assertIn("○", task_str)  # Not completed symbol


class TestTaskManager(unittest.TestCase):
    """
    Test cases for the TaskManager class.
    
    Tests the management of multiple tasks including creation, retrieval,
    deletion, and filtering.
    """
    
    def setUp(self):
        """
        Set up a fresh TaskManager for each test.
        
        This method runs before each test to ensure a clean state.
        """
        self.manager = TaskManager()
    
    def test_initial_state(self):
        """Test that a new TaskManager starts empty."""
        # Verify initial state
        self.assertEqual(len(self.manager.tasks), 0)
        self.assertEqual(self.manager.next_id, 1)
    
    def test_create_task(self):
        """Test creating a task through the manager."""
        # Create a task
        task = self.manager.create_task("Test Task")
        
        # Verify task was created and added
        self.assertEqual(len(self.manager.tasks), 1)
        self.assertEqual(task.task_id, 1)
        self.assertEqual(task.title, "Test Task")
    
    def test_create_multiple_tasks(self):
        """Test creating multiple tasks with auto-incrementing IDs."""
        # Create three tasks
        task1 = self.manager.create_task("Task 1")
        task2 = self.manager.create_task("Task 2")
        task3 = self.manager.create_task("Task 3")
        
        # Verify IDs are sequential
        self.assertEqual(task1.task_id, 1)
        self.assertEqual(task2.task_id, 2)
        self.assertEqual(task3.task_id, 3)
        self.assertEqual(len(self.manager.tasks), 3)
    
    def test_create_task_empty_title(self):
        """Test that creating a task with empty title raises ValueError."""
        # Attempt to create task with empty title
        with self.assertRaises(ValueError):
            self.manager.create_task("")
        
        # Verify no task was created
        self.assertEqual(len(self.manager.tasks), 0)
    
    def test_get_task(self):
        """Test retrieving a task by ID."""
        # Create a task
        created_task = self.manager.create_task("Test Task")
        
        # Retrieve it by ID
        retrieved_task = self.manager.get_task(1)
        
        # Verify it's the same task
        self.assertEqual(retrieved_task, created_task)
    
    def test_get_nonexistent_task(self):
        """Test that getting a nonexistent task returns None."""
        # Try to get task that doesn't exist
        task = self.manager.get_task(999)
        
        # Verify None is returned
        self.assertIsNone(task)
    
    def test_delete_task(self):
        """Test deleting a task."""
        # Create a task
        self.manager.create_task("Test Task")
        
        # Verify it exists
        self.assertEqual(len(self.manager.tasks), 1)
        
        # Delete it
        deleted = self.manager.delete_task(1)
        
        # Verify deletion
        self.assertTrue(deleted)
        self.assertEqual(len(self.manager.tasks), 0)
    
    def test_delete_nonexistent_task(self):
        """Test that deleting a nonexistent task returns False."""
        # Try to delete task that doesn't exist
        deleted = self.manager.delete_task(999)
        
        # Verify False is returned
        self.assertFalse(deleted)
    
    def test_list_all_tasks(self):
        """Test listing all tasks."""
        # Create several tasks
        self.manager.create_task("Task 1")
        self.manager.create_task("Task 2")
        self.manager.create_task("Task 3")
        
        # Get all tasks
        tasks = self.manager.list_tasks()
        
        # Verify count
        self.assertEqual(len(tasks), 3)
    
    def test_list_completed_tasks(self):
        """Test filtering tasks by completion status."""
        # Create tasks and complete some
        task1 = self.manager.create_task("Task 1")
        task2 = self.manager.create_task("Task 2")
        task3 = self.manager.create_task("Task 3")
        
        task1.mark_complete()
        task3.mark_complete()
        
        # Get only completed tasks
        completed = self.manager.list_tasks(completed=True)
        
        # Verify only completed tasks returned
        self.assertEqual(len(completed), 2)
        self.assertTrue(all(t.completed for t in completed))
    
    def test_list_pending_tasks(self):
        """Test filtering for pending (incomplete) tasks."""
        # Create tasks and complete some
        task1 = self.manager.create_task("Task 1")
        self.manager.create_task("Task 2")
        task3 = self.manager.create_task("Task 3")
        
        task1.mark_complete()
        
        # Get only pending tasks
        pending = self.manager.list_tasks(completed=False)
        
        # Verify only pending tasks returned
        self.assertEqual(len(pending), 2)
        self.assertTrue(all(not t.completed for t in pending))
    
    def test_list_by_priority(self):
        """Test filtering tasks by priority."""
        # Create tasks with different priorities
        self.manager.create_task("Task 1", priority="high")
        self.manager.create_task("Task 2", priority="low")
        self.manager.create_task("Task 3", priority="high")
        
        # Get only high priority tasks
        high_priority = self.manager.list_tasks(priority="high")
        
        # Verify only high priority tasks returned
        self.assertEqual(len(high_priority), 2)
        self.assertTrue(all(t.priority == "high" for t in high_priority))
    
    def test_get_stats(self):
        """Test getting statistics about tasks."""
        # Create tasks with various states and priorities
        task1 = self.manager.create_task("Task 1", priority="high")
        task2 = self.manager.create_task("Task 2", priority="medium")
        task3 = self.manager.create_task("Task 3", priority="low")
        
        task1.mark_complete()
        
        # Get statistics
        stats = self.manager.get_stats()
        
        # Verify statistics
        self.assertEqual(stats['total'], 3)
        self.assertEqual(stats['completed'], 1)
        self.assertEqual(stats['pending'], 2)
        self.assertEqual(stats['by_priority']['high'], 1)
        self.assertEqual(stats['by_priority']['medium'], 1)
        self.assertEqual(stats['by_priority']['low'], 1)
    
    def test_clear_completed(self):
        """Test clearing all completed tasks."""
        # Create tasks and complete some
        task1 = self.manager.create_task("Task 1")
        self.manager.create_task("Task 2")
        task3 = self.manager.create_task("Task 3")
        
        task1.mark_complete()
        task3.mark_complete()
        
        # Clear completed tasks
        cleared = self.manager.clear_completed()
        
        # Verify correct number cleared and only pending remain
        self.assertEqual(cleared, 2)
        self.assertEqual(len(self.manager.tasks), 1)
        self.assertTrue(all(not t.completed for t in self.manager.tasks))


# Run the tests when this file is executed
if __name__ == '__main__':
    unittest.main()
