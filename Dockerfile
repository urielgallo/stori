FROM python:3.9 

# Create the working directory (and set it as the working directory)
RUN mkdir -p /app
WORKDIR /app
 
# Install the package dependencies (this step is separated
# from copying all the source code to avoid having to
# re-install all python packages defined in requirements.txt
# whenever any source code change is made)
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt
 
COPY . /app

#ENTRYPOINT [ "python" ]
#CMD [ "app.py" ]
#CMD ["gunicorn"  , "-b", "0.0.0.0:8888", "app:app"]
CMD exec gunicorn --bind :8888 --workers 1 --threads 8 --timeout 0 app:app