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
from src.task_manager import Task, TaskManager, Agent, AgentManager


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


class TestAgent(unittest.TestCase):
    """
    Test cases for the Agent class.
    
    Tests the creation, manipulation, and representation of individual agents.
    """
    
    def test_agent_creation(self):
        """Test that an agent is created with correct default values."""
        # Create a simple agent
        agent = Agent(1, "John Doe")
        
        # Verify attributes are set correctly
        self.assertEqual(agent.agent_id, 1)
        self.assertEqual(agent.name, "John Doe")
        self.assertEqual(agent.position, "available")
        self.assertEqual(len(agent.assigned_task_ids), 0)
        self.assertIsInstance(agent.created_at, datetime)
    
    def test_agent_with_all_parameters(self):
        """Test agent creation with all parameters specified."""
        agent = Agent(
            agent_id=2,
            name="Jane Smith",
            position="busy"
        )
        
        # Verify all parameters are set correctly
        self.assertEqual(agent.agent_id, 2)
        self.assertEqual(agent.name, "Jane Smith")
        self.assertEqual(agent.position, "busy")
    
    def test_invalid_position(self):
        """Test that invalid position raises ValueError."""
        # Attempt to create agent with invalid position
        with self.assertRaises(ValueError):
            Agent(1, "Test", position="invalid")
    
    def test_assign_task(self):
        """Test assigning a task to an agent."""
        agent = Agent(1, "John Doe")
        
        # Initially no tasks
        self.assertEqual(len(agent.assigned_task_ids), 0)
        self.assertEqual(agent.position, "available")
        
        # Assign a task
        agent.assign_task(101)
        
        # Verify task is assigned and position changes
        self.assertIn(101, agent.assigned_task_ids)
        self.assertEqual(len(agent.assigned_task_ids), 1)
        self.assertEqual(agent.position, "busy")
    
    def test_unassign_task(self):
        """Test unassigning a task from an agent."""
        agent = Agent(1, "John Doe")
        
        # Assign then unassign
        agent.assign_task(101)
        success = agent.unassign_task(101)
        
        # Verify task is unassigned and position changes back
        self.assertTrue(success)
        self.assertNotIn(101, agent.assigned_task_ids)
        self.assertEqual(len(agent.assigned_task_ids), 0)
        self.assertEqual(agent.position, "available")
    
    def test_unassign_nonexistent_task(self):
        """Test that unassigning a non-assigned task returns False."""
        agent = Agent(1, "John Doe")
        
        # Try to unassign task that was never assigned
        success = agent.unassign_task(999)
        
        # Verify False is returned
        self.assertFalse(success)
    
    def test_update_position(self):
        """Test updating agent position."""
        agent = Agent(1, "John Doe", position="available")
        
        # Update position
        agent.update_position("offline")
        
        # Verify position changed
        self.assertEqual(agent.position, "offline")
    
    def test_update_invalid_position(self):
        """Test that updating with invalid position raises ValueError."""
        agent = Agent(1, "John Doe")
        
        # Attempt to update with invalid position
        with self.assertRaises(ValueError):
            agent.update_position("invalid")
    
    def test_to_dict(self):
        """Test conversion of agent to dictionary."""
        agent = Agent(1, "John Doe", "busy")
        agent.assign_task(101)
        agent.assign_task(102)
        
        # Convert to dictionary
        agent_dict = agent.to_dict()
        
        # Verify dictionary contains correct keys and values
        self.assertEqual(agent_dict['agent_id'], 1)
        self.assertEqual(agent_dict['name'], "John Doe")
        self.assertEqual(agent_dict['position'], "busy")
        self.assertEqual(agent_dict['task_count'], 2)
        self.assertIn(101, agent_dict['assigned_task_ids'])
        self.assertIn(102, agent_dict['assigned_task_ids'])
        self.assertIsNotNone(agent_dict['created_at'])
    
    def test_str_representation(self):
        """Test string representation of agent."""
        agent = Agent(1, "John Doe", position="available")
        agent.assign_task(101)
        
        # Get string representation
        agent_str = str(agent)
        
        # Verify it contains expected information
        self.assertIn("Agent #1", agent_str)
        self.assertIn("John Doe", agent_str)
        self.assertIn("busy", agent_str)  # Position changes to busy when task is assigned
        self.assertIn("Tasks: 1", agent_str)


class TestAgentManager(unittest.TestCase):
    """
    Test cases for the AgentManager class.
    
    Tests the management of multiple agents including creation, retrieval,
    deletion, and task assignments.
    """
    
    def setUp(self):
        """
        Set up fresh managers for each test.
        
        This method runs before each test to ensure a clean state.
        """
        self.agent_manager = AgentManager()
        self.task_manager = TaskManager()
    
    def test_initial_state(self):
        """Test that a new AgentManager starts empty."""
        # Verify initial state
        self.assertEqual(len(self.agent_manager.agents), 0)
        self.assertEqual(self.agent_manager.next_id, 1)
    
    def test_create_agent(self):
        """Test creating an agent through the manager."""
        # Create an agent
        agent = self.agent_manager.create_agent("John Doe")
        
        # Verify agent was created and added
        self.assertEqual(len(self.agent_manager.agents), 1)
        self.assertEqual(agent.agent_id, 1)
        self.assertEqual(agent.name, "John Doe")
    
    def test_create_multiple_agents(self):
        """Test creating multiple agents with auto-incrementing IDs."""
        # Create three agents
        agent1 = self.agent_manager.create_agent("Agent 1")
        agent2 = self.agent_manager.create_agent("Agent 2")
        agent3 = self.agent_manager.create_agent("Agent 3")
        
        # Verify IDs are sequential
        self.assertEqual(agent1.agent_id, 1)
        self.assertEqual(agent2.agent_id, 2)
        self.assertEqual(agent3.agent_id, 3)
        self.assertEqual(len(self.agent_manager.agents), 3)
    
    def test_create_agent_empty_name(self):
        """Test that creating an agent with empty name raises ValueError."""
        # Attempt to create agent with empty name
        with self.assertRaises(ValueError):
            self.agent_manager.create_agent("")
        
        # Verify no agent was created
        self.assertEqual(len(self.agent_manager.agents), 0)
    
    def test_get_agent(self):
        """Test retrieving an agent by ID."""
        # Create an agent
        created_agent = self.agent_manager.create_agent("John Doe")
        
        # Retrieve it by ID
        retrieved_agent = self.agent_manager.get_agent(1)
        
        # Verify it's the same agent
        self.assertEqual(retrieved_agent, created_agent)
    
    def test_get_nonexistent_agent(self):
        """Test that getting a nonexistent agent returns None."""
        # Try to get agent that doesn't exist
        agent = self.agent_manager.get_agent(999)
        
        # Verify None is returned
        self.assertIsNone(agent)
    
    def test_delete_agent(self):
        """Test deleting an agent."""
        # Create an agent
        self.agent_manager.create_agent("John Doe")
        
        # Verify it exists
        self.assertEqual(len(self.agent_manager.agents), 1)
        
        # Delete it
        deleted = self.agent_manager.delete_agent(1)
        
        # Verify deletion
        self.assertTrue(deleted)
        self.assertEqual(len(self.agent_manager.agents), 0)
    
    def test_delete_nonexistent_agent(self):
        """Test that deleting a nonexistent agent returns False."""
        # Try to delete agent that doesn't exist
        deleted = self.agent_manager.delete_agent(999)
        
        # Verify False is returned
        self.assertFalse(deleted)
    
    def test_list_all_agents(self):
        """Test listing all agents."""
        # Create several agents
        self.agent_manager.create_agent("Agent 1")
        self.agent_manager.create_agent("Agent 2")
        self.agent_manager.create_agent("Agent 3")
        
        # Get all agents
        agents = self.agent_manager.list_agents()
        
        # Verify count
        self.assertEqual(len(agents), 3)
    
    def test_list_by_position(self):
        """Test filtering agents by position."""
        # Create agents with different positions
        self.agent_manager.create_agent("Agent 1", position="available")
        self.agent_manager.create_agent("Agent 2", position="busy")
        self.agent_manager.create_agent("Agent 3", position="available")
        
        # Get only available agents
        available_agents = self.agent_manager.list_agents(position="available")
        
        # Verify only available agents returned
        self.assertEqual(len(available_agents), 2)
        self.assertTrue(all(a.position == "available" for a in available_agents))
    
    def test_assign_agent_to_task(self):
        """Test assigning an agent to a task."""
        # Create an agent and a task
        agent = self.agent_manager.create_agent("John Doe")
        task = self.task_manager.create_task("Test Task")
        
        # Assign agent to task
        success = self.agent_manager.assign_agent_to_task(agent.agent_id, task)
        
        # Verify assignment
        self.assertTrue(success)
        self.assertIn(task.task_id, agent.assigned_task_ids)
        self.assertIn(agent.agent_id, task.assigned_agents)
    
    def test_assign_nonexistent_agent(self):
        """Test that assigning nonexistent agent returns False."""
        # Create a task but no agent
        task = self.task_manager.create_task("Test Task")
        
        # Try to assign nonexistent agent
        success = self.agent_manager.assign_agent_to_task(999, task)
        
        # Verify failure
        self.assertFalse(success)
    
    def test_unassign_agent_from_task(self):
        """Test unassigning an agent from a task."""
        # Create and assign
        agent = self.agent_manager.create_agent("John Doe")
        task = self.task_manager.create_task("Test Task")
        self.agent_manager.assign_agent_to_task(agent.agent_id, task)
        
        # Unassign
        success = self.agent_manager.unassign_agent_from_task(agent.agent_id, task)
        
        # Verify unassignment
        self.assertTrue(success)
        self.assertNotIn(task.task_id, agent.assigned_task_ids)
        self.assertNotIn(agent.agent_id, task.assigned_agents)
    
    def test_get_agent_tasks(self):
        """Test getting all tasks assigned to an agent."""
        # Create an agent and multiple tasks
        agent = self.agent_manager.create_agent("John Doe")
        task1 = self.task_manager.create_task("Task 1")
        task2 = self.task_manager.create_task("Task 2")
        task3 = self.task_manager.create_task("Task 3")
        
        # Assign two tasks to the agent
        self.agent_manager.assign_agent_to_task(agent.agent_id, task1)
        self.agent_manager.assign_agent_to_task(agent.agent_id, task3)
        
        # Get agent's tasks
        agent_tasks = self.agent_manager.get_agent_tasks(agent.agent_id, self.task_manager)
        
        # Verify correct tasks returned
        self.assertEqual(len(agent_tasks), 2)
        self.assertIn(task1, agent_tasks)
        self.assertIn(task3, agent_tasks)
        self.assertNotIn(task2, agent_tasks)
    
    def test_get_stats(self):
        """Test getting statistics about agents."""
        # Create agents with various positions
        agent1 = self.agent_manager.create_agent("Agent 1", position="available")
        agent2 = self.agent_manager.create_agent("Agent 2", position="busy")
        agent3 = self.agent_manager.create_agent("Agent 3", position="offline")
        
        # Assign tasks to some agents
        task1 = self.task_manager.create_task("Task 1")
        task2 = self.task_manager.create_task("Task 2")
        self.agent_manager.assign_agent_to_task(agent2.agent_id, task1)
        self.agent_manager.assign_agent_to_task(agent2.agent_id, task2)
        
        # Get statistics
        stats = self.agent_manager.get_stats()
        
        # Verify statistics
        self.assertEqual(stats['total'], 3)
        self.assertEqual(stats['available'], 1)
        self.assertEqual(stats['busy'], 1)
        self.assertEqual(stats['offline'], 1)
        self.assertEqual(stats['total_assignments'], 2)
    
    def test_monitor_all_agents(self):
        """Test monitoring all agents."""
        # Create agents and assign tasks
        agent1 = self.agent_manager.create_agent("Agent 1")
        agent2 = self.agent_manager.create_agent("Agent 2")
        task1 = self.task_manager.create_task("Task 1")
        self.agent_manager.assign_agent_to_task(agent1.agent_id, task1)
        
        # Monitor all agents
        monitoring_data = self.agent_manager.monitor_all_agents()
        
        # Verify monitoring data
        self.assertEqual(len(monitoring_data), 2)
        self.assertEqual(monitoring_data[0]['agent_id'], 1)
        self.assertEqual(monitoring_data[0]['task_count'], 1)
        self.assertEqual(monitoring_data[1]['agent_id'], 2)
        self.assertEqual(monitoring_data[1]['task_count'], 0)


# Run the tests when this file is executed
if __name__ == '__main__':
    unittest.main()
