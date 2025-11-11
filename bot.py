import os
import asyncio
import time
import logging
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.errors import SessionPasswordNeededError, PhoneNumberInvalidError

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Configuration
api_id = int(os.getenv('API_ID', '20919872'))
api_hash = os.getenv('API_HASH', 'cf09a978564be23bb4325372820876b2')
session_string = os.getenv('SESSION_STRING')

# Validate required environment variables
if not session_string:
    logger.error("❌ SESSION_STRING environment variable is required!")
    exit(1)

async def collect_reward(client):
    """Collect reward from the bot"""
    try:
        # Try to get the bot entity
        try:
            bot_entity = await client.get_entity('Arabic_TeleAdds_1bot')
            logger.info("✅ Bot entity found")
        except Exception as e:
            logger.warning(f"⚠️ Could not get bot entity, using username: {e}")
            bot_entity = 'Arabic_TeleAdds_1bot'
        
        # Send the reward command
        command = "المكافأة اليومية ⏰"
        await client.send_message(bot_entity, command)
        logger.info(f"✅ Reward collected at {time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Wait for potential response
        await asyncio.sleep(3)
        return True
        
    except Exception as e:
        logger.error(f"❌ Error collecting reward: {e}")
        return False

async def main():
    client = None
    try:
        logger.info("🚀 Starting Telegram Reward Bot...")
        
        # Create client with session string
        client = TelegramClient(
            StringSession(session_string), 
            api_id, 
            api_hash
        )
        
        # Connect to Telegram
        await client.connect()
        logger.info("📡 Connecting to Telegram...")
        
        # Check if we're authorized
        if not await client.is_user_authorized():
            logger.error("❌ Client is not authorized. Please generate a new session string.")
            return
        
        logger.info("✅ Successfully connected and authorized!")
        
        # Get current user info
        me = await client.get_me()
        logger.info(f"👤 Logged in as: {me.first_name} (@{me.username})")
        
        # Initial reward collection
        logger.info("🔄 Performing initial reward collection...")
        await collect_reward(client)
        
        # Main loop - run every 2 hours
        logger.info("⏰ Starting 2-hour interval loop...")
        collection_count = 1
        
        while True:
            try:
                # Wait for 2 hours (7200 seconds)
                logger.info(f"⏳ Waiting 2 hours until next collection... (Collection #{collection_count})")
                await asyncio.sleep(7200)
                
                # Collect reward
                collection_count += 1
                success = await collect_reward(client)
                
                if success:
                    logger.info(f"✅ Successfully completed collection #{collection_count}")
                else:
                    logger.warning(f"⚠️ Collection #{collection_count} had issues")
                    
            except Exception as e:
                logger.error(f"❌ Error in main loop: {e}")
                # Wait before retrying
                await asyncio.sleep(300)  # 5 minutes
                
    except SessionPasswordNeededError:
        logger.error("❌ Two-factor authentication is enabled. Please disable it or handle 2FA.")
    except PhoneNumberInvalidError:
        logger.error("❌ Phone number is invalid.")
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")
    finally:
        if client:
            await client.disconnect()
            logger.info("📴 Client disconnected")

if __name__ == "__main__":
    # Run the bot
    asyncio.run(main())
