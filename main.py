from datetime import datetime, timedelta
from typing import List, Optional
import uuid

class TodoItem:
    def __init__(self, title, description="", priority="Medium", due_date=None, completed=False, category="General", tags=None):
        self.id = str(uuid.uuid4())
        self.title = title
        self.description = description
        self.priority = priority
        self.due_date = due_date
        self.completed = completed
        self.category = category
        self.tags = tags or []
        self.created_at = datetime.now()
        self.completed_at = None
        self.estimated_time = None
        self.actual_time = None
        self.subtasks = []
        self.notes = []
    
    def mark_completed(self):
        self.completed = True
        self.completed_at = datetime.now()
    
    def mark_uncompleted(self):
        self.completed = False
        self.completed_at = None
    
    def add_subtask(self, subtask_title):
        subtask = {
            'id': str(uuid.uuid4()),
            'title': subtask_title,
            'completed': False,
            'created_at': datetime.now()
        }
        self.subtasks.append(subtask)
        return subtask
    
    def toggle_subtask(self, subtask_id):
        for subtask in self.subtasks:
            if subtask['id'] == subtask_id:
                subtask['completed'] = not subtask['completed']
                break
    
    def get_subtask_progress(self):
        if not self.subtasks:
            return 0
        completed = sum(1 for st in self.subtasks if st['completed'])
        return (completed / len(self.subtasks)) * 100
    
    def is_overdue(self):
        if not self.due_date or self.completed:
            return False
        return datetime.now() > self.due_date
    
    def days_until_due(self):
        if not self.due_date:
            return None
        delta = self.due_date - datetime.now()
        return delta.days
    
    def add_note(self, note_text):
        note = {
            'id': str(uuid.uuid4()),
            'text': note_text,
            'created_at': datetime.now()
        }
        self.notes.append(note)
        return note

class TodoList:
    def __init__(self):
        self.items = []
        self.categories = ["General", "Work", "Personal", "Shopping", "Health", "Learning", "Projects"]
        self.quick_add_templates = [
            {"title": "Buy groceries", "category": "Shopping", "priority": "Medium"},
            {"title": "Exercise", "category": "Health", "priority": "High"},
            {"title": "Read for 30 minutes", "category": "Learning", "priority": "Low"},
            {"title": "Team meeting", "category": "Work", "priority": "High"},
        ]
    
    def add_item(self, item):
        self.items.append(item)
    
    def remove_item(self, item_id):
        self.items = [item for item in self.items if item.id != item_id]
    
    def get_item_by_id(self, item_id):
        for item in self.items:
            if item.id == item_id:
                return item
        return None
    
    def get_completed_items(self):
        return [item for item in self.items if item.completed]
    
    def get_pending_items(self):
        return [item for item in self.items if not item.completed]
    
    def get_overdue_items(self):
        return [item for item in self.items if item.is_overdue()]
    
    def get_items_by_category(self, category):
        return [item for item in self.items if item.category == category]
    
    def get_items_by_priority(self, priority):
        return [item for item in self.items if item.priority == priority]
    
    def get_items_due_today(self):
        today = datetime.now().date()
        return [item for item in self.items if item.due_date and item.due_date.date() == today and not item.completed]
    
    def get_items_due_this_week(self):
        today = datetime.now().date()
        week_end = today + timedelta(days=7)
        return [item for item in self.items if item.due_date and today <= item.due_date.date() <= week_end and not item.completed]
    
    def search_items(self, query):
        query = query.lower()
        return [item for item in self.items if 
                query in item.title.lower() or 
                query in item.description.lower() or 
                any(query in tag.lower() for tag in item.tags)]
    
    def get_completion_stats(self):
        total = len(self.items)
        completed = len(self.get_completed_items())
        overdue = len(self.get_overdue_items())
        due_today = len(self.get_items_due_today())
        
        # Category stats
        category_stats = {}
        for category in self.categories:
            cat_items = self.get_items_by_category(category)
            cat_completed = [item for item in cat_items if item.completed]
            category_stats[category] = {
                'total': len(cat_items),
                'completed': len(cat_completed),
                'completion_rate': (len(cat_completed) / len(cat_items) * 100) if cat_items else 0
            }
        
        # Priority stats
        priority_stats = {}
        for priority in ["High", "Medium", "Low"]:
            pri_items = self.get_items_by_priority(priority)
            pri_completed = [item for item in pri_items if item.completed]
            priority_stats[priority] = {
                'total': len(pri_items),
                'completed': len(pri_completed),
                'pending': len(pri_items) - len(pri_completed)
            }
        
        return {
            'total': total,
            'completed': completed,
            'pending': total - completed,
            'overdue': overdue,
            'due_today': due_today,
            'completion_rate': (completed / total * 100) if total > 0 else 0,
            'category_stats': category_stats,
            'priority_stats': priority_stats
        }
    
    def get_productivity_insights(self):
        if not self.items:
            return {}
        
        completed_items = self.get_completed_items()
        
        # Weekly completion trend
        weekly_completions = {}
        for item in completed_items:
            if item.completed_at:
                week_start = item.completed_at.date() - timedelta(days=item.completed_at.weekday())
                week_key = week_start.strftime("%Y-%m-%d")
                weekly_completions[week_key] = weekly_completions.get(week_key, 0) + 1
        
        # Average completion time
        completion_times = []
        for item in completed_items:
            if item.completed_at:
                time_diff = item.completed_at - item.created_at
                completion_times.append(time_diff.total_seconds() / 3600)  # in hours
        
        avg_completion_time = sum(completion_times) / len(completion_times) if completion_times else 0
        
        return {
            'weekly_completions': weekly_completions,
            'avg_completion_time_hours': avg_completion_time,
            'most_productive_category': max(self.get_completion_stats()['category_stats'].items(), 
                                          key=lambda x: x[1]['completed'])[0] if self.items else None
        }
