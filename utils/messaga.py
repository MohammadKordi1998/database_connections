class Message:
    def __init__(self, message, status):
        self.message = message
        self.status = status

    def result_message(self):
        message = dict(
            message=self.message,
            status=self.status
        )
        return message
