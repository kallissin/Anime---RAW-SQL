class TypeKeyError(Exception):
    type_key = ['anime', 'released_date', 'seasons']

    def __init__(self, data):
        self.message = {
            "available_keys": self.type_key,
            "wrong_keys_sended": [key for key in data if key not in self.type_key]
        }
        super().__init__(self.message)