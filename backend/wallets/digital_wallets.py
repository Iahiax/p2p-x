from eth_account import Account
from cryptography.fernet import Fernet
from backend.db import get_conn
import os

WALLET_KEY = os.getenv("WALLET_KEY")  # يجب أن يكون 32 بايت قوي جدًا
fernet = Fernet(WALLET_KEY.encode())

def generate_wallet():
    acct = Account.create()
    return acct.address, acct.key.hex()

async def create_user_wallet(user_id: str, network: str = "Ethereum"):
    address, pk = generate_wallet()
    encrypted_pk = fernet.encrypt(pk.encode()).decode()

    conn = await get_conn()
    await conn.execute("""
        INSERT INTO user_wallets (user_id, network, address, encrypted_private_key)
        VALUES ($1,$2,$3,$4)
    """, user_id, network, address, encrypted_pk)
    await conn.close()

async def list_user_wallets(user_id: str):
    conn = await get_conn()
    rows = await conn.fetch("""
        SELECT network, address FROM user_wallets WHERE user_id=$1
    """, user_id)
    await conn.close()
    return [dict(r) for r in rows]
