import re
from typing import Dict, List, Tuple

class ChatParser:
    @staticmethod
    def detect_format(chat_text: str) -> str:
        """Detect which AI platform the chat is from"""
        text_lower = chat_text.lower()
        
        if re.search(r'chatgpt|openai|gpt-\d', text_lower):
            return "chatgpt"
        
        if re.search(r'claude|anthropic', text_lower):
            return "claude"
        
        if re.search(r'gemini|bard|google ai', text_lower):
            return "gemini"
        
        if re.search(r'perplexity', text_lower):
            return "perplexity"
        
        return "unknown"
    
    @staticmethod
    def clean_chat(chat_text: str) -> str:
        """Clean and normalize chat text"""

        cleaned = re.sub(r'\n\s*\n\s*\n', '\n\n', chat_text)

        cleaned = re.sub(r'\d{1,2}:\d{2}(?:\s*[AP]M)?', '', cleaned)
        

        cleaned = re.sub(r'(Copy|Share|Like|Dislike)\s*$', '', cleaned, flags=re.MULTILINE)
        
        return cleaned.strip()
    
    @staticmethod
    def extract_messages(chat_text: str) -> List[Tuple[str, str]]:
        """Extract user and AI messages from chat"""
        messages = []
        
        lines = chat_text.split('\n')
        current_speaker = None
        current_message = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            if line.startswith(('User:', 'You:', 'Human:')):
                if current_speaker and current_message:
                    messages.append((current_speaker, '\n'.join(current_message)))
                current_speaker = 'user'
                current_message = [line.split(':', 1)[1].strip()]
            elif line.startswith(('AI:', 'Assistant:', 'ChatGPT:', 'Claude:', 'Gemini:')):
                if current_speaker and current_message:
                    messages.append((current_speaker, '\n'.join(current_message)))
                current_speaker = 'assistant'
                current_message = [line.split(':', 1)[1].strip()]
            else:
                if current_message:
                    current_message.append(line)
        
        if current_speaker and current_message:
            messages.append((current_speaker, '\n'.join(current_message)))
        
        return messages
