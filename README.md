# Python To-Do List Manager 📝

A feature-rich to-do list application with both **Command Line Interface (CLI)** and **Web Interface (Streamlit)**. Manage your tasks efficiently with priorities, due dates, analytics, and persistent storage.

## Features ✨

### 🖥️ CLI Version (main.py)
- **Add Tasks**: Create new todos with title, description, priority, and due date
- **Task Management**: Mark tasks as complete, update existing tasks, or delete them
- **Priority System**: Organize tasks by priority levels (High 🔴, Medium 🟡, Low 🟢)
- **Filtering**: View tasks by status (pending/completed) or priority level
- **Statistics**: Get insights into your productivity with task statistics
- **Persistent Storage**: All tasks are saved to a JSON file automatically
- **User-Friendly CLI**: Interactive command-line interface with clear menus

### 🌐 Web Interface (streamlit_app.py)
- **Modern Dashboard**: Beautiful web interface with real-time metrics
- **Interactive Forms**: Easy task creation with date pickers and dropdowns
- **Visual Analytics**: Charts and graphs showing task completion trends
- **Bulk Actions**: Complete or delete multiple tasks at once
- **Responsive Design**: Works great on desktop and mobile devices
- **Live Updates**: Real-time updates without page refresh
- **Advanced Filtering**: Multiple filter options with instant results

## Installation 🚀

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/python-todo-list.git
   cd python-todo-list
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**

   **Option A: Use the launcher (Recommended)**
   ```bash
   python run_app.py
   ```
   
   **Option B: Run directly**
   ```bash
   # CLI Version
   python main.py
   
   # Web App Version
   streamlit run streamlit_app.py
   ```

## Quick Start 🎯

### 🚀 Easy Launcher
```bash
python run_app.py
```
This will give you options to run either the CLI or web version.

### 🖥️ CLI Version
```bash
python main.py
```
Perfect for terminal users and automation scripts.

### 🌐 Web App Version
```bash
streamlit run streamlit_app.py
```
Opens a beautiful web interface at `http://localhost:8501`

## Usage 📖

### Main Menu Options

1. **Add Todo** - Create a new task
2. **List Todos** - View all tasks
3. **Complete Todo** - Mark a task as completed
4. **Update Todo** - Modify existing task details
5. **Delete Todo** - Remove a task permanently
6. **Show Statistics** - View task completion statistics
7. **Filter Todos** - View tasks by status or priority
8. **Exit** - Close the application

### Adding a Task

When adding a task, you can specify:
- **Title** (required): Brief description of the task
- **Description** (optional): Detailed information about the task
- **Priority** (optional): high, medium, or low (default: medium)
- **Due Date** (optional): Target completion date in YYYY-MM-DD format

### Example Usage

```
=== TO-DO LIST MANAGER ===
1. Add todo
2. List todos
3. Complete todo
4. Update todo
5. Delete todo
6. Show statistics
7. Filter todos
8. Exit

Enter your choice (1-8): 1
Enter todo title: Complete project documentation
Enter description (optional): Write comprehensive README and API docs
Priority levels: high, medium, low
Enter priority (default: medium): high
Enter due date (YYYY-MM-DD, optional): 2024-12-31
✓ Added todo: Complete project documentation
```

## File Structure 📁

```
python-todo-list/
├── main.py              # CLI application
├── streamlit_app.py     # Web application (Streamlit)
├── run_app.py          # Launcher script
├── todos.json          # CLI data storage (created automatically)
├── streamlit_todos.json # Web app data storage (created automatically)
├── requirements.txt    # Python dependencies
├── README.md          # This file
├── .gitignore        # Git ignore file
└── LICENSE           # MIT license
```

## Data Storage 💾

Tasks are automatically saved to `todos.json` in the same directory as the application. The file is created automatically when you first run the program.

### JSON Structure

```json
{
  "todos": [
    {
      "id": 1,
      "title": "Sample Task",
      "description": "This is a sample task",
      "priority": "medium",
      "due_date": "2024-12-31",
      "completed": false,
      "created_at": "2024-01-01 10:00:00",
      "completed_at": null
    }
  ],
  "next_id": 2
}
```

## Features in Detail 🔍

### Priority System
- **High Priority** 🔴: Urgent tasks that need immediate attention
- **Medium Priority** 🟡: Important tasks with moderate urgency
- **Low Priority** 🟢: Tasks that can be done when time permits

## Streamlit Web App Features 🌐

### 📋 Dashboard
- **Real-time Metrics**: Total tasks, completion rate, priority breakdown
- **Task Cards**: Beautiful visual representation of your tasks
- **Smart Filtering**: Filter by completion status and priority
- **Recent Tasks**: Quick view of your latest activities

### ➕ Add Tasks
- **Interactive Forms**: User-friendly task creation
- **Date Picker**: Easy due date selection
- **Priority Selection**: Visual priority level chooser
- **Instant Feedback**: Immediate confirmation of task creation

### 📊 Analytics
- **Completion Charts**: Visual progress tracking with pie charts
- **Priority Distribution**: Bar charts showing task priorities
- **Timeline View**: Track task creation over time
- **Summary Statistics**: Comprehensive metrics table

### ⚙️ Task Management
- **Task Table**: Sortable and filterable task overview
- **Quick Actions**: One-click complete and delete functions
- **Bulk Operations**: Manage multiple tasks simultaneously
- **Live Updates**: Changes reflect immediately across all views

## Deployment Options 🚀

### 1. Local Development
```bash
# Clone and run locally
git clone https://github.com/yourusername/python-todo-list.git
cd python-todo-list
pip install -r requirements.txt
python run_app.py
```

### 2. Streamlit Cloud (Free!)
1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Deploy with one click!

### 3. Heroku Deployment
Create a `Procfile`:
```
web: streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0
```

### 4. Docker (Optional)
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "streamlit_app.py"]
```

## Contributing 🤝

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## Screenshots 📸

### 🌐 Web Interface
- **Dashboard**: Clean, modern interface with real-time metrics
- **Analytics**: Beautiful charts showing your productivity trends
- **Task Management**: Intuitive forms and bulk operations

### 🖥️ CLI Interface
- **Interactive Menus**: Easy-to-navigate command-line interface
- **Colored Output**: Priority-coded task display
- **Statistics**: Comprehensive productivity reports

## Future Enhancements 🔮

- [ ] Web interface using Flask
- [ ] Task categories/tags
- [ ] Recurring tasks
- [ ] Task reminders
- [ ] Export to CSV/PDF
- [ ] Multi-user support
- [ ] Task sharing
- [ ] Mobile app version

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support 💬

If you encounter any issues or have questions:
1. Check the existing [Issues](https://github.com/yourusername/python-todo-list/issues)
2. Create a new issue if your problem isn't already addressed
3. Provide as much detail as possible about the issue

## Acknowledgments 🙏

- Built with Python's standard library
- Inspired by simple productivity tools
- Thanks to the open-source community for inspiration

---

**Happy task managing! 🎯**