from flask import Flask
from flask import request
from flask import jsonify
from flask import Response
from database import session
from models import Address
from urllib import parse

app = Flask(__name__)


@app.route('/cj/secluded_place')
def cj_secluded_place():
    address = parse.unquote(request.args.get('address')).replace(' ', '')
    result = session.query(Address).filter(Address.trimmed_address == address).first()

    if result is not None:
        result_dict = {
            'zipcode': result.zipcode,
            'address': result.address,
            'additional_fee': result.add_fee,
        }
        return jsonify(result_dict)
    else:
        return Response(status=404)
