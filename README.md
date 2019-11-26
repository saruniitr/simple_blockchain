# Simple Blockchain

This is a simple Django app to learn about Blockchain. It exposes endpoints to create transactions and for each transaction a new block is added to chain. An endpoint available to verify whether a given transaction is part of the chain or not.

Django REST framework is used to implement the API endpoints.

API, Database and Chain server node runs in three different containers. Run the docker-compose.yml to build and spin-up containers.

**Build and Run**

```
docker-compose build && docker-compose up -d && docker-compose logs -f
```

**Browseable API**
It can be found at http://localhost:8000/

**Tests**

```
docker-compose run api bash  # switch to container
python manage.py test
```
