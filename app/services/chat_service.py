import os
import joblib
import random
import logging
from typing import Dict, List
from app.utils.config import settings
from openai import OpenAI

logger = logging.getLogger(__name__)

class ChatService:
    def __init__(self):
        self.model_path = "app/ml_models/intent_model.joblib"
        self.model = self._load_model()
        self.api_key = settings.OPENAI_API_KEY
        self.client = OpenAI(api_key=self.api_key) if self.api_key else None
        
        self.knowledge_base = {
            "jobs": [
                "I can definitely help you find work! We have quite a few remote and freelance opportunities across Cambodia right now.",
                "Searching for a job? You're in the right place. Have you looked at our development or design sections yet?",
                "There are some great freelance openings lately. I'd recommend searching for specific skills like 'React' or 'Node' to find the best fit.",
                "I've seen some exciting new roles posted today. What kind of work are you specifically interested in?",
                "We've got a lot of companies hiring right now! Are you looking for something full-time or more of a side gig?",
                "The job market is quite active! I can show you some of the latest tech or creative roles if you'd like."
            ],
            "pricing": [
                "Great question! KhmerWork is actually 100% free for job seekers. You'll never have to pay a cent to apply.",
                "Pricing-wise, we keep it free for talent. Employers have premium options starting at $29/month, but searching is always free for you!",
                "You can apply to as many jobs as you want for free. We support payments via ABA or Wing if you're an employer looking for premium features.",
                "It's totally free for freelancers. We want to make sure everyone has access to opportunities without any barriers.",
                "No hidden fees for job seekers, I promise! We just want to help you find your next big break.",
                "You don't need a credit card to apply for jobs here. It's completely free for all our amazing talents."
            ],
            "contact": [
                "You can always reach out to our team at support@khmerwork.com. They're super responsive!",
                "Our main office is in Phnom Penh, though we're a remote-first platform. Need help with something specific?",
                "Feel free to drop us an email or follow our Telegram channel for the quickest updates.",
                "If you need immediate assistance, our support team is available Monday through Friday.",
                "You can find us on Facebook and LinkedIn too! We're always happy to chat with our community.",
                "Drop us a line anytime. We usually get back to people within 24 hours."
            ],
            "hiring": [
                "Looking to hire? That's awesome! You just need to create an Employer account to get started.",
                "Our AI actually helps you filter resumes so you find the best talent faster. It's a huge time-saver.",
                "Featured posts really help! They get about 5x more visibility. Would you like to know more about our employer tiers?",
                "Finding the right talent is key. Have you checked out our resume parsing feature yet? It makes screening much easier.",
                "We have a massive pool of local talent! I can help you find exactly who you need for your project.",
                "Getting started as an employer is easy. Just post your first job and our AI will start matching you with candidates!"
            ],
            "profile": [
                "Pro tip: A complete profile makes you 3x more likely to get hired. Have you added your portfolio yet?",
                "I definitely recommend uploading a clean resume. Our AI can even scan it to help match you with the best roles!",
                "Make sure your skills section is up to date. It really helps employers find you in the search results.",
                "Your profile is your digital business card. Adding a professional photo and a bio can really make you stand out.",
                "Don't forget to link your GitHub or Behance! Employers love seeing real-world examples of your work.",
                "A strong bio goes a long way. Tell your story and let companies know why you're the perfect fit!"
            ],
            "ai": [
                "I'm the platform's AI assistant! I use some pretty cool matching algorithms to connect talent with the right jobs.",
                "Basically, I analyze skills and job descriptions to make sure everyone finds their perfect match.",
                "I'm constantly learning from how people use the platform to get even better at recommending jobs!",
                "My goal is to make the job search process as smooth as possible using data and smart matching.",
                "I might be a bot, but I'm here to make your experience on KhmerWork feel a lot more personal!",
                "Think of me as your personal career scout. I'm always looking for the best matches for you."
            ]
        }
        
        self.fillers = [
            "Let me check that for you...",
            "Oh, I can help with that!",
            "That's a great question.",
            "Sure thing!",
            "I'd be happy to explain.",
            "Interesting! Here's the deal:",
            "I see! ",
            "Got it. ",
            "Absolutely! "
        ]

        self.closers = [
            "Does that make sense?",
            "Is there anything else I can help you with?",
            "Hope that helps! Anything else?",
            "Want to know more about that?",
            "I'm here if you have more questions!",
            "Feel free to ask anything else about KhmerWork."
        ]

        self.greetings = [
            "Hey! How's your day going? How can I help you on KhmerWork?",
            "Hi there! Looking for a new opportunity today?",
            "Hello! I'm your AI assistant. What can I do for you?",
            "Greetings! Ready to find your next big project?",
            "Hi! Good to see you. How can I assist you today?"
        ]

        self.unknown = [
            "Hmm, I'm not entirely sure about that yet. I'm still learning!",
            "That's a bit out of my current knowledge base. Want to talk about jobs or pricing instead?",
            "I didn't quite catch that. Could you try rephrasing? I can help with job searches, profiles, and more.",
            "I'm still a work in progress! Could you ask that in a different way?"
        ]

    def _load_model(self):
        try:
            if os.path.exists(self.model_path):
                logger.info(f"Loading intent model from {self.model_path}")
                return joblib.load(self.model_path)
            return None
        except Exception as e:
            logger.error(f"Error loading intent model: {str(e)}")
            return None

    async def get_response(self, message: str, locale: str = "en", context: str = None) -> str:
        message_low = message.lower().strip()
        
        if not message_low:
            return "តើខ្ញុំអាចជួយអ្វីអ្នកបាន?" if locale == "km" else "I'm listening! What can I help you with?"

        # 1. Use ML model for intent detection if available
        intent = "unknown"
        confidence = 0.0
        
        if self.model:
            try:
                # Predict intent
                intent = self.model.predict([message])[0]
                # Get probability
                probs = self.model.predict_proba([message])[0]
                confidence = max(probs)
                
                # If confidence is too low, fall back
                if confidence < 0.3:
                    intent = "unknown"
            except Exception as e:
                logger.error(f"ML Intent detection failed: {str(e)}")

        # 2. Fallback to rule-based if ML failed or low confidence
        if intent == "unknown":
            intent = self._detect_intent_rules(message_low)
        
        # 3. Build response with human-like touches
        if intent == "greeting":
            if locale == "km":
                return random.choice(["សួស្ដី! តើថ្ងៃនេះអ្នកសុខសប្បាយជាទេ? តើខ្ញុំអាចជួយអ្វីអ្នកបាននៅក្នុង KhmerWork?", "សួស្ដី! តើអ្នកកំពុងស្វែងរកឱកាសថ្មីមែនទេ?", "សួស្ដី! ខ្ញុំជាជំនួយការ AI របស់អ្នក។ តើខ្ញុំអាចបម្រើអ្វីអ្នកបាន?"])
            return random.choice(self.greetings)
        
        if intent in self.knowledge_base:
            main_response = random.choice(self.knowledge_base[intent])
            
            # Smart humanization
            roll = random.random()
            if roll > 0.6: # Add filler at start
                filler = random.choice(self.fillers)
                main_response = f"{filler} {main_response}"
            
            if roll < 0.4: # Add closer at end
                closer = random.choice(self.closers)
                main_response = f"{main_response} {closer}"
            
            return main_response
            
        # 4. Final Fallback: Ask OpenAI for an intelligent answer
        if self.client:
            try:
                logger.info(f"Using OpenAI fallback for message: {message[:50]}... Locale: {locale}")
                context_info = f" The user is currently on the page: {context}." if context else ""
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": f"You are the AI assistant for KhmerWork, a premium freelance platform in Cambodia. {lang_instruction}{context_info} Use this info to help: {str(self.knowledge_base)}. Be helpful, professional, and concise. If you don't know something about the platform specifically, give a general helpful freelance advice."},
                        {"role": "user", "content": message}
                    ],
                    temperature=0.7,
                    max_tokens=150
                )
                return response.choices[0].message.content
            except Exception as e:
                logger.error(f"OpenAI Chat fallback failed: {e}")

        if locale == "km":
            return random.choice(["ហ៊ឹម ខ្ញុំមិនទាន់ច្បាស់អំពីចំណុចនោះនៅឡើយទេ។ ខ្ញុំកំពុងរៀនបន្ថែម!", "នោះហួសពីអ្វីដែលខ្ញុំដឹងនៅពេលនេះ។ ចង់និយាយអំពីការងារ ឬតម្លៃជំនួសវិញទេ?", "ខ្ញុំមិនសូវយល់ទេ។ តើអ្នកអាចសាកល្បងនិយាយម្ដងទៀតបានទេ?"])
        return random.choice(self.unknown)

    def _detect_intent_rules(self, message: str) -> str:
        patterns = {
            "greeting": ["hi", "hello", "hey", "greetings", "សួស្ដី", "ជម្រាបសួរ", "សុខសប្បាយ"],
            "jobs": ["job", "work", "find", "remote", "freelance", "ការងារ", "រកការងារ", "ស្វែងរក"],
            "pricing": ["price", "cost", "pay", "free", "តម្លៃ", "លុយ", "បង់"],
            "contact": ["contact", "support", "email", "ទំនាក់ទំនង", "ជំនួយ", "ផ្ញើសារ"],
            "hiring": ["hire", "employer", "post", "រើសបុគ្គលិក", "ជួល", "ប្រកាស"],
            "profile": ["profile", "resume", "cv", "ប្រវត្តិរូប", "ជំនាញ"],
            "ai": ["ai", "bot", "assistant", "ជំនួយការ", "ឆ្លាត"]
        }

        for intent, keywords in patterns.items():
            if any(keyword in message for keyword in keywords):
                return intent
                
        return "unknown"
