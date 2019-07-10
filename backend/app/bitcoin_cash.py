from flask import (
    Blueprint,request,jsonify,abort
)
import requests
from datetime import datetime
from app.util import serialize_doc
from app import mongo


def btc_cash_data(address,symbol,Preferred_Safename,Email,type_id):
    records = mongo.db.symbol_url.find_one({"symbol":symbol})
    url=records['url_balance']
    if "url_transaction" in records:
        url1=records['url_transaction']
    ret=url.replace("{{address}}",''+address+'')
    response_user_token = requests.get(url=ret)
    response = response_user_token.json()       

    data = response['data']
    addr =data[''+address+'']
    add =addr['address']
    balance =add['balance']
    bal = (balance/100000000)
    receive_amount=add['received']
    send_amount=add['spent']
    transactions=addr['transactions']
    array=[]
    for tran in transactions:
        doc=url1.replace("{{address}}",''+tran+'')
        response_user = requests.get(url=doc)
        res = response_user.json()       
        trs =res['data'][''+tran+'']
        inputs=trs['inputs']
        outputs=trs['outputs']
        transact=trs['transaction']
        fee =transact['fee']
        time =transact['time']

        frm=[]
        for inp in inputs:
            recipient = inp['recipient']
            value=inp['value']
            frm.append({"from":recipient,"send_amount":(value/100000000)})
        to=[]
        for out in outputs:
            recipient1 = out['recipient']
            value1=out['value']
            to.append({"to":recipient1,"receive_amount":(value1/100000000)})
        array.append({"fee":fee,"from":frm,"to":to,"date":time})

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
                "balance":bal,
                "transactions":array,
                "amountReceived":(receive_amount/100000000),
                "amountSent":(send_amount/100000000)
            }},upsert=True)
    return jsonify(trs)
