import os
import re
import asyncio
from config import MAX_RETRIES, REQUEST_INTERVAL
from telethon import TelegramClient, errors
from telethon.tl.types import DocumentAttributeFilename
from .progress import StreamProgress

class TurboDownloader:
    def __init__(self, channel_username, api_id, api_hash, phone_number,
                 base_dir, max_workers, progress: StreamProgress):
        self.channel = channel_username
        self.api_id = api_id
        self.api_hash = api_hash
        self.phone = phone_number
        self.base_dir = base_dir
        self.max_workers = max_workers
        self.progress = progress

        self.client = None
        self.semaphore = asyncio.Semaphore(max_workers)
        self.download_dir = self._create_download_path()

    def _create_download_path(self):
        sanitized = re.sub(r'[^\w\-_\.]', '_', self.channel).strip()
        path = os.path.join(self.base_dir, sanitized)
        os.makedirs(path, exist_ok=True)
        return path

    async def _get_client(self):
        client = TelegramClient(
            session=f"{self.channel}_session",
            api_id=self.api_id,
            api_hash=self.api_hash
        )
        await client.start(self.phone)
        return client

    async def _download_media(self, message):
        file_path = os.path.join(self.download_dir, self._get_filename(message))
        filename = os.path.basename(file_path)

        if os.path.exists(file_path):
            return

        async with self.semaphore:
            for attempt in range(MAX_RETRIES):
                try:
                    # Initialize progress before download
                    await self.progress.update(
                        message.id,
                        current=0,
                        total=1,  # Temporary value
                        filename=filename
                    )

                    # Start download with progress tracking
                    result = await self.client.download_media(
                        message,
                        file=file_path,
                        progress_callback=lambda c,t: asyncio.create_task(
                            self.progress.update(
                                message.id,
                                current=c,
                                total=t,
                                filename=filename
                            )
                        )
                    )

                    # Verify final file size
                    if result and os.path.exists(file_path):
                        await self.progress.update(
                            message.id,
                            current=os.path.getsize(file_path),
                            total=os.path.getsize(file_path),
                            filename=filename
                        )
                        return True
                    return False

                except errors.FloodWaitError as e:
                    await asyncio.sleep(e.seconds + 5)
                except Exception as e:
                    await asyncio.sleep(2 ** attempt)
                finally:
                    if attempt == MAX_RETRIES - 1:
                        self.progress.report_failure()
            return False

    def _get_filename(self, message):
        if message.media:
            if hasattr(message.media, 'document'):
                for attr in message.media.document.attributes:
                    if isinstance(attr, DocumentAttributeFilename):
                        return attr.file_name
                return f"document_{message.id}.bin"
            elif hasattr(message.media, 'photo'):
                return f"photo_{message.id}.jpg"
        return f"file_{message.id}_{message.date.timestamp()}.bin"

    async def run(self):
        self.client = await self._get_client()
        try:
            channel = await self.client.get_entity(self.channel)
            async for message in self.client.iter_messages(channel):
                if message.media:
                    success = await self._download_media(message)
                    if success:
                        await asyncio.sleep(REQUEST_INTERVAL)
        except errors.ChannelPrivateError:
            print(f"\n❌ Error: Channel {self.channel} is private or inaccessible")
        except Exception as e:
            print(f"\n⚠️ Unexpected error: {str(e)}")
        finally:
            await self.client.disconnect()
            print()  # Ensure clean line after progress display
