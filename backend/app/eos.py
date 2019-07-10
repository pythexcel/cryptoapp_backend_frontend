from flask import (
    Blueprint,request,jsonify,abort
)
import requests
from datetime import datetime
from app.util import serialize_doc
from app import mongo


def eos_data(address,symbol,Preferred_Safename,Email,type_id):
    records = mongo.db.symbol_url.find_one({"symbol":symbol})
    url=records['url_balance']
    if "url_transaction" in records:
        url1=records['url_transaction']
    acouunt={"account_name":address}
    response_user_token = requests.post(url=url,json=acouunt)
    response = response_user_token.json()       
    pay={"account_name":address,"offset":"-20","pos":"-1"}
    response_user = requests.post(url=url1,json=pay)
    res = response_user.json()       
    transactions=res['actions'] 
    
    array=[]
    
    for transaction in transactions:
        frm=[]
        to=[]
        block_time=transaction['block_time']
        action_trace=transaction['action_trace']['act']['data']
        if "from" in action_trace:
            fro = action_trace['from']
        else:
            fro=""
        if "to" in action_trace:   
            too=action_trace['to']
        else:
            too=""
        if "quantity" in action_trace:   
            amount_sent=action_trace['quantity']
        else:
            amount_sent=""
        frm.append({"from":fro,"send_amount":amount_sent})
        to.append({"to":too,"receive_amount":""})
        array.append({"fee":"","from":frm,"to":to,"date":block_time})
    
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

    balance=response['core_liquid_balance']
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
                "balance":balance,
                "transactions":array,
                "amountReceived":amount_recived,
                "amountSent":amount_sent
            }},upsert=True)
    
    return jsonify(res)
