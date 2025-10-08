#!/usr/bin/env python3
"""
Mirror Notes Backend Server
启动脚本
"""

import uvicorn
from main import app

if __name__ == "__main__":
    print("🚀 Starting Mirror Notes Backend Server...")
    print("📝 API Documentation: http://localhost:8000/docs")
    print("🔗 API Base URL: http://localhost:8000")
    print("💾 Database: MySQL (mirror-notes-db)")
    print("-" * 50)
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True,  # 开发模式下自动重载
        log_level="info"
    )
