"""
Jabidah Systems - Task Management System

This package provides a complete task management system with
well-documented, commented code for educational and practical use.

Modules:
    task_manager: Core task management functionality
    cli: Command-line interface for interacting with the system
"""

# Package version
__version__ = "1.0.0"

# Package author
__author__ = "Jabidah Systems"

# Import main classes for easy access
from .task_manager import Task, TaskManager

# Define what gets imported with "from src import *"
__all__ = ['Task', 'TaskManager']
