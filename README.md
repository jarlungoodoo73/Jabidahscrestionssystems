# Jabidah Task & Agent Management System

## Description

This repository contains a complete Task & Agent Management System with well-documented, extensively commented Python code. The project demonstrates best practices in code documentation and serves as both a functional application and an educational resource.

### Features

**Task Management:**
- **Create and manage tasks** - Add tasks with titles, descriptions, and priority levels
- **Track completion** - Mark tasks as complete or incomplete with timestamps
- **Filter and search** - List tasks by completion status or priority level
- **Statistics** - View comprehensive statistics about your tasks

**Agent Management:**
- **Create and manage agents** - Add agents who can be assigned to work on tasks
- **Agent assignment** - Assign agents to tasks and track their workload
- **Position tracking** - Monitor agent positions/status (available, busy, offline)
- **Agent monitoring** - Watch and control agent workflow across all tasks
- **Agent statistics** - View comprehensive statistics about agent assignments and status

**Additional Features:**
- **Command-line interface** - Interactive CLI for easy task and agent management
- **Well-commented code** - Every function and class includes detailed comments explaining functionality

## Getting Started

### Prerequisites

- Python 3.7 or higher
- No external dependencies required (uses only standard library)

### Installation

```bash
# Clone the repository
git clone https://github.com/jarlungoodoo73/Jabidahscrestionssystems.git
cd Jabidahscrestionssystems
```

No additional installation steps are needed. The project uses only Python standard library modules.

## Usage

### Running the Interactive CLI

To start the interactive command-line interface:

```bash
python -m src.cli
```

This will launch an interactive menu where you can:

**Task Management:**
1. Create new tasks
2. List all tasks (or filter by status)
3. View detailed task information
4. Mark tasks as complete/incomplete
5. Update existing tasks
6. Delete tasks
7. View task statistics
8. Clear completed tasks

**Agent Management:**
9. Create new agents
10. List all agents (or filter by position)
11. View detailed agent information
12. Assign agents to tasks
13. Unassign agents from tasks
14. Update agent positions
15. Monitor all agents
16. View agent statistics
17. Delete agents

### Running the Example Script

To see a demonstration of the system's capabilities:

```bash
python example.py
```

This script demonstrates both task management and agent management features including agent assignment and monitoring.

### Using as a Library

You can also import and use the classes in your own Python code:

**Task Management:**
```python
from src.task_manager import TaskManager

# Create a task manager
manager = TaskManager()

# Create a task
task = manager.create_task(
    title="My first task",
    description="This is a sample task",
    priority="high"
)

# Mark it as complete
task.mark_complete()

# List all tasks
all_tasks = manager.list_tasks()
for task in all_tasks:
    print(task)

# Get statistics
stats = manager.get_stats()
print(f"Total tasks: {stats['total']}")
```

**Agent Management:**
```python
from src.task_manager import TaskManager, AgentManager

# Create managers
task_manager = TaskManager()
agent_manager = AgentManager()

# Create an agent
agent = agent_manager.create_agent(
    name="John Doe",
    position="available"
)

# Create a task
task = task_manager.create_task(
    title="Important task",
    priority="high"
)

# Assign agent to task
agent_manager.assign_agent_to_task(agent.agent_id, task)

# Monitor all agents
monitoring_data = agent_manager.monitor_all_agents()
for data in monitoring_data:
    print(f"Agent {data['name']}: {data['task_count']} tasks")

# Get agent statistics
stats = agent_manager.get_stats()
print(f"Total agents: {stats['total']}")
print(f"Busy agents: {stats['busy']}")
```


## Project Structure

```
Jabidahscrestionssystems/
├── src/                      # Source code directory
│   ├── __init__.py          # Package initialization
│   ├── task_manager.py      # Core task and agent management classes
│   └── cli.py               # Command-line interface for tasks and agents
├── tests/                    # Unit tests
│   ├── __init__.py          # Tests package initialization
│   └── test_task_manager.py # Comprehensive tests for Task, TaskManager, Agent, and AgentManager
├── example.py               # Example usage script
├── README.md                # This file - project documentation
├── LICENSE                  # MIT License
└── .gitignore              # Git ignore patterns
```

## Testing

The project includes comprehensive unit tests for all classes. To run the tests:

```bash
# Run all tests
python -m unittest discover tests

# Run with verbose output
python -m unittest discover tests -v

# Run a specific test file
python -m unittest tests.test_task_manager

# Run a specific test class
python -m unittest tests.test_task_manager.TestTask

# Run a specific test method
python -m unittest tests.test_task_manager.TestTask.test_task_creation
```

All tests include detailed docstrings explaining what they test and why.

## Code Documentation

All code in this project is extensively commented with:

- **Module docstrings** - Explaining the purpose of each file
- **Class docstrings** - Describing what each class does and its attributes
- **Method docstrings** - Detailing parameters, return values, and behavior
- **Inline comments** - Explaining complex logic and important decisions
- **Type hints** - Making code more readable and maintainable

For detailed information about the documentation standards used in this project, see [DOCUMENTATION_STANDARDS.md](DOCUMENTATION_STANDARDS.md).

### Example of Code Comment Quality

Every function includes comprehensive documentation:

```python
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
```

## API Reference

### Task Class

Represents a single task with the following methods:

- `__init__(task_id, title, description, priority)` - Create a new task
- `mark_complete()` - Mark the task as completed
- `mark_incomplete()` - Mark the task as incomplete
- `update(title, description, priority)` - Update task attributes
- `to_dict()` - Convert task to dictionary format

### TaskManager Class

Manages a collection of tasks with these methods:

- `create_task(title, description, priority)` - Create and add a new task
- `get_task(task_id)` - Retrieve a task by ID
- `delete_task(task_id)` - Delete a task by ID
- `list_tasks(completed, priority)` - List tasks with optional filters
- `get_stats()` - Get statistics about all tasks
- `clear_completed()` - Remove all completed tasks

### Agent Class

Represents a single agent with the following methods:

- `__init__(agent_id, name, position)` - Create a new agent
- `assign_task(task_id)` - Assign a task to this agent
- `unassign_task(task_id)` - Unassign a task from this agent
- `update_position(position)` - Update the agent's position/status
- `to_dict()` - Convert agent to dictionary format

### AgentManager Class

Manages a collection of agents with these methods:

- `create_agent(name, position)` - Create and add a new agent
- `get_agent(agent_id)` - Retrieve an agent by ID
- `delete_agent(agent_id)` - Delete an agent by ID
- `list_agents(position)` - List agents with optional filter by position
- `assign_agent_to_task(agent_id, task)` - Assign an agent to a task
- `unassign_agent_from_task(agent_id, task)` - Unassign an agent from a task
- `get_agent_tasks(agent_id, task_manager)` - Get all tasks assigned to an agent
- `get_stats()` - Get statistics about all agents
- `monitor_all_agents()` - Get monitoring data for all agents

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For questions or support, please open an issue in this repository.