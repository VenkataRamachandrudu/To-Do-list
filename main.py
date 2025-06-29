from datetime import datetime
from typing import List, Optional
import json

class TodoItem:
    """Represents a single todo item"""
    
    def __init__(self, title: str, description: str = "", priority: str = "Medium", 
                 due_date: Optional[datetime] = None, completed: bool = False):
        self.title = title
        self.description = description
        self.priority = priority
        self.due_date = due_date
        self.completed = completed
        self.created_at = datetime.now()
        self.completed_at = None
    
    def mark_completed(self):
        """Mark the todo item as completed"""
        self.completed = True
        self.completed_at = datetime.now()
    
    def mark_uncompleted(self):
        """Mark the todo item as uncompleted"""
        self.completed = False
        self.completed_at = None
    
    def to_dict(self):
        """Convert todo item to dictionary for serialization"""
        return {
            'title': self.title,
            'description': self.description,
            'priority': self.priority,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'completed': self.completed,
            'created_at': self.created_at.isoformat(),
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create todo item from dictionary"""
        item = cls(
            title=data['title'],
            description=data.get('description', ''),
            priority=data.get('priority', 'Medium'),
            completed=data.get('completed', False)
        )
        
        if data.get('due_date'):
            item.due_date = datetime.fromisoformat(data['due_date'])
        
        if data.get('created_at'):
            item.created_at = datetime.fromisoformat(data['created_at'])
        
        if data.get('completed_at'):
            item.completed_at = datetime.fromisoformat(data['completed_at'])
            
        return item

class TodoList:
    """Manages a collection of todo items"""
    
    def __init__(self):
        self.items: List[TodoItem] = []
    
    def add_item(self, item: TodoItem):
        """Add a new todo item"""
        self.items.append(item)
    
    def remove_item(self, index: int):
        """Remove a todo item by index"""
        if 0 <= index < len(self.items):
            self.items.pop(index)
    
    def get_item(self, index: int) -> Optional[TodoItem]:
        """Get a todo item by index"""
        if 0 <= index < len(self.items):
            return self.items[index]
        return None
    
    def get_completed_items(self) -> List[TodoItem]:
        """Get all completed todo items"""
        return [item for item in self.items if item.completed]
    
    def get_pending_items(self) -> List[TodoItem]:
        """Get all pending todo items"""
        return [item for item in self.items if not item.completed]
    
    def get_items_by_priority(self, priority: str) -> List[TodoItem]:
        """Get todo items by priority"""
        return [item for item in self.items if item.priority == priority]
    
    def get_overdue_items(self) -> List[TodoItem]:
        """Get overdue todo items"""
        now = datetime.now()
        return [item for item in self.items 
                if not item.completed and item.due_date and item.due_date < now]
    
    def clear_completed(self):
        """Remove all completed items"""
        self.items = [item for item in self.items if not item.completed]
    
    def get_completion_stats(self):
        """Get completion statistics"""
        total = len(self.items)
        completed = len(self.get_completed_items())
        pending = len(self.get_pending_items())
        
        return {
            'total': total,
            'completed': completed,
            'pending': pending,
            'completion_rate': (completed / total * 100) if total > 0 else 0
        }
    
    def to_dict(self):
        """Convert todo list to dictionary for serialization"""
        return {
            'items': [item.to_dict() for item in self.items]
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create todo list from dictionary"""
        todo_list = cls()
        for item_data in data.get('items', []):
            todo_list.add_item(TodoItem.from_dict(item_data))
        return todo_list
