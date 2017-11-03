from unittest import mock
import json
from app import get_response_for_app, get_json_for_app, get_reviews_for_app

upsell_path = './mock_product_upsell_reviews.json'
builder_path = './mock_product_builder_reviews.json'


class MockResponse():
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data


def mocked_requests_get(*args, **kwargs):
    upsell_url = 'https://apps.shopify.com/product-upsell/reviews.json'
    builder_url = 'https://apps.shopify.com/product-builder/reviews.json'

    if args[0] == upsell_url:
        with open(upsell_path, 'r') as file:
            data = json.load(file)
        return MockResponse(data, 200)
    elif args[0] == builder_url:
        with open(builder_path, 'r') as file:
            data = json.load(file)
        return MockResponse(data, 200)

    return MockResponse(None, 404)


def mocked_get_response_for_app(name):
    upsell_name = 'product-upsell'
    builder_name = 'product-builder'

    if name == upsell_name:
        with open(upsell_path, 'r') as file:
            data = json.load(file)
        return MockResponse(data, 200)
    elif name == builder_name:
        with open(builder_path, 'r') as file:
            data = json.load(file)
        return MockResponse(data, 200)

    return MockResponse(None, 404)


def mocked_get_json_for_app(name):
    upsell_name = 'product-upsell'
    builder_name = 'product-builder'
    data = {}
    if name == upsell_name:
        with open(upsell_path, 'r') as file:
            data = json.load(file)
    elif name == builder_name:
        with open(builder_path, 'r') as file:
            data = json.load(file)

    return data


@mock.patch('requests.get', side_effect=mocked_requests_get)
def test_get_response_returns_something(self):
    response = get_response_for_app("product-upsell")
    assert response.status_code == 200


@mock.patch('requests.get', side_effect=mocked_requests_get)
def test_get_response_for_product_upsell_returns_correct_number_of_reviews(self):
    response = get_response_for_app("product-upsell")
    json = response.json()
    reviews = json['reviews']
    assert len(reviews) == 948


@mock.patch('requests.get', side_effect=mocked_requests_get)
def test_get_response_for_product_builder_returns_correct_number_of_reviews(self):
    response = get_response_for_app("product-builder")
    json = response.json()
    reviews = json['reviews']
    assert len(reviews) == 146


@mock.patch('app.get_response_for_app', side_effect=mocked_get_response_for_app)
def test_get_json_for_app_product_builder(self):
    json = get_json_for_app("product-builder")
    reviews = json['reviews']
    assert len(reviews) == 146


@mock.patch('app.get_response_for_app', side_effect=mocked_get_response_for_app)
def test_get_json_for_app_product_upsell(self):
    json = get_json_for_app("product-upsell")
    reviews = json['reviews']
    assert len(reviews) == 948


@mock.patch('app.get_response_for_app', side_effect=mocked_get_response_for_app)
def test_get_reviews_for_app_product_builder(self):
    reviews = get_reviews_for_app("product-builder")
    assert len(reviews) == 146


@mock.patch('app.get_response_for_app', side_effect=mocked_get_response_for_app)
def test_get_reviews_for_app_product_upsell(self):
    reviews = get_reviews_for_app("product-upsell")
    assert len(reviews) == 948
