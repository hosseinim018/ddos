# Asynchronous HTTP Requests using aiohttp and asyncio

This Python script sends multiple GET requests to a URL concurrently using the `aiohttp` library and the `asyncio` library.


#  Dependencies

This script requires the following Python packages to be installed:

-   `aiohttp`
-   `asyncio`
-   `tqdm` (for displaying a progress bar)

## Usage

The script can be run from the command line with the following arguments:

-   `url`: The URL to send GET requests to
-   `num_requests`: The number of requests to send

Example usage:
```
python ddos.py url num_requests

```
```
python ddos.py https://example.com 1000

```

## Code

The code consists of two functions:

-   `create_request_tasks`: A generator function that yields tasks, with each task representing a GET request to the given URL using the provided session.
-   `send_requests`: Sends multiple GET requests to the given URL concurrently using `aiohttp` and `asyncio` libraries.

In the `send_requests` function, we first create a `ClientSession` object from `aiohttp`. We then create a list of tasks using the `create_request_tasks` generator function, and use the `asyncio.as_completed` function to wait for all tasks to complete and display a progress bar using the `tqdm` library.

