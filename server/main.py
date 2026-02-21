#!/usr/bin/env python3
"""
NexusAI FastAPI Server
Universal AI Gateway Backend
"""

import os
import json
import asyncio
from datetime import datetime
from typing import Dict, List, Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel
from dataclasses import dataclass

# Import NexusAI SDK
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'sdk', 'python'))
from nexusai import NexusAI, Priority

# ============== CONFIG ==============
API_VERSION = "1.0.0"
APP_NAME = "NexusAI Server"

# ============== MODELS ==============
class ChatRequest(BaseModel):
    model: str
    messages: List[Dict[str, str]]
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 1000
    stream: Optional[bool] = False
    priority: Optional[str] = "cost"  # cost, speed, quality

class ChatResponse(BaseModel):
    response: str
    provider: str
    model: str
    usage: Dict
    latency_ms: int

class CostResponse(BaseModel):
    total_tokens: int
    by_provider: Dict[str, int]
    estimated_cost: float

class ModelInfo(BaseModel):
    name: str
    provider: str
    status: str
    latency_ms: int

# ============== APP ==============
app = FastAPI(
    title="NexusAI API",
    description="One SDK to Rule All AI Models",
    version=API_VERSION
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize NexusAI
nexus = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global nexus
    # Startup
    nexus = NexusAI()
    print(f"🚀 {APP_NAME} v{API_VERSION} started")
    yield
    # Shutdown
    print("🛑 Shutting down...")

app = FastAPI(lifespan=lifespan)

# ============== ROUTES ==============

@app.get("/")
async def root():
    return {
        "name": APP_NAME,
        "version": API_VERSION,
        "status": "running",
        "docs": "/docs"
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Universal chat endpoint - works with any model"""
    if not nexus:
        raise HTTPException(status_code=500, detail="AI not initialized")
    
    try:
        # Convert priority string to enum
        priority_map = {
            "cost": Priority.COST,
            "speed": Priority.SPEED,
            "quality": Priority.QUALITY
        }
        priority = priority_map.get(request.priority, Priority.COST)
        
        # Make request
        import time
        start = time.time()
        
        response = nexus.chat(
            model=request.model,
            messages=request.messages,
            priority=priority
        )
        
        latency = int((time.time() - start) * 1000)
        
        if "error" in response:
            raise HTTPException(status_code=400, detail=response["error"])
        
        return ChatResponse(
            response=response.get("response", ""),
            provider=response.get("provider", "unknown"),
            model=request.model,
            usage=response.get("usage", {}),
            latency_ms=latency
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    """Streaming chat endpoint"""
    if not nexus:
        raise HTTPException(status_code=500, detail="AI not initialized")
    
    async def generate():
        yield f"data: {json.dumps({'status': 'streaming'})}\n\n"
        # For demo, return mock streaming
        response = nexus.chat(request.model, request.messages)
        for word in response.get("response", "Streaming...").split():
            yield f"data: {json.dumps({'token': word})}\n\n"
        yield f"data: {json.dumps({'done': True})}\n\n"
    
    return StreamingResponse(generate(), media_type="text/event-stream")

@app.get("/cost", response_model=CostResponse)
async def get_cost():
    """Get cost summary"""
    if not nexus:
        raise HTTPException(status_code=500, detail="AI not initialized")
    
    summary = nexus.get_cost_summary()
    
    return CostResponse(
        total_tokens=summary.get("total_tokens", 0),
        by_provider=summary.get("by_provider", {}),
        estimated_cost=summary.get("estimated_cost", 0)
    )

@app.get("/models")
async def list_models():
    """List all available models"""
    if not nexus:
        raise HTTPException(status_code=500, detail="AI not initialized")
    
    models = []
    for name, provider in nexus.providers.items():
        models.append({
            "name": name,
            "provider": provider.name,
            "status": "online" if provider.api_key else "no_key",
            "latency_ms": provider.latency_ms,
            "cost_input": provider.cost_per_1k_input,
            "cost_output": provider.cost_per_1k_output,
            "local": getattr(provider, 'local', False)
        })
    
    return {"models": models, "count": len(models)}

@app.post("/agent/create")
async def create_agent(tools: Optional[List[str]] = None):
    """Create AI agent"""
    if not nexus:
        raise HTTPException(status_code=500, detail="AI not initialized")
    
    agent = nexus.create_agent()
    
    return {
        "agent_id": f"agent_{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "status": "created",
        "tools_count": len(tools) if tools else 0
    }

@app.post("/agent/{agent_id}/run")
async def run_agent(agent_id: str, task: str):
    """Run agent task"""
    if not nexus:
        raise HTTPException(status_code=500, detail="AI not initialized")
    
    agent = nexus.create_agent()
    result = agent.run(task)
    
    return {
        "agent_id": agent_id,
        "task": task,
        "result": result.get("response", ""),
        "status": "completed"
    }

@app.get("/compare")
async def compare_models(prompt: str, models: Optional[str] = None):
    """Compare multiple models"""
    if not nexus:
        raise HTTPException(status_code=500, detail="AI not initialized")
    
    model_list = models.split(",") if models else ["openai/gpt-4o", "gemini/gemini-pro"]
    
    results = nexus.compare_models(prompt, model_list)
    
    return {
        "prompt": prompt,
        "results": results
    }

@app.get("/providers")
async def list_providers():
    """List all configured providers"""
    if not nexus:
        raise HTTPException(status_code=500, detail="AI not initialized")
    
    providers = []
    for name, provider in nexus.providers.items():
        providers.append({
            "name": provider.name,
            "base_url": provider.base_url,
            "cost_input": provider.cost_per_1k_input,
            "cost_output": provider.cost_per_1k_output,
            "latency_ms": provider.latency_ms,
            "configured": bool(provider.api_key)
        })
    
    return {"providers": providers}

@app.post("/providers/add")
async def add_provider(config: Dict):
    """Add new provider"""
    if not nexus:
        raise HTTPException(status_code=500, detail="AI not initialized")
    
    name = config.get("name")
    if not name:
        raise HTTPException(status_code=400, detail="Provider name required")
    
    nexus.add_provider(name, config)
    
    return {"status": "added", "provider": name}

# ============== MAIN ==============
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
