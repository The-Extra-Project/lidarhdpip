import aiosqlite
from typing import List
import time
import sys

sys.path.append('..')

class Database():
    def __init__(self, *, connection: aiosqlite.Connection):
        self.connection = connection
        
    async def add_job_status(
        self, user_id: str, job_id:str, result_id: str, timestamps_created: int
    ) -> int:
        """
        adds the history of the user's history of running the geospatial job, so as to fetch the details when needed 
        user_id: is the user name on discord who created the request
        result_id: is the uid of the bacalhau request  that is returned after the computation of the result.
        job_id: is the uid of the bacalhau request that is instantiated by the user
        timestamp_id: is the time of creation of the instance.
        """
        record: aiosqlite.Connection = self.connection.execute(
            "SELECT id FROM geospatial_jobs WHERE user_id=? AND job_id=? ORDER BY id DESC LIMIT 1"
        )
        
        ## Now if some of the user has added the first job, we will update the correpsonding parameters:
        
        with record as cursor:
            result = await cursor.fetchone()
            timestamp = time.time() 
            await self.connection.execute(
                "INSERT INTO warns(user_id, job_id, result_id, created_at) VALUES (?, ?, ?, ?, ?)",
                (   
                    user_id,
                    job_id,
                    result_id,
                    timestamps_created,
                ),
            )

            await self.connection.commit()
            return user_id
        
        