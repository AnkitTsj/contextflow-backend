import json
import os
import uuid
from datetime import datetime
from typing import Dict, Any, Optional

def save_context(chat_text: str, summary: str, username: str, memory: dict = None) -> str:
    """Save summary + memory with metadata for a specific user"""
    session_id = str(uuid.uuid4())[:8]
    
    user_storage_dir = f"storage/{username}"
    os.makedirs(user_storage_dir, exist_ok=True)
    
    data = {
        "session_id": session_id,
        "username": username,
        "timestamp": datetime.now().isoformat(),
        "version": "2.0",
        "input": chat_text,
        "input_length": len(chat_text),
        "summary": summary,
        "summary_length": len(summary),
        "memory": memory or {}  
    }
    
    with open(f"{user_storage_dir}/{session_id}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    return session_id


def load_context(session_id: str, username: str) -> Dict[str, Any]:
    """Load context for specific user"""
    user_storage_dir = f"storage/{username}"
    with open(f"{user_storage_dir}/{session_id}.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        if data.get("username") != username:
            raise FileNotFoundError("Session not found")
        return data

def list_sessions(username: str) -> list:
    """List all saved sessions for specific user"""
    sessions = []
    user_storage_dir = f"storage/{username}"
    
    if not os.path.exists(user_storage_dir):
        return sessions
    
    for filename in os.listdir(user_storage_dir):
        if filename.endswith('.json'):
            try:
                session_id = filename[:-5]  
                data = load_context(session_id, username)
                sessions.append({
                    "session_id": session_id,
                    "timestamp": data.get("timestamp"),
                    "input_length": data.get("input_length", 0),
                    "preview": data.get("input", "")[:100] + "..." if len(data.get("input", "")) > 100 else data.get("input", "")
                })
            except:
                continue
    
    sessions.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
    return sessions

def delete_all_sessions(username: str):
    """Delete all sessions for specific user"""
    user_storage_dir = f"storage/{username}"
    if not os.path.exists(user_storage_dir):
        return
    
    for fname in os.listdir(user_storage_dir):
        if fname.endswith('.json'):
            os.remove(os.path.join(user_storage_dir, fname))
def delete_session(session_id: str, username: str):
    """Delete a single session for a specific user"""
    user_storage_dir = f"storage/{username}"
    file_path = os.path.join(user_storage_dir, f"{session_id}.json")
    if not os.path.exists(file_path):
        raise FileNotFoundError("Session not found")
    os.remove(file_path)
