class DoubleType(float):
    def __new__(cls, *args, **kwargs):
        return super(DoubleType, cls).__new__(cls, args[0])

