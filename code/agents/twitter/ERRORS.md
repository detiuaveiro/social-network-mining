# Errors

### twitter_bot.py
1. Linha 529 
    - Pq é que o argumento count ( presente no **kwargs ) não é passado no 
    **return self._api.home_timeline()**

2. Linha 
    - Codigo redundante -> Na linha x é verificado se o twitter ja tem like. Na função query_like_tweet() tambem é feita esta verificação ( linha 605 )
