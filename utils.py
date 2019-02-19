import inspect

# 动态的获得函数参数值

def optional_debug(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(args, kwargs)
        print(args[-1])
        print(inspect.getcallargs(func, *args, **kwargs))
        return func(*args, **kwargs)
    return wrapper

@optional_debug
def a(x, debug, cc=5, **aaa):
    debug = 'a'
    pass

a(2, 3, bb='c')

```
[root@zuul zhuangshi]# python args_inspect.py
((2, 3), {'bb': 'c'})
3
{'debug': 3, 'x': 2, 'aaa': {'bb': 'c'}, 'cc': 5}
```
