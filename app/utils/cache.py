import redis
import json
from typing import Optional, Dict, Any
from app.config import settings

class CacheManager:
    """Redis缓存管理器"""
    
    def __init__(self):
        self.client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            decode_responses=True
        )
        self.expire = settings.CACHE_EXPIRE
    
    def get(self, key: str) -> Optional[Dict[str, Any]]:
        """获取缓存数据"""
        try:
            data = self.client.get(key)
            if data:
                return json.loads(data)
            return None
        except Exception as e:
            print(f"缓存读取失败: {str(e)}")
            return None
    
    def set(self, key: str, value: Dict[str, Any], expire: Optional[int] = None) -> bool:
        """设置缓存数据"""
        try:
            expire_time = expire if expire else self.expire
            self.client.set(key, json.dumps(value, ensure_ascii=False), ex=expire_time)
            return True
        except Exception as e:
            print(f"缓存写入失败: {str(e)}")
            return False
    
    def delete(self, key: str) -> bool:
        """删除缓存数据"""
        try:
            self.client.delete(key)
            return True
        except Exception as e:
            print(f"缓存删除失败: {str(e)}")
            return False
    
    def exists(self, key: str) -> bool:
        """检查缓存是否存在"""
        try:
            return self.client.exists(key) > 0
        except Exception as e:
            print(f"缓存检查失败: {str(e)}")
            return False

cache_manager = CacheManager()