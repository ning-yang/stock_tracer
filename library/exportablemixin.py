class ExportableMixin(object):
    """ExportableMixin"""

    def as_dict(self):
        """as_dict"""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        """__repr__"""
        return str(self.as_dict())
