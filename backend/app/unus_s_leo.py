from flask import (
    Blueprint,request,jsonify,abort
)
import requests
from datetime import datetime
import dateutil.parser as parser
from app.util import serialize_doc
from app import mongo


def unus_sed_leo_data(address,symbol,Preferred_Safename,Email,type_id):
    records = mongo.db.symbol_url.find_one({"symbol":symbol})
    url=records['url_balance']
    if "url_transaction" in records:
        url1=records['url_transaction']
    ret=url.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       
    
    doc=url1.replace("{{address}}",''+address+'')
    response_user = requests.get(url=doc)
    res = response_user.json()       
    transactions=res['result']
    array=[]

    for transaction in transactions:
        frm=[]
        to=[]
        fee =transaction['value']
        timestamp = transaction['timeStamp']
        first_date = int(timestamp)
        dt_object = datetime.fromtimestamp(first_date)
        if "to" and "from" in transaction:
            too = transaction['to']
            fro = transaction['from']
            to.append({"to":too,"receive_amount":""})
            frm.append({"from":fro,"send_amount":(int(fee)/1000000000000000000)})
        array.append({"fee":fee,"from":frm,"to":to,"date":dt_object})
    balance = response['result']
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
                "balance":(int(balance)/1000000000000000000),
                "transactions":array,
                "amountReceived":amount_recived,
                "amountSent":amount_sent
            }},upsert=True)
    return jsonify(res)
