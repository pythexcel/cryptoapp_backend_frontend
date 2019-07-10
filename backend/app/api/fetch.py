from flask import (
    Blueprint,request,jsonify,abort
)
import requests
from datetime import datetime
from app.util import serialize_doc
from app.btc import btc_data
from app.eth import eth_data
from app.binance_chain import b_chain_data
from app.bitcoin_cash import btc_cash_data
from app.bitcoin_SV import bitcoin_svs_data
from app.litecoin import ltc_data
from app.tether import tether_data
from app.xtz import xtz_data
from app.qtum import qtum_data
from app.tron import tron_data
from app.mkr import mkr_data
from app.btt import btt_data
from app.vet import vet_data
from app.cro import cro_data
from app.xrp import xrp_data
from app.eos import eos_data
from app.dash import dash_data
from app.usdc import usdc_data
from app.ont import ont_data
from app.bat  import bat_data
import mysql.connector
from app.zcash import zcash_data
from app.btcgold import btc_gold_data
from app.iota import iota_data
from app.unus_s_leo import unus_sed_leo_data
bp = Blueprint('fetch', __name__, url_prefix='/')
from app import mongo

mydb = mysql.connector.connect( user="sql12298045" , password="6EzUA5zMDe", host="sql12.freemysqlhosting.net", database="sql12298045")
mycursor=mydb.cursor()
    
#Main Api which is using a function for return details by post address and symbol
@bp.route("/transaction",methods=["POST"])
def main():
    if not request.json:
        abort(500)
    address=request.json.get("address", None)    
    symbol=request.json.get("symbol", None)
    Preferred_Safename=request.json.get("Preferred_Safename", None)
    Email=request.json.get("Email","")
    type_id=request.json.get("type_id","")
    mycursor.execute('SELECT * FROM sws_whitelist WHERE requested="'+str(Preferred_Safename)+'"')
    result = mycursor.fetchall()
    if result:
        if symbol == "BTC":
            currency = btc_data(address,symbol,Preferred_Safename,Email,type_id)
            return currency
        if symbol == "ETH":
            currency = eth_data(address,symbol,Preferred_Safename,Email,type_id)
            return currency
        
        if symbol == "LTC":
            currency = ltc_data(address,symbol,Preferred_Safename,Email,type_id)
            return currency
        if symbol == "BTC_CASH":
            currency = btc_cash_data(address,symbol,Preferred_Safename,Email,type_id)
            return currency
        if symbol == "BINANCE_COIN":
            currency = b_chain_data(address,symbol,Preferred_Safename,Email,type_id)
            return currency
        if symbol == "BTC_SV":
            currency = bitcoin_svs_data(address,symbol,Preferred_Safename,Email,type_id)
            return currency
        if symbol == "TETHER":
            currency = tether_data(address,symbol,Preferred_Safename,Email,type_id)
            return currency

        if symbol == "TRON":
            currency = tron_data(address,symbol,Preferred_Safename,Email,type_id)
            return currency

        if symbol == "UNUS_SED_LEO":
            currency = unus_sed_leo_data(address,symbol,Preferred_Safename,Email,type_id)
            return currency

        if symbol == "IOTA":
            currency = iota_data(address,symbol,Preferred_Safename,Email,type_id)
            return currency

        if symbol == "Z_CASH":
            currency = zcash_data(address,symbol,Preferred_Safename,Email,type_id)
            return currency
        
        if symbol == "ONT":
            currency = ont_data(address,symbol,Preferred_Safename,Email,type_id)
            return currency

        if symbol == "XTZ":
            currency = xtz_data(address,symbol,Preferred_Safename,Email,type_id)
            return currency

        if symbol == "BTC_GOLD":
            currency = btc_gold_data(address,symbol,Preferred_Safename,Email,type_id)
            return currency

        if symbol == "QTUM":
            currency = qtum_data(address,symbol,Preferred_Safename,Email,type_id)
            return currency

        if symbol == "MKR":
            currency = mkr_data(address,symbol,Preferred_Safename,Email,type_id)
            return currency

        if symbol == "VET":
            currency = vet_data(address,symbol,Preferred_Safename,Email,type_id)
            return currency

        if symbol == "CRO":
            currency = cro_data(address,symbol,Preferred_Safename,Email,type_id)
            return currency

        if symbol == "BAT":
            currency = bat_data(address,symbol,Preferred_Safename,Email,type_id)
            return currency

        if symbol == "USDC":
            currency = usdc_data(address,symbol,Preferred_Safename,Email,type_id)
            return currency

        if symbol == "BTT":
            currency = btt_data(address,symbol,Preferred_Safename,Email,type_id)
            return currency

        if symbol == "XRP":
            currency = xrp_data(address,symbol,Preferred_Safename,Email,type_id)
            return currency

        if symbol == "DASH":
            currency = dash_data(address,symbol,Preferred_Safename,Email,type_id)
            return currency

        if symbol == "EOS":
            currency = eos_data(address,symbol,Preferred_Safename,Email,type_id)
            return currency

    else:
        return jsonify({"msg": "You are not a registered user"}),203


@bp.route("/currency_symbol",methods=['GET'])
def currency_symbol():
    urls = mongo.db.symbol_url.find({})
    urls = [serialize_doc(doc) for doc in urls]
    return jsonify(urls), 200


@bp.route("/local_transaction/<string:address>",methods=['GET'])
def local_transaction(address):
    docs = mongo.db.sws_history.find({"address":address})
    docs = [serialize_doc(doc) for doc in docs]
    return jsonify(docs), 200

    






    