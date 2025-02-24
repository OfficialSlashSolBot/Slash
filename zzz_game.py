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

async def mega_game(tablename: str):
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
                wallets = await cursor.fetchone()
                
                if wallets:
                    participants = [
                        (i, wallet) for i, wallet in enumerate(wallets, start=1) 
                        if wallet and wallet != 'reserved'
                    ]
                    
                    if len(participants) != 32:
                        print(f"Expected 32 participants but found {len(participants)} in {tablename}")
                        return None

                    results = {}
                    current_round = participants
                    
                    for round_number in range(1, 6):
                        half = len(current_round) // 2
                        if half == 0:
                            eliminated = []
                            remaining = current_round
                        else:
                            eliminated = random.sample(current_round, half)
                            remaining = [p for p in current_round if p not in eliminated]

                        round_results = f"Round {round_number} results:\n\n"
                        round_results += f"*Eliminated:*\n"
                        round_results += "\n".join([f"{wallet}" for pos, wallet in eliminated])
                        round_results += "\n\n*Advance to next round*\n"
                        round_results += "\n".join([wallet for pos, wallet in remaining])

                        results[f"round{round_number}"] = {
                            'eliminated': [wallet for _, wallet in eliminated],
                            'remaining': [wallet for _, wallet in remaining],
                            'display': round_results
                        }

                        current_round = remaining
                        

                    return results

    except Exception as e:
        print(f"Error during game execution: {e}")
        return None
    finally:
        pool.close()
        await pool.wait_closed()