
# coroutine


def consumer():
    while True:
        print('需要包子....')
        baozi = yield  
        print('吃了%s个包子'%baozi)


def producer(obj1):
    obj1.send(None)
    for i in range(3):
        print('正在做%s个包子'%i)
        obj1.send(i)



con1 = consumer() 
producer(con1)