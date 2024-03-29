# from asgiref.sync import async_to_sync
# from channels.generic.websocket import WebsocketConsumer
# import json


# class NotificationConsumer(WebsocketConsumer):
#     def connect(self):
#         self.user = self.scope["url_route"]["kwargs"]["username"]
#         self.user_notification = "notification_%s" % self.user
        
#         async_to_sync(self.channel_layer.group_add)(
#             self.user_notification, self.channel_name
#         )
#         self.accept()
#     def disconnect(self, close_code):
#         async_to_sync(self.channel_layer.group_discard)(
#             self.user_notification, self.channel_name
#         )
        
#     def push_notification(self,event):
#         title = event["title"]
#         body = event["body"]
#         created = event["created"]
#         status = event["status"]
        
#         self.send(text_data=json.dumps(
#             {
#                 "title":title, "body":body, "created":created, "status":status
#             }
#         ))