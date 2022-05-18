https://group-server-app.herokuapp.com//oauth/authorize?client_id=1234&response_type=code&redirect_uri=http://localhost/exchange_token&state=423423423423

curl -X POST https://group-server-app.herokuapp.com/oauth/token -F client_id=1234 -F client_secret=secret_4321 -F code=12321 -F grant_type=auth_code
