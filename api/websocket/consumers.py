import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.shortcuts import get_object_or_404
from app import models
from datetime import datetime, timezone
from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model

from api.transaction.serializers import TransactionSerializer

class WebSocketConsumer(AsyncWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._data = None

    async def connect(self):
        await self.channel_layer.group_add("gps_group", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("gps_group", self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)

        # await self.process_gps_data(data)
        self._data = data

        await self.send(text_data=json.dumps(data))

        await self.channel_layer.group_send(
            "gps_group",
            {
                "type": "gps_data_message",
                "message": data,
            }
        )

    @sync_to_async
    def process_gps_data(self, data):
        # Process the GPS data asynchronously
        latitude = data.get('latitude', None)
        longitude = data.get('longitude', None)
        email = data.get('email', None)

        User = get_user_model()

        # Do something with the GPS data
        # print('Received GPS data - Latitude:', latitude, 'Longitude:',
        #       longitude)

        if email:
            search_person = get_object_or_404(models.Person, email=email)

            get_user = User.objects.get(email=email)

            get_transaction, created = models.Transaction.objects.update_or_create(
                persons=search_person,
                defaults={
                    'lat': latitude,
                    'lng': longitude,
                    'datetime': datetime.now(timezone.utc),
                    'modified_by': get_user
                })

        # Respond back to the client (if needed)
        response_data = {'message': 'GPS data received'}
        # self.send(text_data=json.dumps(response_data))

    async def gps_data_message(self, event):
        message = event['message']
        await self.process_gps_data(self._data)
        await self.send(text_data=json.dumps(message))

class DashboardMapConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("gps_group", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("gps_group", self.channel_name)

    async def receive(self, text_data):
        # This consumer does not need to process received data
        # response = await self.dashboard_map()
        # print(response)
        # print("asdasd")
        pass

    @sync_to_async
    def dashboard_map(self):
        all_trans = models.Transaction.objects.all()
        trans_serialize = TransactionSerializer(all_trans, many=True).data

        return trans_serialize

    async def gps_data_message(self, event):
        message = event['message']
        response = await self.dashboard_map()

        await self.send(text_data=json.dumps(response))

class TrackPersonConsumer(AsyncWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._data = None
        self._receive = None

    async def connect(self):
        await self.channel_layer.group_add("gps_group", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("gps_group", self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        self._receive = data
        await self.send(text_data=json.dumps(data))

    @sync_to_async
    def get_data(self, data=None):

        value = data.get("value", None)
        names = list(filter(None, value))
        obj = models.Transaction.objects.filter(persons__full_name__in=names)
        serializer = TransactionSerializer(obj, many=True).data
        return serializer

    async def gps_data_message(self, event):
        data = await self.get_data(self._receive)

        await self.send(text_data=json.dumps(data))
        # pass