import httpx
from app.config import get_settings

settings = get_settings()

# Supabase REST API base URL
SUPABASE_REST_URL = f"{settings.supabase_url}/rest/v1"

def get_headers():
    return {
        "apikey": settings.supabase_key,
        "Authorization": f"Bearer {settings.supabase_key}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }


class SupabaseClient:
    def __init__(self):
        self.base_url = SUPABASE_REST_URL
        self.headers = get_headers()
    
    def table(self, table_name: str):
        return TableQuery(self.base_url, self.headers, table_name)


class TableQuery:
    def __init__(self, base_url: str, headers: dict, table_name: str):
        self.base_url = base_url
        self.headers = headers
        self.table_name = table_name
        self.url = f"{base_url}/{table_name}"
        self.params = {}
        self._select_columns = "*"
    
    def select(self, columns: str = "*"):
        self._select_columns = columns
        self.params["select"] = columns
        return self
    
    def eq(self, column: str, value):
        self.params[column] = f"eq.{value}"
        return self
    
    def execute(self):
        with httpx.Client() as client:
            response = client.get(
                self.url,
                headers=self.headers,
                params=self.params
            )
            response.raise_for_status()
            return type('Response', (), {'data': response.json()})()
    
    def insert(self, data: dict):
        with httpx.Client() as client:
            response = client.post(
                self.url,
                headers=self.headers,
                json=data
            )
            response.raise_for_status()
            return type('Response', (), {'data': response.json()})()


# Global client
supabase = SupabaseClient()


def get_db() -> SupabaseClient:
    return supabase
