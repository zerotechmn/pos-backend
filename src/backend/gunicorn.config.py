import os

bind = "0.0.0.0:8000"

# Sample Worker processes
workers = 2
threads = 4

worker_class = "gthread"
# worker_connections = 1000
timeout = 180
keepalive = 5

errorlog = "-"
loglevel = "info"
syslog = False
accesslog = "-"
access_log_format = (
    '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
)

preload = True

def post_fork(server, worker):
    server.log.info("Worker spawned (pid: %s)", worker.pid)
