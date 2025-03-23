#!/usr/bin/env python3
import asyncio
import argparse
from modules.downloader import TurboDownloader
from modules.progress import StreamProgress
from config import API_ID, API_HASH, PHONE_NUMBER, BASE_DOWNLOAD_DIR

async def main(channel: str, workers: int):
    progress = StreamProgress()
    downloader = TurboDownloader(
        channel_username=channel,
        api_id=API_ID,
        api_hash=API_HASH,
        phone_number=PHONE_NUMBER,
        base_dir=BASE_DOWNLOAD_DIR,
        max_workers=workers,
        progress=progress
    )
    await downloader.run()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Telegram Media Downloader')
    parser.add_argument('-c', '--channel', required=True, help='Channel username')
    parser.add_argument('-w', '--workers', type=int, default=4, 
                      help='Number of concurrent workers')
    args = parser.parse_args()

    try:
        asyncio.run(main(args.channel, args.workers))
    except KeyboardInterrupt:
        print("\n🚨 Download interrupted! Cleaning up...")
