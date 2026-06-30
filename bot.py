#!/usr/bin/env python3
"""
DeltaWorld Donate Bot
Python бот для автоматической выдачи донатов
Запускается на Railway/Vercel
"""

import os
import time
import logging
from mcrcon import MCRcon
import mysql.connector
from mysql.connector import Error

# Настройки из переменных окружения
MYSQL_CONFIG = {
    'host': os.getenv('DB_HOST', 'reseau.proxy.rlwy.net'),
    'port': int(os.getenv('DB_PORT', 44404)),
    'database': os.getenv('DB_NAME', 'railway'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', '')
}

RCON_CONFIG = {
    'host': os.getenv('RCON_HOST', 'd20.aurorix.net'),
    'port': int(os.getenv('RCON_PORT', 25575)),
    'password': os.getenv('RCON_PASSWORD', '')
}

CHECK_INTERVAL = int(os.getenv('CHECK_INTERVAL', 10))
MAX_ATTEMPTS = int(os.getenv('MAX_ATTEMPTS', 3))

# Логирование
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)


def connect_database():
    """Подключение к MySQL"""
    try:
        connection = mysql.connector.connect(**MYSQL_CONFIG)
        if connection.is_connected():
            logger.info("✅ Connected to MySQL")
            return connection
    except Error as e:
        logger.error(f"❌ MySQL connection error: {e}")
        return None


def execute_rcon_command(command):
    """Выполнить команду через RCON"""
    try:
        with MCRcon(RCON_CONFIG['host'], RCON_CONFIG['password'], port=RCON_CONFIG['port'], timeout=10) as mcr:
            response = mcr.command(command)
            logger.info(f"✅ RCON executed: {command[:50]}...")
            return True, response
    except Exception as e:
        logger.error(f"❌ RCON error: {e}")
        return False, str(e)


def process_donate_queue():
    """Обработать очередь донатов"""
    connection = connect_database()
    if not connection:
        logger.warning("⚠️ Cannot connect to database, retry in {CHECK_INTERVAL}s")
        return
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        # Получаем pending заказы
        query = """
            SELECT id, nickname, commands, attempts 
            FROM donate_queue 
            WHERE status = 'pending' 
            ORDER BY created_at ASC 
            LIMIT 5
        """
        cursor.execute(query)
        orders = cursor.fetchall()
        
        if not orders:
            logger.debug("📭 Queue is empty")
            return
        
        logger.info(f"📦 Found {len(orders)} orders in queue")
        
        for order in orders:
            order_id = order['id']
            nickname = order['nickname']
            commands_str = order['commands']
            attempts = order['attempts']
            
            # Проверка лимита попыток
            if attempts >= MAX_ATTEMPTS:
                logger.warning(f"⚠️ Order #{order_id} exceeded max attempts ({MAX_ATTEMPTS})")
                cursor.execute(
                    "UPDATE donate_queue SET status = 'failed', error_message = 'Max attempts exceeded' WHERE id = %s",
                    (order_id,)
                )
                connection.commit()
                continue
            
            # Меняем статус на processing
            cursor.execute(
                "UPDATE donate_queue SET status = 'processing', attempts = attempts + 1 WHERE id = %s",
                (order_id,)
            )
            connection.commit()
            
            logger.info(f"🎮 Processing order #{order_id} for {nickname}")
            
            # Выполняем команды
            commands = [cmd.strip() for cmd in commands_str.split('|') if cmd.strip()]
            all_success = True
            error_msg = None
            
            for cmd in commands:
                # Заменяем {player} на никнейм
                cmd = cmd.replace('{player}', nickname)
                
                success, response = execute_rcon_command(cmd)
                
                if not success:
                    all_success = False
                    error_msg = response
                    logger.error(f"❌ Command failed for #{order_id}: {cmd}")
                    break
                
                time.sleep(0.2)
            
            # Обновляем статус
            if all_success:
                cursor.execute(
                    "UPDATE donate_queue SET status = 'completed', executed_at = NOW() WHERE id = %s",
                    (order_id,)
                )
                logger.info(f"✅ Order #{order_id} completed successfully!")
                
                # Уведомление в игре
                try:
                    notify_cmd = f'tellraw {nickname} {{"text":"[Donate] Ваш донат выдан! Спасибо!","color":"green"}}'
                    execute_rcon_command(notify_cmd)
                except:
                    pass
                
            else:
                # Возвращаем в pending
                cursor.execute(
                    "UPDATE donate_queue SET status = 'pending', error_message = %s WHERE id = %s",
                    (error_msg, order_id)
                )
                logger.warning(f"⚠️ Order #{order_id} returned to queue for retry")
            
            connection.commit()
    
    except Error as e:
        logger.error(f"❌ Queue processing error: {e}")
    
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()


def main():
    """Главный цикл"""
    logger.info("=" * 60)
    logger.info("🚀 DeltaWorld Donate Bot started!")
    logger.info(f"📊 Check interval: {CHECK_INTERVAL}s")
    logger.info(f"🔌 RCON: {RCON_CONFIG['host']}:{RCON_CONFIG['port']}")
    logger.info(f"🗄️ MySQL: {MYSQL_CONFIG['host']}:{MYSQL_CONFIG['port']}")
    logger.info("=" * 60)
    
    # Проверка RCON
    logger.info("🔍 Testing RCON connection...")
    success, response = execute_rcon_command("list")
    if success:
        logger.info(f"✅ RCON OK! Response: {response[:100]}")
    else:
        logger.error("❌ RCON failed! Check RCON settings")
        logger.error("   Make sure enable-rcon=true in server.properties")
    
    # Проверка БД
    logger.info("🔍 Testing database connection...")
    conn = connect_database()
    if conn:
        conn.close()
        logger.info("✅ Database OK!")
    else:
        logger.error("❌ Database connection failed!")
    
    logger.info("✅ All systems ready! Starting processing...")
    logger.info("")
    
    # Главный цикл
    while True:
        try:
            process_donate_queue()
            time.sleep(CHECK_INTERVAL)
        except KeyboardInterrupt:
            logger.info("\n👋 Stopping bot...")
            break
        except Exception as e:
            logger.error(f"❌ Critical error: {e}")
            time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()
