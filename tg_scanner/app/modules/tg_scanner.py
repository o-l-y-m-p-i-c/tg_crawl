import asyncio
import datetime
import random
import threading
import math
from time import sleep
from telethon import TelegramClient, errors, functions

class TGScanner(threading.Thread):
    api_id = 27426964
    api_hash = 'dd1ee07cbf165e7bdd64d85361f7b209'

    max_depth = 4
    from_date = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=1008)
    golden_ratio_conjugate = 0.618033988749895
    h = random.random()

    def __init__(self):
        super().__init__()
        self.update = None
        self.add_node_list = None
        self.remove_node_list = None
        self.set_text = None

    def next_color(self):
        self.h += self.golden_ratio_conjugate
        self.h %= 1
        return self.hsv_to_rgb(self.h, .5, .95)

    @staticmethod
    def hsv_to_rgb(h, s, v):
        h_i = int(h * 6)
        f = h * 6 - h_i
        p = v * (1 - s)
        q = v * (1 - f * s)
        t = v * (1 - (1 - f) * s)
        if h_i == 0:
            r, g, b = v, t, p
        elif h_i == 1:
            r, g, b = q, v, p
        elif h_i == 2:
            r, g, b = p, v, t
        elif h_i == 3:
            r, g, b = p, q, v
        elif h_i == 4:
            r, g, b = t, p, v
        elif h_i == 5:
            r, g, b = v, p, q
        else:
            r, g, b = 0, 0, 0
        return int(r * 256), int(g * 256), int(b * 256)

    async def fetch_channel(self, client, channel_username):
        try:
            return await client.get_entity(channel_username)
        except errors.ChannelPrivateError:
            print(f"Cannot access channel: {channel_username}")
        except Exception as e:
            print(f"Error fetching channel {channel_username}: {e}")

    async def scan(self, channel_list):
        async with TelegramClient('anon', self.api_id, self.api_hash) as client:
            self.set_text({'id': 'date-time', 'text': self.from_date.strftime("%d-%m-%Y %H:%M:%S")})
            self.set_text({'id': 'depth', 'text': self.max_depth})

            start_channel = await client.get_entity(channel_list[0])
            channels_dict = {start_channel.id: self.init_channel_dict(start_channel, 0)}

            print("Starting channels:")
            for ch in channel_list:
                self.display_channel_info(ch)
            print("")

            await self.process_channels(client, channel_list, channels_dict, start_channel)

    def init_channel_dict(self, channel, depth):
        return {
            'out': [],
            'in': [],
            'msg_count': -1,
            'users': {},
            'title': channel.title,
            'depth': depth,
            'color': '#000000'
        }

    def display_channel_info(self, ch):
        print(ch.title if hasattr(ch, 'title') else ch.first_name)
        self.update({
            'nodes': [{'id': ch.id, 'label': ch.title, 'size': 10, 'color': {'border': '#ff0000'}}],
            'edges': []
        })
        self.add_node_list({'label': ch.title})

    async def process_channels(self, client, channel_list, channels_dict, curr_channel):
        channel_idx = 0
        date_time = datetime.datetime.now(datetime.timezone.utc)

        while True:
            if curr_channel.id not in channels_dict:
                channels_dict[curr_channel.id] = self.init_channel_dict(curr_channel, 0)

            hist = await client(self.get_history(curr_channel, date_time))
            channels_dict[curr_channel.id]['msg_count'] = hist.count
            await self.process_history(client, hist, channels_dict, curr_channel)

            if len(hist.messages) < 100 or date_time < self.from_date:
                channel_idx += 1
                self.remove_node_list()

                if channel_idx >= len(channel_list):
                    self.update_channel_colors(curr_channel.id, '#0000ff')
                    break

                self.update_channel_colors(curr_channel.id, '#0000ff', channel_list[channel_idx].id, '#ff0000')
                date_time = datetime.datetime.now(datetime.timezone.utc)
                curr_channel = channel_list[channel_idx]
                print("")
                print("New channel: " + (curr_channel.title if hasattr(curr_channel, 'title') else curr_channel.first_name))
            else:
                date_time = hist.messages[-1].date

    async def process_history(self, client, hist, channels_dict, curr_channel):
        for user in hist.users:
            channels_dict[curr_channel.id]['users'][user.id] = user.first_name

        for msg in hist.messages:
            if msg.date < self.from_date:
                break
            if msg.fwd_from and hasattr(msg.fwd_from.from_id, 'channel_id'):
                ch_ = await self.get_forwarded_channel(client, msg)
                if ch_:
                    self.update_channel_data(channels_dict, curr_channel, ch_)

    async def get_forwarded_channel(self, client, msg):
        try:
            return await client.get_entity(msg.fwd_from.from_id)
        except errors.ChannelPrivateError:
            return None

    def update_channel_data(self, channels_dict, curr_channel, ch_):
        if ch_.id not in channels_dict:
            channels_dict[ch_.id] = self.init_channel_dict(ch_, channels_dict[curr_channel.id]['depth'] + 1)
        channels_dict[ch_.id]['out'].append(curr_channel.id)
        channels_dict[curr_channel.id]['in'].append(ch_.id)

        c = len(channels_dict[ch_.id]['out'])
        if c > 1 and channels_dict[curr_channel.id]['color'] == '#000000':
            channels_dict[curr_channel.id]['color'] = "#%02x%02x%02x" % self.next_color()

        data = {
            'nodes': [{'id': ch_.id, 'label': ch_.title, 'size': math.pow(c, 1 / 1.9) + 10}],
            'edges': [{
                'id': '{}{}'.format(curr_channel.id, ch_.id),
                'from': ch_.id,
                'to': curr_channel.id,
                'color': channels_dict[ch_.id]['color'] if c > len(channels_dict[curr_channel.id]['out']) else channels_dict[curr_channel.id]['color']
            }]
        }
        self.update(data)

    def update_channel_colors(self, curr_id, curr_color, next_id=None, next_color=None):
        nodes = [{'id': curr_id, 'color': {'border': curr_color}}]
        if next_id:
            nodes.append({'id': next_id, 'color': {'border': next_color}})
        self.update({'nodes': nodes})

    def get_history(self, ch, dt):
        return functions.messages.GetHistoryRequest(
            peer=ch,
            offset_id=0,
            offset_date=dt,
            add_offset=0,
            limit=100,
            max_id=0,
            min_id=0,
            hash=0
        )

    async def get_channels(self, keyword):
        async with TelegramClient('anon', self.api_id, self.api_hash) as client:
            result = await client(functions.contacts.SearchRequest(q=keyword, limit=2))
            return [channel for channel in result.chats]

    def run(self):
        keywords = [
            '$PEPE', '$BRETT', '$ANDY', '$LANDWOLF',
            '$TURBO', '$MYRO', '$HOPPY', '$WIF',
            '$MANEKI', '$FOXY', '$MAGA', '$LFGO', '$POLA',
        ]

        channel_list = []
        for keyword in keywords:
            channel_list += asyncio.run(self.get_channels(keyword))

        while True:
            sleep(5)
            try:
                asyncio.run(self.scan(channel_list))
            except (errors.rpcerrorlist.PhoneNumberInvalidError, errors.rpcerrorlist.AccessTokenInvalidError) as e:
                print(e.message)
                pass
