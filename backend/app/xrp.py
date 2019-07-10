from flask import (
    Blueprint,request,jsonify,abort
)
import requests
from datetime import datetime
from app.util import serialize_doc
from app import mongo


def xrp_data(address,symbol,Preferred_Safename,Email,type_id):
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
    transactions=res['transactions']
    array=[]
    
    for transaction in transactions:
        frm=[]
        to=[]
        fro = transaction['Account']
        if "Destination" in transaction:
            too = transaction['Destination']
        else:
            too=""
        fee = transaction['Fee']
        date = transaction['date']
        frm.append({"from":fro,"send_amount":""})
        to.append({"to":too,"receive_amount":""})
        array.append({"fee":fee,"from":frm,"to":to,"date":date})
    
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

    balance=response['initial_balance']
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
    return jsonify(res)
