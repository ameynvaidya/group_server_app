For fetching authorization code:
https://group-server-app.herokuapp.com/oauth/authorize?client_id=1234&response_type=code&redirect_uri=http://localhost/exchange_token&state=423423423423

Login: 
email: amey@abc.com 
password: amey


For exchanging token:
curl -X POST https://group-server-app.herokuapp.com/oauth/token -F client_id=1234 -F client_secret=secret_4321 -F code=#REPLACE_WITH_ACCESS_TOKEN -F grant_type=authorization_code

For refreshing the token
curl -X POST https://group-server-app.herokuapp.com/oauth/token -F client_id=1234 -F client_secret=secret_4321 -F refresh_token=#REPLACE_WITH_REFRESH_TOKEN -F grant_type=refresh_token



For fetching profile info
curl -X GET https://group-server-app.herokuapp.com/api/get_profile -H 'Authorization: Bearer #REPLACE_WITH_ACCESS_TOKEN'

