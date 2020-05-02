from app import db


class Producer(db.Model):
    __tablename__ = 'producer'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    created = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

    def create(self, session, **kwargs):
        new = self.__class__(name=kwargs['name'])
        session.add(new)
        return new

    def fetch(self, session, _id):
        return session.query(self.__class__).filter_by(id=_id).first()

    def fetch_all(self, session):
        return session.query(self.__class__).filter_by().all()

    def delete(self, session, _id):
        model = session.query(self.__class__).filter_by(id=_id).first()
        if not model:
            return False
        session.delete(model)
        return True


class Episode(db.Model):
    __tablename__ = 'episode'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    producer_id = db.Column(db.Integer, db.ForeignKey('producer.id'))
    name = db.Column(db.String(100))
    url = db.Column(db.Text)
    created = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

    def create(self, session, **kwargs):
        new = self.__class__(
            producer_id=kwargs['producer_id'],
            name=kwargs['name'],
            url=kwargs['url']
        )
        session.add(new)
        return new

    def fetch(self, session, _id):
        return session.query(self.__class__).filter_by(id=_id).first()

    def fetch_all(self, session):
        return session.query(self.__class__).filter_by().all()

    def delete(self, session, parent_id, _id):
        model = session.query(self.__class__).filter_by(id=_id, producer_id=parent_id).first()
        if not model:
            return False
        session.delete(model)
        return True

