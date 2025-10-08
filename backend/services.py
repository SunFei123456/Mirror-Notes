from database import db
from models import SolutionNote, UserLike
from datetime import datetime

class SolutionService:
    @staticmethod
    def get_all_notes():
        """获取所有解决方案笔记"""
        query = """
        SELECT id, content, author_name, author_type, like_count, helped_count, created_at
        FROM solution_notes 
        ORDER BY created_at DESC
        """
        result = db.execute_query(query)
        if result:
            return [SolutionNote.from_dict(row) for row in result]
        return []
    
    @staticmethod
    def get_note_by_id(note_id):
        """根据ID获取笔记"""
        query = """
        SELECT id, content, author_name, author_type, like_count, helped_count, created_at
        FROM solution_notes 
        WHERE id = %s
        """
        result = db.execute_query(query, (note_id,))
        if result:
            return SolutionNote.from_dict(result[0])
        return None
    
    @staticmethod
    def create_note(content, author_name="Anonymous", author_type="anonymous"):
        """创建新的解决方案笔记"""
        query = """
        INSERT INTO solution_notes (content, author_name, author_type, like_count, helped_count)
        VALUES (%s, %s, %s, 0, 0)
        """
        affected_rows = db.execute_update(query, (content, author_name, author_type))
        if affected_rows > 0:
            # 获取新创建的笔记ID
            get_id_query = "SELECT LAST_INSERT_ID() as id"
            result = db.execute_query(get_id_query)
            if result:
                return result[0]['id']
        return None
    
    @staticmethod
    def like_note(note_id, user_ip):
        """点赞笔记"""
        # 检查是否已经点赞
        check_query = "SELECT id FROM user_likes WHERE user_ip = %s AND note_id = %s"
        existing_like = db.execute_query(check_query, (user_ip, note_id))
        
        if existing_like:
            return {"success": False, "message": "Already liked"}
        
        # 添加点赞记录
        like_query = "INSERT INTO user_likes (user_ip, note_id) VALUES (%s, %s)"
        like_result = db.execute_update(like_query, (user_ip, note_id))
        
        if like_result > 0:
            # 更新笔记的点赞数和帮助数
            update_query = """
            UPDATE solution_notes 
            SET like_count = like_count + 1, helped_count = helped_count + 1 
            WHERE id = %s
            """
            db.execute_update(update_query, (note_id,))
            return {"success": True, "message": "Liked successfully"}
        
        return {"success": False, "message": "Failed to like"}
    
    @staticmethod
    def unlike_note(note_id, user_ip):
        """取消点赞"""
        # 删除点赞记录
        delete_query = "DELETE FROM user_likes WHERE user_ip = %s AND note_id = %s"
        delete_result = db.execute_update(delete_query, (user_ip, note_id))
        
        if delete_result > 0:
            # 更新笔记的点赞数和帮助数
            update_query = """
            UPDATE solution_notes 
            SET like_count = GREATEST(like_count - 1, 0), 
                helped_count = GREATEST(helped_count - 1, 0) 
            WHERE id = %s
            """
            db.execute_update(update_query, (note_id,))
            return {"success": True, "message": "Unliked successfully"}
        
        return {"success": False, "message": "No like found to remove"}
    
    @staticmethod
    def get_user_likes(user_ip):
        """获取用户点赞的笔记ID列表"""
        query = "SELECT note_id FROM user_likes WHERE user_ip = %s"
        result = db.execute_query(query, (user_ip,))
        if result:
            return [row['note_id'] for row in result]
        return []
    
    @staticmethod
    def is_note_liked_by_user(note_id, user_ip):
        """检查用户是否已点赞某个笔记"""
        query = "SELECT id FROM user_likes WHERE user_ip = %s AND note_id = %s"
        result = db.execute_query(query, (user_ip, note_id))
        return len(result) > 0 if result else False
