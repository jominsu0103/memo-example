from fastapi import FastAPI , Query , HTTPException
from pydantic import BaseModel
from typing import List
from fastapi.staticfiles import StaticFiles
from pymongo import MongoClient
from bson import ObjectId 
import json

class Memo(BaseModel):
  id:int
  title:str
  content:str
  createdAt:str

class Friend(BaseModel):
  name:str
  phoneNumber:str

class Message(BaseModel):
  sender:str
  message:str

client = MongoClient('mongodb://127.0.0.1:27017/')
db = client['database_test']
collection = db['mycollection']

chat_log = []

app = FastAPI()

# 챗 부분
@app.post('/chat')
async def send_chat(message: Message):
  chat_log.append(message)
  return "message received successful"

@app.get("/chat")
async def get_chat_log():
  return chat_log

# 메모 부분
# post method
@app.post("/memos")
def create_memo(memo:Memo):
  data = {
  'id' : memo.id,
  'title' : memo.title,
  'content' : memo.content,
  'created_at' : memo.createdAt
}
  result = collection.insert_one(data)
  return 'request successful'

# get method
@app.get("/memos")
def read_memo(sort: str = Query(None, description="정렬 속성"),
              order: str = Query("ASC", description="정렬 순서 (ASC 또는 DESC)")):
    # MongoDB에서 메모 가져오기 및 정렬
    if sort == "title":
        memos = list(collection.find().sort("title", 1 if order == "ASC" else -1))
    elif sort == "createdAt":
        memos = list(collection.find().sort("created_at", 1 if order == "ASC" else -1))
    else:
        memos = list(collection.find())

    serialized_memos = [{key: memo[key] for key in memo if key != '_id'} for memo in memos]
    return serialized_memos

# put method
@app.put('/memos/{memo_id}')
def put_memo(memo_id:str ,req_memo:Memo):
  # MongoDB에서 메모 업데이트
    update_result = collection.update_one(
        {'id': int(memo_id)},
        {'$set': {'title': req_memo.title, 'content': req_memo.content}}
    )
    if update_result.modified_count:
        return '수정 성공'
    else:
        return '메모를 찾을 수 없습니다'

# delete method
@app.delete('/memos/{memo_id}')
def delete_memo(memo_id:str):
  # MongoDB에서 메모 삭제
    delete_result = collection.delete_one({'id': int(memo_id)})
    if delete_result.deleted_count:
        return '삭제 성공'
    else:
        return '메모를 찾을 수 없습니다'

# friend
# post method
@app.post('/friend')
async def add_friend(friend : Friend):
  data = {
    "name" : friend.name,
    "phone_number" : friend.phoneNumber
  }
  result = collection.insert_one(data)
  return {"message": "친구가 추가되었습니다.", "friend_id": str(result.inserted_id)}

# get method
@app.get("/friend")
async def get_friends():
    # MongoDB에서 모든 친구 조회
    friends = list(collection.find())
    # ObjectId 제거
    for friend in friends:
        friend['_id'] = str(friend['_id'])  # ObjectId를 문자열로 변환
    return friends

# get method (search by name)
@app.get("/friend/search")
async def search_friends_by_name(name: str = Query(..., description="검색할 친구의 이름")):
    # MongoDB에서 이름으로 친구 검색
    friends = list(collection.find({"name": name}))
    # ObjectId 제거
    for friend in friends:
        friend['_id'] = str(friend['_id'])  # ObjectId를 문자열로 변환
    if not friends:
        raise HTTPException(status_code=404, detail="해당 이름의 친구를 찾을 수 없습니다.")
    return friends

# delete method
@app.delete("/friend/{friend_id}")
async def delete_friend(friend_id: str):
    # MongoDB에서 친구 삭제
    result = collection.delete_one({"_id": ObjectId(friend_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="해당 ID의 친구를 찾을 수 없습니다.")
    return {"message": "친구가 삭제되었습니다."}

app.mount("/", StaticFiles(directory='static' , html= True), name='static')
