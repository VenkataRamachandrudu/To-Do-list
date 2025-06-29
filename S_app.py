import streamlit as st
import pandas as pd
from datetime import datetime, date
import plotly.express as px
import plotly.graph_objects as go
from main import TodoList, TodoItem

# Configure Streamlit page
st.set_page_config(
    page_title="📝 To-Do List Manager",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'todo_list' not in st.session_state:
    st.session_state.todo_list = TodoList("streamlit_todos.json")

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #1f77b4;
        margin-bottom: 30px;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .priority-high {
        border-left: 5px solid #ff4444;
        padding-left: 10px;
    }
    .priority-medium {
        border-left: 5px solid #ffaa00;
        padding-left: 10px;
    }
    .priority-low {
        border-left: 5px solid #44ff44;
        padding-left: 10px;
    }
    .completed-task {
        opacity: 0.6;
        text-decoration: line-through;
    }
</style>
""", unsafe_allow_html=True)

def get_priority_color(priority):
    """Get color for priority level"""
    colors = {
        'high': '#ff4444',
        'medium': '#ffaa00',
        'low': '#44ff44'
    }
    return colors.get(priority, '#cccccc')

def get_priority_emoji(priority):
    """Get emoji for priority level"""
    emojis = {
        'high': '🔴',
        'medium': '🟡',
        'low': '🟢'
    }
    return emojis.get(priority, '⚪')

def main():
    # Header
    st.markdown("<h1 class='main-header'>📝 To-Do List Manager</h1>", unsafe_allow_html=True)
    
    # Sidebar for navigation
    st.sidebar.title("🎯 Navigation")
    page = st.sidebar.selectbox(
        "Choose a page:",
        ["📋 Dashboard", "➕ Add Task", "📊 Analytics", "⚙️ Manage Tasks"]
    )
    
    # Get current todo list
    todo_list = st.session_state.todo_list
    
    if page == "📋 Dashboard":
        show_dashboard(todo_list)
    elif page == "➕ Add Task":
        show_add_task(todo_list)
    elif page == "📊 Analytics":
        show_analytics(todo_list)
    elif page == "⚙️ Manage Tasks":
        show_manage_tasks(todo_list)

def show_dashboard(todo_list):
    """Display the main dashboard"""
    st.header("📋 Dashboard")
    
    # Get statistics
    stats = todo_list.get_stats()
    
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📊 Total Tasks", stats['total'])
    
    with col2:
        st.metric("✅ Completed", stats['completed'])
    
    with col3:
        st.metric("⏳ Pending", stats['pending'])
    
    with col4:
        completion_rate = (stats['completed'] / stats['total'] * 100) if stats['total'] > 0 else 0
        st.metric("📈 Completion Rate", f"{completion_rate:.1f}%")
    
    # Priority breakdown
    st.subheader("🎯 Priority Breakdown (Pending Tasks)")
    priority_col1, priority_col2, priority_col3 = st.columns(3)
    
    with priority_col1:
        st.metric("🔴 High Priority", stats['priority_counts']['high'])
    
    with priority_col2:
        st.metric("🟡 Medium Priority", stats['priority_counts']['medium'])
    
    with priority_col3:
        st.metric("🟢 Low Priority", stats['priority_counts']['low'])
    
    # Recent tasks
    st.subheader("📝 Recent Tasks")
    
    # Filter options
    filter_col1, filter_col2 = st.columns(2)
    
    with filter_col1:
        show_completed = st.checkbox("Show completed tasks", value=True)
    
    with filter_col2:
        priority_filter = st.selectbox(
            "Filter by priority:",
            ["All", "High", "Medium", "Low"]
        )
    
    # Get filtered todos
    filter_priority = priority_filter.lower() if priority_filter != "All" else None
    todos = todo_list.list_todos(show_completed=show_completed, filter_priority=filter_priority)
    
    if todos:
        for todo in todos[-10:]:  # Show last 10 tasks
            display_todo_card(todo)
    else:
        st.info("No tasks found with the current filters.")

def display_todo_card(todo):
    """Display a single todo as a card"""
    # Create container for the todo
    with st.container():
        col1, col2, col3 = st.columns([0.1, 0.8, 0.1])
        
        with col1:
            # Status indicator
            if todo.completed:
                st.markdown("✅")
            else:
                st.markdown("⏳")
        
        with col2:
            # Todo content
            priority_emoji = get_priority_emoji(todo.priority)
            title_style = "completed-task" if todo.completed else ""
            
            st.markdown(f"""
            <div class="priority-{todo.priority}">
                <h4 class="{title_style}">{priority_emoji} {todo.title}</h4>
                {f"<p><strong>Description:</strong> {todo.description}</p>" if todo.description else ""}
                {f"<p><strong>Due:</strong> {todo.due_date}</p>" if todo.due_date else ""}
                <small>Created: {todo.created_at}</small>
                {f"<br><small>Completed: {todo.completed_at}</small>" if todo.completed_at else ""}
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"**#{todo.id}**")
        
        st.divider()

def show_add_task(todo_list):
    """Show the add task form"""
    st.header("➕ Add New Task")
    
    with st.form("add_task_form"):
        # Task details
        title = st.text_input("📝 Task Title *", placeholder="Enter task title...")
        description = st.text_area("📄 Description", placeholder="Enter task description (optional)...")
        
        col1, col2 = st.columns(2)
        
        with col1:
            priority = st.selectbox(
                "🎯 Priority Level",
                ["medium", "high", "low"],
                index=0
            )
        
        with col2:
            due_date = st.date_input(
                "📅 Due Date",
                value=None,
                help="Select due date (optional)"
            )
        
        # Submit button
        submitted = st.form_submit_button("✅ Add Task", use_container_width=True)
        
        if submitted:
            if not title.strip():
                st.error("❌ Task title cannot be empty!")
            else:
                # Convert date to string
                due_date_str = due_date.strftime("%Y-%m-%d") if due_date else ""
                
                # Add the task
                new_todo = todo_list.add_todo(
                    title=title.strip(),
                    description=description.strip(),
                    priority=priority,
                    due_date=due_date_str
                )
                
                st.success(f"✅ Task '{new_todo.title}' added successfully!")
                st.rerun()

def show_analytics(todo_list):
    """Show analytics and charts"""
    st.header("📊 Analytics")
    
    todos = todo_list.todos
    
    if not todos:
        st.info("No tasks available for analytics.")
        return
    
    # Create DataFrame for analysis
    df_data = []
    for todo in todos:
        df_data.append({
            'id': todo.id,
            'title': todo.title,
            'priority': todo.priority,
            'completed': todo.completed,
            'created_at': datetime.strptime(todo.created_at, "%Y-%m-%d %H:%M:%S"),
            'has_due_date': bool(todo.due_date),
            'has_description': bool(todo.description)
        })
    
    df = pd.DataFrame(df_data)
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Completion status pie chart
        status_counts = df['completed'].value_counts()
        fig_status = px.pie(
            values=status_counts.values,
            names=['Pending' if not x else 'Completed' for x in status_counts.index],
            title="📊 Task Completion Status",
            color_discrete_map={'Completed': '#28a745', 'Pending': '#ffc107'}
        )
        st.plotly_chart(fig_status, use_container_width=True)
    
    with col2:
        # Priority distribution
        priority_counts = df['priority'].value_counts()
        fig_priority = px.bar(
            x=priority_counts.index,
            y=priority_counts.values,
            title="🎯 Priority Distribution",
            color=priority_counts.index,
            color_discrete_map={'high': '#dc3545', 'medium': '#ffc107', 'low': '#28a745'}
        )
        fig_priority.update_xaxis(title="Priority Level")
        fig_priority.update_yaxis(title="Number of Tasks")
        st.plotly_chart(fig_priority, use_container_width=True)
    
    # Tasks created over time
    df['date'] = df['created_at'].dt.date
    daily_tasks = df.groupby('date').size().reset_index(name='count')
    
    fig_timeline = px.line(
        daily_tasks,
        x='date',
        y='count',
        title="📈 Tasks Created Over Time",
        markers=True
    )
    fig_timeline.update_xaxis(title="Date")
    fig_timeline.update_yaxis(title="Number of Tasks Created")
    st.plotly_chart(fig_timeline, use_container_width=True)
    
    # Statistics table
    st.subheader("📋 Summary Statistics")
    
    stats_data = {
        'Metric': [
            'Total Tasks',
            'Completed Tasks',
            'Pending Tasks',
            'High Priority Tasks',
            'Tasks with Due Dates',
            'Tasks with Descriptions',
            'Average Tasks per Day'
        ],
        'Value': [
            len(df),
            len(df[df['completed'] == True]),
            len(df[df['completed'] == False]),
            len(df[df['priority'] == 'high']),
            len(df[df['has_due_date'] == True]),
            len(df[df['has_description'] == True]),
            f"{len(df) / max(1, (df['created_at'].max() - df['created_at'].min()).days + 1):.1f}"
        ]
    }
    
    stats_df = pd.DataFrame(stats_data)
    st.dataframe(stats_df, use_container_width=True, hide_index=True)

def show_manage_tasks(todo_list):
    """Show task management interface"""
    st.header("⚙️ Manage Tasks")
    
    todos = todo_list.list_todos()
    
    if not todos:
        st.info("No tasks available to manage.")
        return
    
    # Create a DataFrame for display
    df_data = []
    for todo in todos:
        df_data.append({
            'ID': todo.id,
            'Status': '✅' if todo.completed else '⏳',
            'Priority': get_priority_emoji(todo.priority),
            'Title': todo.title,
            'Description': todo.description[:50] + '...' if len(todo.description) > 50 else todo.description,
            'Due Date': todo.due_date,
            'Created': todo.created_at.split(' ')[0]  # Just the date
        })
    
    df = pd.DataFrame(df_data)
    
    # Display tasks table
    st.subheader("📋 All Tasks")
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Task actions
    st.subheader("🔧 Task Actions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Complete Task**")
        pending_todos = [todo for todo in todos if not todo.completed]
        if pending_todos:
            task_options = {f"{todo.id}: {todo.title}": todo.id for todo in pending_todos}
            selected_complete = st.selectbox(
                "Select task to complete:",
                options=list(task_options.keys()),
                key="complete_select"
            )
            
            if st.button("✅ Mark as Complete", key="complete_btn"):
                task_id = task_options[selected_complete]
                if todo_list.complete_todo(task_id):
                    st.success(f"✅ Task completed!")
                    st.rerun()
                else:
                    st.error("❌ Failed to complete task!")
        else:
            st.info("No pending tasks to complete.")
    
    with col2:
        st.write("**Delete Task**")
        if todos:
            delete_options = {f"{todo.id}: {todo.title}": todo.id for todo in todos}
            selected_delete = st.selectbox(
                "Select task to delete:",
                options=list(delete_options.keys()),
                key="delete_select"
            )
            
            if st.button("🗑️ Delete Task", key="delete_btn", type="secondary"):
                task_id = delete_options[selected_delete]
                if todo_list.delete_todo(task_id):
                    st.success(f"🗑️ Task deleted!")
                    st.rerun()
                else:
                    st.error("❌ Failed to delete task!")
        else:
            st.info("No tasks to delete.")
    
    # Bulk actions
    st.subheader("📦 Bulk Actions")
    
    bulk_col1, bulk_col2 = st.columns(2)
    
    with bulk_col1:
        if st.button("✅ Complete All Pending Tasks", key="complete_all"):
            pending_count = 0
            for todo in todos:
                if not todo.completed:
                    todo_list.complete_todo(todo.id)
                    pending_count += 1
            
            if pending_count > 0:
                st.success(f"✅ Completed {pending_count} tasks!")
                st.rerun()
            else:
                st.info("No pending tasks to complete.")
    
    with bulk_col2:
        if st.button("🗑️ Delete All Completed Tasks", key="delete_completed", type="secondary"):
            deleted_count = 0
            completed_todos = [todo for todo in todos if todo.completed]
            for todo in completed_todos:
                todo_list.delete_todo(todo.id)
                deleted_count += 1
            
            if deleted_count > 0:
                st.success(f"🗑️ Deleted {deleted_count} completed tasks!")
                st.rerun()
            else:
                st.info("No completed tasks to delete.")

if __name__ == "__main__":
    main()