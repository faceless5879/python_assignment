# Take-Home Assignment

## Project description:

This is my repository for G123-jp's python assignment

## Tech stack being used in this project

For this assignment, I used below technologies:

1. FastAPI - To build a quick API server with python
2. PostgreSQL - To store and retrieve data
3. Psycopg2 - To set up connection between API server and database
4. Pydantic - To set up and manage data validation
5. Docker - To speed development with the simplicity of docker compose and launch the source code on everywhere

## How to run code in local environment

1.  Create .env file in root folder and set up your local environment variables

```
# Example
DB_USER=postgres
DB_PASS=password
API_KEY=YOUR_AlphaVantage_API_KEY
```

2.  Run server

```
docker-compose up -d --build
```

3.  Get raw data and insert into database

```
python get_raw_data.py
```

- With 2 steps above, you will set up FastAPI server, PostgreSQL database and insert data to PostgreSQL.

4.  Clean up resource

```
docker-compose down
```

- This will clean up FastAPI server and PostgreSQL database. Imported data in step 2 will also be removed

## How to maintain the API key

1. Maintain API key in local enviroment

- To maintain API key in local enviroment, follow best practices below:
  - Never store API key directly in source code
  - Create an .env file and add .env to the repo's .gitignore
  - Store API key in .env, get API key information through os.getenv() method in Python

2. Maintain API key in prod enviroment

- This is depends on where you deploy your server, but using API secret management service is usually a good pratice. In my experience with deploying API server on AWS ECS, I will manage my API key with SSM Parameter Store. Follow the steps below to manage API key:

  - Extend IAM permission in ECS task execution IAM role. Give the role permission to get parameter in SSM.
  - Create API key parameter in SSM Parameter store
  - Add the environment variable to the ECS container definition
  - Create a task definition references to the API key

```
Extended pemission example:

{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ssm:GetParameters",
        "secretsmanager:GetSecretValue",
        "kms:Decrypt"
      ],
      "Resource": [
        "arn:aws:ssm:region:aws_account_id:parameter/parameter_name",
        "arn:aws:secretsmanager:region:aws_account_id:secret:secret_name",
        "arn:aws:kms:region:aws_account_id:key/key_id"
      ]
    }
  ]
}


Extended container definition example:

{
  "containerDefinitions": [{
    "secrets": [{
      "name": "environment_variable_name",
      "valueFrom": "arn:aws:ssm:region:aws_account_id:parameter/parameter_name"
    }]
  }]
}
```
