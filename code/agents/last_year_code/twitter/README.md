# Informação util

Existem 4 sistemas de mensagens
- **vhost** -> PI
1. Tasks
    - **exchange**
        - name -> tasks_deliver
        - xtype -> direct
    - **queue**
        - name -> ***bot-<bot_id>*** 
            - Ex: bot-1 bot-2
    - **binding**
        - **routing_key**
            - name -> ***tasks.twitter.<bot_id>***
                - Ex : tasks.twitter.1 tasks.twitter.2
2. Upload Logs
    - **exchange**
        - name -> logs
        - xtype -> direct
    - **binding**
        - **routing_key**
            - name -> logs.twitter
3. Queries
    - **exchange**
        - name -> queries
        - xtype -> direct
    - **binding**
        - **routing_key**
            - name -> queries.twitter
4. Upload Data
    - **exchange**
        - name -> twitter_data
        - xtype -> direct
    - **binding**
        - **routing_key**
            - name -> data.twitter


# Considerações

## twitter_bot.py
- Caso ocorra um erro devido à suspensão da conta, um log é enviado para a fila de logs . Outro tipos de erros não
- _setup() : 
    1. AS filas de mensagens sao criadas e é feito o binding entre exchange e queue
    2. As credencias do twitter sao validas de acordo com o wrapper da api do twitter
    3. O utilizador criado com as credencias acima é enviado para a exchange "twitter_data"
    4. A  [cache](#cache) é inicializada  e é efetuado o open
    5. O timeLine é lido atraves da funçao [read_timeline](#read_timeline)
<a  name="read_timeline"></a>
- read_timeline() :
    1. Um valor random é gerado: tweets_to_get-> numero de twetts a retirar da timeline
    2. A função responsavel por obter os twetts da timeline é executada ( de acordo com o valor definido anteriromente ) : 
    [get_user_timeline_tweets](#get_user_timeline_tweets) 
    3. Caso não existam tweets para retirar a função é terminada
    4. É definida uma variavel (total_read_time) usada para dar track de quanto tempo o bot usou para ler a timeline do user
    5. Para todos os twetts obtidos
        - o tweet é enviado usando a funçao [send_tweet()](#send_tweet)
        - Caso o tweet seja da timeline do proprio bot , então nao é necessario fazer o pos-processamento ( que será descrito a seguir )
        - Se o tweet nao tiver like , então mandar uma query request para dar like usando a função [query_like_tweet()](#query_like_tweet)
        - Se o tweet nao tiver sido retwetado, então mandar uma query request para dar retwett usando a funçao [query_retweet_twett](#query_retweet_tweet)
         


<a name="query_like_tweet"></a>
- query_like_tweet()
    1. É verificado se o tweet em questão já tem o like do utilizador ( bot)
        - Caso seja verdade a função é terminada ( return )
        - Caso contrario, é enviado uma mensagem de query para o tweet ( passado por argumento , com o tipo de mensagem = MessageType.QUERY_TWEET_LIKE )
        usando a função [send_query()](#send_query)

<a name="query_retweet_tweet"></a>
- query_retweet_tweet()
    1. É verificado se o tweet em questão ja foi retweeted pelo utilizador ( bot )
        - Caso seja verdade a função é terminada (return )
        - Caso contrario, é enviado uma mensagem de query ( passado por argumento,
        com o tipo de mensagem = MessageType.QUERY_TWEET_RETWEET) usando a função 
        [send_query()](#send_query)

<a name="send_tweet"></a>
- send_tweet()
    1. É enviado o tweet em json , com o type de mensagem = MessageType.SAVE_TWEET, usando a função [send_data](#send_data)


<a name="send_query"></a>
- send_query()
    1. Basicamanente isto é um wrapper que envia uma mensagem para a exchange 
    "QUERY_EXCHANGE" ( 'queries' ) usando a função [_send_message()](#_send_message)

<a name="send_data"></a>
- send_data()
    1. Basicamente isto é um wrapper que envia uma mensagem para a exchange "DATA_EXCHANGE" ( 'twitter_data') usando a função [_send_message()](#_send_message)

<a name="_send_message"></a>
- _send_message()
    1. É usado a anotação [@reconnect_messaging](reconnect_messaging)
    2. É usado um wrapper [utils.wrap_message()](#wrap_message) para ter um dicionario estruturado com os argumentos passados
    3. Publicar a mensagem (convertida para json) gerada anteriorimente, no sistema de mensagens numa determinada exchange ( passada por argumento )

<a name="get_user_timeline_tweets" ></a>
- get_user_timeline_tweets()
    1. Caso o tweet seja da autoria do proprio bot (user_obj.id == self.user.id
        - É retornado um lista de tweets da home_timeline()
    2. Caso contrario
        - É retornado uma lista de tweets de timeline do respetivo user . Usando a função [timeline](#timeline)




<a name="models"></a>
## models.py
<a name="timeline"></a>
 - Onde se encontram definidas algumas das entidades do twitter:
   - User
     - é um bocado estranho, mas este user é criado usando uma API, que vem do tweepy, e que contém o nosso utilizador (o nosso bot, ou seja, o utilizador autenticado). Depois, há campos como user_id, que são sobre o utilizador que estamos a analisar.
     - `timeline`: permite obter a lista com os tweets do user que se está a analisar, da sua timeline do twitter 
     - `friends`: permite obter uma lista de objetos User, que são os amigos do user que estamos a analisar (quem é que este segue)
     - `followers`: permite obter uma lista de objetos User, que seguem o user que estamos a analisar
     - `follow`: seguir alguém 
     - `unfollow`: deixar de seguir alguém (dado o user id desse alguém)
   - Tweet
   - DirectMessage


- timeline():
    1. Obter a timeline de um user (user id passado por argumennto a uma função da API do twitter)


<a name="models"></a>
## api.py
<a name="timeline"></a>
 - É apenas um wrapper para o Tweepy
 - Métodos:
   - user_timeline
   - followers
   - create_friendship
   - destroy_friendship
   - retweet
   - create_favourite
   - destroy_favorite
   - verify_credentials
   - get_status
   - get_user
   - home_timeline
   - lookup_users
   - direct_messages
   - update_status


<a name="cache"></a>
## cache.py 
- open():
    1. Um file .json é lido ( ou criado , caso nao exista )
    2. O conteudo do file é carregado para um dicionario (self.cache)
    3. As keys "user" e "tweets" estão sempre presentes no dicionario (self.cache). Caso não existam são inicializadas com um empty dicionario
- _flush():
    1. Da seek(0) no file
    2. Escreve o dicionario cache como json no ficheiro
    3. Da flush no file
- set()
    1. Escrever um pair key,value no dicionario
    2. Faz o _flush() ( função anterior )
- get()
    1. Obter um value pela key
- save_tweet(), save_user(), get_user(), get_tweet(), close() : Trivial (ver o codigo )


<a name="utils"></a>
## utils.py

<a name="wrap_message"></a>
- wrap_message()
    1. Trivial ( ver codigo )


<a name="anotation"></a>
## Anotações
<a name="reconnect_messaging"></a>
- reconnect_messaging()
    1. TODO
 