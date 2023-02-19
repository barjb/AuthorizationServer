# Auth Server Project
Inspiration:
- https://auth0.com/blog/refresh-tokens-what-are-they-and-when-to-use-them/

## Details
- Access and Refresh Token are JWT bearer tokens
- AT expires in 5 mins
- RT expires in 3 months
- Auth Service is meant to provide token rotation for other services
- Auth Service keeps track of Refresh Tokens and saves them in the database
- In production Auth Service shouldn't have access to users data. This issue can be resolved by providing to the Auth Service appropriate endpoints from user microservice.



https://images.ctfassets.net/cdy7uua7fh8z/3sf7RRsy81bt3zcXMnHUSe/2171fdab4ffeb0987c329aa897038abc/rt-and-at.png

## Auth Service Endpoints
- /login - AS returns AT & RT pair
- /refresh - AS returns AT & RT pair 
- /verify - accessed only by resource server. Verify validity of AT

## login route
1. user - auth server /login
- returns jwt access token + refresh token
- store RT in DB on AS side
- user  stores AT + RT in secure storage
1. user - resource
- acces token as bearer in auth header
1. resource server - auth server /verify
- token verification response
- resource returns resource

## expired token flow
3. rs asks as to verify expired token
- token expired response
- rs sends 401 unauthorized back to client
- redirect user to login screen 
- 
## refreshing token
- user - auth server /refresh
- sends expired AT + RT
- as validates both
- if fine returns new AT

## hacker
- when sb tries to use the same rt its removed from DB thus being invalidated

## Refresh Token Rotation
From auth0 article:
"Refresh token rotation guarantees that every time an application exchanges a refresh token to get a new access token, a new refresh token is also returned. Therefore, you no longer have a long-lived refresh token that could provide illegitimate access to resources if it ever becomes compromised. The threat of illegitimate access is reduced as refresh tokens are continually exchanged and invalidated."

## Refresh Token Invalidation
"It's critical for the most recently-issued refresh token to get immediately invalidated when a previously-used refresh token is sent to the authorization server. This prevents any refresh tokens in the same token family from being used to get new access tokens."


## postgres
- psql -U postgres -> enter postgres as user = "postgres"
- psql - in /bin/bash -> enter postgres cmd
- \l list databases
- DROP DATABASE <dbname>;
- \c db_name - switch to db_name
- \dt - list tables
- \d <tablename> describe table
- DROP TABLE <tablename>;
- \q - quit from psql

## QUEUE
- consumer as separate app in background
- producer as part of an service

## docker
- remember to use container name in db connection

## run
- flask --app flaskr --debug run

