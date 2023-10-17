import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.shortcuts import get_object_or_404
from app import models
from datetime import datetime, timezone
from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model

class WebSocketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        await self.process_gps_data(data)

    @sync_to_async
    def process_gps_data(self, data):
        # Process the GPS data asynchronously
        latitude = data.get('latitude', None)
        longitude = data.get('longitude', None)
        email = data.get('email', None)

        User = get_user_model()

        # Do something with the GPS data
        print('Received GPS data - Latitude:', latitude, 'Longitude:',
              longitude)

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
            print(get_transaction)
            print(get_user)

        # Respond back to the client (if needed)
        response_data = {'message': 'GPS data received'}
        self.send(text_data=json.dumps(response_data))
