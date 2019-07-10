
from flask import (
    Blueprint,request,jsonify,abort
)
import requests
from datetime import datetime
from app.util import serialize_doc
import dateutil.parser as parser
from app import mongo


def tron_data(address,symbol,Preferred_Safename,Email,type_id):
    records = mongo.db.symbol_url.find_one({"symbol":symbol})
    url=records['url_balance']
    ret=url.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()
    if "url_transaction" in records:
        url1=records['url_transaction']
    doc=url1.replace("{{address}}",''+address+'')
    response_user = requests.get(url=doc)
    res = response_user.json()       
    transactions = res['data']
    
    array=[]
    
    for transaction in transactions:
        to=[]
        frm=[]
        fee =transaction['fee']
        timestamp = transaction['timestamp']
        conver_d =timestamp/1000.0
        fro = transaction['ownerAddress']
        too = transaction['toAddress']
        to.append({"to":too,"receive_amount":""})
        frm.append({"from":fro,"send_amount":""})
        dt_object = datetime.fromtimestamp(conver_d)
        array.append({"fee":fee,"from":frm,"to":to,"date":dt_object})
    
    balance = response['balance']
    amount_recived =""
    amount_sent =""

    ret = mongo.db.address.update({
            "address":address            
        },{
        "$set":{
                "address":address,
                "symbol":symbol,
                "type_id":type_id,
                "Preferred_Safename":Preferred_Safename,
                "Email":Email
            }},upsert=True)

    ret = mongo.db.address.find_one({
        "address":address
    })
    _id=ret['_id']

    ret = mongo.db.sws_history.update({
        "address":address            
    },{
        "$set":{
                "record_id":str(_id),    
                "address":address,
                "symbol":symbol,
                "type_id":type_id,
                "Preferred_Safename":Preferred_Safename,
                "balance":(balance/1000000),
                "transactions":array,
                "amountReceived":amount_recived,
                "amountSent":amount_sent
            }},upsert=True)
    return jsonify(res)
