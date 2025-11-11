from telethon import TelegramClient, events
import asyncio
import time
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Your API credentials from environment variables
api_id = int(os.getenv('API_ID', '20919872'))
api_hash = os.getenv('API_HASH', 'cf09a978564be23bb4325372820876b2')

# Create the client and connect
client = TelegramClient('session_name', api_id, api_hash)

async def main():
    await client.start()
    logger.info("Client Created and Connected")

    # Get the bot entity
    try:
        bot_entity = await client.get_entity('Arabic_TeleAdds_1bot')
        logger.info("Bot entity retrieved successfully")
    except Exception as e:
        logger.error(f"Error getting bot entity: {e}")
        return

    # Function to send the /start command and click the menu button
    async def collect_reward():
        try:
            # Send the command for the daily reward WITH clock emoji ⏰
            command = "المكافأة اليومية ⏰"  # Daily reward in Arabic with clock emoji
            await client.send_message(bot_entity, command)
            logger.info(f"Reward collected at {time.strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Wait a bit to see if there's any response from the bot
            await asyncio.sleep(5)
            
        except Exception as e:
            logger.error(f"Error collecting reward: {e}")

    # Run immediately when the script starts
    await collect_reward()
    logger.info("Initial reward collected, starting 2-hour interval loop...")

    # Then run every 2 hours (7200 seconds)
    while True:
        await asyncio.sleep(7200)  # 2 hours
        await collect_reward()

if __name__ == "__main__":
    try:
        with client:
            client.loop.run_until_complete(main())
    except Exception as e:
        logger.error(f"Fatal error: {e}")