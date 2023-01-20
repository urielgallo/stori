from datetime import datetime, timezone
import pytz

import sqlalchemy as sa
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy import insert

# build the sqlalchemy URL
url = URL.create(
    drivername='redshift+redshift_connector', # indicate redshift_connector driver and dialect will be used
    host='story-test.265367330608.us-east-2.redshift-serverless.amazonaws.com', # Amazon Redshift host
    port=5439, # Amazon Redshift port
    database='story', # Amazon Redshift database
    username='admin', # Amazon Redshift username
    password='janadarAWS10' # Amazon Redshift password
)

engine = sa.create_engine(url)

#Next, we will create a session using the already established engine above. 

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

# Define Session-based Metadata
metadata = sa.MetaData(bind=session.bind)

class Transaction():
    RedshiftDBTable = sa.Table(
        'transactions',
        metadata,    
        #id = sa.Column('id',sa.Integer, primary_key=True),
        sa.Column('id',sa.INTEGER),
        sa.Column('amount',sa.VARCHAR),
        sa.Column('date',sa.TIMESTAMP),
        sa.Column('number_card',sa.INTEGER),
        redshift_diststyle='KEY',
        redshift_distkey='number_card',
        redshift_sortkey='date'
    )

    def insert(this, data):
        if data['amount'] < 0:
            data['amount'] = str(data['amount'])
        else:
            data['amount'] = f"+{str(data['amount'])}"
        insert_data_row = this.RedshiftDBTable.insert().values(
            #id=data.id,
            amount=data['amount'],
            date=data['date'],
            number_card=data['number_card']
        )
        session.execute(insert_data_row)
        session.commit()    
        return "from model insert" 

    def show(this):
        print("from model show")
        return "from model show"

    def showAll(this):
        print("from model showAll")
        records = []
        for instance in session.execute(this.RedshiftDBTable.select()):
            records.append(instance)
        return records

    def update(this):
        print("from model update")
        return "from model update"

    def delete(this):
        print("from model delete")
        return "from model delete"