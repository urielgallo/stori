# pseudo code

import sys
import os
import requests
import re
import sendgrid
from sendgrid.helpers.mail import *
import pandas as pd
#from flask import render_template, redirect, url_for, request, abort
from models.transactions import Transaction
from flask import jsonify
from flask import request


transaction = Transaction()

def insert(data):
    insertar=transaction.insert(data)
    return insertar

def show():
    ver=transaction.show()
    return ver

def update():
    actualizar=transaction.update()
    return actualizar

def delete():
    eliminar=transaction.delete()
    return eliminar

def read_data():
    df=pd.read_csv("transactions.csv")
    records=df.to_dict('records')
    for record in records:
        insert(record)
    return "data uploaded"

def build_email(data):
    template = ""
    with open("views/emailTemplate.html", "r", encoding='utf-8') as f:
        template=f.read()
    dataRow = ""
    with open("views/dataRow.html", "r", encoding='utf-8') as f:
        dataRow=f.read()
    dataRows = ""
    print("data in build_mail", data)
    for key in data.keys():
        print("key", key)
        print("data", data[key])
        newDataRow = dataRow
        newDataRow = re.sub(r'<% label %>', key, newDataRow)
        value=str(data[key])
        if key == "Total Balance":
            value=f"${str(data[key])}"
        newDataRow = re.sub(r'<% value %>', str(data[key]), newDataRow)
        dataRows += f'{newDataRow}\n'
    template = re.sub(r'<% data %>', dataRows, template)
    return template

def send_mail(data, email):
    html_content = build_email(data)
    with open('views/generatedTemplate.html', 'w') as f:
        f.write(html_content)
    try:
        pass
        #sg = sendgrid.SendGridAPIClient(api_key='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')    
        sg = sendgrid.SendGridAPIClient(api_key='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') #MUMBii mail
        from_email=Email('resort@mumbii.com')
        to_emails=[To('urielrdzg10@gmail.com'),To(email)]
        subject='Financial balance'
        #content = Content("text/plain", "Estado de cuenta " + " - " )
        content = HtmlContent(html_content)
        mail = Mail(from_email, to_emails, subject, content)
        response = sg.client.mail.send.post(request_body=mail.get())
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)

def process():
    email = request.args.get('email')
    records = transaction.showAll()
    print(records)
    data={}
    data=total_balance(records, data)
    data=transactions_per_month(records, data)
    data=average_card(records,data)
    send_mail(data, email)
    return jsonify(data)


def total_balance(records, data):
    total_balance = 0
    for record in records:
        type = record[1][0]
        if (type == "-"):
            total_balance -= float(record[1][1:])
        else:
            total_balance += float(record[1][1:])
    data = {
        'Total Balance': total_balance
    }
    return data

def transactions_per_month(records, data):
    trans_per_month=[0]*12
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
              'August', 'September', 'October', 'November', 'December']
    for record in records:
        month = record[2].month
        trans_per_month[month-1] += 1
    for month,transactions in zip(months, trans_per_month):
        data[f"Transactions in {month}"] = transactions
    return data


def average_card(records, data):
    average_credit = 0
    average_dedit = 0
    counter_debit = 0
    counter_crebit = 0
    for record in records:
        type = record[1][0]
        if (type == "-"):
            counter_debit+=1
            average_dedit -= float(record[1][1:])
        else:
            counter_crebit+=1
            average_credit += float(record[1][1:])
    if counter_debit == 0:
        data[f"Average debit amount"] = 0 
    else:  
        data[f"Average debit amount"] = average_dedit/counter_debit
    if counter_crebit == 0:
        data[f"Average credit amount"] = 0
    data[f"Average credit amount"] = average_credit/counter_crebit
    return data