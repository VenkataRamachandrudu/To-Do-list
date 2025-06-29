import streamlit as st
from datetime import datetime
from main import TodoList, TodoItem
import plotly.express as px

# --- Page Config ---
st.set_page_config("Todo App", "✅", layout="wide")
st.title("📝 Todo List")

# --- Initialize ---
if 'todo_list' not in st.session_state:
    st.session_state.todo_list = TodoList()

# --- Sidebar: Add Todo ---
with st.sidebar:
    st.header("Add Todo")
    with st.form("todo_form"):
        title = st.text_input("Title")
        priority = st.selectbox("Priority", ["Low", "Medium", "High"])
        due_date = st.date_input("Due Date")
        submitted = st.form_submit_button("Add")
        
        if submitted and title:
            item = TodoItem(
                title=title,
                priority=priority,
                due_date=datetime.combine(due_date, datetime.min.time())
            )
            st.session_state.todo_list.add_item(item)
            st.success("Added!")
            st.rerun()

# --- Filter & Display Todos ---
filter_option = st.selectbox("Filter Todos", ["All", "Pending", "Completed"])
if filter_option == "Pending":
    todos = st.session_state.todo_list.get_pending_items()
elif filter_option == "Completed":
    todos = st.session_state.todo_list.get_completed_items()
else:
    todos = st.session_state.todo_list.items

for idx, todo in enumerate(todos):
    original_idx = st.session_state.todo_list.items.index(todo)
    cols = st.columns([1, 6, 1])
    completed = cols[0].checkbox("", value=todo.completed, key=f"done_{original_idx}")
    
    if completed != todo.completed:
        todo.mark_completed() if completed else todo.mark_uncompleted()
        st.rerun()
    
    title = f"~~{todo.title}~~" if todo.completed else todo.title
    cols[1].markdown(f"**{title}**")
    
    if cols[2].button("❌", key=f"del_{original_idx}"):
        st.session_state.todo_list.remove_item(original_idx)
        st.rerun()

# --- Statistics ---
st.markdown("## 📊 Statistics")
stats = st.session_state.todo_list.get_completion_stats()
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total", stats['total'])
col2.metric("Done", stats['completed'])
col3.metric("Pending", stats['pending'])
col4.metric("Rate", f"{stats['completion_rate']:.1f}%")

if stats['total'] > 0:
    fig = px.pie(
        values=[stats['completed'], stats['pending']],
        names=["Completed", "Pending"],
        title="Task Status"
    )
    st.plotly_chart(fig, use_container_width=True)

# --- Footer ---
st.markdown("---")
st.markdown("Crafted with ❤️ using Streamlit")
