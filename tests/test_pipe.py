def func1(val:str):
    val += "__1"
    print("func1", val)
    return val
    
def func2(val: str):
    val += "__2"
    print("func2", val)
    return val
    
def func3(val: str):
    val += "__3"
    print("func3", val)
    return val
    
from src.utils.pipe import Pipe

    
def test_pipe():
    a = "the_val"
    p = Pipe(a) | func1 | func2 | func3
    
    print(p.get())