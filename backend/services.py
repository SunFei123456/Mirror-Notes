from database import db
from models import SolutionNote, UserLike, WallSticker, StickerConnection, StickerReaction
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

class WallStickerService:
    @staticmethod
    def get_all_stickers():
        """获取所有便签"""
        query = """
        SELECT id, text, type, category, body_part, intensity, position_x, position_y, rotation, created_at, updated_at
        FROM wall_stickers 
        ORDER BY created_at DESC
        """
        result = db.execute_query(query)
        if result:
            return [WallSticker.from_dict(row) for row in result]
        return []
    
    @staticmethod
    def get_sticker_by_id(sticker_id):
        """根据ID获取便签"""
        query = """
        SELECT id, text, type, category, body_part, intensity, position_x, position_y, rotation, created_at, updated_at
        FROM wall_stickers 
        WHERE id = %s
        """
        result = db.execute_query(query, (sticker_id,))
        if result:
            return WallSticker.from_dict(result[0])
        return None
    
    @staticmethod
    def create_sticker(text, type='anxiety', category='', body_part='', intensity=3, position_x=50.0, position_y=50.0, rotation=0.0):
        """创建新便签"""
        query = """
        INSERT INTO wall_stickers (text, type, category, body_part, intensity, position_x, position_y, rotation)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        affected_rows = db.execute_update(query, (text, type, category, body_part, intensity, position_x, position_y, rotation))
        if affected_rows > 0:
            get_id_query = "SELECT LAST_INSERT_ID() as id"
            result = db.execute_query(get_id_query)
            if result:
                return result[0]['id']
        return None
    
    @staticmethod
    def update_sticker_position(sticker_id, position_x, position_y, rotation=None):
        """更新便签位置"""
        if rotation is not None:
            query = """
            UPDATE wall_stickers 
            SET position_x = %s, position_y = %s, rotation = %s, updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
            """
            affected_rows = db.execute_update(query, (position_x, position_y, rotation, sticker_id))
        else:
            query = """
            UPDATE wall_stickers 
            SET position_x = %s, position_y = %s, updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
            """
            affected_rows = db.execute_update(query, (position_x, position_y, sticker_id))
        
        return affected_rows > 0
    
    @staticmethod
    def delete_sticker(sticker_id):
        """删除便签"""
        query = "DELETE FROM wall_stickers WHERE id = %s"
        affected_rows = db.execute_update(query, (sticker_id,))
        return affected_rows > 0
    
    @staticmethod
    def get_stickers_by_filter(category='all', intensity='all'):
        """根据过滤条件获取便签"""
        base_query = """
        SELECT id, text, type, category, body_part, intensity, position_x, position_y, rotation, created_at, updated_at
        FROM wall_stickers 
        WHERE 1=1
        """
        params = []
        
        if category != 'all':
            if category == 'support':
                base_query += " AND type = 'support'"
            else:
                base_query += " AND category = %s"
                params.append(category)
        
        if intensity != 'all':
            base_query += " AND intensity = %s"
            params.append(int(intensity))
        
        base_query += " ORDER BY created_at DESC"
        
        result = db.execute_query(base_query, params)
        if result:
            return [WallSticker.from_dict(row) for row in result]
        return []

class StickerConnectionService:
    @staticmethod
    def create_connection(sticker1_id, sticker2_id):
        """创建便签连接"""
        # 检查连接是否已存在
        check_query = """
        SELECT id FROM sticker_connections 
        WHERE (sticker1_id = %s AND sticker2_id = %s) OR (sticker1_id = %s AND sticker2_id = %s)
        """
        existing = db.execute_query(check_query, (sticker1_id, sticker2_id, sticker2_id, sticker1_id))
        
        if existing:
            return {"success": False, "message": "Connection already exists"}
        
        # 创建连接
        query = "INSERT INTO sticker_connections (sticker1_id, sticker2_id) VALUES (%s, %s)"
        affected_rows = db.execute_update(query, (sticker1_id, sticker2_id))
        
        if affected_rows > 0:
            return {"success": True, "message": "Connection created successfully"}
        return {"success": False, "message": "Failed to create connection"}
    
    @staticmethod
    def delete_connection(sticker1_id, sticker2_id):
        """删除便签连接"""
        query = """
        DELETE FROM sticker_connections 
        WHERE (sticker1_id = %s AND sticker2_id = %s) OR (sticker1_id = %s AND sticker2_id = %s)
        """
        affected_rows = db.execute_update(query, (sticker1_id, sticker2_id, sticker2_id, sticker1_id))
        return affected_rows > 0
    
    @staticmethod
    def get_all_connections():
        """获取所有连接"""
        query = """
        SELECT id, sticker1_id, sticker2_id, created_at
        FROM sticker_connections
        ORDER BY created_at DESC
        """
        result = db.execute_query(query)
        if result:
            return [StickerConnection.from_dict(row) for row in result]
        return []

class StickerReactionService:
    @staticmethod
    def add_reaction(sticker_id, reaction_type, user_ip):
        """添加便签反应"""
        # 检查是否已经反应过
        check_query = """
        SELECT id FROM sticker_reactions 
        WHERE sticker_id = %s AND reaction_type = %s AND user_ip = %s
        """
        existing = db.execute_query(check_query, (sticker_id, reaction_type, user_ip))
        
        if existing:
            return {"success": False, "message": "Already reacted"}
        
        # 添加反应
        query = "INSERT INTO sticker_reactions (sticker_id, reaction_type, user_ip) VALUES (%s, %s, %s)"
        affected_rows = db.execute_update(query, (sticker_id, reaction_type, user_ip))
        
        if affected_rows > 0:
            return {"success": True, "message": "Reaction added successfully"}
        return {"success": False, "message": "Failed to add reaction"}
    
    @staticmethod
    def remove_reaction(sticker_id, reaction_type, user_ip):
        """移除便签反应"""
        query = """
        DELETE FROM sticker_reactions 
        WHERE sticker_id = %s AND reaction_type = %s AND user_ip = %s
        """
        affected_rows = db.execute_update(query, (sticker_id, reaction_type, user_ip))
        return affected_rows > 0
    
    @staticmethod
    def get_sticker_reactions(sticker_id):
        """获取便签的反应统计"""
        query = """
        SELECT reaction_type, COUNT(*) as count
        FROM sticker_reactions 
        WHERE sticker_id = %s
        GROUP BY reaction_type
        """
        result = db.execute_query(query, (sticker_id,))
        
        reactions = {'same': 0, 'great': 0}
        if result:
            for row in result:
                reactions[row['reaction_type']] = row['count']
        
        return reactions
    
    @staticmethod
    def get_user_reactions(user_ip):
        """获取用户的所有反应"""
        query = """
        SELECT sticker_id, reaction_type
        FROM sticker_reactions 
        WHERE user_ip = %s
        """
        result = db.execute_query(query, (user_ip,))
        
        user_reactions = {}
        if result:
            for row in result:
                sticker_id = row['sticker_id']
                if sticker_id not in user_reactions:
                    user_reactions[sticker_id] = []
                user_reactions[sticker_id].append(row['reaction_type'])
        
        return user_reactions
