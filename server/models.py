from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin


metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class Customer(db.Model, SerializerMixin):
    __tablename__ = 'customers'
    # Columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    # Relationships
    reviews = db.relationship("Review", back_populates="customer")
    # Association proxy
    items = association_proxy("reviews", "item")
    # Serialization
    serialize_rules = ("reviews", "-reviews.customer")

    # Method
    def __repr__(self):
        return f'<Customer {self.id}, {self.name}>'


class Item(db.Model, SerializerMixin):
    __tablename__ = 'items'
    #Columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)
    # Relationsihps
    reviews = db.relationship("Review", back_populates="item")
    # Serialization
    serialize_rules = ("reviews", "-reviews.item")

    # Method
    def __repr__(self):
        return f'<Item {self.id}, {self.name}, {self.price}>'

class Review(db.Model, SerializerMixin):
    __tablename__ = "reviews"
    # Columns
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String)
    # Foreign Keys
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"))
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"))
    # Relationships
    customer = db.relationship("Customer", back_populates="reviews")
    item = db.relationship("Item", back_populates="reviews")
    # Serialization
    serialize_rules = ("-customer.reviews", "-item.reviews")
