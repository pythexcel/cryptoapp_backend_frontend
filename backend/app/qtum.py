from flask import (
    Blueprint,request,jsonify,abort
)
import requests
from datetime import datetime
from app.util import serialize_doc
from app import mongo


def qtum_data(address,symbol,Preferred_Safename,Email,type_id):
    records = mongo.db.symbol_url.find_one({"symbol":symbol})
    url=records['url_balance']
    url_hash=records['url_hash']
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
        
        
        ret1=url_hash.replace("{{hash}}",''+transaction+'')
        response_u = requests.get(url=ret1)
        res1 = response_u.json()
        
        for tran in res1:
            fee=tran['fees']
            timestamp=tran['timestamp']
            dt_object = datetime.fromtimestamp(timestamp)
            inputs=tran['inputs']
            outputs=tran['outputs']
            frm=[]
            for inp in inputs:
                addre=inp['address']
                val=inp['value']
                frm.append({"from":addre,"send_amount":(int(val)/100000000)})
            to=[]
            for inpp in outputs:
                ad=inpp['address']
                value=inpp['value']
                to.append({"to":ad,"receive_amount":(int(value)/100000000)})
            array.append({"fee":fee,"from":frm,"to":to,"date":dt_object})
    
    balance = response['balance']
    amount_recived =response['totalReceived']
    amount_sent =response['totalSent']

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
                "balance":(int(balance)/100000000),
                "transactions":array,
                "amountReceived":(int(amount_recived)/100000000),
                "amountSent":(int(amount_sent)/100000000)
            }},upsert=True)

    return jsonify(res1)
