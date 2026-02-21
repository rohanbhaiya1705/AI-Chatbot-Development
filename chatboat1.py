import re
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum


class Intent(Enum):
    GREETING = "greeting"
    PRODUCT_INQUIRY = "product_inquiry"
    PRICING = "pricing"
    SUPPORT = "support"
    GOODBYE = "goodbye"
    UNKNOWN = "unknown"


@dataclass
class Response:
    text: str
    follow_up: Optional[str] = None
    requires_input: bool = True


class RuleBasedChatbot:
    """
    A rule-based chatbot using pattern matching and predefined responses.
    Demonstrates fundamental chatbot architecture with clear, extensible structure.
    """
    
    def __init__(self, name: str = "Assistant"):
        self.name = name
        self.conversation_history: List[Dict] = []
        self.user_context: Dict[str, any] = {}
        
        # Define intent patterns for matching
        self.intent_patterns = {
            Intent.GREETING: [
                r'\b(hi|hello|hey|greetings|good morning|good afternoon)\b',
                r'^start$',
            ],
            Intent.PRODUCT_INQUIRY: [
                r'\b(product|service|what do you offer|what can you do)\b',
                r'\btell me about\b',
            ],
            Intent.PRICING: [
                r'\b(price|cost|how much|pricing|fee|charge)\b',
                r'\bhow much does\b',
            ],
            Intent.SUPPORT: [
                r'\b(help|support|issue|problem|trouble|not working)\b',
                r'\bneed assistance\b',
            ],
            Intent.GOODBYE: [
                r'\b(bye|goodbye|see you|quit|exit|stop)\b',
                r'\bthat\'s all\b',
            ],
        }
        
        # Define responses for each intent
        self.responses = {
            Intent.GREETING: Response(
                text=f"Hello! I'm {self.name}, your virtual assistant. "
                     "How can I help you today?",
                follow_up="You can ask about our products, pricing, or get support."
            ),
            Intent.PRODUCT_INQUIRY: Response(
                text="We offer a range of AI-powered solutions including:\n"
                     "• Customer Service Chatbots\n"
                     "• Virtual Assistants\n"
                     "• Knowledge Base Systems\n"
                     "• Analytics Dashboards",
                follow_up="Which product interests you most?"
            ),
            Intent.PRICING: Response(
                text="Our pricing plans are designed to fit businesses of all sizes:\n"
                     "• Starter: $99/month (up to 1,000 conversations)\n"
                     "• Professional: $299/month (up to 10,000 conversations)\n"
                     "• Enterprise: Custom pricing",
                follow_up="Would you like details on a specific plan?"
            ),
            Intent.SUPPORT: Response(
                text="I'm here to help! Please describe the issue you're experiencing.",
                follow_up="Include any error messages or steps that led to the problem."
            ),
            Intent.GOODBYE: Response(
                text="Thank you for chatting with me! Have a great day!",
                requires_input=False
            ),
            Intent.UNKNOWN: Response(
                text="I'm not sure I understand. Could you rephrase that?",
                follow_up="You can ask about products, pricing, or get support."
            ),
        }
    
    def classify_intent(self, user_input: str) -> Intent:
        """
        Classify user input into intent categories using pattern matching.
        Returns the best matching intent or UNKNOWN if no match found.
        """
        input_lower = user_input.lower().strip()
        
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, input_lower, re.IGNORECASE):
                    return intent
        
        return Intent.UNKNOWN
    
    def generate_response(self, user_input: str) -> Response:
        """
        Generate an appropriate response based on user input.
        Maintains conversation history for context-aware interactions.
        """
        intent = self.classify_intent(user_input)
        response = self.responses[intent]
        
        # Log the interaction
        self.conversation_history.append({
            "user_input": user_input,
            "intent": intent.value,
            "bot_response": response.text,
        })
        
        return response
    
    def chat(self, user_input: str) -> str:
        """
        Main chat interface that processes user input and returns response.
        """
        response = self.generate_response(user_input)
        
        # Build response text
        response_text = response.text
        if response.follow_up:
            response_text += f"\n\n{response.follow_up}"
        
        return response_text


# Demonstration of the rule-based chatbot
def demonstrate_rule_based_chatbot():
    """
    Demonstrate the rule-based chatbot with sample conversations.
    """
    bot = RuleBasedChatbot("AI Assistant")
    
    print("=" * 60)
    print("RULE-BASED CHATBOT DEMONSTRATION")
    print("=" * 60)
    
    sample_conversations = [
        "Hello there!",
        "What products do you offer?",
        "How much does it cost?",
        "I'm having an issue with my account",
        "Goodbye"
    ]
    
    for user_input in sample_conversations:
        print(f"\n👤 User: {user_input}")
        print(f"🤖 Bot: {bot.chat(user_input)}")
        print("-" * 40)


if __name__ == "__main__":
    demonstrate_rule_based_chatbot()