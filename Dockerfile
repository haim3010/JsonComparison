FROM localstack/localstack:latest
WORKDIR /code
RUN pip3 install boto3
COPY upload_json.py .
COPY analyzer.json .
ENTRYPOINT ["python", "upload_json.py"]