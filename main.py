from fastapi import FastAPI , Query
from pydantic import BaseModel
from typing import List
from fastapi.staticfiles import StaticFiles

class Memo(BaseModel):
  id:int
  title:str
  content:str
  createdAt:str
  
class Message(BaseModel):
  sender:str
  message:str

#정렬하기 위한 함수
def sort_memo_by_property(memos: List[Memo], prop: str, order: str):
    if prop == "createdAt":
        return sorted(memos, key=lambda x: x.createdAt, reverse=(order == "DESC"))
    else:
        if order == "ASC":
            return sorted(memos, key=lambda x: getattr(x, prop).lower())
        else:
            return sorted(memos, key=lambda x: getattr(x, prop).lower(), reverse=True)

chat_log = []
memos =[]

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
@app.post("/memos")
def create_memo(memo:Memo):
  memos.append(memo)
  return 'request successful'

@app.get("/memos")
def read_memo(sort: str = Query(None, description="정렬 기준 속성"),
              order: str = Query("ASC", description="정렬 방법 (ASC 또는 DESC)")):
  sorted_memos = memos
  
  if sort == "ABC":
      # 가나다ABC순으로 정렬
      sorted_memos = sort_memo_by_property(memos, "title", order)
  elif sort == "createdAt":
      # 등록 순으로 정렬
      sorted_memos = sorted(memos, key=lambda x: x.createdAt, reverse=(order == "DESC"))
    
  return [memo.model_dump() for memo in sorted_memos]

@app.put('/memos/{memo_id}')
def put_memo(req_memo:Memo):
  for memo in memos:
    if memo.id == req_memo.id:
      memo.content = req_memo.content
      return '성공했습니다.'
  return '그런 메모는 없습니다'

@app.delete('/memos/{memo_id}')
def delete_memo(memo_id:int):
  for index,memo in enumerate(memos):
      if memo.id == memo_id:
        memos.pop(index)
        return '성공했습니다'
  return '그런 메모는 없습니다'


app.mount("/", StaticFiles(directory='static' , html= True), name='static')
