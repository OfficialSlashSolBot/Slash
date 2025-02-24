import time
import asyncio
import math
import asyncio
from dotenv import load_dotenv
from balance import get_balance
from solders.pubkey import Pubkey
from solana.rpc.api import Client
from solders.keypair import Keypair
from base58 import b58decode, b58encode
from solana.transaction import Transaction
from solders.system_program import TransferParams, transfer

solana_client = Client("https://api.devnet.solana.com")

async def confirm_transaction(signature, retries=4, delay=5):

    for _ in range(retries):

        transaction_info = solana_client.get_transaction(signature)
        if transaction_info and transaction_info.value:  # Transaction found
        
            return True

        await asyncio.sleep(delay)

    return False

# SEND ENTRY FEE
async def send_sol(to_wallet,user_wallet,sk,amount):

    keypair = b58decode(sk)
    private_key = keypair [:32]
    public_key = keypair[32:]
    wallet_address = b58encode(public_key).decode()
    from_pubkey = Pubkey(b58decode(wallet_address))
    to_pubkey = Pubkey(b58decode(to_wallet))
    from_pubkey_balance = await get_balance(user_wallet)
    balance = from_pubkey_balance*10**9
    amount_lamps = int(amount*10**9)
    
    try:
        transfer_parameters = TransferParams(
            from_pubkey=from_pubkey,
            to_pubkey=to_pubkey,
            lamports=amount_lamps
        )

        sol_transfer = transfer(transfer_parameters)
        transaction = Transaction().add(sol_transfer)

        transaction_result = solana_client.send_transaction(transaction, Keypair.from_seed(private_key))
        signature = transaction_result.value
    
        if not signature:
            return {"success": False, "error": "No signature received"}
        await asyncio.sleep(5)
        # Confirm transaction
        is_confirmed = await confirm_transaction(signature)
        if is_confirmed:

            return {"success": True, "result": signature}
        else:
            return {"success": False, "error": "Transaction not confirmed"}

    except Exception as e:
        print(f"Error sending SOL: {e}")
        return {"success": False, "error": str(e)}

# SEND EXPRESS PRIZE
async def send_sol_e(winner_wallet,table_wallet,fee_wallet,sk,entry_fee):

    keypair = b58decode(sk)
    private_key = keypair [:32]
    wallet_address = table_wallet
    from_pubkey = Pubkey(b58decode(wallet_address))
    to_pubkey1 = Pubkey(b58decode(winner_wallet))
    to_pubkey2 = Pubkey(b58decode(fee_wallet))

    try:
        winner_amount = entry_fee*4*0.9
        fee_amount = entry_fee*4*0.098
        winner_lamports = int(winner_amount*10**9)
        fee_lamports = int(fee_amount*10**9)

        transfer_parameters1 = TransferParams(
            from_pubkey=from_pubkey,
            to_pubkey=to_pubkey1,
            lamports=int(winner_lamports) 
        )

        transfer_parameters2 = TransferParams(
            from_pubkey=from_pubkey,
            to_pubkey=to_pubkey2,
            lamports=int(fee_lamports) 
        )

        sol_transfer1 = transfer(transfer_parameters1)
        sol_transfer2 = transfer(transfer_parameters2)
        transaction = Transaction().add(sol_transfer1)
        transaction.add(sol_transfer2)
        transaction_result = solana_client.send_transaction(transaction, Keypair.from_seed(private_key))
        signature = transaction_result.value
    
        if not signature:
            return {"success": False, "error": "No signature received"}
        await asyncio.sleep(5)
        # Confirm transaction
        is_confirmed = await confirm_transaction(signature)
        if is_confirmed:

            return {"success": True, "result": signature}
        else:
            return {"success": False, "error": "Transaction not confirmed"}

    except Exception as e:
        print(f"Error sending SOL: {e}")
        return {"success": False, "error": str(e)}
    
# SEND MEGA PRIZE
async def send_sol_m(winner_wallet,table_wallet,fee_wallet,second,third,fourth,fifth,sixth,seventh,eighth,sk,entry_fee):

    keypair = b58decode(sk)
    private_key = keypair [:32]
    wallet_address = table_wallet
    from_pubkey = Pubkey(b58decode(wallet_address))
    to_pubkey1 = Pubkey(b58decode(winner_wallet))
    to_pubkey2 = Pubkey(b58decode(fee_wallet))
    to_pubkey3 = Pubkey(b58decode(second))
    to_pubkey4 = Pubkey(b58decode(third))
    to_pubkey5 = Pubkey(b58decode(fourth))
    to_pubkey6 = Pubkey(b58decode(fifth))
    to_pubkey7 = Pubkey(b58decode(sixth))
    to_pubkey8 = Pubkey(b58decode(seventh))
    to_pubkey9 = Pubkey(b58decode(eighth))

    try:
        winner_amount = entry_fee * 14.3
        winner_lamports = int(winner_amount*10**9)
        second_amount = entry_fee*4.3 
        second_lamports = int(second_amount*10**9)
        third_forth_amount = entry_fee*2 
        third_forth_lamports = int(third_forth_amount*10**9)
        fifth_eighth_amount = entry_fee*1.55
        fifth_eighth_lamports = int(fifth_eighth_amount*10**9)
        fee_amount = entry_fee*32*0.098
        fee_lamports = int(fee_amount*10**9)

        transfer_parameters1 = TransferParams(
            from_pubkey=from_pubkey,
            to_pubkey=to_pubkey1,
            lamports=int(winner_lamports) 
        )

        transfer_parameters2 = TransferParams(
            from_pubkey=from_pubkey,
            to_pubkey=to_pubkey2,
            lamports=int(fee_lamports) 
        )

        transfer_parameters3 = TransferParams(
            from_pubkey=from_pubkey,
            to_pubkey=to_pubkey3,
            lamports=int(second_lamports) 
        )

        transfer_parameters4 = TransferParams(
            from_pubkey=from_pubkey,
            to_pubkey=to_pubkey4,
            lamports=int(third_forth_lamports) 
        )

        transfer_parameters5 = TransferParams(
            from_pubkey=from_pubkey,
            to_pubkey=to_pubkey5,
            lamports=int(third_forth_lamports) 
        )

        transfer_parameters6 = TransferParams(
            from_pubkey=from_pubkey,
            to_pubkey=to_pubkey6,
            lamports=int(fifth_eighth_lamports) 
        )

        transfer_parameters7 = TransferParams(
            from_pubkey=from_pubkey,
            to_pubkey=to_pubkey7,
            lamports=int(fifth_eighth_lamports) 
        )
        
        transfer_parameters8 = TransferParams(
            from_pubkey=from_pubkey,
            to_pubkey=to_pubkey8,
            lamports=int(fifth_eighth_lamports) 
        )
        
        transfer_parameters9 = TransferParams(
            from_pubkey=from_pubkey,
            to_pubkey=to_pubkey9,
            lamports=int(fifth_eighth_lamports) 
        )

        sol_transfer1 = transfer(transfer_parameters1)
        sol_transfer2 = transfer(transfer_parameters2)
        sol_transfer3 = transfer(transfer_parameters3)
        sol_transfer4 = transfer(transfer_parameters4)
        sol_transfer5 = transfer(transfer_parameters5)
        sol_transfer6 = transfer(transfer_parameters6)
        sol_transfer7 = transfer(transfer_parameters7)
        sol_transfer8 = transfer(transfer_parameters8)
        sol_transfer9 = transfer(transfer_parameters9)
        transaction = Transaction().add(sol_transfer1)
        transaction.add(sol_transfer2)
        transaction.add(sol_transfer3)
        transaction.add(sol_transfer4)
        transaction.add(sol_transfer5)
        transaction.add(sol_transfer6)
        transaction.add(sol_transfer7)
        transaction.add(sol_transfer8)
        transaction.add(sol_transfer9)
        transaction_result = solana_client.send_transaction(transaction, Keypair.from_seed(private_key))
        signature = transaction_result.value
    
        if not signature:
            return {"success": False, "error": "No signature received"}
        await asyncio.sleep(5)
        # Confirm transaction
        is_confirmed = await confirm_transaction(signature)
        if is_confirmed:

            return {"success": True, "result": signature}
        else:
            return {"success": False, "error": "Transaction not confirmed"}

    except Exception as e:
        print(f"Error sending SOL: {e}")
        return {"success": False, "error": str(e)}

# SEND WITH LEVEL 1 REFERRAL
async def send_sol_ref_1(prize_wallet,fee_wallet,ref_wallet1,bbb_wallet,rev_wallet,sk):

    keypair = b58decode(sk)
    private_key = keypair [:32]
    public_key = keypair[32:]
    wallet_address = b58encode(public_key).decode()
    from_pubkey = Pubkey(b58decode(wallet_address))
    to_pubkey1 = Pubkey(b58decode(prize_wallet))
    to_pubkey2 = Pubkey(b58decode(fee_wallet))
    to_pubkey3 = Pubkey(b58decode(ref_wallet1))
    to_pubkey4 = Pubkey(b58decode(bbb_wallet))
    to_pubkey5 = Pubkey(b58decode(rev_wallet))

    try:
          
        deposit_amount = 30000000 / 100 # 0.3 sol laports in %

        amount_payable = deposit_amount*55
        fee_payable = deposit_amount*27
        ref1amount = deposit_amount*8
        bbb_payable = deposit_amount*5
        rev_payable = deposit_amount*5

        transfer_parameters1 = TransferParams(
            from_pubkey=from_pubkey,
            to_pubkey=to_pubkey1,
            lamports=int(amount_payable) 
        )

        transfer_parameters2 = TransferParams(
            from_pubkey=from_pubkey,
            to_pubkey=to_pubkey2,
            lamports=int(fee_payable) 
        )

        transfer_parameters3 = TransferParams(
            from_pubkey=from_pubkey,
            to_pubkey=to_pubkey3,
            lamports=int(ref1amount) 
        )

        transfer_parameters4 = TransferParams(
            from_pubkey=from_pubkey,
            to_pubkey=to_pubkey4,
            lamports=int(bbb_payable) 
        )

        transfer_parameters5 = TransferParams(
            from_pubkey=from_pubkey,
            to_pubkey=to_pubkey5,
            lamports=int(rev_payable) 
        )

        sol_transfer1 = transfer(transfer_parameters1)
        sol_transfer2 = transfer(transfer_parameters2)
        sol_transfer3 = transfer(transfer_parameters3)
        sol_transfer4 = transfer(transfer_parameters4)
        sol_transfer5 = transfer(transfer_parameters5)
        transaction = Transaction().add(sol_transfer1)
        transaction.add(sol_transfer2)
        transaction.add(sol_transfer3)
        transaction.add(sol_transfer4)
        transaction.add(sol_transfer5)
        transaction_result = solana_client.send_transaction(transaction, Keypair.from_seed(private_key))

        return {"success": True, "result": transaction_result}

    except Exception as e:
        print(f"Error sending SOL: {e}")
        return {"success": False, "error": str(e)}
