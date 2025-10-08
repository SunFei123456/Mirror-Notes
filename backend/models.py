from datetime import datetime

class WallSticker:
    def __init__(self, id=None, text=None, type='anxiety', category='', body_part='', 
                 intensity=3, position_x=50.0, position_y=50.0, rotation=0.0, 
                 created_at=None, updated_at=None, same_count=0, great_count=0):
        self.id = id
        self.text = text
        self.type = type  # 'anxiety' or 'support'
        self.category = category
        self.body_part = body_part
        self.intensity = intensity
        self.position_x = position_x
        self.position_y = position_y
        self.rotation = rotation
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
        self.same_count = same_count
        self.great_count = great_count
    
    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'type': self.type,
            'category': self.category,
            'body_part': self.body_part,
            'intensity': self.intensity,
            'position_x': self.position_x,
            'position_y': self.position_y,
            'position': f"{self.position_x}%, {self.position_y}%",
            'rotation': self.rotation,
            'same_count': self.same_count,
            'great_count': self.great_count,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get('id'),
            text=data.get('text'),
            type=data.get('type', 'anxiety'),
            category=data.get('category', ''),
            body_part=data.get('body_part', ''),
            intensity=data.get('intensity', 3),
            position_x=data.get('position_x', 50.0),
            position_y=data.get('position_y', 50.0),
            rotation=data.get('rotation', 0.0),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at'),
            same_count=data.get('same_count', 0),
            great_count=data.get('great_count', 0)
        )

# StickerConnection 模型已删除 - 连线操作仅在前端UI处理

class StickerReaction:
    def __init__(self, id=None, sticker_id=None, reaction_type=None, user_ip=None, created_at=None):
        self.id = id
        self.sticker_id = sticker_id
        self.reaction_type = reaction_type  # 'same' or 'great'
        self.user_ip = user_ip
        self.created_at = created_at or datetime.now()
    
    def to_dict(self):
        return {
            'id': self.id,
            'sticker_id': self.sticker_id,
            'reaction_type': self.reaction_type,
            'user_ip': self.user_ip,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get('id'),
            sticker_id=data.get('sticker_id'),
            reaction_type=data.get('reaction_type'),
            user_ip=data.get('user_ip'),
            created_at=data.get('created_at')
        )

class SolutionNote:
    def __init__(self, id=None, content=None, author_name=None, author_type='anonymous', 
                 like_count=0, helped_count=0, created_at=None):
        self.id = id
        self.content = content
        self.author_name = author_name
        self.author_type = author_type  # 'anonymous' or 'signature'
        self.like_count = like_count
        self.helped_count = helped_count
        self.created_at = created_at or datetime.now()
    
    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'author_name': self.author_name,
            'author_type': self.author_type,
            'like_count': self.like_count,
            'helped_count': self.helped_count,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get('id'),
            content=data.get('content'),
            author_name=data.get('author_name'),
            author_type=data.get('author_type', 'anonymous'),
            like_count=data.get('like_count', 0),
            helped_count=data.get('helped_count', 0),
            created_at=data.get('created_at')
        )

class UserLike:
    def __init__(self, user_ip=None, note_id=None, created_at=None):
        self.user_ip = user_ip
        self.note_id = note_id
        self.created_at = created_at or datetime.now()
    
    def to_dict(self):
        return {
            'user_ip': self.user_ip,
            'note_id': self.note_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
