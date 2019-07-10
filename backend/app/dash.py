from flask import (
    Blueprint,request,jsonify,abort
)
import requests
from datetime import datetime
from app.util import serialize_doc
from app import mongo


def dash_data(address,symbol,Preferred_Safename,Email,type_id):
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
    transactions=res['txs'] 
    array=[]
    
    for transaction in transactions:
        frm=[]
        to=[]
        fee = transaction['fees']
        time =transaction['time']
        dt_object = datetime.fromtimestamp(time)
        vin = transaction['vin']
        vout = transaction['vout']
        for v_in in vin:
            fro = v_in['addr']
            send_amount=v_in['value']
            frm.append({"from":fro,"send_amount":send_amount})

        for v_out in vout:
            val = v_out['value']
            scriptPubKey = v_out['scriptPubKey']
            if "addresses" in scriptPubKey:
                addresses=scriptPubKey['addresses']
                for addd in addresses:
                    to.append({"to":addd,"receive_amount":val})
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

    balance=response['balance']
    amount_recived =response['totalReceived']
    amount_sent =response['totalSent']
    
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
