import os
import asyncio
import argparse

import aiohttp
from PIL import Image
from io import BytesIO


async def save_image(session, i, dir):
    url = 'https://picsum.photos/600/600?random'

    print(f'Start {i}')
    response = await session.get(url)
    image_raw = await response.read()
    img = Image.open(BytesIO(image_raw))
    img.save(f'{dir}/image_{i}.jpeg', 'JPEG')
    print(f'Finish {i}')

async def main(n, dir):
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*(save_image(session, i, dir) for i in range(n)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dir', default='images/')
    parser.add_argument('--n', type=int, default=10)
    args = parser.parse_args()

    os.makedirs(args.dir, exist_ok=True)

    loop = asyncio.get_event_loop()
    try:
        loop.create_task(main(args.n, args.dir))
        loop.run_forever()
    finally:
        loop.close()