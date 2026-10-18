from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from datetime import time


class preMatch(BaseModel):
    recevant:str
    visiteur: str
    date:datetime
    heure:time
    division:str
    stade:str
