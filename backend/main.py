from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from services import SolutionService
from models import SolutionNote
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
    uvicorn.run(app, host="0.0.0.0", port=8000)
