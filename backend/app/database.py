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


class Response:
    def __init__(self, data):
        self.data = data


class TableQuery:
    def __init__(self, base_url: str, headers: dict, table_name: str):
        self.base_url = base_url
        self.headers = headers.copy()
        self.table_name = table_name
        self.url = f"{base_url}/{table_name}"
        self._filters = []
        self._select_columns = "*"
        self._data_to_insert = None
    
    def select(self, columns: str = "*"):
        self._select_columns = columns
        return self
    
    def eq(self, column: str, value):
        self._filters.append(f"{column}=eq.{value}")
        return self
    
    def insert(self, data: dict):
        self._data_to_insert = data
        return self
    
    def execute(self):
        try:
            with httpx.Client(timeout=30.0) as client:
                if self._data_to_insert is not None:
                    # INSERT operation
                    response = client.post(
                        self.url,
                        headers=self.headers,
                        json=self._data_to_insert
                    )
                    response.raise_for_status()
                    data = response.json()
                    return Response(data if isinstance(data, list) else [data])
                else:
                    # SELECT operation
                    params = {"select": self._select_columns}
                    
                    # Build filter query string
                    if self._filters:
                        # Supabase uses query params for filters
                        for f in self._filters:
                            col, val = f.split("=", 1)
                            params[col] = val
                    
                    response = client.get(
                        self.url,
                        headers=self.headers,
                        params=params
                    )
                    response.raise_for_status()
                    return Response(response.json())
        except httpx.HTTPStatusError as e:
            print(f"HTTP Error: {e.response.status_code} - {e.response.text}")
            return Response([])
        except Exception as e:
            print(f"Database error: {str(e)}")
            return Response([])


class SupabaseClient:
    def __init__(self):
        self.base_url = SUPABASE_REST_URL
        self.headers = get_headers()
    
    def table(self, table_name: str):
        return TableQuery(self.base_url, self.headers, table_name)


# Create client lazily to avoid startup errors
_supabase = None


def get_db() -> SupabaseClient:
    global _supabase
    if _supabase is None:
        _supabase = SupabaseClient()
    return _supabase

