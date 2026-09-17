import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "inventory.db"

SEED_DATA = [
    ("steel_bolts", 40, 100, 2.40),
    ("bearings", 220, 150, 5.10),
    ("gaskets", 80, 100, 1.75),
]

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            component TEXT PRIMARY_KEY,
            quantity INTEGER,
            reorder_threshold INTEGER,
            unit_cost REAL
        )
    """)
    conn.executemany(
        "INSERT OR IGNORE INTO inventory VALUES (?, ?, ?, ?)", SEED_DATA
    )
    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    print(f"DB seeded at {DB_PATH}")
