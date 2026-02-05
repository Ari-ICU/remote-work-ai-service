from typing import Dict, List
import random

class ChatService:
    def __init__(self):
        self.knowledge_base = {
            "jobs": [
                "I can help you find remote, freelance, and full-time jobs across Cambodia.",
                "Currently, we have many openings in Software Development, Graphic Design, and Digital Marketing.",
                "To find the best matches, try searching for specific skills like 'React', 'Node.js', or 'Figma' in our job portal."
            ],
            "pricing": [
                "KhmerWork is 100% free for job seekers. You will never be charged for apply to jobs.",
                "For employers, we offer a Free tier (1 active post) and Premium tiers starting from $29/month for multiple featured posts.",
                "Payment can be made via ABA, Wing, or ACLEDA for your convenience."
            ],
            "contact": [
                "You can reach our support team at support@khmerwork.com.",
                "Our office is located in Phnom Penh, but we operate primarily as a remote-first platform.",
                "Follow us on Telegram and Facebook for the latest platform updates."
            ],
            "hiring": [
                "To hire talent, first create an Employer account.",
                "Our AI helps you filter through hundreds of resumes to find the top 1% of candidates.",
                "Featured job postings get 5x more applications and are pinned to the top of search results."
            ],
            "profile": [
                "A complete profile increases your chances of getting hired by 3x.",
                "Make sure to add your skills and portfolio to stand out.",
                "Our AI can analyze your resume and suggest improvements."
            ],
            "ai": [
                "I use advanced AI to match your skills with the best job opportunities.",
                "I can also help you generate professional job descriptions.",
                "Currently, I'm learning more about the Cambodian job market every day!"
            ]
        }
        
        self.greetings = ["Hello! How can I help you navigate KhmerWork today?", "Hi! Looking for a job or looking to hire?", "Greetings! I'm your AI assistant. What's on your mind?"]
        self.unknown = [
            "I'm still learning about that specific topic. Would you like to know about available jobs, pricing, or how to improve your profile?",
            "That's a great question! While I don't have the exact answer yet, I can assist you with job searching or profile optimization.",
            "I'm not sure about that. Try asking me about 'how to find jobs' or 'pricing for employers'."
        ]

    async def get_response(self, message: str) -> str:
        message = message.lower()
        
        # Priority mapping
        patterns = {
            "hi": self.greetings,
            "hello": self.greetings,
            "hey": self.greetings,
            "job": self.knowledge_base["jobs"],
            "work": self.knowledge_base["jobs"],
            "find": self.knowledge_base["jobs"],
            "price": self.knowledge_base["pricing"],
            "cost": self.knowledge_base["pricing"],
            "free": self.knowledge_base["pricing"],
            "pay": self.knowledge_base["pricing"],
            "contact": self.knowledge_base["contact"],
            "support": self.knowledge_base["contact"],
            "email": self.knowledge_base["contact"],
            "hire": self.knowledge_base["hiring"],
            "employer": self.knowledge_base["hiring"],
            "post": self.knowledge_base["hiring"],
            "profile": self.knowledge_base["profile"],
            "resume": self.knowledge_base["profile"],
            "cv": self.knowledge_base["profile"],
            "ai": self.knowledge_base["ai"],
            "smart": self.knowledge_base["ai"]
        }

        for keyword, responses in patterns.items():
            if keyword in message:
                return random.choice(responses)
            
        return random.choice(self.unknown)
