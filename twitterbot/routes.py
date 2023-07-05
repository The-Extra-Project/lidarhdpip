import traceback
from fastapi import BackgroundTasks,Depends,APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from model import User
from fastapi_jwt_auth import AuthJWT

from tweepy import TwitterAccess


router: APIRouter = APIRouter(prefix='/lidarpip/bot', tags=["bot"])


async def get_twitter(Authorize: AuthJWT = Depends()):
    pass