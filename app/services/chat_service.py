from typing import Dict, List
import random

class ChatService:
    def __init__(self):
        self.knowledge_base = {
            "jobs": [
                "I can definitely help you find work! We have quite a few remote and freelance opportunities across Cambodia right now.",
                "Searching for a job? You're in the right place. Have you looked at our development or design sections yet?",
                "There are some great freelance openings lately. I'd recommend searching for specific skills like 'React' or 'Node' to find the best fit."
            ],
            "pricing": [
                "Great question! KhmerWork is actually 100% free for job seekers. You'll never have to pay a cent to apply.",
                "Pricing-wise, we keep it free for talent. Employers have premium options starting at $29/month, but searching is always free for you!",
                "You can apply to as many jobs as you want for free. We support payments via ABA or Wing if you're an employer looking for premium features."
            ],
            "contact": [
                "You can always reach out to our team at support@khmerwork.com. They're super responsive!",
                "Our main office is in Phnom Penh, though we're a remote-first platform. Need help with something specific?",
                "Feel free to drop us an email or follow our Telegram channel for the quickest updates."
            ],
            "hiring": [
                "Looking to hire? That's awesome! You just need to create an Employer account to get started.",
                "Our AI actually helps you filter resumes so you find the best talent faster. It's a huge time-saver.",
                "Featured posts really help! They get about 5x more visibility. Would you like to know more about our employer tiers?"
            ],
            "profile": [
                "Pro tip: A complete profile makes you 3x more likely to get hired. Have you added your portfolio yet?",
                "I definitely recommend uploading a clean resume. Our AI can even scan it to help match you with the best roles!",
                "Make sure your skills section is up to date. It really helps employers find you in the search results."
            ],
            "ai": [
                "I'm the platform's AI assistant! I use some pretty cool matching algorithms to connect talent with the right jobs.",
                "Basically, I analyze skills and job descriptions to make sure everyone finds their perfect match.",
                "I'm constantly learning from how people use the platform to get even better at recommending jobs!"
            ]
        }
        
        self.fillers = [
            "Let me check that for you...",
            "Oh, I can help with that!",
            "That's a great question.",
            "Sure thing!",
            "I'd be happy to explain.",
            "Interesting! Here's the deal:",
        ]

        self.closers = [
            "Does that make sense?",
            "Is there anything else I can help you with?",
            "Hope that helps! Anything else?",
            "Want to know more about that?",
            "I'm here if you have more questions!",
        ]

        self.greetings = [
            "Hey! How's your day going? How can I help you on KhmerWork?",
            "Hi there! Looking for a new opportunity today?",
            "Hello! I'm your AI assistant. What can I do for you?",
            "Greetings! Ready to find your next big project?",
        ]

        self.unknown = [
            "Hmm, I'm not entirely sure about that yet. I'm still learning!",
            "That's a bit out of my current knowledge base. Want to talk about jobs or pricing instead?",
            "I didn't quite catch that. Could you try rephrasing? I can help with job searches, profiles, and more.",
        ]

    async def get_response(self, message: str) -> str:
        message = message.lower().strip()
        
        if not message:
            return "I'm listening! What can I help you with?"

        # Intent detection
        intent = self._detect_intent(message)
        
        # Build response
        if intent == "greeting":
            return random.choice(self.greetings)
        
        if intent in self.knowledge_base:
            main_response = random.choice(self.knowledge_base[intent])
            
            # Occasionally add a filler or closer to sound more human
            if random.random() > 0.5:
                filler = random.choice(self.fillers)
                return f"{filler} {main_response}"
            
            if random.random() > 0.7:
                closer = random.choice(self.closers)
                return f"{main_response} {closer}"
            
            return main_response
            
        return random.choice(self.unknown)

    def _detect_intent(self, message: str) -> str:
        # Simple rule-based intent detection
        patterns = {
            "greeting": ["hi", "hello", "hey", "greetings", "good morning", "good afternoon"],
            "jobs": ["job", "work", "find", "remote", "freelance", "opportunity", "opening"],
            "pricing": ["price", "cost", "pay", "free", "tier", "subscription", "money"],
            "contact": ["contact", "support", "email", "help", "reach", "office", "telegram"],
            "hiring": ["hire", "employer", "post", "candidate", "talent", "recruitment"],
            "profile": ["profile", "resume", "cv", "portfolio", "skills", "experience"],
            "ai": ["ai", "smart", "how do you work", "assistant", "bot"]
        }

        # Check for direct matches
        for intent, keywords in patterns.items():
            if any(keyword in message for keyword in keywords):
                return intent
                
        return "unknown"
