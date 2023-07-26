# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import aiohttp
import asyncio
import argparse
from typing import Generator, List
from tqdm import tqdm


def create_request_tasks(session: aiohttp.ClientSession, url: str, num_requests: int) -> Generator[asyncio.Task, None, None]:
    """
    A generator function that yields tasks, with each task representing a GET request to the given URL using the provided session.

    Parameters:
    - session: aiohttp.ClientSession object
    - url: str, the URL to send GET requests to
    - num_requests: int, the number of requests to send

    Yields:
    - task: asyncio.Task object
    """
    for i in range(num_requests):
        # Create a GET request with the given URL and SSL disabled
        request = session.get(url, ssl=False)
        # Create a task to execute the request asynchronously and yield it
        yield asyncio.create_task(request)


async def send_requests(url: str, num_requests: int) -> List[aiohttp.ClientResponse]:
    """
    Sends multiple GET requests to the given URL concurrently using aiohttp library and asyncio library.

    Parameters:
    - url: str, the URL to send GET requests to
    - num_requests: int, the number of requests to send

    Returns:
    - responses: list of aiohttp.ClientResponse objects
    """
    async with aiohttp.ClientSession() as session:
        tasks = list(create_request_tasks(session, url, num_requests))

        # Use tqdm to display a loading indicator
        with tqdm(total=len(tasks)) as pbar:
            # Wait for all tasks to complete and return the responses as a list
            for f in asyncio.as_completed(tasks):
                await f
                pbar.update(1)


if __name__ == '__main__':
    # Set up argparse to parse command line arguments
    parser = argparse.ArgumentParser(description='Send multiple GET requests to a URL concurrently using aiohttp and asyncio.')
    parser.add_argument('url', type=str, help='The URL to send GET requests to')
    parser.add_argument('num_requests', type=int, help='The number of requests to send')
    args = parser.parse_args()

    # Set the event loop policy to the WindowsSelectorEventLoopPolicy on Windows platform to avoid a warning message
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    # Send the requests and get the responses
    asyncio.run(send_requests(args.url, args.num_requests))
