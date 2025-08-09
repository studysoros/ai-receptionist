import asyncio
import base64
import json
import websockets
import os
from dotenv import load_dotenv

load_dotenv()


def sts_connect():
    api_key = os.getenv("DEEPGRAM_API_KEY")
    if not api_key:
        raise Exception("DEEPGRAM_API_KEY not found.")

    sts_ws = websockets.connect(
        "wss://agent.deepgram.com/v1/agent/converse", subprotocols=["token", api_key]
    )
    return sts_ws


def load_config():
    with open("config.json", "r") as f:
        json.load(f)


async def handle_barge_in(decoded, twilio_ws, streamsid):
    pass


async def handle_text_message(decoded, twilio_ws, sts_ws, streamsid):
    pass


async def sts_sender(sts_ws, audio_queue):
    pass


async def sts_receiver(sts_ws, twilio_ws, streamsid_queue):
    pass


async def twilio_receiver(twilio_ws, sts_ws, streamsid_queue):
    pass


async def twilio_handler(twilio_ws):
    audio_queue = asyncio.Queue()
    streamsid_queue = asyncio.Queue()

    async with sts_connect() as sts_ws:
        config_message = load_config()
        await sts_ws.send(json.dumps(config_message))

        await asyncio.wait(
            [
                asyncio.ensure_future(sts_sender(sts_ws, audio_queue)),
                asyncio.ensure_future(sts_receiver(sts_ws, twilio_ws, streamsid_queue)),
                asyncio.ensure_future(
                    twilio_receiver(twilio_ws, audio_queue, streamsid_queue)
                ),
            ]
        )

        await twilio_ws.close()


async def main():
    await websockets.serve(twilio_handler, "localhost", 5000)
    print("started server.")
    await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
