import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.shortcuts import get_object_or_404
from app import models
from datetime import datetime, timezone, date
from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model
from collections import defaultdict, OrderedDict
import requests

from api.transaction.serializers import TransactionSerializer, PathTraceSerializer

class WebSocketConsumer(AsyncWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._data = None
        self.user = None
        self.group_name = None

    async def connect(self):
        if self.scope["user"].is_authenticated:
            self.user = self.scope["user"]
            self.group_name = f"user_{self.user.id}"
            await self.channel_layer.group_add(self.group_name,
                                               self.channel_name)
            await self.channel_layer.group_add("admin_group",
                                               self.channel_name)
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name,
                                               self.channel_name)
        await self.channel_layer.group_discard("admin_group",
                                               self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        self._data = data

        await self.process_gps_data(data)

        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "gps_data_message",
                "message": data,
                "user_id": self.user.id
            }
        )

        await self.channel_layer.group_send(
            "admin_group",
            {
                "type": "gps_data_message",
                "message": data,
                "user_id": self.user.id
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

            # get_response = requests.get(f"https://nominatim.openstreetmap.org/"
            #                         f"reverse?lat={latitude}&lon={longitude}"
            #                         f"&zoom=18&addressdetails=1&format=json")
            #
            # location = get_response.json()['display_name']

            get_transaction, created = models.Transaction.objects.update_or_create(
                persons=search_person,
                defaults={
                    'lat': latitude,
                    'lng': longitude,
                    # 'location': location,
                    'datetime': datetime.now(timezone.utc),
                    'modified_by': get_user
                })

            models.PathTrace.objects.create(
                persons=search_person,
                datetime=datetime.now(timezone.utc),
                lat=latitude,
                lng=longitude
            )

        # Respond back to the client (if needed)
        response_data = {'message': 'GPS data received'}
        # self.send(text_data=json.dumps(response_data))

    async def gps_data_message(self, event):
        message = event['message']
        user_id = event['user_id']
        await self.send(text_data=json.dumps({"user_id": user_id,
                                              "data": message}))


class DashboardMapConsumer(AsyncWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None
        self.group_name = None

    async def connect(self):
        if self.scope["user"].is_authenticated:
            self.user = self.scope["user"]
            self.group_name = f"user_{self.user.id}"
            await self.channel_layer.group_add("admin_group",
                                               self.channel_name)
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("admin_group",
                                               self.channel_name)

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
        self.user = None
        self.group_name = None

    async def connect(self):
        if self.scope["user"].is_authenticated:
            self.user = self.scope["user"]
            self.group_name = f"user_{self.user.id}"
            await self.channel_layer.group_add("admin_group",
                                               self.channel_name)
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("admin_group",
                                               self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        self._receive = data
        # await self.send(text_data=json.dumps(data))

    @sync_to_async
    def get_data(self, data):

        if data is not None:
            value = data.get('value', None)
            names = list(filter(None, value))
            # obj = models.Transaction.objects.filter(persons__full_name__in=names)
            # serializer = TransactionSerializer(obj, many=True).data
            get_path = models.PathTrace.objects.filter(
                persons__full_name__in=names,
                datetime__date=date.today())

            path_serializer = PathTraceSerializer(get_path, many=True).data

            grouped_data = defaultdict(list)
            for record in path_serializer:
                person_id = record['person']['id']
                grouped_data[person_id].append({
                    'id': record['id'],
                    'lat': record['lat'],
                    'lng': record['lng'],
                    'name': record['person']['full_name'],
                })

            # Formatting the grouped data
            formatted_data = []
            for person_id, group in grouped_data.items():

                # Get the latest record for lat and lng
                latest_record = group[-1]
                # Fetch the destination from DeployedUnitPerson
                deployed_unit_person = models.DeployedUnitPerson.objects.filter(
                    person_id=person_id, deployed_unit__is_done=False).first()
                if deployed_unit_person:
                    destination = deployed_unit_person.deployed_unit.destination
                else:
                    destination = None


                person_data = {'id': group[0]['id'], 'name': group[0]['name'],
                               'lat': float(group[-1]['lat']),
                               'lng': float(group[-1]['lng']),
                               'destination': destination,
                               'path': [{'lat': float(record['lat']),
                                         'lng': float(record['lng'])} for
                                        record in
                                        group]}
                formatted_data.append(person_data)

            # print(formatted_data)

            return formatted_data

    async def gps_data_message(self, event):
        data = await self.get_data(self._receive)
        await self.send(text_data=json.dumps(data))
        # pass