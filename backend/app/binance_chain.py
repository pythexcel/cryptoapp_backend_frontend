from flask import (
    Blueprint,request,jsonify,abort
)
import requests
from datetime import datetime
from app.util import serialize_doc
from app import mongo


def b_chain_data(address,symbol,Preferred_Safename,Email,type_id):
    records = mongo.db.symbol_url.find_one({"symbol":symbol})
    url=records['url_balance']
    if "url_transaction" in records:
        url1=records['url_transaction']
    ret=url.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       

    bln_detail=response['matchData']
    balances = bln_detail['balance']

    doc=url1.replace("{{address}}",''+address+'')
    response_user = requests.get(url=doc)
    res = response_user.json()       
    
    transactions=res['txArray']
    array=[]

    for transaction in transactions:
        frm=[]
        to=[]
        if "value" in transaction:
            fee =transaction['txFee']
            timestamp = transaction['timeStamp']
            conver_d =timestamp/1000.0
            dt_object = datetime.fromtimestamp(conver_d)
            fromAddr = transaction['fromAddr']
            value = transaction['value']
            frm.append({"from":fromAddr,"send_amount":value})
            array.append({"fee":fee,"from":frm,"to":to,"date":dt_object})
     
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
    for balan in balances:
        sym=balan['mappedAsset']
        if sym =="BNB":
            balance = balan['free']
            amount_recived =""
            amount_sent =""
            ret = mongo.db.sws_history.update({
            "address":address            
            },{
            "$set":{
                    "record_id":str(_id),    
                    "address":address,
                    "symbol":symbol,
                    "type_id":type_id,
                    "Preferred_Safename":Preferred_Safename,
                    "balance":balance,
                    "transactions":array,
                    "amountReceived":amount_recived,
                    "amountSent":amount_sent
                }},upsert=True)
    return jsonify(transactions)
