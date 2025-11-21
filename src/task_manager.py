"""
Task Manager Module

This module provides a Task Management System for organizing and tracking tasks.
It includes functionality for creating, updating, deleting, and listing tasks.
It also includes an Agent Management System for assigning and monitoring agents.

Author: Jabidah Systems
Date: 2025-11-11
"""

from datetime import datetime
from typing import List, Optional, Dict, Set


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
        self.assigned_agents: Set[int] = set()  # Set of agent IDs assigned to this task
    
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
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'assigned_agents': list(self.assigned_agents)
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


class Agent:
    """
    Represents an agent that can be assigned to tasks.
    
    Agents are workers who can be assigned to one or more tasks and have
    a position/status that can be monitored.
    
    Attributes:
        agent_id (int): Unique identifier for the agent
        name (str): Name of the agent
        position (str): Current position/status of the agent (e.g., 'available', 'busy', 'offline')
        assigned_task_ids (Set[int]): Set of task IDs assigned to this agent
        created_at (datetime): Timestamp when the agent was created
    """
    
    def __init__(self, agent_id: int, name: str, position: str = "available"):
        """
        Initialize a new Agent object.
        
        Args:
            agent_id (int): Unique identifier for this agent
            name (str): The name of the agent
            position (str, optional): Initial position/status. Defaults to 'available'.
        
        Raises:
            ValueError: If position is not one of the valid options
        """
        # Validate that position is one of the allowed values
        valid_positions = ['available', 'busy', 'offline']
        if position not in valid_positions:
            raise ValueError(f"Position must be one of {valid_positions}")
        
        # Initialize agent attributes
        self.agent_id = agent_id
        self.name = name
        self.position = position
        self.assigned_task_ids: Set[int] = set()
        self.created_at = datetime.now()
    
    def assign_task(self, task_id: int) -> None:
        """
        Assign a task to this agent.
        
        Args:
            task_id (int): The ID of the task to assign
        """
        self.assigned_task_ids.add(task_id)
        # Update position to busy if agent has tasks
        if len(self.assigned_task_ids) > 0 and self.position == 'available':
            self.position = 'busy'
    
    def unassign_task(self, task_id: int) -> bool:
        """
        Unassign a task from this agent.
        
        Args:
            task_id (int): The ID of the task to unassign
        
        Returns:
            bool: True if task was unassigned, False if task was not assigned to this agent
        """
        if task_id in self.assigned_task_ids:
            self.assigned_task_ids.remove(task_id)
            # Update position to available if agent has no tasks
            if len(self.assigned_task_ids) == 0 and self.position == 'busy':
                self.position = 'available'
            return True
        return False
    
    def update_position(self, position: str) -> None:
        """
        Update the agent's position/status.
        
        Args:
            position (str): New position/status
        
        Raises:
            ValueError: If position is not valid
        """
        valid_positions = ['available', 'busy', 'offline']
        if position not in valid_positions:
            raise ValueError(f"Position must be one of {valid_positions}")
        self.position = position
    
    def to_dict(self) -> Dict:
        """
        Convert agent to a dictionary representation.
        
        Returns:
            Dict: Dictionary containing all agent attributes
        """
        return {
            'agent_id': self.agent_id,
            'name': self.name,
            'position': self.position,
            'assigned_task_ids': list(self.assigned_task_ids),
            'task_count': len(self.assigned_task_ids),
            'created_at': self.created_at.isoformat()
        }
    
    def __str__(self) -> str:
        """
        Return a human-readable string representation of the agent.
        
        Returns:
            str: Formatted string showing agent details
        """
        task_count = len(self.assigned_task_ids)
        return f"Agent #{self.agent_id}: {self.name} (Position: {self.position}, Tasks: {task_count})"
    
    def __repr__(self) -> str:
        """
        Return a detailed representation of the agent for debugging.
        
        Returns:
            str: String representation including all agent attributes
        """
        return f"Agent(id={self.agent_id}, name='{self.name}', position='{self.position}', tasks={len(self.assigned_task_ids)})"


class AgentManager:
    """
    Manages a collection of agents and their assignments to tasks.
    
    This class provides methods to create, read, update, and delete agents,
    as well as assign and monitor agents working on tasks.
    
    Attributes:
        agents (List[Agent]): List of all agents in the system
        next_id (int): Counter for generating unique agent IDs
    """
    
    def __init__(self):
        """Initialize a new AgentManager with an empty agent list."""
        # List to store all agents
        self.agents: List[Agent] = []
        # Counter for assigning unique IDs to new agents
        self.next_id = 1
    
    def create_agent(self, name: str, position: str = "available") -> Agent:
        """
        Create a new agent and add it to the manager.
        
        Args:
            name (str): Name of the new agent
            position (str, optional): Initial position/status. Defaults to 'available'.
        
        Returns:
            Agent: The newly created agent object
        
        Raises:
            ValueError: If name is empty or position is invalid
        """
        # Validate that name is not empty
        if not name or not name.strip():
            raise ValueError("Agent name cannot be empty")
        
        # Create the new agent with auto-incremented ID
        agent = Agent(self.next_id, name, position)
        
        # Add agent to our collection
        self.agents.append(agent)
        
        # Increment ID counter for next agent
        self.next_id += 1
        
        return agent
    
    def get_agent(self, agent_id: int) -> Optional[Agent]:
        """
        Retrieve an agent by its ID.
        
        Args:
            agent_id (int): The ID of the agent to retrieve
        
        Returns:
            Optional[Agent]: The agent if found, None otherwise
        """
        # Search through all agents to find matching ID
        for agent in self.agents:
            if agent.agent_id == agent_id:
                return agent
        
        # Return None if no agent with this ID exists
        return None
    
    def delete_agent(self, agent_id: int) -> bool:
        """
        Delete an agent by its ID.
        
        Args:
            agent_id (int): The ID of the agent to delete
        
        Returns:
            bool: True if agent was deleted, False if agent was not found
        """
        # Find the agent with matching ID
        agent = self.get_agent(agent_id)
        
        # If agent exists, remove it from the list
        if agent:
            self.agents.remove(agent)
            return True
        
        # Agent not found
        return False
    
    def list_agents(self, position: Optional[str] = None) -> List[Agent]:
        """
        List agents with optional filtering by position.
        
        Args:
            position (Optional[str]): Filter by position/status.
                                      None returns all agents.
        
        Returns:
            List[Agent]: List of agents matching the filter criteria
        """
        # Start with all agents
        filtered_agents = self.agents.copy()
        
        # Filter by position if specified
        if position is not None:
            filtered_agents = [a for a in filtered_agents if a.position == position]
        
        return filtered_agents
    
    def assign_agent_to_task(self, agent_id: int, task: Task) -> bool:
        """
        Assign an agent to a task.
        
        Args:
            agent_id (int): The ID of the agent to assign
            task (Task): The task to assign the agent to
        
        Returns:
            bool: True if assignment was successful, False if agent not found
        """
        # Find the agent
        agent = self.get_agent(agent_id)
        
        if not agent:
            return False
        
        # Assign task to agent
        agent.assign_task(task.task_id)
        
        # Add agent to task's assigned agents
        task.assigned_agents.add(agent_id)
        
        return True
    
    def unassign_agent_from_task(self, agent_id: int, task: Task) -> bool:
        """
        Unassign an agent from a task.
        
        Args:
            agent_id (int): The ID of the agent to unassign
            task (Task): The task to unassign the agent from
        
        Returns:
            bool: True if unassignment was successful, False if agent not found or not assigned
        """
        # Find the agent
        agent = self.get_agent(agent_id)
        
        if not agent:
            return False
        
        # Unassign task from agent
        success = agent.unassign_task(task.task_id)
        
        if success:
            # Remove agent from task's assigned agents
            task.assigned_agents.discard(agent_id)
        
        return success
    
    def get_agent_tasks(self, agent_id: int, task_manager: 'TaskManager') -> List[Task]:
        """
        Get all tasks assigned to a specific agent.
        
        Args:
            agent_id (int): The ID of the agent
            task_manager (TaskManager): The task manager to query tasks from
        
        Returns:
            List[Task]: List of tasks assigned to the agent
        """
        agent = self.get_agent(agent_id)
        
        if not agent:
            return []
        
        # Get all tasks that this agent is assigned to
        assigned_tasks = []
        for task_id in agent.assigned_task_ids:
            task = task_manager.get_task(task_id)
            if task:
                assigned_tasks.append(task)
        
        return assigned_tasks
    
    def get_stats(self) -> Dict:
        """
        Get statistics about the agents.
        
        Returns:
            Dict: Dictionary containing various statistics:
                - total: Total number of agents
                - available: Number of available agents
                - busy: Number of busy agents
                - offline: Number of offline agents
                - total_assignments: Total number of task assignments
        """
        # Calculate total counts
        total = len(self.agents)
        available = sum(1 for a in self.agents if a.position == 'available')
        busy = sum(1 for a in self.agents if a.position == 'busy')
        offline = sum(1 for a in self.agents if a.position == 'offline')
        
        # Count total task assignments
        total_assignments = sum(len(a.assigned_task_ids) for a in self.agents)
        
        return {
            'total': total,
            'available': available,
            'busy': busy,
            'offline': offline,
            'total_assignments': total_assignments
        }
    
    def monitor_all_agents(self) -> List[Dict]:
        """
        Monitor all agents and their current status.
        
        Returns a list of dictionaries containing detailed information
        about each agent for monitoring purposes.
        
        Returns:
            List[Dict]: List of agent status dictionaries
        """
        monitoring_data = []
        
        for agent in self.agents:
            monitoring_data.append({
                'agent_id': agent.agent_id,
                'name': agent.name,
                'position': agent.position,
                'task_count': len(agent.assigned_task_ids),
                'assigned_tasks': list(agent.assigned_task_ids)
            })
        
        return monitoring_data
