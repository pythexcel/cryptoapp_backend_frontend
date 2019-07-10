from flask import (
    Blueprint,request,jsonify,abort
)
import requests
from datetime import datetime
from app.util import serialize_doc
from app import mongo


def ltc_data(address,symbol,Preferred_Safename,Email,type_id):
    records = mongo.db.symbol_url.find_one({"symbol":symbol})
    url=records['url_balance']
    ret=url.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()
    data = response['data']
    if "url_transaction" in records:
        url1=records['url_transaction']
    doc=url1.replace("{{address}}",''+address+'')
    response_user = requests.get(url=doc)
    res = response_user.json()       
    
    transactions = res['data']['data']

    array=[]
    for transaction in transactions:
        if transaction:
            inputs = transaction['inputs']
            outputs =transaction['outputs']
            frm=[]
            for inpu in inputs:
                if inpu:
                    prev_value=inpu['prev_value']
                    if "prev_addresses" in inpu:
                        prev_addresses=inpu['prev_addresses']
                        for pre in prev_addresses:
                            frm.append({"from":pre,"send_amount":prev_value})
            to=[]
            for out in outputs:
                if out:    
                    value=out['value']
                    if "addresses" in out:   
                        addresses=out['addresses']
                        for addr in addresses:
                            to.append({"to":addr,"receive_amount":value})
            fee =transaction['income']
            timestamp = transaction['time']
            conver_d = int(timestamp)
            dt_object = datetime.fromtimestamp(conver_d)
            array.append({"fee":fee,"from":frm,"to":to,"date":dt_object})
    
    balance = data['balance']
    amount_recived =data['total_receive']
    amount_sent =data['total_send']

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
                "balance":balance,
                "transactions":array,
                "amountReceived":amount_recived,
                "amountSent":amount_sent
            }},upsert=True)
    return jsonify(res)
    