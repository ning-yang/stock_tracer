import json
class ExportableMixin(object):
    """ExportableMixin"""

    def as_dict(self):
        """as_dict"""
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}

    def __repr__(self):
        """__repr__"""
        return json.dumps(self.as_dict())
