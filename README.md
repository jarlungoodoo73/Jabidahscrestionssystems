# Jabidah Task Management System

## Description

This repository contains a complete Task Management System with well-documented, extensively commented Python code. The project demonstrates best practices in code documentation and serves as both a functional application and an educational resource.

### Features

- **Create and manage tasks** - Add tasks with titles, descriptions, and priority levels
- **Track completion** - Mark tasks as complete or incomplete with timestamps
- **Filter and search** - List tasks by completion status or priority level
- **Statistics** - View comprehensive statistics about your tasks
- **Command-line interface** - Interactive CLI for easy task management
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
1. Create new tasks
2. List all tasks (or filter by status)
3. View detailed task information
4. Mark tasks as complete/incomplete
5. Update existing tasks
6. Delete tasks
7. View statistics
8. Clear completed tasks

### Running the Example Script

To see a demonstration of the system's capabilities:

```bash
python example.py
```

This script shows programmatic usage of the Task and TaskManager classes.

### Using as a Library

You can also import and use the classes in your own Python code:

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


## Project Structure

```
Jabidahscrestionssystems/
├── src/                      # Source code directory
│   ├── __init__.py          # Package initialization
│   ├── task_manager.py      # Core task management classes (Task, TaskManager)
│   └── cli.py               # Command-line interface
├── tests/                    # Unit tests
│   ├── __init__.py          # Tests package initialization
│   └── test_task_manager.py # Comprehensive tests for Task and TaskManager
├── example.py               # Example usage script
├── README.md                # This file - project documentation
├── LICENSE                  # MIT License
└── .gitignore              # Git ignore patterns
```

## Testing

The project includes comprehensive unit tests. To run the tests:

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

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For questions or support, please open an issue in this repository.