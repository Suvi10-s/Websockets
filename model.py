from fastapi import WebSocket

class ConnectionManager():
    def __init__(self):
        self.active_users={}
    async def connect(self,websocket:WebSocket,user_id:str):
        await websocket.accept()
        self.active_users[user_id]=websocket
    def disconnect(self,user_id):
        self.active_users.pop(user_id,None)
    async def private_chat(self,user_id,receiver_id,message):
        websocket=self.active_users.get(receiver_id)
        if websocket:
            await websocket.send_text(f'{message}')
            
    async def broadcast(self,message):
        for websocket in self.active_users.values():
            await websocket.send_text(f'{message}')
