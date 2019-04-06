from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate, identity
app = Flask(__name__)
app.secret_key = 'juju'
api = Api(app)
jwt = JWT(app, authenticate, identity)

items = []
class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type = float,
        required = True,
        help = "This field cannot be blank!")

    #@app.route('/student/<string:name>') save us a bit of hassle
    @jwt_required() #before deploy get method, we need to be authenticated
    def get(self, name):
        item = next(filter(lambda x: x['name'] == name ,items), None)
        return {'item': item}, 200 if item else 404


    def post(self, name):
        if next(filter(lambda x: x['name'] == name ,items), None):
            return {'message':"The item with name '{}' has already existed".format(name)}, 400
        data = Item.parser.parse_args()
        item = {'name':name, 'price':data['price']}
        items.append(item)
        return item, 201

    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message':'The item deleted'}

    def put(self, name):
        data = Item.parser.parse_args()
        item = next(filter(lambda x: x['name'] == name, items), None)
        if not item:
            item = {'name':name, 'price':data['price']}
            items.append(item)
        else:
            item.update(data)
        return item

class Itemlist(Resource):
    def get(self):
        return {'items':items}
api.add_resource(Item, '/item/<string:name>')   #http://127.0.0.1:500/student/Mona
api.add_resource(Itemlist,'/items')
app.run(port=5000, debug = True)
