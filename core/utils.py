import requests
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def send_telegram_message(message):
    """
    Telegram bot orqali xabar yuborish
    """
    bot_token = settings.TELEGRAM_BOT_TOKEN
    chat_id = settings.TELEGRAM_CHAT_ID
    
    if not bot_token or not chat_id:
        logger.warning("Telegram bot token yoki chat ID sozlanmagan")
        return False
    
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    
    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'HTML'
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        logger.info(f"Telegramga xabar yuborildi: {response.status_code}")
        return True
    except requests.exceptions.RequestException as e:
        logger.error(f"Telegramga xabar yuborishda xatolik: {e}")
        return False