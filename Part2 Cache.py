"""
    Assumption:
        1. Used for functions. Users can remove individual functions and their arguments combined,
            but they will not be able to remove all the values of functions itself.
        2. Redis needs to be installed with port number of 6379.
"""
from functools import wraps
from typing import TypeVar
from walrus.cache import Cache as Cbase
from walrus.database import Database

T = TypeVar('T')    # Generic value

# Cache
class Cache:
    expTime: int
    db: Database
    cache: Cbase

    def __init__(self, expTime=10*60):
        """
            Initiates the cache class. If the expTime was passed, the expTime will be set accordingly.
            input: expTime
        """
        self.expTime = expTime
        self.db = Database(host='localhost', port=6379)
        self.cache = self.db.cache()

    def __funcToKey__(self, func, args: [], kwargs: dict) -> str:
        """
            Converts passed in functions and args into list.
            input: function and arguments and keyword arguments
            output: key in string
        """
        return "{}:{}:{}".format(func.__name__, str(args), str(kwargs))

    def get(self, key):
        """
            Gets an item from the cache. Returns None if cache miss.
        """
        return self.cache.get(key)
    
    def set(self, key, val):
        """
            Sets an item to the cache.
        """
        self.cache.set(key, val, self.expTime)
    
    def getFuncItem(self, func, args: [], kwargs: dict) -> (bool, T):
        """
            Gets the item from the cache. The first returned value is False if cache miss.
            If it's a cache-miss, the value returned will be None.
            input: function and arguments and keyword arguments
            output: (bool, val)
        """
        key = self.__funcToKey__(func, args, kwargs)
        val = self.cache.get(key)
        if val is None:
            return (False, None)
        
        return (True, val)
    
    def setFuncItem(self, func, args: [], kwargs: dict):
        """
            Stores the result into the cache.
            input: function and arguments and keyword arguments
        """
        key = self.__funcToKey__(func, args, kwargs)
        val = self.cache.set(key, func(*args, **kwargs), self.expTime)

    def cached(self):
        def decorator(function):
            @wraps(function)
            def wrapper(*args, **keyargs):
                isIn, val = self.getFuncItem(function, args, keyargs)
                if isIn:
                    return val
                else:
                    val = function(*args, **keyargs)
                    self.setFuncItem(function, args, keyargs)
                    return val
            return wrapper
        return decorator

cache = Cache()

# Testing Functions
@cache.cached()
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

def fibonacciUC(n):
    if n <= 1:
        return n
    return fibonacciUC(n-1) + fibonacciUC(n-2)

# Run Test
if __name__ == "__main__":
    import timeit

    val = 41
    start = timeit.default_timer()
    print(fibonacciUC(val))
    print("Time: {}".format(timeit.default_timer()-start))
    start = timeit.default_timer()
    print(fibonacci(val))
    print("Time: {}".format(timeit.default_timer()-start))
