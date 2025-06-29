import streamlit as st
import pandas as pd
from datetime import datetime, date
import plotly.express as px
import plotly.graph_objects as go
from main import TodoList, TodoItem

# Configure Streamlit page
st.set_page_config(
    page_title="Todo List App",
    page_icon="✅",
    layout="wide"
)

# Initialize session state
if 'todo_list' not in st.session_state:
    st.session_state.todo_list = TodoList()

# Title
st.title("📝 Todo List Manager")

# Sidebar for adding new todos
with st.sidebar:
    st.header("Add New Todo")
    
    with st.form("add_todo"):
        title = st.text_input("Title", placeholder="Enter todo title...")
        description = st.text_area("Description", placeholder="Optional description...")
        priority = st.selectbox("Priority", ["Low", "Medium", "High"])
        due_date = st.date_input("Due Date", value=None)
        
        submitted = st.form_submit_button("Add Todo")
        
        if submitted and title:
            # Convert date to datetime if provided
            due_datetime = datetime.combine(due_date, datetime.min.time()) if due_date else None
            
            new_item = TodoItem(
                title=title,
                description=description,
                priority=priority,
                due_date=due_datetime
            )
            st.session_state.todo_list.add_item(new_item)
            st.success("Todo added successfully!")
            st.rerun()

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.header("Your Todos")
    
    # Filter options
    filter_option = st.selectbox("Filter", ["All", "Pending", "Completed"])
    
    # Get filtered items
    if filter_option == "Pending":
        items = st.session_state.todo_list.get_pending_items()
    elif filter_option == "Completed":
        items = st.session_state.todo_list.get_completed_items()
    else:
        items = st.session_state.todo_list.items
    
    # Display todos
    if items:
        for i, item in enumerate(items):
            # Find the original index
            original_index = st.session_state.todo_list.items.index(item)
            
            with st.container():
                col_check, col_content, col_delete = st.columns([1, 8, 1])
                
                with col_check:
                    completed = st.checkbox("", value=item.completed, key=f"check_{original_index}")
                    if completed != item.completed:
                        if completed:
                            item.mark_completed()
                        else:
                            item.mark_uncompleted()
                        st.rerun()
                
                with col_content:
                    if item.completed:
                        st.markdown(f"~~**{item.title}**~~")
                        if item.description:
                            st.markdown(f"~~{item.description}~~")
                    else:
                        st.markdown(f"**{item.title}**")
                        if item.description:
                            st.markdown(item.description)
                    
                    # Show priority and due date
                    info_cols = st.columns(3)
                    with info_cols[0]:
                        color = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}
                        st.write(f"{color[item.priority]} {item.priority}")
                    
                    with info_cols[1]:
                        if item.due_date:
                            st.write(f"📅 Due: {item.due_date.strftime('%Y-%m-%d')}")
                    
                    with info_cols[2]:
                        st.write(f"📝 Created: {item.created_at.strftime('%m/%d')}")
                
                with col_delete:
                    if st.button("🗑️", key=f"delete_{original_index}"):
                        st.session_state.todo_list.remove_item(original_index)
                        st.rerun()
                
                st.divider()
    else:
        st.info("No todos found. Add some todos using the sidebar!")

with col2:
    st.header("Statistics")
    
    stats = st.session_state.todo_list.get_completion_stats()
    
    # Display stats
    st.metric("Total Todos", stats['total'])
    st.metric("Completed", stats['completed'])
    st.metric("Pending", stats['pending'])
    st.metric("Completion Rate", f"{stats['completion_rate']:.1f}%")
    
    # Progress bar
    if stats['total'] > 0:
        st.progress(stats['completion_rate'] / 100)
    
    # Pie chart
    if stats['total'] > 0:
        fig = px.pie(
            values=[stats['completed'], stats['pending']],
            names=['Completed', 'Pending'],
            title="Todo Status Distribution"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Clear completed button
    if stats['completed'] > 0:
        if st.button("Clear Completed Todos"):
            st.session_state.todo_list.items = [item for item in st.session_state.todo_list.items if not item.completed]
            st.rerun()

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit")
