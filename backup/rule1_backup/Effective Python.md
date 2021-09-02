---
title: Effective Python
author: Free
description: 关于Effective Python书籍的阅读笔记。
tags: Python
categories: 读书笔记
comments: true
abbrlink: effective-python
---

{% note info modern %}
笔记未完成，有待{% label 更新 %}。
{% endnote %}

# Effective Python

## 第1章：培养Pythonic思维

### 第1条 查询使用的Python版本

学会查询Python的版本

```python
import sys
print(sys.version_info)
print(sys.version)

>>>
sys.version_info(major=3, minor=8, micro=3, releaselevel='final', serial=0)
3.8.3 (default, Jul  2 2020, 17:30:36) [MSC v.1916 64 bit (AMD64)]
```

### 第2条 遵循PEP 8 风格指南

要让Python代码更具有Pythonic特点，那么编写代码的风格最好遵循PEP 8指南（针对Python代码格式而编订的指南）。

完整的内容可以从网上找到，这里推荐两个地址：

①[英文原版](https://www.python.org/dev/peps/pep-0008/)

②[中文翻译](https://python.freelycode.com/contribution/detail/47)

Effective Python书中主要踢到的建议是关于以下几个方面：

- 与空白相关：主要注意缩进时空格与制表符不能混用、长代码的缩进处理
- 与命名相关：函数、变量、类等命名时的规范
- 与表达式和语句相关：规范表达式和语句的写法，尽量从简
- 与引入相关：import语句总是在文件开头，引入模块用绝对名称

### 第3条 了解bytes与str的区别

Python3中的字符串有两种：str和bytes，我们需要区分这两者的区别，文本（str）和二进制数据（bytes），文本总是Unicode，用str类型，二进制数据则用bytes类型表示。

bytes类型之间可以使用`+`操作符以及比较大小，str类型也可以。但是两者不能混搭进行操作。如：

```python
b'one' + b'two'  ✔
b'one' + 'two'   ✗
```

str与bytes的相互转换：

**str.encode('encoding') ---> bytes**

**bytes.decode('encoding') ---> str**

其中encoding指的是编码方式，对于中文，它可以是'utf-8'，'gb2312'，'gbk'，'big5'等，一般默认是'utf-8'。不同编码方式，结果也不同。

下面的图示与例子便于理解。并且要注意的是转换之后的长度可能会因编码方案的不同而发生改变。

![image-20210311180850691](https://i.loli.net/2021/03/11/JGFpYPRovf3mZQE.png)

```python
str_a = 'T恤'
bytes_a = str_a.encode('utf-8')
str_a1 = bytes_a.decode('utf-8')

>>>
bytes_a = b'T\xe6\x81\xa4'
str_a1 = 'T恤'
```

### 第4条 用支持插值的f-string取代C风格的格式字符串与str.format方法

在Python中采用%格式化操作符有四个缺点：

- %右侧元组里面的值在类型或顺序上发生变化时，程序可能因转换类型时不兼容而出现错误。
- 在填充具体变量时经常需要做一些处理（居中，保留小数位等），使得表达式冗长混乱。
- 同一个值填充格式字符串的多个位置时，在%右侧的元组需要多次重复这个值。
- 把dict写到格式化表达式里会让表达式特别长。

而`str.format`方法虽然比C风格的格式化字符串好一些，但是仍然不能解决上述第二个缺点。而插值格式字符串`f-string`用新的写法，尽可能的简化了表达式的写法。以下是几种表达式写法的对比：

```python
key = 'my_var'
value = 1.234
f_string = f'{key:<10} = {value:.2f}'
c_tuple = '%-10s = %.2f' % (key, value)
str_args = '{:<10} = {:.2f}'.format(key, value)
str_kw = '{key:<10} = {value:.2f}'.format(key = key, value = value)
c_dict = '%(key)-10s = %(value).2f' % {'key': key, 'value': value}
```

`f-string`是个简洁而强大的机制，可以直接在格式说明符里嵌入任意Python表达式，所以应当利用好这个方法，以简化代码。

### 第5条 用辅助函数取代复杂的表达式

- 对于一个变量或是其他什么数据结构，如果需要对其进行多种操作，如转换为整数、布尔表达式等，应当尽量简化写法，而不要一起堆积到一行中。
- 对于复杂的表达式，并且是需要重复使用的情况，应该将表达式写到辅助函数中。
- 用`if/else`结构写成的条件表达式，要比`or`与`and`写成的Boolean表达式更易懂。

### 第6条 把数据结构直接拆分到多个变量里，不要专门通过下标访问

元组类型变量不能修改其值，如果要将元组中的值分别赋给不同的其他变量，可以采用拆分(unpacking)的写法，只需一条语句就可以完成。

```python
item = ('blue', 'red')
first, second = item
print(first,'-',second)

>>>blue - red
```

通过unpacking赋值要比通过下标访问变量值更清晰，unpacking用法灵活，可迭代对象都能拆分，对于列表等都适用。

交换两个对象的值时也可以一行解决。

```python
a, b = b, a
```

上述拆分机制在for循环或类似的结构（推导与生成表达式，见27条）很重要，可以把复杂的变量拆分到相关的变量中。

### 第7条 尽量用enumerate取代range

对于需要迭代的情况，尽量使用`enumerate`，而不是`range`，`enumerate`可以把任何一种迭代器（iterator）封装成惰性生成器（lazy generator，见30条），同时给出本轮循环的序号。用法如下：

```python
color = ['red', 'green', 'blue']
for i, col in enumerate(color, 1):
    print(f'{i}: {col}')

>>>
1: red
2: green
3: blue
```

`enumerate`的第二个参数为起始的序号，省去了打印时额外调整的步骤。

### 第8条 用zip函数同时遍历两个迭代器

有时需要从源列表中产生另一个列表（派生列表），如果想同时遍历这两份列表，那么可以使用内置的`zip`函数实现，如下：

```python
num = [1, 2, 3, 4]
num_2 = [1, 4, 9, 16]
for a, a_2 in zip(num, num_2):
    print(f'{a} squared is {a_2}')

>>>
1 squared is 1
2 squared is 4
3 squared is 9
4 squared is 16
```

而如果`zip`中的列表长度不一致，则其循环次数取决于最短的列表长度。如果想按最长的迭代器来遍历，需要用`itertools`模块的`zip_longest`函数。

### 第9条 不要在for与while循环后面写else块

在使用`for`循环以及`while`循环时，其后可以跟`else`语句，而只有在整个循环没有因为`break`提前跳出的情况下，`else`块才会执行。并且因为这里的`else`与`if/else`中的`else`含义不一样，所以会让人看不太懂，应当避免在循环后使用`else`语句。

### 第10条 用赋值表达式减少重复代码

`a = b`是普通的赋值语句，Python 3.8引入了新的语法：赋值表达式，它是使用海象操作符`:=`给变量赋值，并且让这个值成为表达式的结果。相比普通的赋值，使用海象操作符可以减少重复代码，让代码更精简。

一般在写`if/else`结构、模拟`switch/case`结构、`do/while`结构时，常需要在代码前写好变量初始赋值语句，然后再进入`if`语句进行判断，如果使用海象操作符则可以将之前的赋值语句合并到后面进行`if`语句判断的地方，从而减少重复代码。

需要注意的是，如果赋值表达式是大表达式中的一部分，就要用一对括号把它括起来。参考下面的例子：

```python
my_list = [1,2,3,4]

if (count := len(my_list)) >= 3:
   print(f"The length of my_list is {count}")

if count := len(my_list) >= 3:
   print(f"The length of my_list is {count}")

>>>
The length of my_list is 4
The length of my_list is True
```



## 第2章：列表与字典

### 第11条 学会对序列做切片

Python可以对序列做切割(slice)，只要实现了\_\_getitem\_\_与\_\_setitem\_\_两个特殊方法的类都可以切割（见43条）。

基本用法就是somelist[start:end]。这样实际取值是从somelist[start]到somelist[end-1]，如果从起始位置0切割，即start为0，则0可以省略，若end为somelist的长度时（序列末尾），end也可省略。

切片比较需要注意的有以下三点：

- start或end可以取负数，取负数时表示的位置是从相反方向开始数，最后结果就是序列中start所指位置的元素到end所指位置的元素。最简单的理解方式是，可以将含有负数的切片转变为正常的切片方式，只需要将负数值加上序列的长度就变成正常的切片了。

- 切片时start和end允许越界，超出范围时系统会自动忽略不存在的元素。但是直接对序列取值则不能越界。

- 在赋值时可以在赋值符号左边使用切片，这样表示的意义是把序列切片所取的值用右边的元素替换，所以当赋值符号左右两边表示的元素个数不相等时，序列的长度会发生变化。

范例代码：

```python
>>>a = [1, 2, 3, 4, 5, 6]

>>>a[:3]
[1, 2, 3]

>>>a[4:]
[5, 6]

>>>a[1:-1]  # 第一点。等同a[1:5]
[2, 3, 4, 5]

>>>a[:50]  # 第二点。
[1, 2, 3, 4, 5, 6]

>>>a[1:3] = ['a']  # 第三点
[1, 'a', 4, 5, 6]
```



### 第12条 不要在切片里同时指定起止下标与步进

序列的切片方法还有一种步进的形式，就是somelist[start:*end*:stride]，那么和普通的切片形式相比，就是end之后多指定了stride步进这个值，表示从start开始每过stride便取一次值，而没有指定stride时可以认为是默认为1。

但是带有步进的切片常常会引发意外的效果，使程序出现bug。步进stride值可以取负数，因此可以做到bytes字符串、Unicode字符串反转等操作，但是stride不能取0，会报ValueError错误。如果正常使用时，同时含有起止下标和步进值，会让切片比较难看懂，尤其是步进值为负数的时候。所以，应当尽量避免把起止下标和步进值同时放入切片，而可以考虑分两次（一次隔位选取，一次切割）来写，也可以用itertools内置模块的islice方法，因为它的起止位置和步进值都不能为负值。

范例代码：

```python
>>>from itertools import islice

>>>a = 'world'

>>>a[::2]
'wrd'

>>>a[::-1]
'dlrow'

>>>a[2::-2]
'rw'

>>>list(islice(a, 0, 5, 2))
['w', 'r', 'd']
```



### 第13条 通过带星号的unpacking操作来捕获多个元素，不要用切片

基本的unpacking操作（见第6条）有一项限制，就是需要确定拆解的序列长度才能把其中的值拆分给变量，而有时候我们只是需要其中的某一个值，不需要把所有值都拆分出来。而unpacking操作还可以使用带`*`的表达式来捕获多个值，而不需要使用多个切片的语句。

需要注意的有以下几点：

- 使用带`*`的unpacking操作时，至少要要有一个普通的接收变量搭配，否则报SyntaxError。
- 对单层结构来说，同一级最多只能有一个带`*`的unpacking。对于多层结构，不同层级部分可以出现带`*`的unpacking。
- 带`*`的unpacking表达式会形成一份列表实例，其有可能为空。当要拆分的序列数据量非常庞大时，要确定系统有足够的内存存储拆分出来的数据，再进行带`*`的unpacking操作，否则可能耗尽计算机的内存导致程序崩溃。

范例代码：

```python
>>>num = [1, 2, 3, 4, 5]
>>>book_dict = {'Effective Python': ('Brett Slatkin', 'Python', 129), 'Python classic example': ('Steven F. Lott', 'Python', 139), 'Python Crawler': ('Cui Qingcai', 99)}

>>>min_num, *others, max_num = num
>>>print(min_num, others, max_num)
1 [2, 3, 4] 5

>>>*others = num  # 第一点
  File "<input>", line 1
SyntaxError: starred assignment target must be in a list or tuple

>>>first, *middle1, *middle2, last = num  # 第二点
  File "<input>", line 1
SyntaxError: multiple starred expressions in assignment
```



### 第14条 用sort方法的key参数来表示复杂的排序逻辑

Python中的sort函数可以给列表排序（默认为升序），前提是列表中的元素是具备自然顺序的内置类型，如：字符串、整数、浮点数。而对于一般的类的对象构成的列表，如果这个类像整数一样具有自然顺序，那么可以定义一些特殊的方法（见第73条），使其可以像整数、字符串那样直接调用sort函数进行排序；否则一般情况下就是针对对象中某一属性进行排序，把这样的排序逻辑定义成函数传给sort方法的key参数，再以该标准排序。

下面的代码分别实现了不同的排序情况：

- 按类某一指标进行排序
- 按类的多个指标进行同向排序

```python
class Student:
    def __init__(self, name, stuid, weight):
        self.name = name
        self.stuid = stuid
        self.weight = weight
    
    def __repr__(self):  # __repr__只是用于显示对象信息
        return f'Student {self.name}\'s ID is {self.stuid}'
    
>>>p = [
    Student('Tom', '001', 120),
    Student('Lisa', '002', 115),
    Student('Jack', '003', 117),
    Student('Peter', '004', 120),
    Student('Lisa', '005', 104)
       ]

>>>p.sort(key = lambda x: x.name)  #以姓名为标准给对象排序
>>>
[Student Jack's ID is 003,
 Student Lisa's ID is 002,
 Student Peter's ID is 004,
 Student Tom's ID is 001]

>>>p.sort(key = lambda x: (x.name, x.stuid))


```



### 第15条 不要过分依赖给字典添加条目时所用的顺序

从Python 3.7版开始，迭代标准的字典的顺序与键值插入字典时的顺序一致，而早期的版本则没有这个特性。

在Python代码中，很容易定义跟标准字典很像但本身不是dict实例的对象，对于这种对象，不能保证迭代的顺序与插入时的顺序一致。因此编写代码时需要注意：

- 不要依赖插入时的顺序编写代码
- 在程序运行时明确判断它是否是标准字典
- 给代码添加类型注解并静态分析



### 第16条 用get处理键不在字典中的情况，不要使用in与KeyError

字典的三种基本操作：访问、赋值及删除键值对。在处理键不在字典中的情况时，有四种方法：

- 用in表达式判断
- 抛出KeyError异常
- 利用get方法
- 利用setdefault方法

前两种方法没有后两种更简单，而如果与键关联的值是像计数器这样的基本类型，那么用get是最好的方案；如果是构造开销较大或容易出异常的类型，那么可以把这个方法与赋值表达式结合使用。

此外即使看上去最应该使用setdefault方案，也不一定要真的使用setdefault方案，而是可以考虑用defaultdict取代普通的dict。

### 第17条 用defaultdict处理内部状态中缺失的元素，而不要用setdefault

如果管理的字典需要添加任意的键，则应该考虑是否用内置的collections模块的defaultdict实例来解决问题。

### 第18条 学会利用\_\_missing\_\_构造依赖键的默认值



## 第3章：函数

### 第19条 不要把函数返回的多个数值拆分到三个以上的变量中

### 第20条 遇到意外状况时应该抛出异常，不要返回None

### 第21条 了解如何在闭包里面使用外围作用域中的变量

### 第22条 用数量可变的位置参数给函数设计清晰的参数列表

### 第23条 用关键字参数来表示可选的行为

### 第24条 用None和docstring来描述默认值会变的参数

### 第25条 用只能以关键字指定和只能按位置传入的参数来设计

### 第26条 用functools.wraps定义函数修饰器

## 第4章：推导与生成

### 第27条 用列表推导取代map与filter

### 第28条 控制推导逻辑的子表达式不要超过两个

### 第29条 用赋值表达式消除推导中的重复代码

### 第30条 不要让函数直接返回列表，应该让它逐个生成列表里的值

### 第31条 谨慎地迭代函数所收到的参数

### 第32条 考虑用生成器表达式改写数据量较大的列表推导

### 第33条 通过yield from 把多个生成器连起来用

### 第34条 不要用send给生成器注入数据

### 第35条 不要通过throw变换生成器的状态

### 第36条 考虑用itertools拼装迭代器与生成器

## 第5章：类与接口

### 第37条 用组合起来的类来实现多层结构，不要用嵌套的内置类型

### 第38条 让简单的接口接受函数，而不是类的实例

### 第39条 通过@classmethod多态来构造同一体系中的各类对象

### 第40条 通过super初始化超类

### 第41条 考虑用max-in类来表示可组合的功能

### 第42条 优化考虑用public属性表示应受保护的数据，不要用private属性表示

### 第43条 自定义的容器类型应该从collections.abc继承

## 第6章：元类与属性

第44

## 第7章：并发与并行

## 第8章：稳定与性能

## 第9章：测试与调试

## 第10章：协作开发