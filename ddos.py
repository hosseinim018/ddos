import aiohttp
import asyncio
import time
import argparse
from typing import Generator, List


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
        # Wait for all tasks to complete and return the responses as a list
        responses = await asyncio.gather(*create_request_tasks(session, url, num_requests))
        return responses


if __name__ == '__main__':
    # Set up argparse to parse command line arguments
    parser = argparse.ArgumentParser(description='Send multiple GET requests to a URL concurrently using aiohttp and asyncio.')
    parser.add_argument('url', type=str, help='The URL to send GET requests to')
    parser.add_argument('num_requests', type=int, help='The number of requests to send')
    args = parser.parse_args()

    # Set the event loop policy to the WindowsSelectorEventLoopPolicy on Windows platform to avoid a warning message
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    start_time = time.time()

    # Send the requests and get the responses
    responses: List[aiohttp.ClientResponse] = asyncio.run(send_requests(args.url, args.num_requests))

    end_time = time.time()

    # Print out the status code of each response received from the GET requests
    for response in responses:
        print(response.status)

    print(f"Total time taken: {end_time - start_time} seconds")