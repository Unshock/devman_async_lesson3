from aiohttp import web

from archive_downloader.handlers import handle_index_page, handle_archive


def get_urls():

    urls = [
        web.get('/', handle_index_page),
        web.get('/archive/{archive_hash}/', handle_archive),
    ]

    return urls
