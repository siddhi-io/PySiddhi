class LongType(int):
    def __new__(cls, *args, **kwargs):
        return super(LongType, cls).__new__(cls, args[0])

