from eth_account import Account
from cryptography.fernet import Fernet
from backend.db import get_conn
import os

WALLET_KEY = os.getenv("WALLET_KEY")

def create_eth_wallet():
    acct = Account.create()
    return acct.address, acct.key.hex()

async def create_user_wallet(user_id: str, network: str = "Ethereum"):
    address, pk = create_eth_wallet()
    f = Fernet(WALLET_KEY.encode())
    enc_pk = f.encrypt(pk.encode()).decode()

    conn = await get_conn()
    await conn.execute("""
        INSERT INTO user_wallets (user_id, network, address, encrypted_private_key)
        VALUES ($1,$2,$3,$4)
    """, user_id, network, address, enc_pk)
    await conn.close()
    return {"user_id": user_id, "network": network, "address": address}

async def list_user_wallets(user_id: str):
    conn = await get_conn()
    rows = await conn.fetch("""
        SELECT network, address FROM user_wallets WHERE user_id=$1
    """, user_id)
    await conn.close()
    return [dict(r) for r in rows]
