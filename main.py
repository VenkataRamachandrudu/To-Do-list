from datetime import datetime

class TodoItem:
    def __init__(self, title, description="", priority="Medium", due_date=None):
        self.title = title
        self.description = description
        self.priority = priority
        self.due_date = due_date
        self.completed = False
        self.created_at = datetime.now()

    def mark_completed(self):
        self.completed = True

    def mark_uncompleted(self):
        self.completed = False

class TodoList:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, index):
        if 0 <= index < len(self.items):
            self.items.pop(index)

    def get_completed_items(self):
        return [item for item in self.items if item.completed]

    def get_pending_items(self):
        return [item for item in self.items if not item.completed]

    def get_completion_stats(self):
        total = len(self.items)
        completed = len(self.get_completed_items())
        pending = total - completed
        rate = (completed / total * 100) if total else 0
        return {
            'total': total,
            'completed': completed,
            'pending': pending,
            'completion_rate': rate
        }
