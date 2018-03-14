class WorkoutDataFrameValidationException(Exception):
        def __init__(self, errors):
            self.message = 'Validation failed at:\n' + '\n'.join(errors)
            super(WorkoutDataFrameValidationException, self).__init__(self.message)
