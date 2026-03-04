from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import json
from database import messages_collection,group_collection
from model import ConnectionManager

private = APIRouter(prefix="/chat", tags=["chat"])

html ="""
<!DOCTYPE html>
<html>
<head>
    <title>Private Chat</title>
</head>
<body>
    <h2>Private Chat App</h2>

    <h3>Your ID: <span id="my-id"></span></h3>

    <input type="text" id="receiverId" placeholder="Enter Receiver ID" />
    <br><br>

    <form onsubmit="sendMessage(event)">
        <input type="text" id="messageText" placeholder="Type message..." autocomplete="off"/>
        <button>Send</button>
    </form>

    <ul id="messages"></ul>

    <script>
        // Generate unique ID
        var client_id = Date.now().toString();
        document.getElementById("my-id").textContent = client_id;

        // Connect to WebSocket
        var ws = new WebSocket(`ws://localhost:8000/chat/ws/${client_id}`);

        // When message received
        ws.onmessage = function(event) {
            var messages = document.getElementById("messages");
            var li = document.createElement("li");
            li.textContent = event.data;
            messages.appendChild(li);
        };

        // Send message function
        function sendMessage(event) {
            event.preventDefault();

            var messageInput = document.getElementById("messageText");
            var receiverInput = document.getElementById("receiverId");

            if (!receiverInput.value) {
                alert("Enter Receiver ID bro!");
                return;
            }

            var messageData = {
                receiver_id: receiverInput.value,
                message: messageInput.value
            };

            ws.send(JSON.stringify(messageData));

            // Show own message in UI
            var messages = document.getElementById("messages");
            var li = document.createElement("li");
            li.textContent = "Me: " + messageInput.value;
            messages.appendChild(li);

            messageInput.value = "";
        }
    </script>
</body>
</html>
"""
manager = ConnectionManager()
@private.get("/")
async def get():
    return HTMLResponse(html)

@private.websocket('/ws/{user_id}')
async def websocket_endpoint(websocket:WebSocket,user_id:str):
    await manager.connect(websocket,user_id)
    try:
        while True:
            data=await websocket.receive_text()
            message=json.loads(data)
            receiver_id=message["receiver_id"]
            message_text=message["message"]
            data={'user_id':user_id,'receiver_id':receiver_id,'message':message_text}
            data.pop("_id",None)
            await messages_collection.insert_one(data)
            await manager.private_chat(user_id=data['user_id'],receiver_id=data['receiver_id'],message=data['message'])
    except WebSocketDisconnect:
        manager.disconnect(user_id)
        
        
# @private.websocket('/ws/{user_id}')
# async def websocket_endpoint(websocket:WebSocket,user_id:str):
#     await manager.connect(websocket,user_id)
#     try:
#         while True:
#             data= await websocket.receive_text()
#             message=json.loads(data)
#             data={'user_id':user_id,'message':message_text}
#             await group_collection.insert_one({'user_id':user_id,'message':message})
            
#     except WebSocketDisconnect:
#         manager.disconnect(user_id)
        

            
            # if receiver_id in active_users:
            #     receiver_socket=active_users[receiver_id]
            # for receiver, connection in active_users.items():
            #     if receiver == receiver_id:
                # await receiver_socket.send_text(f'{user_id} sent you message: {message_text}')
    # except WebSocketDisconnect:
    #     active_users.pop(user_id,None)
        
        # while True:
        #     data = await websocket.receive_text()
        #     message = json.loads(data)
        #     receiver = message["receiver_id"]
        #     message = message["message"]
        #     for receiver_id, connection in active_users.items():
        #         if receiver == receiver_id:
        #             await active_users[receiver_id].send_text(f"{user_id}: {message}")
    # except WebSocketDisconnect:
    #     active_users.pop(user_id, None)                
    
        
        
# 		data=await websocket.receive_text()
# For connection in active_users:
# 		await connection.send_text(f’{user id} sends message: {data}’)
# class ConnectionManager:
#     def __init__(self):
#         self.active_connections:list[WebSocket] = []
#     async def connect(self,websocket:WebSocket):
#         await websocket.accept()
#         self.active_connections.append(websocket)
#     def disconnect(self,websocket:WebSocket):
#         self.active_connections.remove(websocket)
#     async def personal_message(self,message:str,websocket:WebSocket):
#         await websocket.send_text(message)
#     async def broadcast(self,message:str):
#         for connections in self.active_connections:
#             await connections.send_text(message)
            
            
# manager= ConnectionManager()

# @app.websocket('/ws/{client_id}')
# async def websocket_endpoint(websocket:WebSocket,client_id:int):
#     await manager.connect(websocket)
#     while True:
#         data= await websocket.receive_text()
#         await manager.broadcast(f'Broadcast message: {data}')

# @app.websocket('/ws')
# async def websocket_endpoint(websocket:WebSocket):
#     await websocket.accept() 
#     while True:
#         data= await websocket.receive_text() 
#         await websocket.send_text(f' you have sent {data}' )

# active_users={} or []

# @app.websocket('/ws/{user_id}')
# async def websocket_endpoint(websocket:WebSocket,user_id:int):
#     await websocket.accept()
#     if user_id not in active_users:
#         # active_users.append[websocket] or active_users[user_id]=websocket
#         active_users[user_id]=websocket
#     try:
#         while True:
#             message =await websocket.receive_text()
#             for user, connection in active_users.items():
#                 if connection != websocket:
#                     await connection.send_text(f"User {user} says: {message}")
#     except WebSocketDisconnect:
#         active_users.pop(user_id, None)

    
    
    
# @app.post('/send_message')
# async def send_message(private:Private):
#     if private.receiver_id in active_users:
#         await active_users[private.receiver_id].send_text(f'{private.user_id} sends message: {private.message} to {private.receiver_id}')
