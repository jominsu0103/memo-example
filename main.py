from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles

class Memo(BaseModel):
  id:int
  content:str
  
class Message(BaseModel):
  sender:str
  message:str

chat_log = []
memos =[]

app = FastAPI()

@app.post('/chat')
async def send_chat(message: Message):
  chat_log.append(message)
  return "message received successful"

@app.get("/chat")
async def get_chat_log():
  return chat_log

@app.post("/memos")
def create_memo(memo:Memo):
  memos.append(memo)
  return 'request successful'

@app.get("/memos")
def read_memo():
  return memos

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
