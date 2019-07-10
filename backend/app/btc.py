from flask import (
    Blueprint,request,jsonify,abort
)
import requests
from datetime import datetime
from app.util import serialize_doc
from app import mongo


def btc_data(address,symbol,Preferred_Safename,Email,type_id):
    records = mongo.db.symbol_url.find_one({"symbol":symbol})
    url=records['url_balance']
    if "url_trans" in records:
        url1=records['url_trans']
    ret=url.replace("{{address}}",''+address+'')
    ret1=ret.replace("{{symbol}}",''+symbol+'')
    response_user_token = requests.get(url=ret1)
    response = response_user_token.json()       
    

    if symbol == "BTC":
        transaction = response['data']
        balance =transaction['balance']
        amountReceived =transaction['amountReceived']
        amountSent =transaction['amountSent']
        transactions = transaction['txs']
        array=[]
        
        for transaction in transactions:
            fee=transaction['fee']
            frmm=transaction['inputs']
            frm=[]
            for trans in frmm:
                fro=trans['address']
                send=trans['value']
                frm.append({"from":fro,"send_amount":(send/100000000)})
            transac=transaction['outputs']
            to=[]
            for too in transac:
                t = too['address'] 
                recive =too['value']
                to.append({"to":t,"receive_amount":(recive/100000000)})
            timestamp =transaction['timestamp']
            dt_object = datetime.fromtimestamp(timestamp)
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
                "amountReceived":(int(amountReceived)/100000000),
                "amountSent":(int(amountSent)/100000000)
            }},upsert=True)
    
    return jsonify(response)
