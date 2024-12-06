import asyncio
import datetime
import json
import math
import random
import base64
import hashlib
import threading
from time import sleep
import requests
from html.parser import HTMLParser
import urllib.request
# from bs4 import BeautifulSou
import numpy as np
from telethon.errors import ChannelPrivateError, rpcerrorlist
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.types import ChatPhotoEmpty

def hash_file(file_path):
    # Create a SHA-256 hash object
    sha256_hash = hashlib.sha256()
    
    # Open the file in binary mode
    with open(file_path, "rb") as f:
        # Read the file in chunks to avoid large memory usage
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    
    # Return the hexadecimal digest of the hash
    return sha256_hash.hexdigest()
def get_history(ch, dt):
    return GetHistoryRequest(
        peer=ch,
        offset_id=0,
        offset_date=dt,
        add_offset=0,
        limit=100,
        max_id=0,
        min_id=0,
        hash=0
    )

def get_channel_photo_url(channel_username):
    url = f"https://t.me/{channel_username}"
    
    try:
        with urllib.request.urlopen(url) as response:
            html = response.read().decode('utf-8')
        
        parser = ImageParser()
        parser.feed(html)
        
        if parser.image_url:
            return parser.image_url
        else:
            print(f"No image found with class 'tgme_page_photo_image' for channel {channel_username}")
            return None
    
    except urllib.error.URLError as e:
        print(f"Error fetching page for channel {channel_username}: {e}")
        return None

def color_gradient(x):
    return 255 * x, 0, 255 - 255 * x

def get_complex_telegram_url(entity):
    if not hasattr(entity, 'photo') or not entity.photo or isinstance(entity.photo, ChatPhotoEmpty):
        return None
    
    if not hasattr(entity, 'access_hash') or not entity.access_hash:
        return None
    
    if not hasattr(entity.photo, 'photo_id') or not hasattr(entity.photo, 'dc_id'):
        return None

    # Extract necessary information
    photo_id = entity.photo.photo_id
    access_hash = entity.access_hash
    entity_id = entity.id
    dc_id = entity.photo.dc_id

    # Create a unique identifier
    unique_id = f"{entity_id}:{access_hash}:{photo_id}"

    # Generate a hash of the unique identifier
    hash_object = hashlib.sha256(unique_id.encode())
    hash_digest = hash_object.digest()

    # Convert the hash to a URL-safe base64 string
    url_hash = base64.urlsafe_b64encode(hash_digest).decode('utf-8').rstrip('=')

    # Construct the URL
    return f"https://cdn{dc_id}.cdn-telegram.org/file/{unique_id}.jpg"

def get_image_from_api(entity):
    if not hasattr(entity, 'photo') or not entity.photo or isinstance(entity.photo, ChatPhotoEmpty):
        return None
    if not hasattr(entity, 'username'):
        return None

    url = f"https://core-api.privateai.com/social/telegram/profilePhoto/@{entity.username}"

    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        content_type = response.headers.get('Content-Type', '')
        if content_type.startswith('image/'):
            return url
        else:
            print(f"Unexpected content type: {content_type}")
            return None
    except requests.RequestException as e:
        print(f"Error fetching image from API: {e}")
        return None


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

class ImageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.image_url = None

    def handle_starttag(self, tag, attrs):
        if tag == 'img':
            attrs = dict(attrs)
            if 'class' in attrs and 'tgme_page_photo_image' in attrs['class']:
                self.image_url = attrs.get('src')

class TGScanner(threading.Thread):
    api_id = 22222967
    api_hash = 'fe6a3f18e0ceb89afd2527b7ff0f1c47'

    start_channel = "t.me/hamsterdrops"

    max_depth = 4
    from_date = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=18)

    golden_ratio_conjugate = 0.618033988749895
    h = random.randint(0, 256)

    def __init__(self):
        super().__init__()
        self.update = None
        self.add_node_list = None
        self.remove_node_list = None
        self.set_text = None

    def next_color(self):
        self.h += self.golden_ratio_conjugate
        self.h %= 1
        return hsv_to_rgb(self.h, .5, .95)

    async def fetch_channel(self, client, channel_username):
        try:
            return await client.get_entity(channel_username)
        except ChannelPrivateError:
            print(f"Cannot access channel: {channel_username}")
        except Exception as e:
            print(f"Error fetching channel {channel_username}: {e}")

    async def scan(self):
        async with TelegramClient('anon', self.api_id, self.api_hash) as client:

            self.set_text({'id': 'date-time', 'text': self.from_date.strftime("%d-%m-%Y %H:%M:%S")})
            self.set_text({'id': 'depth', 'text': self.max_depth})

            channels_usernames = [
                "t.me/Tradinatorr",
                "t.me/ALGOCAL",
                "t.me/Abiskar_Calls",
                "t.me/AmikusID_Official",
                "t.me/AnbessasAlphaTA",
                "t.me/Aquariumcall",
                "t.me/AsiaCommunity",
                "t.me/BNB_CaII",
                "t.me/BadBoyCall",
                "t.me/Bear_Call",
                "t.me/BigsmokeCall",
                "t.me/Biyoti_Call",
                "t.me/BlockchainCoal_News",
                "t.me/CALL_KINGS",
                "t.me/Call_Wolverine",
                "t.me/Calls_wolf",
                "t.me/CoinPost",
                "t.me/CommunityHomeS",
                "t.me/CryptoAdvanceNews",
                "t.me/CryptoDamin",
                "t.me/CryptoDanceClub",
                "t.me/CryptoExplorerNews",
                "t.me/CryptoFun_id",
                "t.me/CryptoGemo",
                "t.me/CryptoGemsKing",
                "t.me/CryptoNPro",
                "t.me/CryptoNiceCalls",
                "t.me/CryptoTribalcommunity",
                "t.me/Cryptolandann",
                "t.me/DarkAngelCall",
                "t.me/DegenerateChronicles",
                "t.me/EngagingCalls",
                "t.me/EurosniperDegen",
                "t.me/Ezcoinmarketcalls",
                "t.me/FCI_ChannelOfficial",
                "t.me/FalleraCrypto",
                "t.me/Finance_Calls",
                "t.me/Football_Calls",
                "t.me/GAMING_Call",
                "t.me/GARUDACALL",
                "t.me/Gems_Call97",
                "t.me/GhostRider_Call",
                "t.me/Gladiator_Call",
                "t.me/Globallcall",
                "t.me/GobellCallss",
                "t.me/GodfatherCall",
                "t.me/Golf_Call",
                "t.me/HOSPITALCAII",
                "t.me/Helios_call",
                "t.me/HerooDoge",
                "t.me/HotSpeed_Call",
                "t.me/KanyesGreatestHits",
                "t.me/KaptenCallsOfficial",
                "t.me/KazutoraLounge",
                "t.me/KinCalls",
                "t.me/Lambe_Kripto",
                "t.me/LeclercCalls",
                "t.me/LeoCryptoID",
                "t.me/LeoDiCryptoCalls",
                "t.me/LeopardKollz",
                "t.me/LoverCalls",
                "t.me/MASK_CALL",
                "t.me/MidasAlpha",
                "t.me/Mini_Crypto_News",
                "t.me/MissCallz",
                "t.me/Monkeycall2",
                "t.me/Naruto_CALL",
                "t.me/NationalBlockchainAnn",
                "t.me/Nothing_call",
                "t.me/OneinBillions",
                "t.me/PauliesCannoli",
                "t.me/Poker_Calls",
                "t.me/PowsGemCalls",
                "t.me/PresaleSignals",
                "t.me/Princess_callss",
                "t.me/QualityPresale",
                "t.me/ROYALCROWN_CALL",
                "t.me/Rabbit_Calls_202",
                "t.me/Rainbow_call",
                "t.me/RakyatKripto",
                "t.me/RedBull_Calls",
                "t.me/Rhinocal",
                "t.me/RocketCallzz",
                "t.me/Rooster_Call",
                "t.me/Royallcall",
                "t.me/RscAnnouncement",
                "t.me/SerbaSerbiCrypto",
                "t.me/Shanghaicalls",
                "t.me/SimplicityGroup",
                "t.me/Snake_Call",
                "t.me/Spooky_Call",
                "t.me/StarSong_Call",
                "t.me/Sword_Calls",
                "t.me/TROYCALL",
                "t.me/TheUniqueTech",
                "t.me/Tigers_Calls",
                "t.me/Timoncall",
                "t.me/USACommunitysupportNews",
                "t.me/Universe_Call",
                "t.me/Vinscall",
                "t.me/WallstreetbetsGemsX100",
                "t.me/Westsideforum",
                "t.me/XMoonCall",
                "t.me/YakuzaCall",
                "t.me/alisresearch",
                "t.me/alphapleaseupdates",
                "t.me/call_Unicorn",
                "t.me/call_currency",
                "t.me/chainedgealpha",
                "t.me/cmcomm_ann",
                "t.me/crismooncalls",
                "t.me/cryptoclubn01",
                "t.me/cryptogoodreads",
                "t.me/cryptoironsalerts",
                "t.me/cryptolyxecalls",
                "t.me/cryptonarratives1",
                "t.me/cryptorugmuncher",
                "t.me/defi_hanzo",
                "t.me/defiantportal",
                "t.me/degensgems/",
                "t.me/dexcall",
                "t.me/dopevelligambles",
                "t.me/emperor_calls",
                "t.me/eunicalls",
                "t.me/excavonews",
                "t.me/fatmancalls",
                "t.me/finish_aIpha",
                "t.me/hatoriinvestments",
                "t.me/houseofdegeneracy",
                "t.me/infinityhedge",
                "t.me/lobsters_daily",
                "t.me/maisoncalls",
                "t.me/monkeykingcall",
                "t.me/overdose_gems_calls",
                "t.me/panda_call",
                "t.me/pantheracalls",
                "t.me/pinkcatkols",
                "t.me/planetcalls",
                "t.me/rektplebs",
                "t.me/richchatpublic",
                "t.me/senzu_calls",
                "t.me/shahlito",
                "t.me/shineigems",
                "t.me/shitcoinsandgems",
                "t.me/smolinsanity",
                "t.me/solsticebillboard",
                "t.me/solsticesmoonshots",
                "t.me/swordcalls",
                "t.me/whaleGem_calls",
                "t.me/yajuzacalls",
                "t.me/yurnerocall",
                "t.me/DJTtoken",
                "t.me/blumcrypto",
                "t.me/CoingraphNews",
                "t.me/crypto",
                "t.me/cryptobosh",
                "t.me/Cryptoy",
                "t.me/blumcrypto",
                "t.me/CoingraphNews",
                "t.me/crypto",
                "t.me/cryptobosh",
                "t.me/Cryptoy",
                "t.me/eunicalls",
                "t.me/infinityhedge",
                "t.me/rektplebs",
                "t.me/cryptolyxecalls",
                "t.me/EngagingCalls",
                "t.me/defiantportal",
                "t.me/lobsters_daily",
                "t.me/PowsGemCalls",
                "t.me/houseofdegeneracy",
                "t.me/hatoriinvestments",
                "t.me/dopevelligambles",
                "t.me/LeoDiCryptoCalls",
                "t.me/richchatpublic",
                "t.me/DegenerateChronicles",
                "t.me/alisresearch",
            ]

            channels = []
            for username in channels_usernames:
                ch = await self.fetch_channel(client, username)
                if ch:
                    channels.append(ch)

            start_channel = await client.get_entity(self.start_channel)
            channels.append(start_channel)

            channels_dict = {}
            channels_dict[start_channel.id] = {
                'out': [],
                'in': [],
                'msg_count': -1,
                'users': {},
                'title': start_channel.title,
                'depth': 0,
                'color': '#ffffff'
            }

            c_max = 10
            channel_idx = 0
            date_time = datetime.datetime.now(datetime.timezone.utc)
            curr_channel = start_channel

           
            print("Starting channels:")
            for ch_ in channels:

                # if hasattr(ch_, 'username'):
                #     image = get_channel_photo_url(ch_.username)
                # else:
                #     image = None

                # info = get_complex_telegram_url(ch_)
                image_url = get_image_from_api(ch_)

                print(ch_.title if hasattr(ch_, 'title') else ch_.first_name)
                if image_url:
                    self.update({
                        'nodes': [{
                            'id': ch_.id,
                            'label': ch_.title,
                            'msg':str(ch_.title)  + str(ch_.username),
                            'telegram_username': ch_.username,
                            'image': image_url,
                            'size': 30,
                            'color': {
                                'border': '#ff0000'
                            }
                        }],
                        'edges': []
                    })
                else:
                    self.update({
                        'nodes': [{
                            'id': ch_.id,
                            'label': ch_.title,
                            'msg':str(ch_.title) + str(ch_.username),
                            'telegram_username': ch_.username,
                            'size': 30,
                            'color': {
                                'border': '#ff0000'
                            }
                        }],
                        'edges': []
                    })
                self.add_node_list({'label': ch_.title})
            print("")
            print("New channel: " + (curr_channel.title if hasattr(curr_channel, 'title') else curr_channel.first_name))

            while True:
                hist = (await asyncio.gather(client(get_history(curr_channel, date_time))))[0]

                if curr_channel.id not in channels_dict:
                    channels_dict[curr_channel.id] = {
                        'out': [],
                        'in': [],
                        'msg_count': -1,
                        'users': {},
                        'title': curr_channel.title,
                        'depth': 0,
                        'color': '#ffffff'
                    }

                channels_dict[curr_channel.id]['msg_count'] = hist.count

                for user in hist.users:
                    channels_dict[curr_channel.id]['users'][user.id] = user.first_name

                for msg in hist.messages:
                    if msg.date < self.from_date:
                        date_time = msg.date
                        break
                    if msg.fwd_from and hasattr(msg.fwd_from.from_id, 'channel_id'):
                        try:
                            ch_ = (await asyncio.gather(client.get_entity(msg.fwd_from.from_id)))[0]
                        except ChannelPrivateError:
                            continue

                        if channels_dict[curr_channel.id]['depth'] < self.max_depth and ch_ not in channels:
                            channels.append(ch_)
                            print("New channel found: " + ch_.title)
                            
                            self.add_node_list({'label': ch_.title})

                        if ch_.id not in channels_dict.keys():
                            channels_dict[ch_.id] = {
                                'out': [curr_channel.id],
                                'in': [],
                                'msg_count': -1,
                                'users': {},
                                'title': ch_.title,
                                'depth': channels_dict[curr_channel.id]['depth'] + 1,
                                'color': '#ffffff'
                            }
                        else:
                            if channels_dict[ch_.id]['depth'] > channels_dict[curr_channel.id]['depth'] + 1:
                                channels_dict[ch_.id]['depth'] = channels_dict[curr_channel.id]['depth'] + 1
                            channels_dict[ch_.id]['out'].append(curr_channel.id)

                        channels_dict[curr_channel.id]['in'].append(ch_.id)

                        c = len(channels_dict[ch_.id]['out'])

                        if c > 1 and channels_dict[curr_channel.id]['color'] == '#000000':
                            channels_dict[curr_channel.id]['color'] = "#%02x%02x%02x" % self.next_color()

                        image_url = get_image_from_api(ch_)

                        if image_url:
                            data = {
                                'nodes': [{
                                    'id': ch_.id,
                                    'label': ch_.title,
                                    'telegram_username': ch_.username,
                                    'msg':msg.message + str(ch_.title) + str(ch_.username),
                                    'image':image_url,
                                    'size': math.pow(len(channels_dict[ch_.id]['out']), 1 / 1.9) + 30
                                }],
                                'edges': [{
                                    'id': '{}{}'.format(curr_channel.id, ch_.id),
                                    'from': ch_.id,
                                    'to': curr_channel.id,
                                    'color': channels_dict[ch_.id]['color']
                                    if c > len(channels_dict[curr_channel.id]['out'])
                                    else channels_dict[curr_channel.id]['color']
                                }]
                            }
                        else: 
                            data = {
                                'nodes': [{
                                    'id': ch_.id,
                                    'label': ch_.title,
                                    'msg':msg.message + str(ch_.title) + str(ch_.username),
                                    'telegram_username': ch_.username,
                                    'size': math.pow(len(channels_dict[ch_.id]['out']), 1 / 1.9) + 30
                                }],
                                'edges': [{
                                    'id': '{}{}'.format(curr_channel.id, ch_.id),
                                    'from': ch_.id,
                                    'to': curr_channel.id,
                                    'color': channels_dict[ch_.id]['color']
                                    if c > len(channels_dict[curr_channel.id]['out'])
                                    else channels_dict[curr_channel.id]['color']
                                }]
                            }
                        self.update(data)

                if len(hist.messages) < 100 or date_time < self.from_date:
                    channel_idx += 1
                    self.remove_node_list()

                    if channel_idx >= len(channels):
                        self.update({
                            'nodes': [
                                {
                                    'id': curr_channel.id,
                                    'color': {
                                        'border': '#0000ff'
                                    }
                                }]
                        })
                        break

                    self.update({
                        'nodes': [
                            {
                                'id': curr_channel.id,
                                'color': {
                                    'border': '#0000ff'
                                }
                            },
                            {
                                'id': channels[channel_idx].id,
                                'color': {
                                    'border': '#ff0000'
                                }
                            }]
                    })
                    date_time = datetime.datetime.now(datetime.timezone.utc)
                    curr_channel = channels[channel_idx]
                    print("")
                    print("New channel: " + (curr_channel.title if hasattr(curr_channel, 'title') else curr_channel.first_name))
                else:
                    date_time = hist.messages[-1].date
    def run(self):
        # sleep(1)
        
        # self.update({
        #     'nodes': [{
        #         'id': 15,
        #         'label': "ch_.title"
        #     }],
        #     'edges': [{
        #         'id': '{}{}'.format(15, 1),
        #         'from': 1,
        #         'to': 15
        #     }]
        # })

        while True:
            sleep(15)
            try:
                asyncio.run(self.scan())
            except (rpcerrorlist.PhoneNumberInvalidError, rpcerrorlist.AccessTokenInvalidError) as e:
                print(e.message)
                pass
                
