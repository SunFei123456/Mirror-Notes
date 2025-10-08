from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from services import SolutionService, WallStickerService, StickerConnectionService, StickerReactionService
from models import SolutionNote, WallSticker
import json

app = FastAPI(
    title="Mirror Notes API",
    description="API for Mirror Notes - Share Your Strength",
    version="1.0.0"
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境中应该设置具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 获取客户端IP地址的辅助函数
def get_client_ip(request: Request) -> str:
    """获取客户端真实IP地址"""
    # 检查X-Forwarded-For头（代理服务器）
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    
    # 检查X-Real-IP头
    real_ip = request.headers.get("X-Real-IP")
    if real_ip:
        return real_ip
    
    # 使用客户端IP
    return request.client.host if request.client else "127.0.0.1"

@app.get("/")
async def root():
    """根路径，返回API信息"""
    return {
        "message": "Mirror Notes API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/api/notes")
async def get_all_notes():
    """获取所有解决方案笔记"""
    try:
        notes = SolutionService.get_all_notes()
        return {
            "success": True,
            "data": [note.to_dict() for note in notes],
            "count": len(notes)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch notes: {str(e)}")

@app.get("/api/notes/{note_id}")
async def get_note_by_id(note_id: int):
    """根据ID获取特定笔记"""
    try:
        note = SolutionService.get_note_by_id(note_id)
        if not note:
            raise HTTPException(status_code=404, detail="Note not found")
        
        return {
            "success": True,
            "data": note.to_dict()
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch note: {str(e)}")

@app.post("/api/notes")
async def create_note(request: Request):
    """创建新的解决方案笔记"""
    try:
        body = await request.json()
        content = body.get("content", "").strip()
        author_name = body.get("author_name", "Anonymous").strip()
        author_type = body.get("author_type", "anonymous")
        
        if not content:
            raise HTTPException(status_code=400, detail="Content is required")
        
        if len(content) > 1000:
            raise HTTPException(status_code=400, detail="Content too long (max 1000 characters)")
        
        if author_type not in ["anonymous", "signature"]:
            author_type = "anonymous"
        
        if author_type == "anonymous":
            author_name = "Anonymous"
        elif not author_name or author_name == "Anonymous":
            author_name = "Anonymous"
            author_type = "anonymous"
        
        note_id = SolutionService.create_note(content, author_name, author_type)
        
        if note_id:
            return {
                "success": True,
                "message": "Note created successfully",
                "data": {"id": note_id}
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to create note")
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create note: {str(e)}")

@app.post("/api/notes/{note_id}/like")
async def like_note(note_id: int, request: Request):
    """点赞笔记"""
    try:
        client_ip = get_client_ip(request)
        result = SolutionService.like_note(note_id, client_ip)
        
        if result["success"]:
            return {
                "success": True,
                "message": result["message"]
            }
        else:
            return {
                "success": False,
                "message": result["message"]
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to like note: {str(e)}")

@app.delete("/api/notes/{note_id}/like")
async def unlike_note(note_id: int, request: Request):
    """取消点赞"""
    try:
        client_ip = get_client_ip(request)
        result = SolutionService.unlike_note(note_id, client_ip)
        
        if result["success"]:
            return {
                "success": True,
                "message": result["message"]
            }
        else:
            return {
                "success": False,
                "message": result["message"]
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to unlike note: {str(e)}")

@app.get("/api/notes/{note_id}/liked")
async def check_note_liked(note_id: int, request: Request):
    """检查用户是否已点赞某个笔记"""
    try:
        client_ip = get_client_ip(request)
        is_liked = SolutionService.is_note_liked_by_user(note_id, client_ip)
        
        return {
            "success": True,
            "data": {"liked": is_liked}
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to check like status: {str(e)}")

@app.get("/api/user/likes")
async def get_user_likes(request: Request):
    """获取用户点赞的笔记ID列表"""
    try:
        client_ip = get_client_ip(request)
        liked_notes = SolutionService.get_user_likes(client_ip)
        
        return {
            "success": True,
            "data": {"liked_notes": liked_notes}
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get user likes: {str(e)}")

# ==================== Message Wall Stickers API ====================

@app.get("/api/wall/stickers")
async def get_all_stickers():
    """获取所有便签"""
    try:
        stickers = WallStickerService.get_all_stickers()
        return {
            "success": True,
            "data": [sticker.to_dict() for sticker in stickers],
            "count": len(stickers)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch stickers: {str(e)}")

@app.get("/api/wall/stickers/{sticker_id}")
async def get_sticker_by_id(sticker_id: int):
    """根据ID获取特定便签"""
    try:
        sticker = WallStickerService.get_sticker_by_id(sticker_id)
        if not sticker:
            raise HTTPException(status_code=404, detail="Sticker not found")
        
        return {
            "success": True,
            "data": sticker.to_dict()
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch sticker: {str(e)}")

@app.post("/api/wall/stickers")
async def create_sticker(request: Request):
    """创建新便签"""
    try:
        body = await request.json()
        text = body.get("text", "").strip()
        type = body.get("type", "anxiety")
        category = body.get("category", "").strip()
        body_part = body.get("body_part", "").strip()
        intensity = body.get("intensity", 3)
        position_x = body.get("position_x", 50.0)
        position_y = body.get("position_y", 50.0)
        rotation = body.get("rotation", 0.0)
        
        if not text:
            raise HTTPException(status_code=400, detail="Text is required")
        
        if len(text) > 500:
            raise HTTPException(status_code=400, detail="Text too long (max 500 characters)")
        
        if type not in ["anxiety", "support"]:
            type = "anxiety"
        
        if intensity not in [1, 2, 3, 4, 5]:
            intensity = 3
        
        sticker_id = WallStickerService.create_sticker(
            text, type, category, body_part, intensity, position_x, position_y, rotation
        )
        
        if sticker_id:
            return {
                "success": True,
                "message": "Sticker created successfully",
                "data": {"id": sticker_id}
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to create sticker")
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create sticker: {str(e)}")

@app.put("/api/wall/stickers/{sticker_id}/position")
async def update_sticker_position(sticker_id: int, request: Request):
    """更新便签位置"""
    try:
        body = await request.json()
        position_x = body.get("position_x")
        position_y = body.get("position_y")
        rotation = body.get("rotation")
        
        if position_x is None or position_y is None:
            raise HTTPException(status_code=400, detail="position_x and position_y are required")
        
        success = WallStickerService.update_sticker_position(sticker_id, position_x, position_y, rotation)
        
        if success:
            return {
                "success": True,
                "message": "Position updated successfully"
            }
        else:
            raise HTTPException(status_code=404, detail="Sticker not found or update failed")
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update position: {str(e)}")

@app.delete("/api/wall/stickers/{sticker_id}")
async def delete_sticker(sticker_id: int):
    """删除便签"""
    try:
        success = WallStickerService.delete_sticker(sticker_id)
        
        if success:
            return {
                "success": True,
                "message": "Sticker deleted successfully"
            }
        else:
            raise HTTPException(status_code=404, detail="Sticker not found")
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete sticker: {str(e)}")

@app.get("/api/wall/stickers/filter")
async def get_stickers_by_filter(category: str = "all", intensity: str = "all"):
    """根据过滤条件获取便签"""
    try:
        stickers = WallStickerService.get_stickers_by_filter(category, intensity)
        return {
            "success": True,
            "data": [sticker.to_dict() for sticker in stickers],
            "count": len(stickers)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch filtered stickers: {str(e)}")

# ==================== Sticker Connections API ====================

@app.post("/api/wall/connections")
async def create_connection(request: Request):
    """创建便签连接"""
    try:
        body = await request.json()
        sticker1_id = body.get("sticker1_id")
        sticker2_id = body.get("sticker2_id")
        
        if not sticker1_id or not sticker2_id:
            raise HTTPException(status_code=400, detail="sticker1_id and sticker2_id are required")
        
        if sticker1_id == sticker2_id:
            raise HTTPException(status_code=400, detail="Cannot connect sticker to itself")
        
        result = StickerConnectionService.create_connection(sticker1_id, sticker2_id)
        
        return {
            "success": result["success"],
            "message": result["message"]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create connection: {str(e)}")

@app.delete("/api/wall/connections")
async def delete_connection(request: Request):
    """删除便签连接"""
    try:
        body = await request.json()
        sticker1_id = body.get("sticker1_id")
        sticker2_id = body.get("sticker2_id")
        
        if not sticker1_id or not sticker2_id:
            raise HTTPException(status_code=400, detail="sticker1_id and sticker2_id are required")
        
        success = StickerConnectionService.delete_connection(sticker1_id, sticker2_id)
        
        if success:
            return {
                "success": True,
                "message": "Connection deleted successfully"
            }
        else:
            return {
                "success": False,
                "message": "Connection not found"
            }
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete connection: {str(e)}")

@app.get("/api/wall/connections")
async def get_all_connections():
    """获取所有连接"""
    try:
        connections = StickerConnectionService.get_all_connections()
        return {
            "success": True,
            "data": [conn.to_dict() for conn in connections],
            "count": len(connections)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch connections: {str(e)}")

# ==================== Sticker Reactions API ====================

@app.post("/api/wall/stickers/{sticker_id}/reactions")
async def add_sticker_reaction(sticker_id: int, request: Request):
    """添加便签反应"""
    try:
        body = await request.json()
        reaction_type = body.get("reaction_type")
        user_ip = get_client_ip(request)
        
        if not reaction_type or reaction_type not in ["same", "great"]:
            raise HTTPException(status_code=400, detail="Invalid reaction_type. Must be 'same' or 'great'")
        
        result = StickerReactionService.add_reaction(sticker_id, reaction_type, user_ip)
        
        return {
            "success": result["success"],
            "message": result["message"]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add reaction: {str(e)}")

@app.delete("/api/wall/stickers/{sticker_id}/reactions")
async def remove_sticker_reaction(sticker_id: int, request: Request):
    """移除便签反应"""
    try:
        body = await request.json()
        reaction_type = body.get("reaction_type")
        user_ip = get_client_ip(request)
        
        if not reaction_type or reaction_type not in ["same", "great"]:
            raise HTTPException(status_code=400, detail="Invalid reaction_type. Must be 'same' or 'great'")
        
        success = StickerReactionService.remove_reaction(sticker_id, reaction_type, user_ip)
        
        if success:
            return {
                "success": True,
                "message": "Reaction removed successfully"
            }
        else:
            return {
                "success": False,
                "message": "Reaction not found"
            }
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to remove reaction: {str(e)}")

@app.get("/api/wall/stickers/{sticker_id}/reactions")
async def get_sticker_reactions(sticker_id: int):
    """获取便签反应统计"""
    try:
        reactions = StickerReactionService.get_sticker_reactions(sticker_id)
        return {
            "success": True,
            "data": reactions
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get reactions: {str(e)}")

@app.get("/api/wall/user/reactions")
async def get_user_reactions(request: Request):
    """获取用户的所有反应"""
    try:
        user_ip = get_client_ip(request)
        reactions = StickerReactionService.get_user_reactions(user_ip)
        return {
            "success": True,
            "data": reactions
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get user reactions: {str(e)}")

# 全局异常处理
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """全局异常处理器"""
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Internal server error",
            "detail": str(exc)
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True, log_level="info")
