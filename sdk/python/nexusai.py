#!/usr/bin/env python3
"""
NexusAI SDK - Universal AI Gateway
One SDK to Rule All AI Models
"""

import os
import time
import json
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
import requests

class Priority(Enum):
    SPEED = "speed"
    COST = "cost"
    QUALITY = "quality"

@dataclass
class ModelProvider:
    name: str
    api_key: str
    base_url: str
    cost_per_1k_input: float = 0
    cost_per_1k_output: float = 0
    latency_ms: int = 1000
    supports_streaming: bool = True
    
class NexusAI:
    """
    Universal AI Gateway - One SDK for all models
    """
    
    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.providers: Dict[str, ModelProvider] = {}
        self.router_rules: List[Dict] = []
        self.cost_tracker = CostTracker()
        self.fallback_chain: List[str] = []
        
        # Default providers (can be configured)
        self._init_default_providers()
    
    def _init_default_providers(self):
        """Initialize with common providers"""
        # OpenAI
        self.add_provider("openai", {
            "api_key": os.getenv("OPENAI_API_KEY", ""),
            "base_url": "https://api.openai.com/v1",
            "cost_input": 0.003,
            "cost_output": 0.015,
            "latency": 800
        })
        
        # Anthropic
        self.add_provider("anthropic", {
            "api_key": os.getenv("ANTHROPIC_API_KEY", ""),
            "base_url": "https://api.anthropic.com",
            "cost_input": 0.003,
            "cost_output": 0.015,
            "latency": 1000
        })
        
        # Gemini
        self.add_provider("gemini", {
            "api_key": os.getenv("GEMINI_API_KEY", ""),
            "base_url": "https://generativelanguage.googleapis.com/v1",
            "cost_input": 0.00025,
            "cost_output": 0.0005,
            "latency": 600
        })
        
        # Groq (Free!)
        self.add_provider("groq", {
            "api_key": os.getenv("GROQ_API_KEY", ""),
            "base_url": "https://api.groq.com/openai/v1",
            "cost_input": 0,
            "cost_output": 0,
            "latency": 300
        })
        
        # Ollama (Local)
        self.add_provider("ollama", {
            "api_key": "local",
            "base_url": os.getenv("OLLAMA_URL", "http://localhost:11434"),
            "cost_input": 0,
            "cost_output": 0,
            "latency": 100,
            "local": True
        })
    
    def add_provider(self, name: str, config: Dict):
        """Add a new provider"""
        provider = ModelProvider(
            name=name,
            api_key=config.get("api_key", ""),
            base_url=config.get("base_url", ""),
            cost_per_1k_input=config.get("cost_input", 0),
            cost_per_1k_output=config.get("cost_output", 0),
            latency_ms=config.get("latency", 1000)
        )
        self.providers[name] = provider
        print(f"✅ Added provider: {name}")
    
    def set_router_rule(self, rule: Dict):
        """Add routing rule"""
        self.router_rules.append(rule)
        print(f"✅ Added router rule: {rule.get('name', 'unnamed')}")
    
    def chat(self, model: str, messages: List[Dict], 
             priority: Priority = Priority.COST,
             **kwargs) -> Dict:
        """
        Universal chat interface
        Examples:
            nexus.chat("openai/gpt-4o", [...])
            nexus.chat("gemini/gemini-pro", [...])
            nexus.chat("groq/llama3-70b", [...])
        """
        # Parse model string
        provider_name, model_name = self._parse_model(model)
        
        if not provider_name or provider_name not in self.providers:
            return {"error": f"Unknown provider: {provider_name}"}
        
        provider = self.providers[provider_name]
        
        # Try primary provider
        response = self._call_provider(provider, model_name, messages, **kwargs)
        
        # Auto-fallback if failed
        if "error" in response:
            fallback = self._get_fallback(provider_name, priority)
            if fallback:
                print(f"⚠️ Fallback to {fallback}")
                response = self._call_provider(
                    self.providers[fallback], 
                    model_name, 
                    messages, 
                    **kwargs
                )
        
        # Track cost
        if "error" not in response:
            tokens = response.get("usage", {}).get("total_tokens", 0)
            self.cost_tracker.track(provider_name, tokens)
        
        return response
    
    def _parse_model(self, model: str) -> tuple:
        """Parse model string like 'openai/gpt-4o'"""
        parts = model.split("/")
        if len(parts) == 2:
            return parts[0], parts[1]
        # Try to detect from model name
        for provider_name in self.providers:
            if provider_name in model.lower():
                return provider_name, model
        return "openai", model
    
    def _call_provider(self, provider: ModelProvider, model: str, 
                      messages: List[Dict], **kwargs) -> Dict:
        """Call specific provider"""
        # For demo, return mock response
        return {
            "provider": provider.name,
            "model": model,
            "response": f"[Mock response from {provider.name}/{model}]",
            "usage": {
                "input_tokens": 100,
                "output_tokens": 200,
                "total_tokens": 300
            },
            "latency_ms": provider.latency_ms,
            "cost": (provider.cost_per_1k_input * 0.1 + 
                     provider.cost_per_1k_output * 0.2)
        }
    
    def _get_fallback(self, failed_provider: str, priority: Priority) -> Optional[str]:
        """Get fallback provider based on priority"""
        available = [p for p in self.providers.keys() if p != failed_provider]
        
        if priority == Priority.SPEED:
            # Fastest
            return min(available, 
                      key=lambda p: self.providers[p].latency_ms)
        elif priority == Priority.COST:
            # Cheapest (local first)
            for p in available:
                if self.providers[p].cost_per_1k_input == 0:
                    return p
            return available[0] if available else None
        else:
            # Quality - use best
            return available[0] if available else None
    
    def set_fallback_chain(self, chain: List[str]):
        """Set explicit fallback chain"""
        self.fallback_chain = chain
    
    def get_cost_summary(self) -> Dict:
        """Get cost summary"""
        return self.cost_tracker.get_summary()
    
    def compare_models(self, prompt: str, models: List[str]) -> Dict:
        """Compare multiple models"""
        results = {}
        for model in models:
            start = time.time()
            response = self.chat(model, [{"role": "user", "content": prompt}])
            results[model] = {
                "response": response.get("response", "")[:100],
                "latency": time.time() - start,
                "cost": response.get("cost", 0)
            }
        return results
    
    def create_agent(self, tools: List[Callable] = None) -> 'NexusAgent':
        """Create AI agent with tools"""
        return NexusAgent(self, tools)


class CostTracker:
    """Track API costs"""
    
    def __init__(self):
        self.provider_costs: Dict[str, float] = {}
        self.provider_tokens: Dict[str, int] = {}
    
    def track(self, provider: str, tokens: int):
        if provider not in self.provider_tokens:
            self.provider_tokens[provider] = 0
        self.provider_tokens[provider] += tokens
    
    def get_summary(self) -> Dict:
        return {
            "total_tokens": sum(self.provider_tokens.values()),
            "by_provider": self.provider_tokens,
            "estimated_cost": sum(self.provider_costs.values())
        }


class NexusAgent:
    """AI Agent with tools"""
    
    def __init__(self, nexus: NexusAI, tools: List[Callable] = None):
        self.nexus = nexus
        self.tools = tools or []
    
    def add_tool(self, tool: Callable):
        self.tools.append(tool)
    
    def run(self, task: str) -> Dict:
        # Simple agent implementation
        messages = [{"role": "user", "content": task}]
        return self.nexus.chat("groq/llama3-70b", messages)


# Convenience functions
def quick_chat(model: str, message: str) -> str:
    """Quick chat helper"""
    nexus = NexusAI()
    response = nexus.chat(model, [{"role": "user", "content": message}])
    return response.get("response", "Error: " + str(response.get("error")))


# Example usage
if __name__ == "__main__":
    print("🚀 NexusAI SDK")
    print("=" * 50)
    
    # Initialize
    nexus = NexusAI()
    
    # Example 1: Simple chat
    print("\n📝 Example 1: Simple Chat")
    response = nexus.chat("groq/llama3-70b", [
        {"role": "user", "content": "Hello! What is Python?"}
    ])
    print(f"Response: {response.get('response')}")
    print(f"Provider: {response.get('provider')}")
    
    # Example 2: Different providers
    print("\n📝 Example 2: Multi-provider")
    models = ["openai/gpt-4o", "gemini/gemini-pro", "groq/llama3-70b"]
    for model in models:
        resp = nexus.chat(model, [{"role": "user", "content": "Hi"}])
        print(f"  {model}: {resp.get('provider')}")
    
    # Example 3: Model comparison
    print("\n📝 Example 3: Compare Models")
    results = nexus.compare_models("What is AI?", [
        "openai/gpt-4o",
        "gemini/gemini-pro"
    ])
    for model, data in results.items():
        print(f"  {model}: {data['latency']:.2f}s")
    
    # Example 4: Cost tracking
    print("\n📝 Example 4: Cost Summary")
    print(f"  {nexus.get_cost_summary()}")
    
    # Example 5: Create agent
    print("\n📝 Example 5: AI Agent")
    agent = nexus.create_agent()
    result = agent.run("Search for top AI news today")
    print(f"  Agent: {result}")
