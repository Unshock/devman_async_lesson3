from aiohttp import web

from archive_downloader.urls import get_urls


def create_app():
    app = web.Application()
    app.add_routes(get_urls())
    return app
