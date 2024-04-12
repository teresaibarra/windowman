# Authorization Code: _vHmUfh0uHVKftErMQV3kt5K5rrX8HVS2SUTdrcSRmWLj
# Code Verifier: JuaSKLOkYOhSe3VpkUR9ACoYcd1eBi7rq73sF2BsNag5XCb6eHkQ

import asyncio

from aiohttp import ClientSession
from simplipy import API
import json

session = None
my_simplisafe = None
my_refresh_token = None
my_systems = None


# To get the following variables, run the auth script in the simplisafe-python module
# AUTH_CODE = ""
# CODE_VERIFIER = ""


async def async_get_refresh_token() -> str:
    """Get a refresh token from storage."""
    file_path = "refresh_token.json"

    with open(file_path, 'r') as file:
        # Read the contents of the file as a string
        file_contents = file.read()

        global my_refresh_token
        my_refresh_token = file_contents
        print("refresh_token: ", file_contents)
        return file_contents

async def async_set_refresh_token(refresh_token) -> str:
    """Store a refresh token."""
    file_path = "refresh_token.json"

    with open(file_path, 'w') as file:
        # Write the string content to the file
        file.write(refresh_token)

async def main() -> None:
    """Create the aiohttp session and run."""
    async with ClientSession() as session:
        simplisafe = await API.async_from_auth(
            AUTH_CODE,
            CODE_VERIFIER,
            session=session,
        )

        global my_simplisafe 
        my_simplisafe = simplisafe

        global my_systems
        systems = await simplisafe.async_get_systems()
        my_systems = systems
        print(systems)

        await simplisafe.websocket.async_connect()

        print("I have been connected! now listening...")
        


        async def async_connect_handler(event):
            await asyncio.sleep(1)
            print("""⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠶⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡼⣋⡂⡘⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡾⠑⠈⢰⡈⠘⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡞⢡⠀⢻⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⡀⠂⠀⣼⠃⡎⠀⣴⢗⢂⠘⣧⠀⠀⠀⠀⠀⠀⠀⠀⣀⡾⠋⢀⡜⠉⠈⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠠⠈⠀⠀⢠⡇⣸⠇⠀⣼⠂⠀⡄⢸⡇⠀⠀⠀⠀⠀⠀⣴⠋⢀⠈⢞⡄⠀⠀⢻⡄⠀⠀⠀⠀⠀⣀⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠆⠸⡇⠀⢉⠀⠀⠉⠁⠀⠉⠉⠉⠙⠓⠚⠧⢄⠁⠐⢮⠀⠀⠀⢸⡇⠀⢀⡤⠚⠉⠀⠀⢀⢌⠙⠢⡀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡄⠸⠣⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠃⠀⠀⠃⢸⡃⠀⡜⠀⠀⠸⣿⣧⣿⣼⠠⠀⢻⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢘⡧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠢⡀⠔⠀⣾⠁⠀⢣⠀⠨⠀⠛⢷⢯⠃⠈⠀⢸⠇⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⠀⠀⠀⠀⠀⠀⠀⠀⣆⢀⠀⠀⠀⡠⠒⡄⠀⠀⠀⠀⠀⠈⠀⣴⠃⠀⠀⠀⠑⢤⠀⠀⠀⠀⢀⣀⠶⠋⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⠃⠀⠀⠀⠀⠀⣠⣤⡄⠑⠈⠀⠀⠀⠁⠄⠁⠀⠀⠀⠀⠀⠀⠀⡵⠃⠀⠀⠀⢀⡜⡠⠊⠉⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢰⡟⠐⠉⠁⠂⠀⢸⣿⣷⠇⠀⠀⠀⠀⠀⠀⠀⡠⣤⡀⠀⠀⠀⠀⠀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⠁⠌⠙⠉⠀⠀⢿⣿⣷⣦⠀⠀⣿⣿⡇⠀⠀⡀⠀⢀⢸⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⡆⠀⠀⠀⠈⠉⠀⢐⡀⠀⠀⠉⠉⠀⢀⡐⠘⠛⠁⠀⠀⠀⠀⠀⢸⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠸⡀⠁⠀⠀⠀⠈⠈⢿⣆⡀⠀⠀⠀⠀⠉⠉⠉⠉⠷⠦⠤⠊⠀⠀⠓⠂⠀⠀⠀⠀⣠⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠓⠂⠀⠀⠀⠁⠀⠀⠘⢿⠒⠂⠀⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⠁⠰⡐⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢞⠁⠀⠀⠀⠀⠈⠉⠛⠒⠒⠒⠠⠀⠀⠠⠖⠚⠛⢻⠁⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠊⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣈⠏⢳⣄⠀⠀⠀⠀⠀⣠⠖⢦⠔⢚⠉⠉⠉⠙⠲⡄⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣨⠃⠀⠀⠀⠀⠄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠁⠀⠀⠙⢶⣀⠀⠀⢠⣏⡉⠈⠈⠀⠀⠀⠀⠐⠀⠙⠢⢄⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⡡⠀⠀⠀⠀⢀⡬⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠳⣄⡘⡀⠀⠀⠀⢀⣀⣀⠀⠀⠀⠀⠐⠠⠑⡄⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⠁⠀⠀⠀⡾⠋⠀⠀⠀⠀⠠⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⢧⡄⠀⠀⠈⠉⢆⠣⠤⣄⠀⠀⠑⡛⢥⡀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⡜⠀⠀⢸⠀⠀⠀⠀⠀⠀⢀⣸⠆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣆⠀⠀⠀⠀⠀⡁⠈⣱⠀⠀⠀⡀⢱⡁
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢧⡇⠀⠀⡸⠀⠀⠀⠀⠀⠀⠀⡇⢀⠀⣠⡴⠒⠒⠒⠒⠒⠠⠄⠀⠀⠀⠀⠀⠀⠀⠙⣧⠀⠀⠀⡠⢈⠙⣇⠀⠀⠀⡀⠅⡇
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⠀⠀⡟⠀⠀⠀⠀⠀⠀⡞⠁⢠⡟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⡆⠒⠂⢠⡞⠉⠁⠀⠀⠐⣥⡜⠁
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⡟⢄⢣⡇⠀⠀⠀⠀⠀⢰⡇⠀⣼⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣟⠛⠛⠉⠀⠀⠀⠀⠀⠄⡸⡁⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣇⠀⢨⡇⠀⠀⠀⠀⠀⣸⠁⠀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠀⠀⠀⠀⠀⣀⠰⠀⢸⣁⠃⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠆⢸⡇⠀⠀⠀⠀⢠⡏⠀⠀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣏⡀⠀⢀⠀⣁⣀⣶⠟⠉⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⢸⠀⠀⠀⠀⠀⣾⣳⣄⡄⠸⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡾⠁⠈⠙⠒⠛⠙⠋⠉⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡁⡜⠀⠀⠀⠀⣾⠃⠀⠀⠙⠼⣌⣳⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣤⠞⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢶⣇⠀⢀⣠⠾⠉⠒⠒⠒⠒⠒⢒⣿⣫⠙⠓⠓⠛⠋⠀⠀⠀⠀⠀⢀⣀⡼⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⠚⠋⠁⠀⠀⠀⠀⠀⠀⠀⠈⠓⠷⢤⣤⣤⣴⠤⠶⠶⠶⠒⠛⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀""")

            print("CUTE DOG ALERT! CUTE DOG ALERT! CUTE DOG ALERT! CUTE DOG ALERT!")
            print(f"I received a SimpliSafe™ event: {event}")

        remove_1 = simplisafe.websocket.add_event_callback(async_connect_handler)

        await simplisafe.websocket.async_listen()

async def get_new_object():
    global my_session

    refresh_token = await async_get_refresh_token()
    api = await API.async_from_refresh_token(
        refresh_token, session=my_session
    )
    global my_simplisafe 
    my_simplisafe = api


    async_set_refresh_token(api.refresh_token)
    return api
