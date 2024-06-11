from datetime import datetime

import pymongo
from pymongo.command_cursor import CommandCursor

from src.config import FORMAT_INTERVAL, DATABASE, MONGO_DB

class Request:
    def __init__(self, dt_from, dt_upto, group_type):
        self.dt_from = datetime.fromisoformat(dt_from)
        self.dt_upto = datetime.fromisoformat(dt_upto)
        self.group_type = group_type

async def get_queryset(request: Request) -> CommandCursor:
    pipeline = [
        {"$match": {"dt": {"$gte": request.dt_from, "$lte": request.dt_upto}}},
        {
            "$group": {
                "_id": {
                    "$dateToString": {
                        "format": FORMAT_INTERVAL.get(
                            request.group_type,
                            "month"
                        ),
                        "date": "$dt"
                    }
                }, "total_salary": {"$sum": "$value"}
            }
        },
        {"$sort": {"_id": 1}}
    ]
    with pymongo.MongoClient(MONGO_DB) as client:
        db = client[DATABASE]
        queryset = db.salary.aggregate(pipeline)
    return queryset