# Auth Server Project

## Description
- Access and Refresh Token are JWT bearer tokens
- AT expires in 5 mins
- RT expires in 3 months
- Auth Service is meant to provide token rotation for other services
- Auth Service keeps track of Refresh Tokens and saves them in the database
- In production Auth Service shouldn't have access to users data. This issue can be resolved by providing to the Auth Service appropriate endpoints from user microservice.
- For convenience AT and RT are being send as json object. On the other hand sending data in headers can be accessed before the body is downloaded, so there's a place for an improvement.

![alt text](/img/rt-and-at.png "Title")

## Auth Service Endpoints
1. /login - SPA => Auth Service
    - POST, requires username && password send in body
    - return AT & RT pair

2. /refresh - Resource Server => Auth Service 
    - POST, AT && RT send in body
    - return new AT && RT pair

3. /verify - Resource Server => Auth Service
    - POST, AT send in body
    - return boolean

## Auth Service DB
1. Stores Refresh Tokens
2. Columns
   - id
   - tokenstr - token in string form 
   - rootId - id of root token used to invalidate a family of tokens
   - refreshed - set to True upon token rotation
3. Improvements
   - tokens expire after 90 days, so whole tokens families could be deleted automatically

## Flows
### Login
1. SPA makes a request to Auth Server's /login endpoint
    1. If login & password combinaction is correct
      - AS responses with jwt access & refresh token pair
      - AS stores RT in database on AS side. DB can't be accessed by ohter services.
      - SPA stores AT + RT in secure storage
    2. Otherwise user is asked to input correct login data.
2. SPA asks Resource Server for sensitive data
   - Access Token is being sent as part of a request (header or body, pros and cons are described in Details section above)
3. Resource Server makes a request to Auth Server's /verify endpoint
    1. AS verifies token and sends response
    2. If token is valid
       - RS responds to SPA with a protected resource 
    3. Otherwise RS tries to refresh token 

### Expired refresh token flow
1. Resource Server makes a request to Auth Server's /refresh endpoint with expired token pair
   - AS responds with 401 unauthorized
2. RS redirects SPA to login screen

### Refreshing token
1. Resource Server makes a request to Auth Server's  /refresh endpoint (expired AT & valid RT)
   - AS validates both
   - If validation passes RS responds with new AT & RT pair

## Protection against stolen tokens

### Flow
1. Malicious user steals Refresh Token from User
2. User continues using SPA
3. RS refreshes AT & RT pair
4. User goes offline
5. Malicious user tries to use stolen RT
6. AS keeps track of previously used tokens and invalidates stolen token and Users newest token.
7. User comes back online
8. User has to log in again due to security breach

### Refresh Token Rotation & Invalidation
From auth0 article:
```text
"Refresh token rotation guarantees that every time an application exchanges a refresh token to get a new access token, a new refresh token is also returned. Therefore, you no longer have a long-lived refresh token that could provide illegitimate access to resources if it ever becomes compromised. The threat of illegitimate access is reduced as refresh tokens are continually exchanged and invalidated."

"It's critical for the most recently-issued refresh token to get immediately invalidated when a previously-used refresh token is sent to the authorization server. This prevents any refresh tokens in the same token family from being used to get new access tokens."
```
## Run in local machine
- flask --app flaskr --debug run

## Links
- https://auth0.com/blog/refresh-tokens-what-are-they-and-when-to-use-them/