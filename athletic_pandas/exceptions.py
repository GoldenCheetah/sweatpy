class MissingDataException(Exception):
        def __init__(self, func, missing_fields):
            self.message = "Method \'{}\' is missing data: {}".format(
                    func.__name__,
                    ", ".join(missing_fields))

            super(MissingDataException, self).__init__(self.message)
