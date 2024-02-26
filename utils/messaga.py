class Message:
    def __init__(self, text_message, status):
        self.text_message = text_message
        self.status = status

    def result_message(self):
        message = dict(
            message=self.text_message,
            status=self.status
        )
        return message
