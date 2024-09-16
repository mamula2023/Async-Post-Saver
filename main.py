import asyncio
import aiohttp


async def fetch_data(url, session, lock, filename):
    async with session.get(url) as response:
        result_json = await response.json()

        async with lock:
            with open(filename, mode='r') as f:
                content = f.read()

                if content == '':
                    result = '[' + str(result_json).replace('\'', '"') + ']'
                else:
                    result = content[0:-1] + ',' + str(result_json).replace('\'', '"') + ']'

            with open(filename, mode='w') as f:
                f.write(result)
            print('fetched: ' + url)


async def main(url, filename, file_lock):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(1, 78):
            tasks.append(asyncio.create_task(fetch_data(url + str(i), session, file_lock, filename)))

        await asyncio.gather(*tasks)


if __name__ == '__main__':
    base_url = "https://jsonplaceholder.typicode.com/posts/"
    filename = 'result.json'
    file_lock = asyncio.Lock()

    with open(filename, 'w') as f:
        f.close()

    asyncio.run(main(base_url, filename, file_lock))
