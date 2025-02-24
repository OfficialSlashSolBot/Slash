import os
import math
import time 
import boto3
import base58
import random
import asyncio
import logging
import asyncio
import aiomysql
import warnings
import threading
import json
import aiofiles
import datetime
import pymysql.cursors
from dotenv import load_dotenv
from xxx_game import xxx_game
from zzz_game import zzz_game
from transfer import send_sol, send_sol_m, send_sol_e
from balance import get_balance
from solders.keypair import Keypair
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, CallbackContext, ContextTypes
from dbcalls import (
                        
                        get_user_id,
                        get_wallet_address_by_user_id,
                        get_game_private_key,
                        get_game_wallet,
                        generate_wallet_if_needed,
                        save_wallet_address_new,
                        save_wallet_address,
                        get_wallet_address,
                        get_private_key,
                        get_entries,
                        get_entries2,
                        get_total_users,
                    )

warnings.simplefilter("ignore")
load_dotenv('.env')
logging.basicConfig(level=logging.ERROR)

TOKEN = os.getenv('TOKEN')  
DB_NAME = os.getenv('DB_NAME')  
DB_HOST = os.getenv('DB_HOST')  
DB_USER = os.getenv('DB_USER')  
DB_PASSWORD = os.getenv('DB_PASSWORD')
GROUPID = int(os.getenv('TG_GROUP_ID')) 
CHANNELID = int(os.getenv('TG_CHANNEL_ID')) 
FEEWALLET = os.getenv('FEEWALLET')  
END = 0
AUTHORIZED_USER_ID = os.getenv('AUTHORIZED_USER_ID')
bot = Bot(token=TOKEN)

user_last_start_time = {}
START_COMMAND_COOLDOWN = 3  
MAX_START_COMMAND_COOLDOWN = 30  
user_last_start_time = {}  
user_spam_count = {}  
user_notified = {}  
video_filename1 = 'es.mp4'
video_filename2 = 'er.mp4'
video_filename3 = 'ms.mp4'
video_filename4 = 'mr.mp4'


async def setup_database():
    pool = await aiomysql.create_pool(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        autocommit=True
    )

    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
            await cursor.execute(f"USE {DB_NAME}")
            await cursor.execute(f"GRANT ALL PRIVILEGES ON {DB_NAME}.* TO '{DB_USER}'@'%'")
            await cursor.execute("FLUSH PRIVILEGES")
            await cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id BIGINT PRIMARY KEY,
                    wallet_address TEXT NOT NULL,
                    token_balance BIGINT,
                    encrypted_private_key TEXT NOT NULL,
                    referrer_id BIGINT,
                    second_level_referrer_id BIGINT,
                    earned DOUBLE DEFAULT 0,
                    FOREIGN KEY(referrer_id) REFERENCES users(user_id),
                    FOREIGN KEY(second_level_referrer_id) REFERENCES users(user_id)
                )
            ''')
            
            await cursor.execute('''
                    CREATE TABLE IF NOT EXISTS xyz_001 (
                        id BIGINT PRIMARY KEY AUTO_INCREMENT,
                        wallet_address TEXT NOT NULL,
                        encrypted_private_key TEXT NOT NULL,
                        round DOUBLE DEFAULT 0,
                        wallet_address1 TEXT DEFAULT NULL,
                        wallet_address2 TEXT DEFAULT NULL,
                        wallet_address3 TEXT DEFAULT NULL,
                        wallet_address4 TEXT DEFAULT NULL
                    )
                ''')
            await asyncio.shield(generate_wallet_if_needed(cursor, 'xyz_001'))

            await cursor.execute('''
                    CREATE TABLE IF NOT EXISTS xyz_010 (
                        id BIGINT PRIMARY KEY AUTO_INCREMENT,
                        wallet_address TEXT NOT NULL,
                        encrypted_private_key TEXT NOT NULL,
                        round DOUBLE DEFAULT 0,
                        wallet_address1 TEXT DEFAULT NULL,
                        wallet_address2 TEXT DEFAULT NULL,
                        wallet_address3 TEXT DEFAULT NULL,
                        wallet_address4 TEXT DEFAULT NULL
                    )
                ''')
            await asyncio.shield(generate_wallet_if_needed(cursor, 'xyz_010'))

            await cursor.execute('''
                    CREATE TABLE IF NOT EXISTS xyz_100 (
                        id BIGINT PRIMARY KEY AUTO_INCREMENT,
                        wallet_address TEXT NOT NULL,
                        encrypted_private_key TEXT NOT NULL,
                        round DOUBLE DEFAULT 0,
                        wallet_address1 TEXT DEFAULT NULL,
                        wallet_address2 TEXT DEFAULT NULL,
                        wallet_address3 TEXT DEFAULT NULL,
                        wallet_address4 TEXT DEFAULT NULL
                    )
                ''')
            await asyncio.shield(generate_wallet_if_needed(cursor, 'xyz_100'))

            await cursor.execute('''
                    CREATE TABLE IF NOT EXISTS zyx_001 (
                        id BIGINT PRIMARY KEY AUTO_INCREMENT,
                        wallet_address TEXT NOT NULL,
                        encrypted_private_key TEXT NOT NULL,
                        round DOUBLE DEFAULT 0,
                        wallet_address1 TEXT DEFAULT NULL,
                        wallet_address2 TEXT DEFAULT NULL,
                        wallet_address3 TEXT DEFAULT NULL,
                        wallet_address4 TEXT DEFAULT NULL,
                        wallet_address5 TEXT DEFAULT NULL,
                        wallet_address6 TEXT DEFAULT NULL,
                        wallet_address7 TEXT DEFAULT NULL,
                        wallet_address8 TEXT DEFAULT NULL,
                        wallet_address9 TEXT DEFAULT NULL,
                        wallet_address10 TEXT DEFAULT NULL,
                        wallet_address11 TEXT DEFAULT NULL,
                        wallet_address12 TEXT DEFAULT NULL,
                        wallet_address13 TEXT DEFAULT NULL,
                        wallet_address14 TEXT DEFAULT NULL,
                        wallet_address15 TEXT DEFAULT NULL,
                        wallet_address16 TEXT DEFAULT NULL,
                        wallet_address17 TEXT DEFAULT NULL,
                        wallet_address18 TEXT DEFAULT NULL,
                        wallet_address19 TEXT DEFAULT NULL,
                        wallet_address20 TEXT DEFAULT NULL,
                        wallet_address21 TEXT DEFAULT NULL,
                        wallet_address22 TEXT DEFAULT NULL,
                        wallet_address23 TEXT DEFAULT NULL,
                        wallet_address24 TEXT DEFAULT NULL,
                        wallet_address25 TEXT DEFAULT NULL,
                        wallet_address26 TEXT DEFAULT NULL,
                        wallet_address27 TEXT DEFAULT NULL,
                        wallet_address28 TEXT DEFAULT NULL,
                        wallet_address29 TEXT DEFAULT NULL,
                        wallet_address30 TEXT DEFAULT NULL,
                        wallet_address31 TEXT DEFAULT NULL,
                        wallet_address32 TEXT DEFAULT NULL
                    )
                ''')
            await asyncio.shield(generate_wallet_if_needed(cursor, 'zyx_001'))

            await cursor.execute('''
                    CREATE TABLE IF NOT EXISTS zyx_010 (
                        id BIGINT PRIMARY KEY AUTO_INCREMENT,
                        wallet_address TEXT NOT NULL,
                        encrypted_private_key TEXT NOT NULL,
                        round DOUBLE DEFAULT 0,
                        wallet_address1 TEXT DEFAULT NULL,
                        wallet_address2 TEXT DEFAULT NULL,
                        wallet_address3 TEXT DEFAULT NULL,
                        wallet_address4 TEXT DEFAULT NULL,
                        wallet_address5 TEXT DEFAULT NULL,
                        wallet_address6 TEXT DEFAULT NULL,
                        wallet_address7 TEXT DEFAULT NULL,
                        wallet_address8 TEXT DEFAULT NULL,
                        wallet_address9 TEXT DEFAULT NULL,
                        wallet_address10 TEXT DEFAULT NULL,
                        wallet_address11 TEXT DEFAULT NULL,
                        wallet_address12 TEXT DEFAULT NULL,
                        wallet_address13 TEXT DEFAULT NULL,
                        wallet_address14 TEXT DEFAULT NULL,
                        wallet_address15 TEXT DEFAULT NULL,
                        wallet_address16 TEXT DEFAULT NULL,
                        wallet_address17 TEXT DEFAULT NULL,
                        wallet_address18 TEXT DEFAULT NULL,
                        wallet_address19 TEXT DEFAULT NULL,
                        wallet_address20 TEXT DEFAULT NULL,
                        wallet_address21 TEXT DEFAULT NULL,
                        wallet_address22 TEXT DEFAULT NULL,
                        wallet_address23 TEXT DEFAULT NULL,
                        wallet_address24 TEXT DEFAULT NULL,
                        wallet_address25 TEXT DEFAULT NULL,
                        wallet_address26 TEXT DEFAULT NULL,
                        wallet_address27 TEXT DEFAULT NULL,
                        wallet_address28 TEXT DEFAULT NULL,
                        wallet_address29 TEXT DEFAULT NULL,
                        wallet_address30 TEXT DEFAULT NULL,
                        wallet_address31 TEXT DEFAULT NULL,
                        wallet_address32 TEXT DEFAULT NULL
                    )
                ''')
            await asyncio.shield(generate_wallet_if_needed(cursor, 'zyx_010'))

            await cursor.execute('''
                    CREATE TABLE IF NOT EXISTS zyx_100 (
                        id BIGINT PRIMARY KEY AUTO_INCREMENT,
                        wallet_address TEXT NOT NULL,
                        encrypted_private_key TEXT NOT NULL,
                        round DOUBLE DEFAULT 0,
                        wallet_address1 TEXT DEFAULT NULL,
                        wallet_address2 TEXT DEFAULT NULL,
                        wallet_address3 TEXT DEFAULT NULL,
                        wallet_address4 TEXT DEFAULT NULL,
                        wallet_address5 TEXT DEFAULT NULL,
                        wallet_address6 TEXT DEFAULT NULL,
                        wallet_address7 TEXT DEFAULT NULL,
                        wallet_address8 TEXT DEFAULT NULL,
                        wallet_address9 TEXT DEFAULT NULL,
                        wallet_address10 TEXT DEFAULT NULL,
                        wallet_address11 TEXT DEFAULT NULL,
                        wallet_address12 TEXT DEFAULT NULL,
                        wallet_address13 TEXT DEFAULT NULL,
                        wallet_address14 TEXT DEFAULT NULL,
                        wallet_address15 TEXT DEFAULT NULL,
                        wallet_address16 TEXT DEFAULT NULL,
                        wallet_address17 TEXT DEFAULT NULL,
                        wallet_address18 TEXT DEFAULT NULL,
                        wallet_address19 TEXT DEFAULT NULL,
                        wallet_address20 TEXT DEFAULT NULL,
                        wallet_address21 TEXT DEFAULT NULL,
                        wallet_address22 TEXT DEFAULT NULL,
                        wallet_address23 TEXT DEFAULT NULL,
                        wallet_address24 TEXT DEFAULT NULL,
                        wallet_address25 TEXT DEFAULT NULL,
                        wallet_address26 TEXT DEFAULT NULL,
                        wallet_address27 TEXT DEFAULT NULL,
                        wallet_address28 TEXT DEFAULT NULL,
                        wallet_address29 TEXT DEFAULT NULL,
                        wallet_address30 TEXT DEFAULT NULL,
                        wallet_address31 TEXT DEFAULT NULL,
                        wallet_address32 TEXT DEFAULT NULL
                    )
                ''')
            await asyncio.shield(generate_wallet_if_needed(cursor, 'zyx_100'))

    pool.close()
    await pool.wait_closed()

    tasks = [
        monitor_and_select_winner("xyz_001"),
        monitor_and_select_winner("xyz_010"),
        monitor_and_select_winner("xyz_100"),
        monitor_and_select_winner2("zyx_001"),
        monitor_and_select_winner2("zyx_010"),
        monitor_and_select_winner2("zyx_100")
    ]
    
    await asyncio.gather(*tasks)

async def private_chat_only(update: Update, context: CallbackContext):
    if update.effective_chat.type != 'private':
    
        return False
    return True

async def create_start_task(update: Update, context: CallbackContext) -> None:
    if not await private_chat_only(update, context):
        return

    user_id = update.effective_user.id
    current_time = time.time()

    if user_id in user_last_start_time:
        last_call_time = user_last_start_time[user_id]
        time_diff = current_time - last_call_time
        if time_diff < START_COMMAND_COOLDOWN:
            if user_id in user_spam_count:
                user_spam_count[user_id] += 1
            else:
                user_spam_count[user_id] = 1
            cooldown_time = START_COMMAND_COOLDOWN + (user_spam_count[user_id] * 3)
            cooldown_time = min(cooldown_time, MAX_START_COMMAND_COOLDOWN)
            if user_id not in user_notified:
                user_notified[user_id] = True
                await update.message.reply_text(
                    f"Please wait {cooldown_time} seconds before trying again."
                )
            return
        else:
            user_spam_count[user_id] = 0
            user_notified[user_id] = False
    user_last_start_time[user_id] = current_time

    asyncio.create_task(start(update, context, user_id))

async def start(update: Update, context: CallbackContext, user_id: int = None) -> None:

    if update and update.message and update.message.chat.type != "private":
        return
    if user_id and update and update.message and update.message.from_user.id != user_id:
        return
    await asyncio.sleep(2.5)

    try:
        if update.message:
            user_id = update.message.from_user.id
        wallet_address = await asyncio.shield(get_wallet_address(user_id))
        users = await get_total_users()
        if wallet_address:
            balance = await asyncio.shield(get_balance(wallet_address))
            balance_rounded = math.floor(balance * 1000) / 1000
            balance_formatted = f"{balance_rounded:.3f}"
            welcome_message = (f"⚔ *Welcome to [BOT_NAME]!* ⚔\n\n"
                   f"An exciting *elimination game* where only the strongest survive!\n\n"
                   f"🎮 *Game Modes:*\n"
                   f"• *Express* – Fast-paced, 4 players, winner takes all!\n"
                   f"• *Mega* – 32 players, top 8 get paid!\n\n"
                   f"🔹 *How It Works:*\n"
                   f"• Each round, *50% of players are randomly [BOT_NAME]ed* until there's a winner.\n"
                   f"• *Deposit SOL* to your in-game balance.\n"
                   f"• *Choose your game mode* and join the battle.\n"
                   f"• *Wait for the round to start* and survive the eliminations!\n\n"
                   f"💰 *Your Account:*\n"
                   f"• *Balance:* {balance_formatted} SOL\n"
                   f"• *Wallet:* `{wallet_address}`\n"
                   f"• *Total Players:* {users}\n\n"
                   f"⚡ *Let the [BOT_NAME]ing begin!*")

        else:
            private_key = Keypair()
            new_wallet = private_key.pubkey()  
            private_key_str = str(private_key)
            new_wallet_str = str(new_wallet)
            earned = 0
            token_balance = 0
            referrer_id = context.args[0] if context.args else None
            await asyncio.shield(save_wallet_address_new(user_id, new_wallet_str, token_balance, private_key_str, earned, referrer_id))
            balance = 0.0
            balance_rounded = math.floor(balance * 1000) / 1000
            balance_formatted = f"{balance_rounded:.3f}"
            welcome_message = (f"⚔ *Welcome to [BOT_NAME]!* ⚔\n\n"
                   f"An exciting *elimination game* where only the strongest survive!\n\n"
                   f"🎮 *Game Modes:*\n"
                   f"• *Express* – Fast-paced, 4 players, winner takes all!\n"
                   f"• *Mega* – 32 players, top 8 get paid!\n\n"
                   f"🔹 *How It Works:*\n"
                   f"• Each round, *50% of players are randomly [BOT_NAME]ed* until there's a winner.\n"
                   f"• *Deposit SOL* to your in-game balance.\n"
                   f"• *Choose your game mode* and join the battle.\n"
                   f"• *Wait for the round to start* and survive the eliminations!\n\n"
                   f"💰 *Your Account:*\n"
                   f"• *Balance:* {balance_formatted} SOL\n"
                   f"• *Wallet:* `{new_wallet_str}`\n"
                   f"Your Wallet was auto generated\n"
                   f"• *Total Players:* {users}\n\n"
                   f"⚡ *Let the [BOT_NAME]ing begin!*")
        entries_1 = await get_entries("xyz_001")
        entries_2 = await get_entries("xyz_010")
        entries_3 = await get_entries("xyz_100")
        entries_4 = await get_entries2("zyx_001")
        entries_5 = await get_entries2("zyx_010")
        entries_6 = await get_entries2("zyx_100")
        keyboard = [
                [InlineKeyboardButton(f"🥷 MODE A 0.01 Sol ({entries_1}/4)", callback_data='xxx_4_001'),InlineKeyboardButton(f"🥷 MODE A 0.10 Sol ({entries_2}/4)", callback_data='xxx_4_010')],
                [InlineKeyboardButton(f"🥷 MODE A 1.0 Sol ({entries_3}/4)", callback_data='xxx_4_100')],
                [InlineKeyboardButton(f"🏆 MODE B 0.01 Sol ({entries_4}/32)", callback_data='zzz_32_001'),InlineKeyboardButton(f"🏆 MODE B 0.1 Sol ({entries_5}/32)", callback_data='zzz_32_010')],
                [InlineKeyboardButton(f"🏆 MODE B 1.0 Sol ({entries_6}/32)", callback_data='zzz_32_100')],
                [InlineKeyboardButton("How to Play?", callback_data='info'),InlineKeyboardButton("Wallet", callback_data='wallet')],
                [InlineKeyboardButton("Transfer", callback_data='transfer_sol')],
            ]
            
        reply_markup = InlineKeyboardMarkup(keyboard)
        if update.message:
            await update.message.reply_text(welcome_message, reply_markup=reply_markup, parse_mode = "markdown")
        else:
            await context.bot.send_message(chat_id=user_id, text=welcome_message, reply_markup=reply_markup,parse_mode = "markdown")
    except Exception as e:
        logging.error(f"Error processing start command for user {user_id}: {e}")
    
#CALLBACKS START

async def button(update: Update, context: Application) -> None:
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    async def handle_query():

        if query.data == 'info':
                        how_it_works_message = (
                            "*⚔️ [BOT_NAME] - Telegram Elimination Game*\n\n"
                            "[BOT_NAME]Bot is an action-packed *elimination game* on Telegram where players compete in knockout-style battles to win SOL rewards! Choose between *Express* and *Mega* game modes and climb your way to the top!\n\n"
                            "*🎮 How to Play:*\n"
                            "Join the *[BOT_NAME]* game via Telegram and battle it out in two exciting game modes:\n\n"
                            "1️⃣ *Express* – 4 players, winner takes all!\n"
                            "2️⃣ *Mega* – 32 players, top 8 get paid!\n\n"
                            "🔹 Games start automatically when all slots are filled.\n"
                            "🔹 Eliminate opponents and survive until the final round to win SOL prizes!\n\n"
                            "*🔥 Express Mode:*\n"
                            "• *Fast & intense* – Only *2 rounds* of elimination\n"
                            "• *Winner takes all!* Earn *3.6x* your entry fee\n\n"
                            "*💪 Mega Mode:*\n"
                            "• *Survive 5 rounds* to secure your rewards\n"
                            "• *Prize Structure:*\n"
                            "  - 🥇 *1st place:* *14.3x* entry fee\n"
                            "  - 🥈 *2nd place:* *4.3x* entry fee\n"
                            "  - 🥉 *3rd-4th place:* *2x* entry fee\n"
                            "  - 🎖 *5th-8th place:* *1.55x* entry fee\n\n"
                            "*🚀 How to Join:*\n"
                            "1. Open Telegram and search for *[BOT_NAME]*\n"
                            "2. Join a game by selecting *Express* or *Mega* mode\n"
                            "3. Place your bet, compete, and win rewards!\n\n"
                            "*⚡ Start Playing Now!*\n"
                            "Think you have what it takes to *eliminate the competition* and *claim the prize*? Join the battle now and let the games begin!"
                        )

                        await query.edit_message_text(how_it_works_message, parse_mode='Markdown')

                        await start(update, context, user_id=user_id)

        elif query.data == 'xxx_4_001':
                keyboard = [
                    [InlineKeyboardButton("No", callback_data='no_deposit'),InlineKeyboardButton("Yes", callback_data='yes_xxx_4_001')],
                    [InlineKeyboardButton("Cancel", callback_data='cancel_xyz_001')]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                await query.edit_message_text(
                    "You're about to enter a game of EXPRESS [BOT_NAME] for 0.01 Sol!!\n\nWould you like to proceed?\n\nOr click Cancel to remove your entries from the game (this will incur a 10% penalty fee).",
                    reply_markup=reply_markup
                )

        elif query.data == 'xxx_4_010':
                keyboard = [
                    [InlineKeyboardButton("No", callback_data='no_deposit'),InlineKeyboardButton("Yes", callback_data='yes_xxx_4_010')],
                    [InlineKeyboardButton("Cancel", callback_data='cancel_xyz_010')]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                await query.edit_message_text(
                    "You're about to enter a game of EXPRESS [BOT_NAME] for 0.10 Sol!!\n\nWould you like to proceed?\n\nOr click Cancel to remove your entries from the game (this will incur a 10% penalty fee).",
                    reply_markup=reply_markup
                )

        elif query.data == 'xxx_4_100':
                keyboard = [
                    [InlineKeyboardButton("No", callback_data='no_deposit'), InlineKeyboardButton("Yes", callback_data='yes_xxx_4_100')],
                    [InlineKeyboardButton("Cancel", callback_data='cancel_xyz_100')]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                await query.edit_message_text(
                    "You're about to enter a game of EXPRESS [BOT_NAME] for 1.0 Sol!!\n\nWould you like to proceed?\n\nOr click Cancel to remove your entries from the game (this will incur a 10% penalty fee).",
                    reply_markup=reply_markup
                )

        elif query.data.startswith('cancel_'):
                await query.edit_message_text("Checking for entries...")
                tablename = query.data.split('_')[1:]  
                table_name = "_".join(tablename)
                user_wallet = await get_wallet_address_by_user_id(user_id)
                entry_exists = await check_entry(table_name, user_wallet)
                await asyncio.sleep(2)
                if entry_exists['success']:
                    await query.edit_message_text("Processing refund...")
                    entries = entry_exists['entries']
                    try:
                        number = int(table_name[-3:])  
                    except ValueError:
                        number = 0  
                    amount = (number / 100) * entries * 0.9
                    from_wallet = await get_game_wallet(table_name)
                    pk = await get_game_private_key(table_name)
                    refund_result = await send_sol(user_wallet, from_wallet, pk, amount)
                    if refund_result['success']:
                        signature = refund_result['result']
                        remove_result = await remove_entry(table_name, user_wallet)
                        await bot.send_message(
                            chat_id=user_id,
                            text=(f"Successfully refunded your entries\n\n"
                                f"[TX](https://solscan.io/tx/{signature})"),
                            parse_mode='Markdown',
                            disable_web_page_preview=True
                        )
                        await start(update, context, user_id=user_id)
                    else:
                        await bot.send_message(
                            chat_id=user_id,
                            text="There was an issue processing your refund. Please try again later.",
                            parse_mode='Markdown'
                        )
                        await start(update, context, user_id=user_id)
                else:
                    await bot.send_message(
                        chat_id=user_id,
                        text="You do not have any entries to refund or there was an error, please try again.",
                        parse_mode='Markdown'
                    )
                    
                    await start(update, context, user_id=user_id)
 
        elif query.data.startswith('yes_xxx_4_'):
            entry_fee = query.data.split('_')[-1]
            table_name = f"xyz_{entry_fee}"
            table_wallet = await get_game_wallet(table_name)
            pk = await get_private_key(user_id)
            user_wallet = await get_wallet_address_by_user_id(user_id)
            amount = int(entry_fee)/100
            user_balance = await get_balance(user_wallet)
            amount_needed = int(amount+0.0005)
            if user_balance >= amount_needed:
                pool = await aiomysql.create_pool(
                    host=DB_HOST,
                    user=DB_USER,
                    password=DB_PASSWORD,
                    db=DB_NAME,
                    autocommit=True
                )

                async with pool.acquire() as conn:
                    async with conn.cursor() as cursor:
                        await cursor.execute(f'''
                            SELECT wallet_address1, wallet_address2, wallet_address3, wallet_address4 
                            FROM {table_name}
                            WHERE id = 1
                        ''')
                        result = await cursor.fetchone()
                        if result:
                            available_slots = [i for i, addr in enumerate(result) if addr is None]
                            if available_slots:
                                slot_to_reserve = available_slots[0]
                                wallet_column = f"wallet_address{slot_to_reserve + 1}"
                                await cursor.execute(f'''
                                    UPDATE {table_name} 
                                    SET {wallet_column} = 'reserved'
                                    WHERE id = 1
                                ''')
                                
                                await query.edit_message_text("Processing payment...")
                                payment_success = await send_sol(table_wallet,user_wallet, pk, amount)
                                if payment_success["success"]:
                                    signature = payment_success["result"]

                                    await cursor.execute(f'''
                                        UPDATE {table_name} 
                                        SET {wallet_column} = %s
                                        WHERE id = 1
                                    ''', (user_wallet,))
                                    await query.edit_message_text(
                                                                f"You have successfully entered the round! It will begin automatically when the round fills up.\n\n"
                                                                f"[TX](https://solscan.io/tx/{signature})",
                                                                parse_mode="Markdown", disable_web_page_preview = True
                                                                )
                                    await start(update, context, user_id=user_id)
                                else:
                                    await cursor.execute(f'''
                                        UPDATE {table_name} 
                                        SET {wallet_column} = NULL
                                        WHERE id = 1
                                    ''')
                                    await query.edit_message_text("Payment failed. Please try again.")
                                    await start(update, context, user_id=user_id)
                            else:
                                await query.edit_message_text("Sorry, all slots are full at the moment. Please try again in a few minutes.")
                                await start(update, context, user_id=user_id)
                pool.close()
                await pool.wait_closed()

            else:
                await query.edit_message_text("You do not have enough Sol to enter")
                await start(update, context, user_id=user_id)

        elif query.data == 'zzz_32_001':
                        keyboard = [
                            [InlineKeyboardButton("No", callback_data='no_deposit'),InlineKeyboardButton("Yes", callback_data='yes_zzz_32_001')],
                            [InlineKeyboardButton("Cancel", callback_data='cancel_zyx_001')]
                        ]
                        reply_markup = InlineKeyboardMarkup(keyboard)
                        await query.edit_message_text(
                            "You're about to enter a game of MEGA [BOT_NAME] for 0.01 Sol!!\n\nWould you like to proceed?\n\nOr click Cancel to remove your entries from the game (this will incur a 10% penalty fee).",
                            reply_markup=reply_markup
                        )
        
        elif query.data == 'zzz_32_010':
                        keyboard = [
                            [InlineKeyboardButton("No", callback_data='no_deposit'),InlineKeyboardButton("Yes", callback_data='yes_zzz_32_010')],
                            [InlineKeyboardButton("Cancel", callback_data='cancel_zyx_010')]
                        ]
                        reply_markup = InlineKeyboardMarkup(keyboard)
                        await query.edit_message_text(
                            "You're about to enter a game of MEGA [BOT_NAME] for 0.10 Sol!!\n\nWould you like to proceed?\n\nOr click Cancel to remove your entries from the game (this will incur a 10% penalty fee).",
                            reply_markup=reply_markup
                        )
        
        elif query.data == 'zzz_32_100':
                        keyboard = [
                            [InlineKeyboardButton("No", callback_data='no_deposit'),InlineKeyboardButton("Yes", callback_data='yes_zzz_32_100')],
                            [InlineKeyboardButton("Cancel", callback_data='cancel_zyx_100')]
                        ]
                        reply_markup = InlineKeyboardMarkup(keyboard)
                        await query.edit_message_text(
                            "You're about to enter a game of EXPRESS [BOT_NAME] for 1.0 Sol!!\n\nWould you like to proceed?\n\nOr click Cancel to remove your entries from the game (this will incur a 10% penalty fee).",
                            reply_markup=reply_markup
                        )

        elif query.data.startswith('yes_zzz_32_'):
            entry_fee = query.data.split('_')[-1]
            table_name = f"zyx_{entry_fee}"
            table_wallet = await get_game_wallet(table_name)
            pk = await get_private_key(user_id)
            user_wallet = await get_wallet_address_by_user_id(user_id)
            amount = int(entry_fee)/100
            user_balance = await get_balance(user_wallet)
            amount_needed = int(amount+0.0005)
            if user_balance >= amount_needed:
                pool = await aiomysql.create_pool(
                    host=DB_HOST,
                    user=DB_USER,
                    password=DB_PASSWORD,
                    db=DB_NAME,
                    autocommit=True
                )

                async with pool.acquire() as conn:
                    async with conn.cursor() as cursor:
                        await cursor.execute(f'''
                            SELECT wallet_address1, wallet_address2, wallet_address3, wallet_address4, wallet_address5, wallet_address6, wallet_address7, wallet_address8, wallet_address9, wallet_address10, wallet_address11, wallet_address12, wallet_address13, wallet_address14, wallet_address15, wallet_address16, wallet_address17, wallet_address18, wallet_address19, wallet_address20, wallet_address21, wallet_address22, wallet_address23, wallet_address24, wallet_address25, wallet_address26, wallet_address27, wallet_address28, wallet_address29, wallet_address30, wallet_address31, wallet_address32
                            FROM {table_name}
                            WHERE id = 1
                        ''')
                        result = await cursor.fetchone()
                        if result:
                            available_slots = [i for i, addr in enumerate(result) if addr is None]
                            if available_slots:
                                slot_to_reserve = available_slots[0]
                                wallet_column = f"wallet_address{slot_to_reserve + 1}"
                                await cursor.execute(f'''
                                    UPDATE {table_name} 
                                    SET {wallet_column} = 'reserved'
                                    WHERE id = 1
                                ''')
                                await query.edit_message_text("Processing payment...")
                                payment_success = await send_sol(table_wallet,user_wallet, pk, amount)
                                if payment_success["success"]:
                                    signature = payment_success["result"]
                                    await cursor.execute(f'''
                                        UPDATE {table_name} 
                                        SET {wallet_column} = %s
                                        WHERE id = 1
                                    ''', (user_wallet,))
                                    await query.edit_message_text(
                                                                f"You have successfully entered the round! It will begin automatically when the round fills up.\n\n"
                                                                f"[TX](https://solscan.io/tx/{signature})",
                                                                parse_mode="Markdown", disable_web_page_preview = True
                                                                )
                                    await start(update, context, user_id=user_id)
                                else:
                                    await cursor.execute(f'''
                                        UPDATE {table_name} 
                                        SET {wallet_column} = NULL
                                        WHERE id = 1
                                    ''')
                                    await query.edit_message_text("Payment failed. Please try again.")
                                    await start(update, context, user_id=user_id)
                            else:
                                await query.edit_message_text("Sorry, all slots are full at the moment. Please try again in a few minutes.")
                                await start(update, context, user_id=user_id)

                pool.close()
                await pool.wait_closed()

            else:
                await query.edit_message_text("You do not have enough Sol to enter")
                await start(update, context, user_id=user_id)

        elif query.data == 'wallet':
            keyboard = [
                [InlineKeyboardButton("Secret Key", callback_data='secret_key'),InlineKeyboardButton("Import Wallet", callback_data='import_wallet')],
                [InlineKeyboardButton("Cancel", callback_data='cancel_button')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text("Wallet options:", reply_markup=reply_markup)


        elif query.data == 'cancel_button':
            await context.bot.delete_message(chat_id=query.message.chat_id, message_id=query.message.message_id)

            await start(update, context, user_id=user_id)

        elif query.data == 'no_deposit':
            await context.bot.delete_message(chat_id=query.message.chat_id, message_id=query.message.message_id)

            await start(update, context, user_id=user_id)

        elif query.data == 'secret_key':
            private_key = await get_private_key(user_id)
            if private_key:
                message = await query.edit_message_text(
                    f"YOUR PRIVATE KEY: ||{private_key}||\n\n"
                    f"This message will self destruct in 15 seconds",
                    parse_mode="MarkdownV2" 
                )
                await asyncio.sleep(15)
                await context.bot.delete_message(chat_id=message.chat_id, message_id=message.message_id)
            else:
                await query.edit_message_text("No secret key found.")

            await start(update, context, user_id=user_id)

        elif query.data == 'import_wallet':
            keyboard = [
                [InlineKeyboardButton("Yes", callback_data='yes_wallet')],
                [InlineKeyboardButton("No", callback_data='no_wallet')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(
                                            "*Are you sure you want to update your wallet?*\n\n"
                                            "Please ensure you have:\n"
                                            "- Backed up your previous wallet.\n"
                                            "- Transferred any SOL and tokens out of your previous wallet.\n\n"
                                            "*Note: We do not store any of your wallets data*",
                                            reply_markup=reply_markup,
                                            parse_mode="Markdown"
                                        )

        elif query.data == 'yes_wallet':
            await query.edit_message_text("Please reply with your private key to import your wallet")
            handler = MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                lambda update, context: import_wallet(update, context, user_id, handler)
            )
            context.application.add_handler(handler)

        elif query.data == 'no_wallet':

            await context.bot.delete_message(chat_id=query.message.chat_id, message_id=query.message.message_id)

            await start(update, context, user_id=user_id)

        elif query.data == 'transfer_sol':
            keyboard = [
                [InlineKeyboardButton("Yes", callback_data='yes_transfer')],
                [InlineKeyboardButton("No", callback_data='no_transfer')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            public_key = await get_wallet_address(user_id)
            await query.edit_message_text(f"This function will send all SOL \n\nFrom:{public_key} \nTo: a solana wallet of your choice\n\n"
                                          f"Would you like to proceed?", reply_markup=reply_markup)

        elif query.data == 'yes_transfer':
            await query.edit_message_text("Please reply with your receiving wallet address")
            handler = MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                lambda update, context: transfer_sol(update, context, user_id, handler)
            )
            context.application.add_handler(handler)

        elif query.data == 'no_transfer':
            await context.bot.delete_message(chat_id=query.message.chat_id, message_id=query.message.message_id)
            await start(update, context, user_id=user_id)
    
    asyncio.create_task(handle_query())

async def check_entry(table_name: str, user_wallet: str) -> dict:
    pool = await aiomysql.create_pool(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        db=DB_NAME,
        autocommit=True
    )

    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute(f"SHOW COLUMNS FROM {table_name}")
            columns = await cursor.fetchall()
            wallet_columns = [col[0] for col in columns if col[0].startswith('wallet_address')]
            max_columns = len(wallet_columns)
            total_entries = 0
            for i in range(1, max_columns + 1):
                wallet_column = f'wallet_address{i}'
                try:
                    await cursor.execute(f'SELECT COUNT(*) FROM {table_name} WHERE {wallet_column} = %s', (user_wallet,))
                    result = await cursor.fetchone()
                    total_entries += result[0]
                except pymysql.err.OperationalError:
                    break
            if total_entries > 0:
                return {'success': True, 'entries': total_entries}
            return {'success': False, 'entries': 0}

    pool.close()
    await pool.wait_closed()

async def remove_entry(table_name: str, user_wallet: str):
    pool = await aiomysql.create_pool(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        db=DB_NAME,
        autocommit=True
    )

    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute(f"SHOW COLUMNS FROM {table_name}")
            columns = await cursor.fetchall()
            wallet_columns = [col[0] for col in columns if col[0].startswith('wallet_address')]
            max_columns = len(wallet_columns)
            removed_count = 0
            for i in range(1, max_columns + 1):
                wallet_column = f'wallet_address{i}'
                try:
                    await cursor.execute(f'SELECT COUNT(*) FROM {table_name} WHERE {wallet_column} = %s', (user_wallet,))
                    result = await cursor.fetchone()
                    if result[0] > 0:
                        await cursor.execute(f'UPDATE {table_name} SET {wallet_column} = NULL WHERE {wallet_column} = %s', (user_wallet,))
                        removed_count += result[0]
                except pymysql.err.OperationalError:
                    break
            if removed_count > 0:
                return {"success": True, "result": f"Successfully removed {removed_count} entries"}
            return {"success": False, "error": "No entries found for your wallet"}

    pool.close()
    await pool.wait_closed()

async def transfer_sol(update: Update, context: Application, user_id: int, handler: MessageHandler) -> None:
    
    public_key_base58 = update.message.text.strip()
    try:
        public_key_bytes = base58.b58decode(public_key_base58)
        public_key_hex = public_key_bytes.hex()
    except ValueError:
        await update.message.reply_text("Invalid public key format. Please retry.")
        return

    if len(public_key_hex) == 64:  
        to_wallet = public_key_base58
        sk = await get_private_key(user_id)
        wallet_address = await get_wallet_address(user_id)
        balance = await get_balance(wallet_address)
        balance_lamps = balance *10**9
        if balance_lamps >= 1000000:
            amount_needed = balance - 0.001
            sent_amount = amount_needed
            processing_message = await update.message.reply_text(f"Processing your transaction, please wait...")
            send_result = await send_sol(to_wallet,wallet_address, sk, sent_amount)
            if send_result["success"]:
                loop_counter = 5
                while True:
                    new_balance = await get_balance(wallet_address)
                    if new_balance < balance or loop_counter <= 0:
                        await processing_message.edit_text(f"Successfully sent {sent_amount:.3f} SOL")
                        break
                    else:
                        loop_counter -=1
                        await asyncio.sleep(5)
            else:
                await processing_message.edit_text(f"An error occured please try again")
                await start(update, context)
        else:
                await update.message.reply_text("Insufficient funds")
    else:
        await update.message.reply_text("Invalid public key. Please retry.")

    context.application.remove_handler(handler)
    await start(update, context)

async def save_game_results_e(game_number, results, tablename, entry_amount, prize_amount):
    filename = "xxx_game_results.json"
    game_data = {
        "game_number": game_number,
        "tablename": tablename,
        "entry_amount": entry_amount,
        "prize_amount": prize_amount,
        "participants": results['participants'] if 'participants' in results else [],
        "round1": {
            "eliminated": results['round1']['eliminated'],
            "advanced": results['round1']['advanced'] if 'advanced' in results['round1'] else []
        },
        "final_round": {
            "winner": results['final_round']['winner'],
            "eliminated": results['final_round']['eliminated']
        },
        "timestamp": datetime.datetime.now().isoformat()
    }

    if os.path.exists(filename):
        async with aiofiles.open(filename, 'r') as f:
            content = await f.read()
            data = json.loads(content) if content else {"games": {}}
    else:
        data = {"games": {}}

    data["games"][str(game_number)] = game_data

    async with aiofiles.open(filename, 'w') as f:
        await f.write(json.dumps(data, indent=2))

async def monitor_and_select_winner(tablename: str):

    entry_amount = int(tablename.split('_')[-1]) / 100
    prize_amount = round((entry_amount*3.6),3)
    pool = await aiomysql.create_pool(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        db=DB_NAME,
        autocommit=True
    )

    filename = "xxx_game_results.json"
    if os.path.exists(filename):
        async with aiofiles.open(filename, 'r') as f:
            content = await f.read()
            data = json.loads(content) if content else {"games": {}}
            game_number = max([int(n) for n in data["games"].keys()], default=0) + 1
    else:
        game_number = 1

    try:
        while True:
            async with pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(f'''
                        SELECT 
                            wallet_address1, wallet_address2, wallet_address3, wallet_address4
                        FROM 
                            {tablename}
                        WHERE 
                            id = 1
                    ''')
                    result = await cursor.fetchone()
                    
                    if result:
                        all_filled = all(addr and addr != 'reserved' for addr in result)
                        if all_filled:
                            notified_wallets = set()
                            for wallet in [addr for addr in result if addr != 'reserved']:
                                user_id = await get_user_id(wallet)
                                if user_id and user_id not in notified_wallets:
                                    try:
                                        send_sticker = "CAACAgIAAxkBAAExzS5nsdhvyB7omklmDT4YeVCjNTakSAACFwEAAlKJkSOqvO85lUg92zYE"
                                        await bot.send_sticker(sticker=send_sticker, chat_id=user_id)
                                        await bot.send_message(chat_id=user_id, text="Your game is about to start in 30 seconds\\!", parse_mode='MarkdownV2')
                                        await asyncio.sleep(3)
                                    except Exception as e:
                                        print(f"Failed to notify user {user_id}: {e}")
                                    notified_wallets.add(user_id)
                            
                            game_results = await xxx_game(tablename)
                            if game_results:
                                entry_list = "\n".join([f"[{addr[:4]}...{addr[-4:]}](https://solscan.io/account/{addr})" for addr in result if addr != 'reserved'])
                                round1_start_msg = f"Express Game {game_number}\n\nRound 1 for Express [BOT_NAME] starting: \n\nWallets:\n{entry_list}\n\n*Prize:* {prize_amount} Sol\n*Entry Fee:* {entry_amount} Sol"
                                await bot.send_video(
                                                                chat_id=CHANNELID,
                                                                video=open(video_filename1, 'rb'),
                                                                caption=round1_start_msg,
                                                                parse_mode="Markdown"
                                                            )
                                                            
                                for user_id in notified_wallets:
                                    try:
                                        
                                        await bot.send_video(
                                            chat_id=user_id,
                                            video =open(video_filename1, 'rb'),
                                            caption=round1_start_msg, 
                                            parse_mode='Markdown'
                                        )
                                        await asyncio.sleep(3)
                                        send_sticker = "CAACAgIAAxkBAAExsbdnrNePZPbQ7CsFKxIxl7PmC1ILSgACGAEAAlKJkSNb3Pli_y_o4zYE"
                                        await bot.send_sticker(sticker=send_sticker, chat_id=user_id)
                                        await bot.send_message(chat_id=user_id, text="[BOT_NAME]ing 50% of wallets randomly", parse_mode='Markdown')
                                        await asyncio.sleep(3)
                                    except Exception as e:
                                        print(f"Failed to send Round 1 start message to {user_id}: {e}")

                                for user_id in notified_wallets:
                                    try:
                                        display_lines = game_results['round1']['display'].split('\n')
                                        formatted_display = []
                                        for line in display_lines:
                                            if line.startswith('Round 1 results:'):
                                                formatted_display.append(line.strip())
                                            elif line.startswith('*Eliminated:') or line.startswith('*Advance to next round'):
                                                formatted_display.append(line.replace('*', '').strip())
                                            elif line.strip():
                                                wallet = line.strip()
                                                formatted_display.append(f"[{wallet[:4]}...{wallet[-4:]}](https://solscan.io/account/{wallet})")
                                        formatted_display.insert(1, '')  
                                        formatted_display.insert(5, '')  
                                        await bot.send_message(
                                            chat_id=user_id, 
                                            text="\n".join(formatted_display),
                                            parse_mode='Markdown', 
                                            disable_web_page_preview=True
                                        )
                                    except Exception as e:
                                        print(f"Failed to send Round 1 results to {user_id}: {e}")
                                await asyncio.sleep(3)
                                for user_id in notified_wallets:
                                    try:
                                        send_sticker = "CAACAgIAAxkBAAExsbdnrNePZPbQ7CsFKxIxl7PmC1ILSgACGAEAAlKJkSNb3Pli_y_o4zYE"
                                        await bot.send_message(chat_id=user_id, text="Round 2 is about to start!", parse_mode='Markdown')
                                        await asyncio.sleep(3)
                                        await bot.send_sticker(sticker=send_sticker, chat_id=user_id)
                                        await bot.send_message(chat_id=user_id, text="[BOT_NAME]ing 50% of wallets randomly", parse_mode='Markdown')
                                        await asyncio.sleep(3)
                                    except Exception as e:
                                        print(f"Failed to send next Round start message to {user_id}: {e}")
                                for user_id in notified_wallets:
                                    try:
                                        display_lines = game_results['final_round']['display'].split('\n')
                                        formatted_display = []

                                        for line in display_lines:
                                            if line.strip() == 'Final round results:':
                                                formatted_display.append(line.strip())
                                            elif line.strip() == 'Eliminated:':
                                                formatted_display.append(line.strip())
                                            elif line.strip().startswith('Winner!!'):
                                                wallet = line.split('Winner!!')[-1].strip()
                                                formatted_display.append(f'Winner!!\n[{wallet[:4]}...{wallet[-4:]}](https://solscan.io/account/{wallet})')
                                            elif line.strip():
                                                formatted_display.append(f"[{line.strip()[:4]}...{line.strip()[-4:]}](https://solscan.io/account/{line.strip()})")
                                        formatted_display.insert(1, '')
                                        formatted_display.insert(4, '') 
                                        await bot.send_message(
                                            chat_id=user_id, 
                                            text="\n".join(formatted_display),
                                            parse_mode='Markdown', 
                                            disable_web_page_preview=True
                                        )
                                    except Exception as e:
                                        print(f"Failed to send final round results to {user_id}: {e}")
                                await asyncio.sleep(3)
                                final_results_msg = (
                                    f"Express Game {game_number}\n\n"
                                    "*GAME SUMMARY*\n\n"
                                    "*Round 1 [BOT_NAME]ed Wallets:*\n" +
                                    "\n".join([f"[{wallet[:4]}...{wallet[-4:]}](https://solscan.io/account/{wallet})" 
                                            for wallet in game_results['round1']['eliminated']]) +
                                    "\n\n*Round 2 [BOT_NAME]ed Wallet:*\n" +
                                    "\n".join([f"[{wallet[:4]}...{wallet[-4:]}](https://solscan.io/account/{wallet})" 
                                            for wallet in game_results['final_round']['eliminated']]) +
                                    f"\n\n*First Place Won {prize_amount} Sol:* \n\n[{game_results['final_round']['winner'][:4]}...{game_results['final_round']['winner'][-4:]}](https://solscan.io/account/{game_results['final_round']['winner']})"
                                )
                                await bot.send_video(
                                                                chat_id=CHANNELID,
                                                                video=open(video_filename2, 'rb'),
                                                                caption=final_results_msg,
                                                                parse_mode="Markdown"
                                                            )
                                for user_id in notified_wallets:
                                    try:
                                        await bot.send_video(chat_id=user_id,video = open(video_filename2, 'rb'), caption=final_results_msg, parse_mode='Markdown')
                                    except Exception as e:
                                        print(f"Failed to send Overall game results to {user_id}: {e}")
                                        
                                winner = game_results['final_round']['winner']
                                to_wallet = winner
                                from_wallet = await get_game_wallet(tablename)
                                pk = await get_game_private_key(tablename)
                                fee_wallet = FEEWALLET
                                send_e_prize = await asyncio.create_task(send_sol_e(to_wallet,from_wallet,fee_wallet,pk,entry_amount))
                                if send_e_prize["success"]:
                                    signature = send_e_prize["result"]
                                winner_id = await get_user_id(winner)
                                final_eliminated = game_results['final_round']['eliminated']
                                for loser in final_eliminated:
                                    loser_id = await get_user_id(loser)
                                    if loser_id and loser_id != winner_id:
                                        try:
                                            await bot.send_message(chat_id=loser_id, text="You did not win this time\\. Better luck next round\\!", parse_mode='MarkdownV2')
                                        except Exception as e:
                                            print(f"Failed to notify loser {loser_id}: {e}")

                                winner_amount = round(entry_amount * 3.6, 3)
                                if winner_id:
                                    try:
                                        await bot.send_message(chat_id=winner_id, text=(f"Congratulations! You've won this round!\n\n"
                                                                                        f"[TX](https://solscan.io/tx/{signature})\n"
                                                                                        f"*Prize:* {winner_amount} Sol"), parse_mode='Markdown',disable_web_page_preview = True)
                                    except Exception as e:
                                        print(f"Failed to notify winner {winner_id}: {e}")

                            game_results['participants'] = [addr for addr in result if addr != 'reserved']
                            await save_game_results_e(game_number, game_results, tablename, entry_amount, prize_amount)
                            game_number += 1 

                            await cursor.execute(f'''
                                UPDATE {tablename} 
                                SET 
                                    wallet_address1 = NULL,
                                    wallet_address2 = NULL,
                                    wallet_address3 = NULL,
                                    wallet_address4 = NULL
                                WHERE id = 1
                            ''')

            await asyncio.sleep(10) 

    except Exception as e:
        print(f"An error occurred while monitoring {tablename}: {e}")
    finally:
        pool.close()
        await pool.wait_closed()

async def save_zzz_game_results(game_number, results, tablename, prize_amount1, prize_amount2, prize_amount3, prize_amount4):
    filename = "zzz_game_results.json"
    game_data = {
        "game_number": game_number,
        "tablename": tablename,
        "prize_amounts": {
            "first": prize_amount1,
            "second": prize_amount2,
            "round4": prize_amount3,
            "round3": prize_amount4
        },
        "participants": results.get('participants', []),
        "round1": {
            "eliminated": results['round1']['eliminated']
        },
        "round2": {
            "eliminated": results['round2']['eliminated']
        },
        "round3": {
            "eliminated": results['round3']['eliminated']
        },
        "round4": {
            "eliminated": results['round4']['eliminated']
        },
        "round5": {
            "eliminated": results['round5']['eliminated'],
            "winners": results['round5']['remaining']
        },
        "timestamp": datetime.datetime.now().isoformat()
    }

    if os.path.exists(filename):
        async with aiofiles.open(filename, 'r') as f:
            content = await f.read()
            data = json.loads(content) if content else {"games": {}}
    else:
        data = {"games": {}}

    data["games"][str(game_number)] = game_data

    async with aiofiles.open(filename, 'w') as f:
        await f.write(json.dumps(data, indent=2))

async def monitor_and_select_winner2(tablename: str):

    entry_amount = int(tablename.split('_')[-1]) / 100
    prize_amount1 = round((entry_amount * 14.3), 3)
    prize_amount2 = round((entry_amount * 4.3), 3)
    prize_amount3 = round((entry_amount * 2), 3)
    prize_amount4 = round((entry_amount * 1.55), 3)
    pool = await aiomysql.create_pool(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        db=DB_NAME,
        autocommit=True
    )

    filename = "zzz_game_results.json"
    if os.path.exists(filename):
        async with aiofiles.open(filename, 'r') as f:
            content = await f.read()
            data = json.loads(content) if content else {"games": {}}
            game_number = max([int(n) for n in data["games"].keys()], default=0) + 1
    else:
        game_number = 1

    try:
        while True:
            async with pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(f'''
                        SELECT 
                            wallet_address1, wallet_address2, wallet_address3, wallet_address4, 
                            wallet_address5, wallet_address6, wallet_address7, wallet_address8, 
                            wallet_address9, wallet_address10, wallet_address11, wallet_address12, 
                            wallet_address13, wallet_address14, wallet_address15, wallet_address16,
                            wallet_address17, wallet_address18, wallet_address19, wallet_address20,
                            wallet_address21, wallet_address22, wallet_address23, wallet_address24,
                            wallet_address25, wallet_address26, wallet_address27, wallet_address28,
                            wallet_address29, wallet_address30, wallet_address31, wallet_address32
                        FROM 
                            {tablename}
                        WHERE 
                            id = 1
                    ''')
                    result = await cursor.fetchone()
                    if result:
                        all_filled = all(addr and addr != 'reserved' for addr in result)
                        if all_filled:
                            notified_wallets = set()
                            for wallet in [addr for addr in result if addr != 'reserved']:
                                user_id = await get_user_id(wallet)
                                if user_id and user_id not in notified_wallets:
                                    try:
                                        send_sticker = "CAACAgIAAxkBAAExzS5nsdhvyB7omklmDT4YeVCjNTakSAACFwEAAlKJkSOqvO85lUg92zYE"
                                        await bot.send_sticker(sticker=send_sticker, chat_id=user_id)
                                        await bot.send_message(chat_id=user_id, text="The game is about to start\\!", parse_mode='MarkdownV2')
                                        await asyncio.sleep(3)
                                    except Exception as e:
                                        print(f"Failed to notify user {user_id}: {e}")
                                    notified_wallets.add(user_id)
                            game_results = await zzz_game(tablename)
                            if game_results:
                                entry_list = "\n".join([addr for addr in result if addr != 'reserved'])
                                entry_list = "\n".join([f"[{addr[:4]}...{addr[-4:]}](https://solscan.io/account/{addr})" for addr in result if addr != 'reserved'])
                                round1_start_msg = f"Express Game {game_number}\n\nExpress Game {game_number}\n\nRound 1 for Mega [BOT_NAME] starting: \n\nWallets:\n{entry_list}\n\n*Entry Fee:* {entry_amount} Sol\n*Prize:* 🥇{prize_amount1} 🥈{prize_amount2}  3️⃣4️⃣{prize_amount3}  5️⃣8️⃣{prize_amount4} Sol"
                                await bot.send_video(
                                                                chat_id=CHANNELID,
                                                                video=open(video_filename3, 'rb'),
                                                                caption=round1_start_msg,
                                                                parse_mode="Markdown"
                                                            )
                                #ROUND 1
                                for user_id in notified_wallets:
                                    try:
                                        
                                        await bot.send_video(
                                            chat_id=user_id,
                                            video = open(video_filename3, 'rb'),
                                            caption=round1_start_msg, 
                                            parse_mode='Markdown', 
                                            disable_web_page_preview=True
                                        )
                                        await asyncio.sleep(3)
                                        send_sticker = "CAACAgIAAxkBAAExsbdnrNePZPbQ7CsFKxIxl7PmC1ILSgACGAEAAlKJkSNb3Pli_y_o4zYE"
                                        await bot.send_sticker(sticker=send_sticker, chat_id=user_id)
                                        await bot.send_message(chat_id=user_id, text="[BOT_NAME]ing 50% of wallets randomly", parse_mode='Markdown')
                                        await asyncio.sleep(5)

                                    except Exception as e:
                                        print(f"Failed to send Round 1 start message to {user_id}: {e}")
                                for user_id in notified_wallets:
                                    try:
                                        display_lines = game_results['round1']['display'].split('\n')
                                        formatted_display = []

                                        for line in display_lines:
                                            if line.startswith('Round 1 results:'):
                                                formatted_display.append(line.strip())
                                            elif line.startswith('*Eliminated:') or line.startswith('*Advance to next round'):
                                                formatted_display.append(line.replace('*', '').strip())  
                                            elif line.strip():  
                                                wallet = line.strip()
                                                formatted_display.append(f"[{wallet[:4]}...{wallet[-4:]}](https://solscan.io/account/{wallet})")
                                        
                                        
                                        formatted_display.insert(1, '') 
                                        formatted_display.insert(19, '')  
                                        

                                        await bot.send_message(
                                            chat_id=user_id, 
                                            text="\n".join(formatted_display),
                                            parse_mode='Markdown', 
                                            disable_web_page_preview=True
                                        )
                                        await asyncio.sleep(5)
                                    except Exception as e:
                                        print(f"Failed to send Round 1 results to {user_id}: {e}")

                                #ROUND 2
                                for user_id in notified_wallets:
                                    try:
                                        send_sticker = "CAACAgIAAxkBAAExsbdnrNePZPbQ7CsFKxIxl7PmC1ILSgACGAEAAlKJkSNb3Pli_y_o4zYE"
                                        await bot.send_message(chat_id=user_id, text="Round 2 is about to start!", parse_mode='Markdown')
                                        await asyncio.sleep(3)
                                        await bot.send_sticker(sticker=send_sticker, chat_id=user_id)
                                        await bot.send_message(chat_id=user_id, text="[BOT_NAME]ing 50% of wallets randomly", parse_mode='Markdown')
                                        await asyncio.sleep(5)
                                    except Exception as e:
                                        print(f"Failed to send next Round start message to {user_id}: {e}")
                                for user_id in notified_wallets:
                                    try:
                                        display_lines = game_results['round2']['display'].split('\n')
                                        formatted_display = []

                                        for line in display_lines:
                                            if line.startswith('Round 2 results:'):
                                                formatted_display.append(line.strip())
                                            elif line.startswith('*Eliminated:') or line.startswith('*Advance to next round'):
                                                formatted_display.append(line.replace('*', '').strip()) 
                                            elif line.strip():  
                                                wallet = line.strip()
                                                formatted_display.append(f"[{wallet[:4]}...{wallet[-4:]}](https://solscan.io/account/{wallet})")
                                        formatted_display.insert(1, '') 
                                        formatted_display.insert(11, '')  
                                        await bot.send_message(
                                            chat_id=user_id, 
                                            text="\n".join(formatted_display),
                                            parse_mode='Markdown', 
                                            disable_web_page_preview=True
                                        )
                                        await asyncio.sleep(5)
                                    except Exception as e:
                                        print(f"Failed to send Round 1 results to {user_id}: {e}")

                                #ROUND 3 
                                for user_id in notified_wallets:
                                    try:
                                        send_sticker = "CAACAgIAAxkBAAExsbdnrNePZPbQ7CsFKxIxl7PmC1ILSgACGAEAAlKJkSNb3Pli_y_o4zYE"
                                        await bot.send_message(chat_id=user_id, text="Round 3 is about to start!", parse_mode='Markdown')
                                        await asyncio.sleep(3)
                                        await bot.send_sticker(sticker=send_sticker, chat_id=user_id)
                                        await bot.send_message(chat_id=user_id, text="[BOT_NAME]ing 50% of wallets randomly", parse_mode='Markdown')
                                        await asyncio.sleep(5)
                                    except Exception as e:
                                        print(f"Failed to send next Round start message to {user_id}: {e}")
                                for user_id in notified_wallets:
                                    try:
                                        display_lines = game_results['round3']['display'].split('\n')
                                        formatted_display = []
                                        for line in display_lines:
                                            if line.startswith('Round 3 results:'):
                                                formatted_display.append(line.strip())
                                            elif line.startswith('*Eliminated:') or line.startswith('*Advance to next round'):
                                                formatted_display.append(line.replace('*', '').strip()) 
                                            elif line.strip(): 
                                                wallet = line.strip()
                                                formatted_display.append(f"[{wallet[:4]}...{wallet[-4:]}](https://solscan.io/account/{wallet})")
                                        formatted_display.insert(1, '')  
                                        formatted_display.insert(7, '') 
                                        await bot.send_message(
                                            chat_id=user_id, 
                                            text="\n".join(formatted_display),
                                            parse_mode='Markdown',  
                                            disable_web_page_preview=True
                                        )
                                        await asyncio.sleep(5)
                                    except Exception as e:
                                        print(f"Failed to send Round 1 results to {user_id}: {e}")
                                
                                #ROUND 4
                                for user_id in notified_wallets:
                                    try:
                                        send_sticker = "CAACAgIAAxkBAAExsbdnrNePZPbQ7CsFKxIxl7PmC1ILSgACGAEAAlKJkSNb3Pli_y_o4zYE"
                                        await bot.send_message(chat_id=user_id, text="Round 4 is about to start!", parse_mode='Markdown')
                                        await asyncio.sleep(3)
                                        await bot.send_sticker(sticker=send_sticker, chat_id=user_id)
                                        await bot.send_message(chat_id=user_id, text="[BOT_NAME]ing 50% of wallets randomly", parse_mode='Markdown')
                                        await asyncio.sleep(5)
                                    except Exception as e:
                                        print(f"Failed to send next Round start message to {user_id}: {e}")
                                for user_id in notified_wallets:
                                    try:
                                        display_lines = game_results['round4']['display'].split('\n')
                                        formatted_display = []

                                        for line in display_lines:
                                            if line.startswith('Round 4 results:'):
                                                formatted_display.append(line.strip())
                                            elif line.startswith('*Eliminated:') or line.startswith('*Advance to next round'):
                                                formatted_display.append(line.replace('*', '').strip())  
                                            elif line.strip():  
                                                wallet = line.strip()
                                                formatted_display.append(f"[{wallet[:4]}...{wallet[-4:]}](https://solscan.io/account/{wallet})")
                                        
                                        formatted_display.insert(1, '') 
                                        formatted_display.insert(5, '')  
                                        await bot.send_message(
                                            chat_id=user_id, 
                                            text="\n".join(formatted_display),
                                            parse_mode='Markdown',  
                                            disable_web_page_preview=True
                                        )
                                        await asyncio.sleep(5)
                                    except Exception as e:
                                        print(f"Failed to send Round 1 results to {user_id}: {e}")

                                #FINAL ROUND
                                for user_id in notified_wallets:
                                    try:
                                        send_sticker = "CAACAgIAAxkBAAExsbdnrNePZPbQ7CsFKxIxl7PmC1ILSgACGAEAAlKJkSNb3Pli_y_o4zYE"
                                        await bot.send_message(chat_id=user_id, text="Round 5 Final Round about to start!", parse_mode='Markdown')
                                        await asyncio.sleep(3)
                                        await bot.send_sticker(sticker=send_sticker, chat_id=user_id)
                                        await bot.send_message(chat_id=user_id, text="[BOT_NAME]ing 50% of wallets randomly", parse_mode='Markdown')
                                        await asyncio.sleep(5)
                                    except Exception as e:
                                        print(f"Failed to send next Round start message to {user_id}: {e}")
                                for user_id in notified_wallets:
                                    try:
                                        display_lines = game_results['round5']['display'].split('\n')
                                        formatted_display = []

                                        for line in display_lines:
                                            if line.startswith('Round 5 results:'):
                                                formatted_display.append("Final Round Results")
                                            elif line.startswith('*Eliminated:*'):
                                                formatted_display.append(line.replace('*', '').strip())
                                            elif line.startswith('*Advance to next round*'):
                                                formatted_display.append("Winner:")
                                            elif line.strip() and not line.startswith('*'): 
                                                wallet = line.strip()
                                                
                                                formatted_display.append(f"[{wallet[:4]}...{wallet[-4:]}](https://solscan.io/account/{wallet})")
                                        formatted_display.insert(1, '')  
                                        formatted_display.insert(4, '') 
                                        await bot.send_message(
                                            chat_id=user_id, 
                                            text="\n".join(formatted_display),
                                            parse_mode='Markdown',  
                                            disable_web_page_preview=True
                                        )
                                        await asyncio.sleep(5)
                                    except Exception as e:
                                        print(f"Failed to send Round 5 results to {user_id}: {e}")
                                winner = game_results['round5']['remaining'][0]
                                final_results_msg = (f"Mega Game {game_number}\n\n"
                                    "*GAME SUMMARY*\n\n"
                                    "*Round 1 [BOT_NAME]ed Wallets:*\n" +
                                    "\n".join([f"[{wallet[:4]}...{wallet[-4:]}](https://solscan.io/account/{wallet})" 
                                            for wallet in game_results['round1']['eliminated']]) +
                                    "\n\n*Round 2 [BOT_NAME]ed Wallets:*\n" +
                                    "\n".join([f"[{wallet[:4]}...{wallet[-4:]}](https://solscan.io/account/{wallet})" 
                                            for wallet in game_results['round2']['eliminated']]) +
                                    f"\n\n*Round 3 Winners Won {prize_amount4} Sol:*\n" +
                                    "\n".join([f"[{wallet[:4]}...{wallet[-4:]}](https://solscan.io/account/{wallet})" 
                                            for wallet in game_results['round3']['eliminated']]) +
                                    f"\n\n*Round 4 Winners Won {prize_amount3} Sol:*\n" +
                                    "\n".join([f"[{wallet[:4]}...{wallet[-4:]}](https://solscan.io/account/{wallet})" 
                                            for wallet in game_results['round4']['eliminated']]) +
                                    f"\n\n*Second Place Won {prize_amount2} Sol:*\n" +
                                    "\n".join([f"[{wallet[:4]}...{wallet[-4:]}](https://solscan.io/account/{wallet})" 
                                            for wallet in game_results['round5']['eliminated']]) +
                                    f"\n\n*First Place Won {prize_amount1} Sol:*\n" +
                                    "\n".join([f"[{winner[:4]}...{winner[-4:]}](https://solscan.io/account/{winner})" 
                                            for winner in game_results['round5']['remaining']])
                                )
                                await bot.send_video(
                                                                chat_id=CHANNELID,
                                                                video=open(video_filename4, 'rb'),
                                                                caption=final_results_msg,
                                                                parse_mode="Markdown"
                                                            )
                                for user_id in notified_wallets:
                                    try:
                                        await asyncio.sleep(3)
                                        await bot.send_video(chat_id=user_id, video = open(video_filename4, 'rb'), caption=final_results_msg, parse_mode='Markdown')
                                    except Exception as e:
                                        print(f"Failed to send Overall game results to {user_id}: {e}")
                                        
                                winner = game_results['round5']['remaining'][0]
                                second = game_results['round5']['eliminated'][0]
                                third = game_results['round4']['eliminated'][0]
                                forth = game_results['round4']['eliminated'][1]
                                fifth = game_results['round3']['eliminated'][0]
                                sixth = game_results['round3']['eliminated'][1]
                                seventh = game_results['round3']['eliminated'][2]
                                eighth = game_results['round3']['eliminated'][3]
                                from_wallet = await get_game_wallet(tablename)
                                pk = await get_game_private_key(tablename)
                                fee_wallet = FEEWALLET

                                send_m_prize = await asyncio.create_task(send_sol_m(winner,from_wallet, fee_wallet,second,third,forth,fifth,sixth,seventh,eighth,pk,entry_amount))
                                if send_m_prize["success"]:
                                    signature = send_m_prize["result"]
                                winner_id = await get_user_id(winner)
                                second_id = await get_user_id(second)
                                third_id = await get_user_id(third)
                                forth_id = await get_user_id(forth)
                                fifth_id = await get_user_id(fifth)
                                sixth_id = await get_user_id(sixth)
                                seventh_id = await get_user_id(seventh)
                                eighth_id = await get_user_id(eighth)
                                winner_amount = round(entry_amount * 14.3, 3)
                                second_amount = round(entry_amount * 4.3, 3) 
                                third_forth_amount = round(entry_amount * 2, 3)
                                fifth_eighth_amount = round(entry_amount * 1.55, 3)
                                game_results['participants'] = []  
                                await save_zzz_game_results(game_number, game_results, tablename, winner_amount, second_amount, third_forth_amount, fifth_eighth_amount)
                                game_number += 1  
                                
                                for i in range(1, 3):
                                    for loser in game_results[f'round{i}']['eliminated']:
                                        loser_id = await get_user_id(loser)
                                        if loser_id and loser_id not in [winner_id, second_amount, third_id, forth_id, fifth_id, sixth_id, seventh_id, eighth_id]:  
                                            try:
                                                await bot.send_message(chat_id=loser_id, text="You did not win this time. Better luck next round!", parse_mode='Markdown')
                                            except Exception as e:
                                                print(f"Failed to notify loser {loser_id}: {e}")

                                if winner_id:
                                    try:
                                        await bot.send_message(chat_id=winner_id, text=(
                                                                                    f"Congratulations! You've won this round!\n\n"
                                                                                    f"[TX](https://solscan.io/tx/{signature})\n"
                                                                                    f"*Prize:* {winner_amount} Sol"), 
                                                                                    parse_mode='Markdown',disable_web_page_preview = True)
                                    except Exception as e:
                                        print(f"Failed to notify winner {winner_id}: {e}")

                                if second_id:
                                    try:
                                        await bot.send_message(chat_id=second_id, text=(
                                                                                    f"Congratulations! You've came 2nd this round!\n\n"
                                                                                    f"[TX](https://solscan.io/tx/{signature})\n"
                                                                                    f"*Prize:* {second_amount} Sol"), 
                                                                                    parse_mode='Markdown',disable_web_page_preview = True)
                                    except Exception as e:
                                        print(f"Failed to notify winner {second_id}: {e}")

                                if third_id:
                                    try:
                                        await bot.send_message(chat_id=third_id, text=(
                                                                                    f"Congratulations! You've came 3rd this round!\n\n"
                                                                                    f"[TX](https://solscan.io/tx/{signature})\n"
                                                                                    f"*Prize:* {third_forth_amount} Sol"), 
                                                                                    parse_mode='Markdown',disable_web_page_preview = True)
                                    except Exception as e:
                                        print(f"Failed to notify winner {third_id}: {e}")

                                if forth_id:
                                    try:
                                        await bot.send_message(chat_id=forth_id, text=(
                                                                                    f"Congratulations! You've came 4th this round!\n\n"
                                                                                    f"[TX](https://solscan.io/tx/{signature})\n"
                                                                                    f"*Prize:* {third_forth_amount} Sol"), 
                                                                                    parse_mode='Markdown',disable_web_page_preview = True)
                                    except Exception as e:
                                        print(f"Failed to notify winner {forth_id}: {e}")

                                if fifth_id:
                                    try:
                                        await bot.send_message(chat_id=fifth_id, text=(
                                                                                    f"Congratulations! You've came 5th this round!\n\n"
                                                                                    f"[TX](https://solscan.io/tx/{signature})\n"
                                                                                    f"*Prize:* {fifth_eighth_amount} Sol"), 
                                                                                    parse_mode='Markdown',disable_web_page_preview = True)
                                    except Exception as e:
                                        print(f"Failed to notify winner {fifth_id}: {e}")

                                if sixth_id:
                                    try:
                                        await bot.send_message(chat_id=sixth_id, text=(
                                                                                    f"Congratulations! You've came 6th this round!\n\n"
                                                                                    f"[TX](https://solscan.io/tx/{signature})\n"
                                                                                    f"*Prize:* {fifth_eighth_amount} Sol"), 
                                                                                    parse_mode='Markdown',disable_web_page_preview = True)
                                    except Exception as e:
                                        print(f"Failed to notify winner {sixth_id}: {e}")

                                if seventh_id:
                                    try:
                                        await bot.send_message(chat_id=seventh_id, text=(
                                                                                    f"Congratulations! You've came 7th this round!\n\n"
                                                                                    f"[TX](https://solscan.io/tx/{signature})\n"
                                                                                    f"*Prize:* {fifth_eighth_amount} Sol"), 
                                                                                    parse_mode='Markdown',disable_web_page_preview = True)
                                    except Exception as e:
                                        print(f"Failed to notify winner {seventh_id}: {e}")

                                if eighth_id:
                                    try:
                                        await bot.send_message(chat_id=eighth_id, text=(
                                                                                    f"Congratulations! You've came 8th this round!\n\n"
                                                                                    f"[TX](https://solscan.io/tx/{signature})\n"
                                                                                    f"*Prize:* {fifth_eighth_amount} Sol"), 
                                                                                    parse_mode='Markdown',disable_web_page_preview = True)
                                    except Exception as e:
                                        print(f"Failed to notify winner {eighth_id}: {e}")

                            await cursor.execute(f'''
                                UPDATE {tablename} 
                                SET 
                                    wallet_address1 = NULL,
                                    wallet_address2 = NULL,
                                    wallet_address3 = NULL,
                                    wallet_address4 = NULL,
                                    wallet_address5 = NULL,
                                    wallet_address6 = NULL,
                                    wallet_address7 = NULL,
                                    wallet_address8 = NULL,
                                    wallet_address9 = NULL,
                                    wallet_address10 = NULL,
                                    wallet_address11 = NULL,
                                    wallet_address12 = NULL,
                                    wallet_address13 = NULL,
                                    wallet_address14 = NULL,
                                    wallet_address15 = NULL,
                                    wallet_address16 = NULL,
                                    wallet_address17 = NULL,
                                    wallet_address18 = NULL,
                                    wallet_address19 = NULL,
                                    wallet_address20 = NULL,
                                    wallet_address21 = NULL,
                                    wallet_address22 = NULL,
                                    wallet_address23 = NULL,
                                    wallet_address24 = NULL,
                                    wallet_address25 = NULL,
                                    wallet_address26 = NULL,
                                    wallet_address27= NULL,
                                    wallet_address28 = NULL,
                                    wallet_address29 = NULL,
                                    wallet_address30 = NULL,
                                    wallet_address31 = NULL,
                                    wallet_address32 = NULL
                                WHERE id = 1
                            ''')

            await asyncio.sleep(10)  

    except Exception as e:
        print(f"An error occurred while monitoring {tablename}: {e}")
    finally:
        pool.close()
        await pool.wait_closed()

async def import_wallet(update: Update, context: Application, user_id: int, handler: MessageHandler) -> None:

    if update.message.chat.type != "private":
        return

    if update.message.from_user.id != user_id:
        return

    private_key_base58 = update.message.text.strip()

    try:

        private_key_bytes = base58.b58decode(private_key_base58)
        private_key_hex = private_key_bytes.hex()
        
    except ValueError:
        raise ValueError("Invalid private key format")
    
    if len(private_key_hex) == 128:
        
        private_key = Keypair.from_base58_string(private_key_base58)
        update_wallet = str(private_key.pubkey())
        await save_wallet_address(user_id, wallet_address=update_wallet, private_key=private_key_base58)
        await update.message.reply_text(f"Your wallet {update_wallet} has been successfully imported!")
    else:
        await update.message.reply_text("Invalid private key format. Please retry.")

    try:
        await context.bot.delete_message(chat_id=update.message.chat.id, message_id=update.message.message_id)
    except Exception as e:
        print(f"Failed to delete message: {e}")

    context.application.remove_handler(handler)

    await start(update, context)


def main():

    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", create_start_task))
    application.add_handler(CallbackQueryHandler(button))
    threading.Thread(target=async_init, daemon=True).start()
    application.run_polling()

def async_init():
  
    asyncio.run(setup_database())
    
if __name__ == '__main__':
    main()
