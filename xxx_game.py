import asyncio
import random
import aiomysql
import os
from dotenv import load_dotenv

load_dotenv('.env')

DB_NAME = os.getenv('DB_NAME')  
DB_HOST = os.getenv('DB_HOST')  
DB_USER = os.getenv('DB_USER')  
DB_PASSWORD = os.getenv('DB_PASSWORD')

async def express_game(tablename: str):
    pool = await aiomysql.create_pool(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        db=DB_NAME,
        autocommit=True
    )

    try:
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
                wallets = await cursor.fetchone()
                if wallets:
                    participants = [
                        (i, wallet) for i, wallet in enumerate(wallets, start=1) 
                        if wallet and wallet != 'reserved'
                    ]
                    if not participants:
                        print(f"No valid participants found in {tablename}")
                        return None
                    half = len(participants) // 2
                    if half == 0:
                        eliminated_first_round = []
                        remaining_after_round1 = participants
                    else:
                        eliminated_first_round = random.sample(participants, half)
                        remaining_after_round1 = [p for p in participants if p not in eliminated_first_round]
                    round1_results = "Round 1 results:\n\n"
                    round1_results += "*Eliminated:*\n"
                    round1_results += "\n".join([f"{wallet}" for pos, wallet in eliminated_first_round])
                    round1_results += "\n\n*Advance to next round*\n"
                    round1_results += "\n".join([wallet for pos, wallet in remaining_after_round1])
                    if remaining_after_round1:
                        winner_pos, winner = random.choice(remaining_after_round1)
                        eliminated_final_round = [wallet for pos, wallet in remaining_after_round1 if pos != winner_pos]
                        final_round_results = "Final round results:\n"
                        final_round_results += "Eliminated:\n"
                        final_round_results += "\n".join([f"{wallet}" for wallet in eliminated_final_round])
                        final_round_results += f"\n\nWinner!!{winner}"
                    else:
                        return {
                            'round1': {
                                'eliminated': [wallet for _, wallet in eliminated_first_round],
                                'remaining': [],
                                'display': round1_results
                            },
                            'final_round': {
                                'eliminated': [],
                                'winner': None,
                                'display': "No final round due to no remaining players\\."
                            }
                        }

                    return {
                        'round1': {
                            'eliminated': [wallet for _, wallet in eliminated_first_round],
                            'remaining': [wallet for _, wallet in remaining_after_round1],
                            'display': round1_results
                        },
                        'final_round': {
                            'eliminated': eliminated_final_round,
                            'winner': winner,
                            'display': final_round_results
                        }
                    }

    except Exception as e:
        print(f"Error during game execution: {e}")
        return None
    finally:
        pool.close()
        await pool.wait_closed()