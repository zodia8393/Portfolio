import mysql.connector
from mysql.connector import Error, pooling
from typing import Optional, List, Dict
import logging
import asyncio
from aiomysql import create_pool
import json

logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self, host: str, user: str, password: str, database: str, port: int, pool_size: int = 5):
        self.db_config = {
            'host': host,
            'user': user,
            'password': password,
            'db': database,
            'port': port,
            'maxsize': pool_size,
            'minsize': 1,
            'autocommit': True,
        }
        self.pool = None

    async def initialize(self):
        try:
            self.pool = await create_pool(**self.db_config)
            await self.create_tables()
        except Error as e:
            logger.error(f"Error connecting to MySQL Database: {e}")
            raise RuntimeError(f"Error connecting to MySQL Database: {e}")

    async def create_tables(self) -> None:
        create_participants_table = """
            CREATE TABLE IF NOT EXISTS participants (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                face_embedding JSON,
                avg_lip_sync_score FLOAT
            )
        """
        create_speech_segments_table = """
            CREATE TABLE IF NOT EXISTS speech_segments (
                id INT AUTO_INCREMENT PRIMARY KEY,
                participant_id INT,
                start_time FLOAT,
                end_time FLOAT,
                transcription TEXT,
                FOREIGN KEY (participant_id) REFERENCES participants(id)
            )
        """
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(create_participants_table)
                await cur.execute(create_speech_segments_table)

    async def add_participant(self, name: str, face_embedding: List[float], avg_lip_sync_score: float) -> Optional[int]:
        query = """
            INSERT INTO participants (name, face_embedding, avg_lip_sync_score)
            VALUES (%s, %s, %s)
        """
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                try:
                    await cur.execute(query, (name, json.dumps(face_embedding), avg_lip_sync_score))
                    return cur.lastrowid
                except Error as e:
                    logger.error(f"Error adding participant: {e}")
                    return None

    async def add_speech_segment(self, participant_id: int, start_time: float, end_time: float, transcription: str) -> None:
        query = """
            INSERT INTO speech_segments (participant_id, start_time, end_time, transcription)
            VALUES (%s, %s, %s, %s)
        """
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                try:
                    await cur.execute(query, (participant_id, start_time, end_time, transcription))
                except Error as e:
                    logger.error(f"Error adding speech segment: {e}")

    async def get_participant_id(self, name: str) -> Optional[int]:
        query = "SELECT id FROM participants WHERE name = %s"
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                try:
                    await cur.execute(query, (name,))
                    result = await cur.fetchone()
                    return result[0] if result else None
                except Error as e:
                    logger.error(f"Error getting participant ID: {e}")
                    return None

    async def get_all_participants(self) -> List[Dict]:
        query = "SELECT * FROM participants"
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                try:
                    await cur.execute(query)
                    columns = [column[0] for column in cur.description]
                    results = await cur.fetchall()
                    return [dict(zip(columns, row)) for row in results]
                except Error as e:
                    logger.error(f"Error getting all participants: {e}")
                    return []

    async def get_speech_segments_by_participant(self, participant_id: int) -> List[Dict]:
        query = "SELECT * FROM speech_segments WHERE participant_id = %s"
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                try:
                    await cur.execute(query, (participant_id,))
                    columns = [column[0] for column in cur.description]
                    results = await cur.fetchall()
                    return [dict(zip(columns, row)) for row in results]
                except Error as e:
                    logger.error(f"Error getting speech segments: {e}")
                    return []

    async def close(self) -> None:
        self.pool.close()
        await self.pool.wait_closed()

# Usage example
async def main():
    db_manager = DatabaseManager('localhost', 'user', 'password', 'database', 3306)
    await db_manager.initialize()
    
    # Add a participant
    participant_id = await db_manager.add_participant('John Doe', [0.1, 0.2, 0.3], 0.85)
    
    # Add a speech segment
    if participant_id:
        await db_manager.add_speech_segment(participant_id, 0.0, 5.0, "Hello, world!")
    
    # Get all participants
    participants = await db_manager.get_all_participants()
    print(participants)
    
    # Get speech segments for a participant
    if participant_id:
        segments = await db_manager.get_speech_segments_by_participant(participant_id)
        print(segments)
    
    await db_manager.close()

if __name__ == "__main__":
    asyncio.run(main())