from webapp.db import DB


class Defects(DB.Model):
    """Defects model"""
    id = DB.Column(DB.Integer, primary_key=True)
    image = DB.Column(DB.String(128), nullable=True)
    object_class = DB.Column(DB.Integer, nullable=False)
    object_label = DB.Column(DB.String(64), nullable=False)

    def __repr__(self):
        """repr method"""
        return "<Defects {}>".format(self.id)


class CarCounts(DB.Model):
    """CarCounts model"""
    id = DB.Column(DB.Integer, primary_key=True)
    image = DB.Column(DB.String(128), nullable=True)
    car_count = DB.Column(DB.Integer, nullable=False)
    ratio = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        """repr method"""
        return "<CarCounts {}>".format(self.id)
