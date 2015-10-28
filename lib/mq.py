import redis

def redis_connect(**redis_kwargs):
    con = redis.Redis(**redis_kwargs)
    return con

def qsize(key,con):
    return con.llen(key)

def put(key,con,item):
    con.rpush(key,item)

def block_pop(key,con):
    item = con.blpop(key, timeout=0)
    if item:
        item = item[1]
    return item

def pop(key,con):
    item = con.blpop(key,timeout=1)
    if item:
        item = item[1]
    return item

def get(key,con):
    item = con.get(key)
    return item

def set(key,con,item):
    con.set(key,item)

def setex(key,con,item,timeout=2):
    con.setex(key,item,timeout)

def delete(key,con):
    con.delete(key)

def exists(key,con):
    return con.exists(key)
