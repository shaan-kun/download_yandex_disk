import asyncio
import json
from pathlib import Path
from typing import List, Dict

import m3u8
from aiohttp import ClientSession

PLAYLIST_FILE = "playlists.json"


async def download_video_by_parts(playlist_url: str, video_name: str):
    async with ClientSession() as session:
        async with session.get(playlist_url) as response:
            playlist = m3u8.loads(await response.text())

        video_dir = Path('videos') / video_name
        video_dir.mkdir()

        base_url = '/'.join(playlist_url.split('/')[:-1])
        for segment in playlist.data["segments"]:
            segment = segment['uri'].split('?')[0]
            async with session.get('/'.join((base_url, segment))) as response:
                video_content = await response.read()

            with open(video_dir / segment, "wb") as f:
                f.write(video_content)


async def main(videos: List[Dict]):
    tasks = []
    for video in videos:
        task = asyncio.create_task(download_video_by_parts(video['url'], video['name']))
        tasks.append(task)

    for task in tasks:
        await task


with open(PLAYLIST_FILE, encoding='utf-8') as f:
    videos = json.loads(f.read())

asyncio.run(main(videos))
