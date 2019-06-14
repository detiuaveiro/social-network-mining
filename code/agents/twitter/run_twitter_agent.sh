docker run -d \
--name Twitter-$NAME \
-e KEY=$KEY \
-e SECRET=$SECRET \
-e TOKEN=$TOKEN \
-e TOKEN_SECRET=$TOKEN_SECRET \
-e SERVER_HOST=$SERVER_HOST \
-e SERVER_PORT=$SERVER_PORT \
-e TOR_PROXY=$TOR_PROXY \
twitter_agents