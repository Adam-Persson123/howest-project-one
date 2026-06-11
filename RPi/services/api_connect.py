import gradio as gr
import httpx
import pandas as pd

class_url = "http://localhost:8000/class/"
detection_url = "http://localhost:8000/detection/"
log_url = "http://localhost:8000/log/"
session_url = "http://localhost:8000/session/"

def fetch_class_data():
    global class_url
    try:
        r = httpx.get(class_url)
        r.raise_for_status()  
        return pd.DataFrame(r.json())
    except httpx.HTTPStatusError as e:
        print(f"HTTP error occurred: {e}")
    except httpx.RequestError as e:
        print(f"Request error occurred: {e}")
    except ValueError as e:
        print(f"Failed to decode JSON: {e}")
    return None

def fetch_detection_data():
    global detection_url
    try:
        r = httpx.get(detection_url)
        r.raise_for_status()  
        return pd.DataFrame(r.json())
    except httpx.HTTPStatusError as e:
        print(f"HTTP error occurred: {e}")
    except httpx.RequestError as e:
        print(f"Request error occurred: {e}")
    except ValueError as e:
        print(f"Failed to decode JSON: {e}")
    return None

def fetch_log_data():
    global log_url
    try:
        r = httpx.get(log_url)
        r.raise_for_status()  
        return pd.DataFrame(r.json())
    except httpx.HTTPStatusError as e:
        print(f"HTTP error occurred: {e}")
    except httpx.RequestError as e:
        print(f"Request error occurred: {e}")
    except ValueError as e:
        print(f"Failed to decode JSON: {e}")
    return None

def fetch_session_data():
    global session_url
    try:
        r = httpx.get(session_url)
        r.raise_for_status()  
        return pd.DataFrame(r.json())
    except httpx.HTTPStatusError as e:
        print(f"HTTP error occurred: {e}")
    except httpx.RequestError as e:
        print(f"Request error occurred: {e}")
    except ValueError as e:
        print(f"Failed to decode JSON: {e}")
    return Noned

#######################

def load_classes():
    df = fetch_class_data()
    if df is None or df.empty:
        return pd.DataFrame(columns=['Class ID', 'Name', 'Description'])
    df = df[['id', 'name', 'description']]
    df.columns = ['Class ID', 'Name', 'Description']
    return df

def load_detections():
    df = fetch_detection_data()
    if df is None or df.empty:
        return pd.DataFrame(columns=['Detection ID', 'Class', 'Confidence', 'Timestamp'])
    df = df[['id', 'class_id', 'confidence', 'timestamp']]
    df.columns = ['Detection ID', 'Class', 'Confidence', 'Timestamp']
    return df

def load_logs():    
    df = fetch_log_data()
    if df is None or df.empty:
        return pd.DataFrame(columns=['Log ID', 'Type', 'Log', 'Timestamp'])
    df = df[['id', 'type', 'log', 'timestamp']]
    df.columns = ['Log ID', 'Type', 'Log', 'Timestamp']
    return df

def load_sessions():
    df = fetch_session_data()
    if df is None or df.empty:
        return pd.DataFrame(columns=['Session ID', 'Start', 'End'])
    df = df[['id', 'time_from', 'time_to']]
    df.columns = ['Session ID', 'Start', 'End']
    return df

#######################

def create_new_detection(class_id, confidence, timestamp):
    global detection_url
    data = {
        "class_id": class_id,
        "confidence": confidence,
        "timestamp": timestamp
    }
    try:
        r = httpx.post(detection_url, json=data)
        r.raise_for_status()  
        return r.json()
    except httpx.HTTPStatusError as e:
        print(f"HTTP error occurred: {e}")
    except httpx.RequestError as e:
        print(f"Request error occurred: {e}")
    except ValueError as e:
        print(f"Failed to decode JSON: {e}")
    return None

def create_new_log(type, log, timestamp):
    global log_url
    data = {
        "type": type,
        "log": log,
        "timestamp": timestamp
    }
    try:
        r = httpx.post(log_url, json=data)
        r.raise_for_status()  
        return r.json()
    except httpx.HTTPStatusError as e:
        print(f"HTTP error occurred: {e}")
    except httpx.RequestError as e:
        print(f"Request error occurred: {e}")
    except ValueError as e:
        print(f"Failed to decode JSON: {e}")
    return None

def create_new_session(time_from, time_to):
    global session_url
    data = {
        "time_from": time_from,
        "time_to": time_to
    }
    try:
        r = httpx.post(session_url, json=data)
        r.raise_for_status()  
        return r.json()
    except httpx.HTTPStatusError as e:
        print(f"HTTP error occurred: {e}")
    except httpx.RequestError as e:
        print(f"Request error occurred: {e}")
    except ValueError as e:
        print(f"Failed to decode JSON: {e}")
    return None

#######################

def delete_detection(id):
    global detection_url
    try:
        r = httpx.delete(f"{detection_url}{id}")
        r.raise_for_status()  
        return r.json()
    except httpx.HTTPStatusError as e:
        print(f"HTTP error occurred: {e}")
    except httpx.RequestError as e:
        print(f"Request error occurred: {e}")
    except ValueError as e:
        print(f"Failed to decode JSON: {e}")
    return None

def delete_all_detections():
    global detection_url
    try:
        r = httpx.delete(f"{detection_url}")
        r.raise_for_status()  
        return r.json()
    except httpx.HTTPStatusError as e:
        print(f"HTTP error occurred: {e}")
    except httpx.RequestError as e:
        print(f"Request error occurred: {e}")
    except ValueError as e:
        print(f"Failed to decode JSON: {e}")
    return None

def delete_log(id):
    global log_url
    try:
        r = httpx.delete(f"{log_url}{id}")
        r.raise_for_status()  
        return r.json()
    except httpx.HTTPStatusError as e:
        print(f"HTTP error occurred: {e}")
    except httpx.RequestError as e:
        print(f"Request error occurred: {e}")
    except ValueError as e:
        print(f"Failed to decode JSON: {e}")
    return None

def delete_session(id):
    global session_url
    try:
        r = httpx.delete(f"{session_url}{id}")
        r.raise_for_status()  
        return r.json()
    except httpx.HTTPStatusError as e:
        print(f"HTTP error occurred: {e}")
    except httpx.RequestError as e:
        print(f"Request error occurred: {e}")
    except ValueError as e:
        print(f"Failed to decode JSON: {e}")
    return None

def delete_all_sessions():
    global session_url
    try:
        r = httpx.delete(f"{session_url}")
        r.raise_for_status()  
        return r.json()
    except httpx.HTTPStatusError as e:
        print(f"HTTP error occurred: {e}")
    except httpx.RequestError as e:
        print(f"Request error occurred: {e}")
    except ValueError as e:
        print(f"Failed to decode JSON: {e}")
    return None

#######################

def get_class_choices():
    df = fetch_class_data()
    if df is None or df.empty:
        return []
    return df["name"].tolist()

def get_class_id_from_name(class_name):
    df = fetch_class_data()
    if df is None or df.empty:
        return None
    return df[df["name"] == class_name]["id"].values[0]

def get_class_name_from_id(class_id):
    df = fetch_class_data()
    if df is None or df.empty:
        return None
    return df[df["id"] == class_id]["name"].values[0]

#######################

def get_log_types():
    df = fetch_log_data()
    return df["type"].unique().tolist()

def get_logs_by_type(type):
    global log_url
    try:
        r = httpx.get(log_url + "type/" + type)
        r.raise_for_status()  
        return pd.DataFrame(r.json())
    except httpx.HTTPStatusError as e:
        print(f"HTTP error occurred: {e}")
    except httpx.RequestError as e:
        print(f"Request error occurred: {e}")
    except ValueError as e:
        print(f"Failed to decode JSON: {e}")
    return None

#######################

def get_detections_by_class_name(class_name):
    global detection_url
    class_id = get_class_id_from_name(class_name)
    try:
        r = httpx.get(f"{detection_url}class/{class_id}")
        r.raise_for_status()  
        return pd.DataFrame(r.json())
    except httpx.HTTPStatusError as e:
        print(f"HTTP error occurred: {e}")
    except httpx.RequestError as e:
        print(f"Request error occurred: {e}")
    except ValueError as e:
        print(f"Failed to decode JSON: {e}")
    return None

def get_latest_detection():
    df = load_detections()
    if df is None or df.empty:
        return None
    df = df.sort_values("Timestamp")
    last_index = df.index[-1]
    class_id = df.loc[last_index, "Class"]
    class_name = get_class_name_from_id(class_id)
    df.loc[last_index, "Class Name"] = class_name
    return df.loc[last_index]