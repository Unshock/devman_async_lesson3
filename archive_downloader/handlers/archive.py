import os
from aiohttp import web

from archive_downloader import constants as c
from archive_downloader.services.archive import archive_service
from archive_downloader.settings import STORAGE_DIRECTORY


async def handle_archive(request):
    archive_hash = request.match_info['archive_hash']
    if archive_hash in os.listdir(STORAGE_DIRECTORY):
        return await archive_service(request)

    raise web.HTTPNotFound(text=c.ARCHIVE_NOT_FOUND_MESSAGE)
