FROM python:alpine3.7
RUN mkdir /app
COPY app.py requirements.txt ./app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 8080
ENTRYPOINT [ "python" ]
CMD [ "app.py" ]