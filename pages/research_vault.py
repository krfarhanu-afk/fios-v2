import streamlit as st

# --- PAGE CONFIG ---
st.set_page_config(page_title="Research Vault", page_icon="📓", layout="wide")

# --- SESSION STATE INITIALIZATION ---
if 'notes' not in st.session_state:
    st.session_state.notes = [
        {"title": "Initial Thoughts on Q4", "content": "The upcoming earnings season looks to be pivotal, especially for the tech sector. Watching for margin compression."},
        {"title": "Macro Thesis", "content": "If inflation remains sticky above 3.5%, the Fed may be forced into one more hike than the market expects."}
    ]

# --- UI LAYOUT ---
st.title("Research Vault")
st.write("Your personal space for market thoughts, ideas, and research.")

st.divider()

# --- NOTE EDITOR ---
st.subheader("New Note")
with st.form(key="note_form", clear_on_submit=True):
    new_title = st.text_input("Title")
    new_content = st.text_area("Content")
    submit_button = st.form_submit_button(label="Add Note")

    if submit_button and new_title and new_content:
        st.session_state.notes.append({"title": new_title, "content": new_content})
        st.success("Note added!")

st.divider()

# --- DISPLAY NOTES ---
st.subheader("Your Notes")
if not st.session_state.notes:
    st.info("You haven't added any notes yet.")
else:
    for i, note in enumerate(reversed(st.session_state.notes)):
        with st.expander(f"{note['title']}"):
            st.write(note['content'])
            if st.button("Delete", key=f"delete_{i}"):
                # This will delete the note from the original list
                st.session_state.notes.remove(note)
                st.rerun()