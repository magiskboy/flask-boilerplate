bind = "0.0.0.0:5000"

backlog = 2048

workers = 1

worker_class = "gevent"

worker_connections = 1000

timeout = 30

errorlog = "-"
loglevel = "info"
accesslog = "-"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
