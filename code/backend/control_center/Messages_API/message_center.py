from rabbitmq import Rabbitmq

if __name__ == "__main__":
    rabbit = Rabbitmq(host='mqtt-redesfis.5g.cn.atnog.av.it.pt', port=5672, vhost="PI",username='pi_rabbit_admin', password='yPvawEVxks7MLg3lfr3g')
    rabbit.receive(q='API')
    rabbit.close()