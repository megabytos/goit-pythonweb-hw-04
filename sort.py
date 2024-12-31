import argparse
from aiopath import AsyncPath
import aioshutil
import asyncio
import logging
from time import time

logging.basicConfig(
    format="%(asctime)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
    handlers=[logging.StreamHandler()],
)


def parse_arguments():
    parser = argparse.ArgumentParser(description="File sorter by extension")
    parser.add_argument('-s', '--source', type=str, help='Path to the source folder', required=False)
    parser.add_argument('-t', '--target', type=str, help='Path to the target folder', required=False)
    args, unknown_args = parser.parse_known_args()
    if args.source and args.target:
        source = args.source
        target = args.target
    elif len(unknown_args) == 2:
        source = unknown_args[0]
        target = unknown_args[1]
    else:
        source = input("Enter a path for source folder: ")
        target = input("Enter a path for target folder: ")
    return source, target


async def read_folder(folder: AsyncPath):
    file_paths = []
    async for path in folder.rglob('*'):
        if await path.is_file():
            file_paths.append(path)
    return file_paths


async def copy_file(file_path, target_folder):
    extension = file_path.suffix.lstrip('.') or "no_extension"
    extension_folder = target_folder / extension
    target_path = extension_folder / file_path.name
    try:
        await extension_folder.mkdir(parents=True, exist_ok=True)
        await aioshutil.copy(file_path, target_path)
    except Exception as e:
        logging.error(f"Error copying {file_path} to {target_path}: {e}")


async def main():
    source, target = parse_arguments()
    source_folder = AsyncPath(source)
    target_folder = AsyncPath(target)

    start = time()
    if not await source_folder.exists() or not await source_folder.is_dir():
        logging.error(f"Source folder {source_folder} does not exist")
        return
    file_paths = await read_folder(source_folder)
    if not file_paths:
        logging.error(f"Source folder {source_folder} is empty")
        return
    logging.info('Files read in %.2f seconds', time() - start)

    start = time()
    copy_coroutines = [copy_file(file_path, target_folder) for file_path in file_paths]
    await asyncio.gather(*copy_coroutines)
    logging.info('Files copied in %.2f seconds', time() - start)


if __name__ == "__main__":
    asyncio.run(main())
