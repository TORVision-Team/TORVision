import sqlite3
from utils.config import DB_NAME

def get_connection():
    return sqlite3.connect(DB_NAME)

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tor_nodes (
        fingerprint TEXT PRIMARY KEY,
        nickname TEXT,
        ip TEXT,
        or_port INTEGER,
        dir_port INTEGER,
        country TEXT,
        bandwidth INTEGER,
        last_seen TEXT
    )
    """)

    conn.commit()
    conn.close()

def save_node(node):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR REPLACE INTO tor_nodes
    (fingerprint, nickname, ip, or_port, dir_port, country, bandwidth, last_seen)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        node["fingerprint"],
        node.get("nickname"),
        node.get("ip"),
        node.get("or_port"),
        node.get("dir_port"),
        node.get("country"),
        node.get("bandwidth"),
        node.get("last_seen")
    ))

    conn.commit()
    conn.close()
