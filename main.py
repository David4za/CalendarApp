import tempfile
import streamlit as st

from ics import Calendar, Event
from datetime import datetime, timedelta

st.title("Calendar Invite Creation")

if "events" not in st.session_state:
    st.session_state.events = []
    
st.subheader("Add Event")
col1 = st.columns(1)
with col1:
    event_name = st.text_input("Event Name","")
    event_description = st.text_area("Event description", "")

selected_date = st.date_input("Select date", datetime.today())
start_time = st.time_input("Select start time", value=datetime.strptime("18:30", "%H:%M").time())
duration = st.slider("Event duration (hours)", 1, 8, 1)


if st.button("Add Event", key="add-event"):
    start_datetime = datetime.combine(selected_date, start_time)
    end_datetime = start_datetime + timedelta(hours=duration)
    
    st.session_state.events.append({
        "name":event_name,
        "description":event_description,
        "start": start_datetime,
        "end": end_datetime
    })
    
    st.success(f"Added: {event_name} on {selected_date}")

if st.session_state.events:
    st.subheader("Event Added")
    for (i, event) in enumerate(st.session_state.events, 1):
        st.markdown(f"{i}, {event["name"]} at {event["start"]} till {event["end"]}")
    
    if st.button("Generate", key="generate-btn"):
        try:
            c = Calendar()            
            for evt in st.session_state.events:
                e = Event()
                e.name = evt["name"]
                e.description = evt["description"]
                e.begin = evt["start"]
                e.end = evt["end"]
                c.events.add(e)
                
            with tempfile.NamedTemporaryFile(delete=False, suffix=".ics", mode="w") as f:
                f.writelines(c)
                tmp_file_path = f.name
            
            with open(tmp_file_path, "rb") as file:
                st.success("File Created")
                st.download_button(
                    label="Download calendar events.ics",
                    data=file,
                    file_name="calendar_events.ics",
                    mime="text/calendar",
                    key="download-btn"
                )
        except Exception as e:
            st.error(f"something went wrong with {e}")
        
else:
    st.info("No events added yet")
