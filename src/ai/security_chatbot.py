import openai
import os
from datetime import datetime
import json
import logging
from typing import Dict, List, Optional
from functools import wraps

def handle_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"Error in {func.__name__}: {str(e)}")
            return {
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "status": "error"
            }
    return wrapper

class SecurityChatbot:
    def __init__(self, api_key: str):
        self.api_key = api_key
        openai.api_key = api_key
        self.logger = logging.getLogger(__name__)
        self.setup_logging()
        self.conversation_history: List[Dict] = []
        self.max_history = 5

    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

    def add_to_history(self, role: str, content: str):
        """Add a message to the conversation history."""
        self.conversation_history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
        # Keep only the last N messages
        self.conversation_history = self.conversation_history[-self.max_history:]

    @handle_errors
    def get_security_analysis(self, query: str, context: Optional[Dict] = None) -> Dict:
        """Get security analysis for a specific query."""
        messages = [
            {"role": "system", "content": """You are a security expert assistant. 
            Provide detailed security analysis and recommendations based on the query.
            Focus on:
            1. Security implications
            2. Best practices
            3. Potential vulnerabilities
            4. Remediation steps"""},
            {"role": "user", "content": query}
        ]

        if context:
            messages.append({"role": "system", "content": f"Context: {json.dumps(context)}"})

        messages.extend(self.conversation_history)

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )

        analysis = response.choices[0].message.content
        self.add_to_history("assistant", analysis)

        return {
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "analysis": analysis,
            "confidence_score": response.choices[0].finish_reason,
            "status": "success"
        }

    @handle_errors
    def get_threat_intelligence(self, threat_data: Dict) -> Dict:
        """Get threat intelligence analysis for detected threats."""
        return self.get_security_analysis(
            f"Analyze this security threat and provide detailed intelligence: {json.dumps(threat_data)}",
            {"analysis_type": "threat_intelligence"}
        )

    @handle_errors
    def get_compliance_check(self, compliance_data: Dict) -> Dict:
        """Check compliance requirements and provide recommendations."""
        return self.get_security_analysis(
            f"Analyze these compliance requirements: {json.dumps(compliance_data)}",
            {"analysis_type": "compliance_check"}
        )

    @handle_errors
    def get_remediation_steps(self, issue_data: Dict) -> Dict:
        """Get detailed remediation steps for security issues."""
        return self.get_security_analysis(
            f"Provide detailed remediation steps for this security issue: {json.dumps(issue_data)}",
            {"analysis_type": "remediation"}
        )

if __name__ == "__main__":
    # Example usage
    chatbot = SecurityChatbot(os.getenv("OPENAI_API_KEY"))

    # Example security analysis
    analysis = chatbot.get_security_analysis(
        "Analyze the security implications of using JWT tokens for authentication"
    )
    print(json.dumps(analysis, indent=2))

    # Example threat intelligence
    threat_data = {
        "type": "suspicious_login",
        "severity": "high",
        "source_ip": "192.168.1.100",
        "timestamp": datetime.now().isoformat()
    }
    intelligence = chatbot.get_threat_intelligence(threat_data)
    print(json.dumps(intelligence, indent=2)) 