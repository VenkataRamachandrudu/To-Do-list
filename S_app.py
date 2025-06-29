import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
from main import TodoList, TodoItem

# Configure Streamlit page
st.set_page_config(
    page_title="Advanced Todo Manager",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .todo-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .todo-card.completed {
        opacity: 0.7;
        border-left-color: #28a745;
    }
    
    .todo-card.overdue {
        border-left-color: #dc3545;
        background: #fff5f5;
    }
    
    .priority-high { color: #dc3545; font-weight: bold; }
    .priority-medium { color: #ffc107; font-weight: bold; }
    .priority-low { color: #28a745; font-weight: bold; }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding-left: 20px;
        padding-right: 20px;
        background-color: #f0f2f6;
        border-radius: 10px 10px 0 0;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #667eea;
        color: white;
    }
    
    .quick-add-btn {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        cursor: pointer;
        margin: 0.25rem;
        font-size: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'todo_list' not in st.session_state:
    st.session_state.todo_list = TodoList()
if 'selected_todo' not in st.session_state:
    st.session_state.selected_todo = None
if 'view_mode' not in st.session_state:
    st.session_state.view_mode = "Dashboard"
if 'search_query' not in st.session_state:
    st.session_state.search_query = ""

# Header
st.markdown("""
<div class="main-header">
    <h1>🚀 Advanced Todo Manager</h1>
    <p>Supercharge your productivity with intelligent task management</p>
</div>
""", unsafe_allow_html=True)

# Sidebar Navigation
with st.sidebar:
    st.markdown("### 🎯 Navigation")
    view_mode = st.radio("", ["📊 Dashboard", "📝 Tasks", "📈 Analytics", "⚙️ Settings"], 
                        key="nav_radio")
    st.session_state.view_mode = view_mode.split(" ", 1)[1]
    
    st.markdown("---")
    
    # Quick Stats
    stats = st.session_state.todo_list.get_completion_stats()
    st.markdown("### 📊 Quick Stats")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total", stats['total'])
        st.metric("Completed", stats['completed'])
    with col2:
        st.metric("Pending", stats['pending'])
        st.metric("Overdue", stats['overdue'])
    
    # Progress ring
    if stats['total'] > 0:
        progress = stats['completion_rate'] / 100
        st.markdown(f"**Overall Progress: {stats['completion_rate']:.1f}%**")
        st.progress(progress)
    
    st.markdown("---")
    
    # Quick Add Templates
    st.markdown("### ⚡ Quick Add")
    templates = st.session_state.todo_list.quick_add_templates
    
    for template in templates:
        if st.button(template['title'], key=f"template_{template['title']}", 
                    help=f"Category: {template['category']} | Priority: {template['priority']}"):
            new_item = TodoItem(
                title=template['title'],
                category=template['category'],
                priority=template['priority']
            )
            st.session_state.todo_list.add_item(new_item)
            st.success(f"Added: {template['title']}")
            time.sleep(1)
            st.rerun()

# Main Content Area
if st.session_state.view_mode == "Dashboard":
    # Dashboard View
    st.markdown("## 📊 Dashboard Overview")
    
    # Key Metrics Row
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>{stats['total']}</h3>
            <p>Total Tasks</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>{stats['pending']}</h3>
            <p>Pending</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3>{stats['completed']}</h3>
            <p>Completed</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <h3>{stats['overdue']}</h3>
            <p>Overdue</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown(f"""
        <div class="metric-card">
            <h3>{stats['due_today']}</h3>
            <p>Due Today</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Charts Row
    col1, col2 = st.columns(2)
    
    with col1:
        # Priority Distribution
        if stats['total'] > 0:
            priority_data = stats['priority_stats']
            fig = px.bar(
                x=list(priority_data.keys()),
                y=[priority_data[p]['pending'] for p in priority_data.keys()],
                title="📋 Pending Tasks by Priority",
                color=[priority_data[p]['pending'] for p in priority_data.keys()],
                color_continuous_scale="Reds"
            )
            fig.update_layout(showlegend=False, height=300)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Category Completion Rate
        if stats['total'] > 0:
            cat_data = stats['category_stats']
            categories = [cat for cat in cat_data.keys() if cat_data[cat]['total'] > 0]
            completion_rates = [cat_data[cat]['completion_rate'] for cat in categories]
            
            fig = px.pie(
                values=completion_rates,
                names=categories,
                title="🎯 Completion Rate by Category"
            )
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
    
    # Recent Activity
    st.markdown("### 🕒 Recent Activity")
    recent_items = sorted(st.session_state.todo_list.items, key=lambda x: x.created_at, reverse=True)[:5]
    
    if recent_items:
        for item in recent_items:
            status_icon = "✅" if item.completed else "⏳"
            priority_class = f"priority-{item.priority.lower()}"
            
            st.markdown(f"""
            <div class="todo-card {'completed' if item.completed else ''}">
                {status_icon} <strong>{item.title}</strong>
                <span class="{priority_class}">({item.priority})</span>
                <br><small>📁 {item.category} | 📅 {item.created_at.strftime('%m/%d/%Y %H:%M')}</small>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No tasks yet. Create your first task to get started!")

elif st.session_state.view_mode == "Tasks":
    # Tasks Management View
    st.markdown("## 📝 Task Management")
    
    # Search and Filter Bar
    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
    
    with col1:
        search_query = st.text_input("🔍 Search tasks...", value=st.session_state.search_query, 
                                   placeholder="Search by title, description, or tags")
        st.session_state.search_query = search_query
    
    with col2:
        filter_category = st.selectbox("Category", ["All"] + st.session_state.todo_list.categories)
    
    with col3:
        filter_priority = st.selectbox("Priority", ["All", "High", "Medium", "Low"])
    
    with col4:
        filter_status = st.selectbox("Status", ["All", "Pending", "Completed", "Overdue"])
    
    # Add New Task Button
    if st.button("➕ Add New Task", type="primary"):
        st.session_state.show_add_form = True
    
    # Add Task Form (in modal-like container)
    if st.session_state.get('show_add_form', False):
        with st.container():
            st.markdown("### ➕ Create New Task")
            
            with st.form("add_task_advanced"):
                col1, col2 = st.columns(2)
                
                with col1:
                    title = st.text_input("Task Title *", placeholder="What needs to be done?")
                    category = st.selectbox("Category", st.session_state.todo_list.categories)
                    priority = st.selectbox("Priority", ["High", "Medium", "Low"], index=1)
                    due_date = st.date_input("Due Date", value=None)
                    due_time = st.time_input("Due Time", value=None)
                
                with col2:
                    description = st.text_area("Description", placeholder="Add more details...")
                    tags = st.text_input("Tags", placeholder="Comma-separated tags")
                    estimated_time = st.number_input("Estimated Hours", min_value=0.0, value=0.0, step=0.5)
                
                # Subtasks
                st.markdown("**Subtasks**")
                subtask_input = st.text_input("Add subtask", placeholder="Enter subtask and press Enter")
                
                col1, col2 = st.columns(2)
                with col1:
                    submitted = st.form_submit_button("Create Task", type="primary")
                with col2:
                    cancelled = st.form_submit_button("Cancel")
                
                if submitted and title:
                    # Combine date and time
                    due_datetime = None
                    if due_date:
                        if due_time:
                            due_datetime = datetime.combine(due_date, due_time)
                        else:
                            due_datetime = datetime.combine(due_date, datetime.min.time())
                    
                    # Process tags
                    tag_list = [tag.strip() for tag in tags.split(',') if tag.strip()] if tags else []
                    
                    new_item = TodoItem(
                        title=title,
                        description=description,
                        priority=priority,
                        due_date=due_datetime,
                        category=category,
                        tags=tag_list
                    )
                    
                    if estimated_time > 0:
                        new_item.estimated_time = estimated_time
                    
                    st.session_state.todo_list.add_item(new_item)
                    st.session_state.show_add_form = False
                    st.success("Task created successfully!")
                    time.sleep(1)
                    st.rerun()
                
                if cancelled:
                    st.session_state.show_add_form = False
                    st.rerun()
    
    # Filter and Display Tasks
    items = st.session_state.todo_list.items
    
    # Apply filters
    if search_query:
        items = st.session_state.todo_list.search_items(search_query)
    
    if filter_category != "All":
        items = [item for item in items if item.category == filter_category]
    
    if filter_priority != "All":
        items = [item for item in items if item.priority == filter_priority]
    
    if filter_status == "Pending":
        items = [item for item in items if not item.completed]
    elif filter_status == "Completed":
        items = [item for item in items if item.completed]
    elif filter_status == "Overdue":
        items = [item for item in items if item.is_overdue()]
    
    # Sort options
    sort_by = st.selectbox("Sort by", ["Created Date", "Due Date", "Priority", "Title"])
    
    if sort_by == "Priority":
        priority_order = {"High": 3, "Medium": 2, "Low": 1}
        items = sorted(items, key=lambda x: priority_order[x.priority], reverse=True)
    elif sort_by == "Due Date":
        items = sorted(items, key=lambda x: x.due_date or datetime.max)
    elif sort_by == "Title":
        items = sorted(items, key=lambda x: x.title.lower())
    else:
        items = sorted(items, key=lambda x: x.created_at, reverse=True)
    
    st.markdown(f"**Showing {len(items)} task(s)**")
    
    # Display Tasks
    if items:
        for item in items:
            # Determine card class
            card_class = "todo-card"
            if item.completed:
                card_class += " completed"
            elif item.is_overdue():
                card_class += " overdue"
            
            # Task card
            with st.container():
                col1, col2, col3 = st.columns([1, 8, 1])
                
                with col1:
                    completed = st.checkbox("", value=item.completed, key=f"check_{item.id}")
                    if completed != item.completed:
                        if completed:
                            item.mark_completed()
                        else:
                            item.mark_uncompleted()
                        st.rerun()
                
                with col2:
                    # Title and priority
                    priority_color = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}
                    status_text = "~~" if item.completed else ""
                    
                    st.markdown(f"""
                    <div class="{card_class}">
                        <h4>{status_text}{item.title}{status_text} {priority_color[item.priority]}</h4>
                        {f"<p>{status_text}{item.description}{status_text}</p>" if item.description else ""}
                        <div style="display: flex; gap: 15px; align-items: center; margin-top: 10px;">
                            <span>📁 {item.category}</span>
                            {f"<span>📅 Due: {item.due_date.strftime('%m/%d/%Y %H:%M')}</span>" if item.due_date else ""}
                            {f"<span>⏱️ Est: {item.estimated_time}h</span>" if item.estimated_time else ""}
                            {f"<span>🏷️ {', '.join(item.tags)}</span>" if item.tags else ""}
                        </div>
                        {f"<div style='margin-top: 10px;'><strong>Subtasks:</strong> {item.get_subtask_progress():.0f}% complete ({len([st for st in item.subtasks if st['completed']])}/{len(item.subtasks)})</div>" if item.subtasks else ""}
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    col_edit, col_delete = st.columns(2)
                    with col_edit:
                        if st.button("✏️", key=f"edit_{item.id}", help="Edit task"):
                            st.session_state.selected_todo = item.id
                    with col_delete:
                        if st.button("🗑️", key=f"delete_{item.id}", help="Delete task"):
                            st.session_state.todo_list.remove_item(item.id)
                            st.rerun()
                
                # Expandable details
                with st.expander(f"📋 Task Details - {item.title}"):
                    det_col1, det_col2 = st.columns(2)
                    
                    with det_col1:
                        st.write(f"**Created:** {item.created_at.strftime('%m/%d/%Y %H:%M')}")
                        if item.completed_at:
                            st.write(f"**Completed:** {item.completed_at.strftime('%m/%d/%Y %H:%M')}")
                        if item.is_overdue():
                            st.error(f"⚠️ Overdue by {abs(item.days_until_due())} days")
                        elif item.days_until_due() is not None:
                            if item.days_until_due() == 0:
                                st.warning("📅 Due today!")
                            elif item.days_until_due() > 0:
                                st.info(f"📅 Due in {item.days_until_due()} days")
                    
                    with det_col2:
                        # Add subtask
                        new_subtask = st.text_input(f"Add subtask to '{item.title}'", key=f"subtask_{item.id}")
                        if st.button("Add Subtask", key=f"add_subtask_{item.id}") and new_subtask:
                            item.add_subtask(new_subtask)
                            st.rerun()
                    
                    # Display subtasks
                    if item.subtasks:
                        st.write("**Subtasks:**")
                        for subtask in item.subtasks:
                            sub_col1, sub_col2 = st.columns([1, 10])
                            with sub_col1:
                                subtask_completed = st.checkbox("", value=subtask['completed'], 
                                                              key=f"subtask_check_{subtask['id']}")
                                if subtask_completed != subtask['completed']:
                                    item.toggle_subtask(subtask['id'])
                                    st.rerun()
                            with sub_col2:
                                status = "~~" if subtask['completed'] else ""
                                st.write(f"{status}{subtask['title']}{status}")
                    
                    # Add note
                    new_note = st.text_area(f"Add note to '{item.title}'", key=f"note_{item.id}")
                    if st.button("Add Note", key=f"add_note_{item.id}") and new_note:
                        item.add_note(new_note)
                        st.rerun()
                    
                    # Display notes
                    if item.notes:
                        st.write("**Notes:**")
                        for note in item.notes:
                            st.write(f"• {note['text']} _{note['created_at'].strftime('%m/%d %H:%M')}_")
                
                st.markdown("---")
    else:
        st.info("No tasks match your current filters. Try adjusting your search criteria.")

elif st.session_state.view_mode == "Analytics":
    # Analytics View
    st.markdown("## 📈 Analytics & Insights")
    
    if stats['total'] == 0:
        st.info("📊 No data available yet. Create some tasks to see analytics!")
    else:
        # Productivity insights
        insights = st.session_state.todo_list.get_productivity_insights()
        
        # Key insights cards
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if insights.get('most_productive_category'):
                st.markdown(f"""
                <div class="metric-card">
                    <h4>🏆 Top Category</h4>
