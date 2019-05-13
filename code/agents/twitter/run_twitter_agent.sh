docker build -t agents . ;
docker run \
--name Twitter-1 \
-e KEY=lYa4VucwdoUUTQLC2utgtg \
-e SECRET=NfnIALNRMcrvC844yypUubWp2xmuiL3zbLN8osjWntM \
-e TOKEN=1103294806497902594-bI8hncZU8h4JHAmZ4vrPYZ0eDMA5jk \
-e TOKEN_SECRET=BYtMX7efD0lTl1FZcN6D8zQr4WVcLjjvxL6BpHCQCQFbI \
-e SERVER_HOST=mqtt-redesfis.ws.atnog.av.it.pt \
-e SERVER_PORT=80 \
-e TOR_PROXY=http://18.130.65.85:9050
