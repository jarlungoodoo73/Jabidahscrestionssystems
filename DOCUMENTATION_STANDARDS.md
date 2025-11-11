# Code Documentation Standards

This document explains the commenting and documentation standards used throughout the Jabidah Task Management System codebase.

## Philosophy

The code in this project follows the principle that **code should be self-documenting through clear naming and structure**, with comments providing:
1. **Context and reasoning** - Why decisions were made
2. **Usage examples** - How to use functions and classes
3. **Edge cases** - Important behaviors and limitations
4. **Implementation details** - Complex logic explanations

## Documentation Levels

### 1. Module-Level Documentation

Every Python file starts with a module docstring that explains:
- The purpose of the module
- What functionality it provides
- Author and date information

Example:
```python
"""
Task Manager Module

This module provides a Task Management System for organizing and tracking tasks.
It includes functionality for creating, updating, deleting, and listing tasks.

Author: Jabidah Systems
Date: 2025-11-11
"""
```

### 2. Class-Level Documentation

Every class includes a docstring that describes:
- What the class represents
- Its main responsibilities
- Key attributes with types and descriptions

Example:
```python
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
        completed_at (Optional[datetime]): Timestamp when completed
    """
```

### 3. Method/Function Documentation

Every method and function has a docstring following the Google style guide:
- Summary line describing what it does
- Detailed description if needed
- Args section listing all parameters with types and descriptions
- Returns section describing the return value
- Raises section listing exceptions that may be raised

Example:
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
```

### 4. Inline Comments

Inline comments are used to:
- Explain non-obvious logic
- Mark important steps in algorithms
- Clarify business rules
- Highlight edge cases

Guidelines:
- Place comments on the line before the code they describe
- Use complete sentences with proper capitalization and punctuation
- Explain WHY, not WHAT (the code shows what)
- Keep comments concise but clear

Example:
```python
# Validate that title is not empty
if not title or not title.strip():
    raise ValueError("Task title cannot be empty")

# Create the new task with auto-incremented ID
task = Task(self.next_id, title, description, priority)

# Add task to our collection
self.tasks.append(task)

# Increment ID counter for next task
self.next_id += 1
```

## Type Hints

All functions and methods use type hints to make the code more readable and enable static analysis:
```python
def get_task(self, task_id: int) -> Optional[Task]:
    """Retrieve a task by its ID."""
```

## Testing Documentation

Test methods also include docstrings explaining:
- What is being tested
- Expected behavior
- Any special conditions

Example:
```python
def test_mark_complete(self):
    """Test marking a task as complete."""
    task = Task(1, "Test Task")
    
    # Initially not completed
    self.assertFalse(task.completed)
    
    # Mark as complete
    task.mark_complete()
    
    # Verify completion
    self.assertTrue(task.completed)
```

## Best Practices Applied

1. **Docstrings over comments** - Use docstrings for public APIs
2. **Type hints** - Always provide type information
3. **Clear naming** - Use descriptive variable and function names
4. **Consistent style** - Follow PEP 257 for docstrings, PEP 8 for code
5. **Example-driven** - Provide examples in documentation
6. **Comprehensive coverage** - Document all public interfaces
7. **Update with code** - Keep documentation in sync with changes

## Tools and Standards

- **Style Guide**: PEP 8 (Python Enhancement Proposal 8)
- **Docstring Convention**: Google Style (via PEP 257)
- **Type Hints**: PEP 484
- **Testing**: Python unittest framework

## Summary

This codebase demonstrates professional software engineering practices with:
- **100% documented** - Every module, class, and function has documentation
- **Type-safe** - Type hints throughout for better tooling support
- **Well-tested** - Comprehensive test coverage with documented tests
- **Maintainable** - Clear structure and explanations for future developers
- **Educational** - Can serve as a reference for good documentation practices

The result is code that is easy to understand, maintain, and extend.
