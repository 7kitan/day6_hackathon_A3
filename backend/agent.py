import os
import json
from typing import Annotated, List, TypedDict, Union, Sequence, Dict, Any
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langgraph.graph.message import add_messages

# Nạp các biến môi trường từ file .env
load_dotenv(override=True)

# --- CẤU HÌNH TRẠNG THÁI VÀ ĐỒ THỊ (GRAPH) ---

# Định nghĩa cấu trúc dữ liệu cho trạng thái của Agent
class AgentState(TypedDict):
    # 'messages' lưu trữ lịch sử hội thoại. 
    # 'add_messages' là một reducer giúp gộp các tin nhắn mới vào danh sách cũ.
    messages: Annotated[Sequence[BaseMessage], add_messages]

# --- ĐỊNH NGHĨA CÁC CÔNG CỤ (TOOLS) ---

def get_attractions_data():
    from data import ATTRACTIONS
    return ATTRACTIONS

@tool
def search_nearby_attractions(user_lat: float, user_lng: float, radius_km: float = 5.0) -> str:
    """Tìm kiếm các điểm tham quan du lịch trong bán kính nhất định quanh tọa độ người dùng."""
    from data import calculate_distance
    attractions = get_attractions_data()
    nearby = []
    
    for attr in attractions:
        # attr['coordinates'] là một Tuple(lat, lng)
        dist = calculate_distance((user_lat, user_lng), attr['coordinates'])
        if dist <= radius_km:
            nearby.append({
                "id": attr["id"],
                "name": attr["name"],
                "category": attr.get("type") or attr.get("category") or "attraction",
                "distance_km": round(dist, 2),
                "description": attr["description"]
            })
    
    # Sắp xếp theo khoảng cách
    nearby.sort(key=lambda x: x["distance_km"])
    return json.dumps(nearby, ensure_ascii=False)

@tool
def get_attraction_details(attraction_id: str) -> str:
    """Lấy thông tin chi tiết của một địa điểm cụ thể dựa trên ID."""
    attractions = get_attractions_data()
    for attr in attractions:
        if attr["id"] == attraction_id:
            return json.dumps(attr, ensure_ascii=False)
    return "Attraction not found."

# Danh sách các công cụ mà Agent có quyền sử dụng
tools = [search_nearby_attractions, get_attraction_details]
# Khởi tạo đối tượng ToolNode để quản lý việc thực thi các tool trong đồ thị
tool_node = ToolNode(tools)

# --- Agent Logic ---

# Khởi tạo mô hình ngôn ngữ (LLM) gpt-4o
#llm = ChatOpenAI(model="gpt-4o", temperature=0)
llm = ChatAnthropic(
    model="claude-3-haiku-20240307",
    temperature=0
)

# 'Gắn' các công cụ vào mô hình để nó biết mình có quyền gọi tool
llm_with_tools = llm.bind_tools(tools)

SYSTEM_PROMPT = """You are a helpful and friendly local travel assistant in Vietnam. 
Your goal is to help users discover attractions, find interesting places nearby, and build personalized itineraries.

# LOCATION AWARENESS (CRITICAL):
- You will receive the user's current location details in the context (formatted as `[User is currently at: ...]`).
- ALWAYS prioritize this information to provide a personalized greeting and relevant suggestions.
- Do NOT assume you are in a specific city unless the context tells you so. Adapting to the user's actual location is your primary mission.
- Example: "Chào bạn! Tôi thấy bạn đang ở [Tên địa danh thực tế]. Bạn có muốn khám phá các điểm tham quan gần đây không?"

# CRITICAL RULES:
1. Always respond in Vietnamese and maintain a warm, welcoming tone.
2. Only use `search_nearby_attractions` when the user explicitly asks for recommendations, "what's nearby", or looking for something to do.
3. If the user only says "hello", use the provided location info to make the greeting personalized and relevant to where they are.

When you identify a set of places for an itinerary, always include a JSON block at the end of your response with the exact format below (use the real IDs from the tools, NOT names):
```json
{
  "action": "BUILD_ITINERARY",
  "ids": ["id1", "id2", "id3"]
}
```

If the user asks about a specific place, you can also use:
```json
{
  "action": "SHOW_LOCATION",
  "id": "attraction_id"
}
```"""

def call_model(state: AgentState):
    """Gửi toàn bộ lịch sử tin nhắn cùng với System Prompt tới AI."""
    messages = state['messages']
    # Thêm System Prompt vào đầu danh sách để định hướng hành vi cho AI
    has_system = any(isinstance(m, SystemMessage) for m in messages)
    if not has_system:
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + list(messages)
    
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

def should_continue(state: AgentState):
    """Quyết định xem nên tiếp tục gọi Tool hay kết thúc hội thoại."""
    messages = state['messages']
    last_message = messages[-1]
    # Nếu tin nhắn cuối cùng có yêu cầu gọi tool (tool_calls), chuyển sang node 'tools'
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    # Ngược lại, kết thúc quy trình
    return END

# --- XÂY DỰNG LUỒNG XỬ LÝ (LANGGRAPH) ---

workflow = StateGraph(AgentState)

# Định nghĩa các nút (Nodes) trong đồ thị
workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)

# Thiết lập điểm bắt đầu
workflow.set_entry_point("agent")

# Thiết lập các cạnh (Edges) có điều kiện sau khi AI phản hồi
workflow.add_conditional_edges(
    "agent",
    should_continue,
)

# Sau khi thực thi Tool, quay trở lại hỏi AI để tổng hợp câu trả lời
workflow.add_edge("tools", "agent")

# Biên dịch đồ thị thành một ứng dụng có thể thực thi
agent_app = workflow.compile()
