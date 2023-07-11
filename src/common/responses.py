class MainResponse:
    def __init__(self, status, data=None, details=None):
        self.status = status
        self.data = data
        self.details = details

    def get_response(self):
        return {
            "status": self.status,
            "data": self.data,
            "details": self.details,
        }
