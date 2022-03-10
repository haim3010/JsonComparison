# Json comparison 

* run main.py in order to create an analyzer report as a jsonFile
  - command : python main.py
  
# upload analyzer.json to localstack

* run :
  - docker-compose build
  - docker-compose up -d


* ensure analyzer.json loaded to localstack
    - docker ps -a
    - docker logs <CONTAINER ID>

