from aiohttp import web
import asyncio

from archive_downloader.settings import (
    STORAGE_DIRECTORY,
    CHUNK_SIZE_KB,
    SLOWING_TIME,
    SLOWING_STATE,
)
from archive_downloader.utils import convert_kilo_bytes_to_bytes
from archive_downloader.logger import setup_logger


logger = setup_logger()


async def archive_service(request):
    archive_hash = request.match_info['archive_hash']
    archive_name = _get_archive_name(archive_hash)

    response = web.StreamResponse()
    response = _prepare_response_with_headers(response, archive_name)
    await response.prepare(request)

    chunk_size = convert_kilo_bytes_to_bytes(CHUNK_SIZE_KB)
    zip_command = ['zip', '-r', '-', archive_hash]

    process = await asyncio.create_subprocess_exec(
        *zip_command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        cwd=STORAGE_DIRECTORY,
    )

    chunk_result = b''
    is_end_of_file = False
    try:
        while True:
            if process.stdout.at_eof():
                is_end_of_file = True

            archive_chunk = await process.stdout.read(chunk_size)
            chunk_result += archive_chunk
            cur_chunk_size = len(chunk_result)

            if cur_chunk_size >= chunk_size or is_end_of_file:
                logger.info(
                    f'Sending archive chunk of {cur_chunk_size}'
                    f' bytes into {archive_name}'
                )

                if SLOWING_STATE:
                    await asyncio.sleep(SLOWING_TIME)

                await response.write(chunk_result)
                chunk_result = b''

            if is_end_of_file:
                break

    except asyncio.CancelledError:
        logger.warning(
            f'Download was interrupted while sending {archive_name}',
        )
        raise

    except (SystemExit, KeyboardInterrupt, Exception) as exc:
        logger.error(
            f'Download was interrupted while sending {archive_name}'
            f' with exception: {exc}',
        )
        raise

    finally:
        await _finish_process(process)

    return response


async def _finish_process(process: asyncio.subprocess.Process) -> None:
    if process.returncode is None:
        try:
            await asyncio.wait_for(process.communicate(), timeout=5)
            logger.info(f'Process finished normally')
        except asyncio.TimeoutError:
            process.kill()
            logger.warning('Process was forcefully killed due to timeout')
            await process.communicate()
    else:
        await process.communicate()
        logger.info(f'Process already completed')


def _get_archive_name(archive_hash: str) -> str:
    return 'archive-' + archive_hash + '.zip'


def _prepare_response_with_headers(
        response: web.StreamResponse,
        archive_name: str,
) -> web.StreamResponse:
    response.headers['Transfer-Encoding'] = 'chunked'
    response.headers['Content-Disposition'] = (
        f'attachment; filename="{archive_name}"'
    )

    return response
