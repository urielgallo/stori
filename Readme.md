#

System to process transactions to get total balance, transactions per month and average debit and credits amounts

The app can run local for development or with docker.

General requirements:
- transactions.csv: This file contains the transactions.
- AWS Redshift: Databse to store the data
- AWS S3: Store the image (Stori logo)

The content of "transactions.csv" is stored on AWS Redshift.


### LOCAL

Requirements 

Python 3.9.11

Instructions
1. Create a virtual enviroment

```
python3 -m venv /<venv>
```

2. Activate virtual enviroment
```
source <venv>/bin/activate
````

3. Run the app
````
flask run -p 5050
````

### WITH DOKER

1. Biuld image
```
docker image build -t flask_app .  
```

2. Run image
```
docker run -p 5050:5050 flask_app 
```

## API Documentation

URL (if running local or with Docker in local):
http://localhost:5050/

---

GET 
```
transaction/read_data
```
Calling this endpoint, the file "transactions.csv" will be read and uploaded to AWS Redshift database.

---

GET 
```
transaction/process?email=<email>
```
Params:

`email`: email to send the information

Response example:
```
{
    "Average credit amount": 22564.007500000003,
    "Average debit amount": -16302.72916666667,
    "Total Balance": 165391.37,
    "Transactions in April": 0,
    "Transactions in August": 0,
    "Transactions in December": 10,
    "Transactions in February": 0,
    "Transactions in January": 8,
    "Transactions in July": 0,
    "Transactions in June": 0,
    "Transactions in March": 0,
    "Transactions in May": 0,
    "Transactions in November": 10,
    "Transactions in October": 0,
    "Transactions in September": 0
}
```

Calling this endpoint, the file response will compute: the total balance, transactions per month and average debit and credits amounts. And will send an email 

