import os
import json
import requests
import time
from typing import List, Dict, Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent import agent_app
from langchain_core.messages import HumanMessage, AIMessage, AIMessageChunk
from data import ATTRACTIONS, calculate_distance

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.responses import StreamingResponse
import asyncio

class ChatRequest(BaseModel):
    messages: List[Dict[str, Any]]
    lat: float = None
    lng: float = None
    radius: float = 10.0
    location_name: str = None

@app.post("/chat")
async def chat(request: ChatRequest):
    async def event_generator():
        try:
            # Chuyển đổi tin nhắn từ Frontend sang định dạng HumanMessage/AIMessage của LangChain
            langchain_messages = []
            for msg in request.messages:
                content = msg.get("content", "")
                if not content and "parts" in msg:
                    part_texts = [p.get("text", "") for p in msg["parts"] if p.get("type") == "text"]
                    content = "".join(part_texts)
                if not content and "text" in msg:
                    content = msg["text"]
                
                # Skip empty messages
                if not content:
                    continue

                if msg.get("role") == "user":
                    langchain_messages.append(HumanMessage(content=content))
                elif msg.get("role") == "assistant":
                    langchain_messages.append(AIMessage(content=content))
            
            # Thêm ngữ cảnh vị trí vào tin nhắn cuối cùng để Agent phản hồi chính xác hơn
            location_context = ""
            if request.location_name:
                location_context = f"\n[User is currently at: {request.location_name}]"
            elif request.lat is not None and request.lng is not None:
                location_context = f"\n[User GPS Coordinates: {request.lat}, {request.lng}. Use identify_current_location if needed.]"
            
            if location_context:
                if langchain_messages and isinstance(langchain_messages[-1], HumanMessage):
                    langchain_messages[-1].content += location_context
                else:
                    langchain_messages.append(HumanMessage(content=f"System Context: {location_context}"))

            # Định nghĩa dữ liệu đầu vào cho quy trình AI
            inputs = {"messages": langchain_messages}

            # Khởi tạo các biến đo lường hiệu năng (Telemetry) và lưu trữ phản hồi
            start_time = time.perf_counter()
            total_prompt_tokens = 0
            total_completion_tokens = 0
            full_response_content = ""
            
            # Chạy Agent ở chế độ streaming với LangGraph 0.2
            async for msg, metadata in agent_app.astream(inputs, stream_mode="messages"):
                # Ghi Log chi tiết khi AI quyết định sử dụng công cụ (Tool)
                if hasattr(msg, "tool_calls") and msg.tool_calls:
                    for tc in msg.tool_calls:
                        print(f"🛠️  GỌI CÔNG CỤ: {tc['name']} | Tham số: {tc['args']}")

                # CHÚ Ý: Chỉ lấy tin nhắn do node 'agent' tạo ra để tránh trùng lặp dữ liệu
                if metadata.get('langgraph_node') != 'agent':
                    continue
                
                # Trích xuất thông tin Token (Yêu cầu thư viện LangChain v0.2.x)
                if hasattr(msg, "usage_metadata") and msg.usage_metadata:
                    total_prompt_tokens = msg.usage_metadata.get("input_tokens", 0)
                    total_completion_tokens = msg.usage_metadata.get("output_tokens", 0)
                
                # Xử lý và tích lũy nội dung tin nhắn để gửi về Frontend
                if isinstance(msg, (AIMessage, AIMessageChunk)) and msg.content:
                    content_to_yield = ""
                    # Xử lý định dạng stream token (Chunks)
                    if isinstance(msg, AIMessageChunk):
                        if isinstance(msg.content, str):
                            content_to_yield = msg.content
                        elif isinstance(msg.content, list):
                            for block in msg.content:
                                if isinstance(block, dict) and block.get("type") == "text":
                                    content_to_yield += block.get("text", "")
                    
                    # Xử lý định dạng tin nhắn đầy đủ (Full Message)
                    elif isinstance(msg, AIMessage) and not isinstance(msg, AIMessageChunk):
                         if isinstance(msg.content, str):
                             content_to_yield = msg.content
                         elif isinstance(msg.content, list):
                             for block in msg.content:
                                 if isinstance(block, dict) and block.get("type") == "text":
                                     content_to_yield += block.get("text", "")
                    
                    if content_to_yield:
                        full_response_content += content_to_yield
                        yield content_to_yield
            
            # Ghi Log tổng hợp sau khi AI đã phản hồi xong
            end_time = time.perf_counter()
            latency = end_time - start_time
            print(f"\n--- [THÔNG SỐ AI - TELEMETRY] ---")
            print(f"⏱️  Độ trễ phản hồi: {latency:.2f}s")
            print(f"🎟️  Prompt Tokens (Đầu vào): {total_prompt_tokens}")
            print(f"💬  Completion Tokens (Đầu ra): {total_completion_tokens}")
            print(f"📊  Tổng số Tokens: {total_prompt_tokens + total_completion_tokens}")
            print(f"📝  Nội dung AI đã nhắn: {full_response_content[:150]}..." if len(full_response_content) > 150 else f"📝 Phản hồi: {full_response_content}")
            print(f"---------------------------------\n")
                
        except Exception as e:
            print(f"Streaming error: {str(e)}")
            yield f"Error: {str(e)}"

    return StreamingResponse(
        event_generator(), 
        media_type='text/plain; charset=utf-8',
        headers={
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'X-Content-Type-Options': 'nosniff'
        }
    )

@app.get("/reverse-geocode")
async def reverse_geocode(lat: float, lng: float):
    """Resolve coordinates to a human-readable location name (district prioritized)."""
    try:
        url = f"https://photon.komoot.io/reverse?lon={lng}&lat={lat}"
        headers = {"User-Agent": "TravelBuddy/1.0"}
        response = requests.get(url, headers=headers, timeout=5)
        
        if response.status_code != 200:
            print(f"❌ Komoot API Error: {response.status_code} - {response.text[:100]}")
            return {"location_name": "Unknown location"}

        data = response.json()
        
        if data.get("features"):
            props = data["features"][0].get("properties", {})
            
            # Prioritize fields that identify the district or local area
            location_name = (
                props.get("district") or 
                props.get("city_district") or 
                props.get("suburb") or 
                props.get("city") or 
                props.get("name") or 
                "Unknown location"
            )
            
            print(f"📍 Resolved location to: {location_name}")
            return {"location_name": location_name}
        
        return {"location_name": "Unknown location"}
    except Exception as e:
        print(f"❌ Geocoding Exception: {str(e)}")
        # Don't throw 500, return a safe default to keep the UI running
        return {"location_name": "Hoi An"}

@app.get("/attractions")
async def get_attractions(lat: float = None, lng: float = None, radius: float = 10.0):
    if lat is None or lng is None:
        # Return all attractions if no coordinates
        return ATTRACTIONS
    
    user_loc = (lat, lng)
    results = []
    for a in ATTRACTIONS:
        dist = calculate_distance(user_loc, a["coordinates"])
        if dist <= radius:
            # Flatten coordinates for JSON response to match original schema [lat, lng]
            a_copy = a.copy()
            a_copy["distance"] = round(dist, 2)
            results.append(a_copy)
    
    # Sort by distance
    results.sort(key=lambda x: x.get("distance", 0))
    return results

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
