import requests
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from dateutil.parser import parse


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///review_manager.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


admin = Admin(app, name="Review Manager", template_mode='bootstrap3', url='/')


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    app = db.Column(db.String(255))
    author = db.Column(db.String(255), index=True)
    body = db.Column(db.Text())
    created_at = db.Column(db.DateTime())
    shop_domain = db.Column(db.String(255), index=True)
    shop_name = db.Column(db.String(255), index=True)
    star_rating = db.Column(db.Integer)


class ReviewModelView(ModelView):
    can_view_details = True
    can_create = False
    can_delete = False
    can_edit = False
    column_searchable_list = ['app', 'author', 'shop_domain', 'shop_name']
    column_filters = ['app', 'author', 'shop_domain', 'shop_name', 'star_rating']

admin.add_view(ReviewModelView(Review, db.session))


def get_response_for_app(app_name):
    """requets response from shoify reviews endpoints for given app and returns that request"""
    return requests.get("https://apps.shopify.com/{}/reviews.json".format(app_name))


# TO DO - Add error handeling
def get_json_for_app(app_name):
    """requets response from shoify reviews endpoints for given app and returns the json for that app"""
    response = get_response_for_app(app_name)
    json = response.json()
    return json


def get_reviews_for_app(app_name):
    """requets response from shoify reviews endpoitn for a given app and returns an array containing all reivews"""
    json = get_json_for_app(app_name)
    reviews = json['reviews']
    return reviews

@app.route('/refresh_reviews')
def refresh_reviews():
    Review.query.delete()
    apps = ['product-upsell', 'product-options', 'recurring-orders', 'social-triggers', 'product-discount', 'product-builder', 'multi-currency',
    'quantity-breaks', 'the-motivator', 'quickbooks-online', 'customer-pricing', 'product-bundles', 'store-locator', 'loyalty-points-by-bold', 
    'xero', 'the-bold-brain', 'recurring-memberships', 'returns-manager']
    for app in apps:
        reviews = get_reviews_for_app(app)
        for review in reviews:
            new_review = Review(app=app, author=review['author'], body=review['body'], created_at=parse(review['created_at']),
                shop_domain=review['shop_domain'], shop_name=review['shop_name'], star_rating=review['star_rating'])
            db.session.add(new_review)
            db.session.commit()

    return "reviews refreshed"

db.create_all()

if __name__ == '__main__':
    app.run()
