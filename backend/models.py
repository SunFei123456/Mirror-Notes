from datetime import datetime

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
