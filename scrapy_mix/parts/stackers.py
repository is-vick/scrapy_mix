"""
思路:
1. 通过节点存储数据达到链式存储的目的
2. 封装方法,实现栈的基本操作(入栈,出栈,栈空,查看栈顶)
3. top为栈顶,在链表的头作为栈顶位置 (不需要遍历)
"""

# 自定义异常
class StackError(Exception):
    pass

# 节点类
class Node:
    def __init__(self,val,next = None):
        self.val = val
        self.next = next

# 链式栈模型
class LStack:
    def __init__(self):
        # top作为栈顶的标记
        self.__top = None

    def empty(self):
        return self.__top is None

    # 入栈
    def put(self,val):
        self.__top = Node(val,self.__top)

        # node = Node(val)
        # node.next = self.__top
        # self.__top = node

    # 出栈
    def get(self):
        if self.__top is None:
            raise StackError("pop from empty stack")
        data =  self.__top.val
        self.__top = self.__top.next
        return data
    
    # 查看栈顶元素
    def top(self):
        if self.__top is None:
            raise StackError("get top from empty stack")
        return self.__top.va


class SStack:
    def __init__(self) -> None:
        self.stacker = []

    def empty(self):
        return not bool(len(self.stacker))
    
    def put(self, val):
        self.stacker.append(val)
    
    def get(self):
        if self.empty():
            raise StackError("pop from empty stack")
        return self.stacker.pop()
    
    def top(self):
        if self.empty():
            raise StackError("get top from empty stack")
        return self.stacker[-1]
