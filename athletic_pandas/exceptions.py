class MissingDataException(Exception):
        def __init__(self, func, missing_fields):
            self.message = 'Method \'{}\' is missing data: {}'.format(
                    func.__name__,
                    ', '.join(missing_fields))

            super(MissingDataException, self).__init__(self.message)


class WorkoutDataFrameValidationException(Exception):
        def __init__(self, errors):
            self.message = 'Validation failed at:\n' + '\n'.join(errors)
            super(WorkoutDataFrameValidationException, self).__init__(self.message)
