import redis
import pickle

class RedisHandler:
    def __init__(self, host='localhost', port=6379, db=0):
        self.client = redis.Redis(
            host=host,
            port=port,
            db=db,
            decode_responses=False  # Keep binary data as is
        )

    def cache_video_chunk(self, chunk_path, data, expire_time=3600):
        """Cache video chunk data with expiration time"""
        redis_key = f"video_chunk:{chunk_path}"
        return self.client.setex(
            redis_key,
            expire_time,
            pickle.dumps(data)
        )

    def get_video_chunk(self, chunk_path):
        """Retrieve video chunk from cache"""
        redis_key = f"video_chunk:{chunk_path}"
        data = self.client.get(redis_key)
        return pickle.loads(data) if data else None

    def clear_cache(self):
        """Clear all cached video chunks"""
        self.client.flushdb()

    def is_connected(self):
        """Check if Redis connection is alive"""
        try:
            return self.client.ping()
        except redis.ConnectionError:
            return False