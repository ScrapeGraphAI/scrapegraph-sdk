class APIError(Exception):
    """Base exception for API errors."""

    def __init__(self, message: str, status_code: int = None):
        self.status_code = status_code
        self.message = message
        super().__init__(f"[{status_code}] {message}")
