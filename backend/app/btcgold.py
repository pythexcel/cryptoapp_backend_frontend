from flask import (
    Blueprint,request,jsonify,abort
)
import requests
from datetime import datetime
from app.util import serialize_doc
from app import mongo


def btc_gold_data(address,symbol,Preferred_Safename,Email,type_id):
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
    transactions = res['txs']
    array=[]
    
    for transaction in transactions:
        fee =transaction['fees']
        timestamp = transaction['time']
        dt_object = datetime.fromtimestamp(timestamp)
        transfers=transaction['vin']
        vout = transaction['vout']
        frm=[]
        for v_in in transfers:
            amount = v_in['value']
            fro = v_in['addr']
            frm.append({"from":fro,"send_amount":amount})
        to=[]
        for v_out in vout:
            scriptPubKey =v_out['scriptPubKey']
            recv_amount =v_out['value']
            if "addresses" in scriptPubKey:
                adrr =scriptPubKey['addresses']
                for addre in adrr:
                    to.append({"to":addre,"receive_amount":recv_amount})
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

    amount_recived =response['totalReceived']
    amount_sent =response['totalSent']
    balance = response['balance']
                
    
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
    return jsonify(response)
