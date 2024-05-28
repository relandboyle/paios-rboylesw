from uuid import uuid4
import backend.db as db
from backend.encryption import Encryption
from paths import db_path

class ConfigManager:
    def __init__(self, tenant=None):
        self.encryption = Encryption()
        self.tenant = tenant
        db.init_db()

    # CRUD operations
    # Note: Creating a new config item without specifying a key is unusual; use update_config_item instead.
    async def create_config_item(self, value):
        key = str(uuid4())
        encrypted_value = self.encryption.encrypt_value(value)
        print(f"ConfigManager: create_config_item {encrypted_value}")
        query = 'INSERT INTO config (key, value) VALUES (?, ?)'
        await db.execute_query(query, (key, encrypted_value))
        return key
    
    async def retrieve_config_item(self, key):
        query = 'SELECT value FROM config WHERE key = ?'
        result = await db.execute_query(query, (key,))
        if result:
            encrypted_value = result[0][0]
            return self.encryption.decrypt_value(encrypted_value)
        return None

    async def update_config_item(self, key, value):
        encrypted_value = self.encryption.encrypt_value(value)
        query = 'INSERT OR REPLACE INTO config (key, value) VALUES (?, ?)'
        await db.execute_query(query, (key, encrypted_value))

    async def delete_config_item(self, key):
        query = 'DELETE FROM config WHERE key = ?'
        await db.execute_query(query, (key,))
