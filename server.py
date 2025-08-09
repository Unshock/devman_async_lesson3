import argparse
from aiohttp import web

from archive_downloader.logger import setup_logger
from archive_downloader.application import create_app

logger = setup_logger()

def parse_arguments():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument(
        '--host',
        type=str,
        help='host name',
        required=False,
        default='0.0.0.0',
    )
    parser.add_argument(
        '-p',
        '--port',
        type=int,
        help='port number',
        required=False,
        default=8080,
    )
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()
    host = args.host
    port = args.port
    logger.info(f'Starting the server with host={host}, port={port}')

    app = create_app()
    web.run_app(app, host=host, port=port)
