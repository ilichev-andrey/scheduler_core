from database import DB


class TimetableProvider(object):
    def __init__(self, db: DB):
        self.db = db
