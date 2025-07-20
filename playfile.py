import math
from parameterized import parameterized
nested = {"a": 1, "a": {"b": 2}, "a": {"b": 2}} 
path = ("a", "a", ("a", "b"))
for x in path and nested:
    value = nested[x]
    
