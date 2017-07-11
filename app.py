from flask import Flask
from flask import request
from flask import jsonify
from flask import Response
from flask_cors import CORS
from database import session
from models import Address
from urllib import parse
from utils import replace_if_short_address

app = Flask(__name__)
CORS(app)


@app.route('/cj/secluded_place')
def cj_secluded_place():
    address_args = request.args.get('address')
    if address_args:
        trimmed_address = parse.unquote(address_args).replace(' ', '')
        address = replace_if_short_address(trimmed_address)
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
    else:
        return Response(status=400)


if __name__ == '__main__':
    app.run(debug=True)
