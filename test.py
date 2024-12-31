import asyncio
import logging
import random
import aioshutil
from aiopath import AsyncPath
from time import time

logging.basicConfig(
    format="%(asctime)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
    handlers=[logging.StreamHandler()],
)


async def create_test_files(base_path, num_files, num_folders):
    extensions = ['txt', 'jpg', 'csv', 'json', 'py']
    base_folder = AsyncPath(base_path)

    if await base_folder.exists():
        await aioshutil.rmtree(base_folder)
    await base_folder.mkdir(parents=True, exist_ok=True)

    files_per_folder = (num_files + num_folders - 1) // num_folders
    file_count = 0

    for folder_index in range(1, num_folders + 1):
        folder_path = base_folder / f"folder_{folder_index}"
        await folder_path.mkdir(parents=True, exist_ok=True)

        for _ in range(files_per_folder):
            if file_count >= num_files:
                break
            ext = random.choice(extensions)
            file_path = folder_path / f"test_file_{file_count + 1}.{ext}"
            async with file_path.open(mode='w') as f:
                await f.write(f"This is {file_path.name}\n"*10)
            file_count += 1


async def main():
    source = input("Enter a path for target folder: ")
    num_files = int(input("Number of files to generate: "))
    num_folders = int(input("Number of folder to generate: "))
    source_path = AsyncPath(source)
    start = time()
    await create_test_files(source_path, num_files, num_folders)
    logging.info('Files generated in %.2f seconds', time() - start)


if __name__ == "__main__":
    asyncio.run(main())
