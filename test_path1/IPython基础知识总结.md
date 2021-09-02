# IPython基础知识总结

## 1.简介

IPython是一个增强的Python解释器，相比于标准Python，它有非常多的优点，这里结合自身的使用总结列出了一些：

- 语法突出显示

- 有强大的交互式shell，并能方便的执行shell命令
- 支持Tab自动补全
- 通过一系列魔法命令或语法能够快速获取类、函数信息

学习IPython少不了Jupyter，推荐使用JupyterLab而不是JupyterNotebook，因为JupyterLab可谓是增强版的notebook，拥有JupyterNotebook的所有功能。

## 2.用法总结

### 2.1 运行IPython命令行

启动标准python解释器只需在命令行输入`python`，而启动IPython只需输入`ipython`，然后所有你想运行的命令几乎和在标准python中是一样的。如果想查看某个变量的值，不需要print，直接输入变量名就能看到被格式化的值，要比直接print更为美观。

```python
$ ipython
Python 3.9.2 (tags/v3.9.2:1a79785, Feb 19 2021, 13:44:55) [MSC v.1928 64 bit (AMD64)]
Type 'copyright', 'credits' or 'license' for more information
IPython 7.22.0 -- An enhanced Interactive Python. Type '?' for help.

In [1]: import numpy as np

In [2]: sample = {i : np.random.randn() for i in range(5)}

In [3]: sample
Out[3]:
{0: -0.9589600514703817,
 1: 0.8946231513135603,
 2: -0.8710720078167812,
 3: 1.0476440988079867,
 4: 0.02542113081227873}

In [4]: print(sample)
{0: -0.9589600514703817, 1: 0.8946231513135603, 2: -0.8710720078167812, 3: 1.0476440988079867, 4: 0.02542113081227873}
```



### 2.2 运行JupyterLab

有关JupyterLab的安装可以在网络上找到很多，也可以去[Try Jupyter](https://hub.gke2.mybinder.org/user/jupyterlab-jupyterlab-demo-pnuiwdsm/lab/tree/demo)这个网站试试在线的Jupyterlab，当然可能运行会慢些，因此还是建议本地安装一下。

启动JupyterLab只需在你想要的文件夹路径下打开命令终端，输入`jupyter lab`就可以运行JupyterLab。然后会自动打开你的默认浏览器（除非使用`--no-browser`命令）显示JupyterLab的界面。

![20210902101347](http://img.whfree.top/20210902101347.png)

你可以在这新建ipynb文件，然后执行你想要运行的所有命令，体验是很不错的，以后熟悉了会有更高的效率。

### 2.3 Tab补全

相较于标准Python命令行，IPython的提升之一就是tab补全功能，一般这个功能在IDE或者其他交互式计算分析环境才有。

当在命令行输入代码时，按Tab键即可为任意变量搜索命名空间，匹配已输入的字符。

![image-20210902104538936](http://img.whfree.top/image-20210902104538936.png)

### 2.4 内省

在一个变量名的前后使用`?`可以显示关于该对象的概要信息；如果是函数或实例方法，还会显示出文档字符串，双问号`??`会显示函数源码。这在一些需要调试程序的情况下非常有用。`?`还有一个用途是像标准Unix或Windows命令行一样搜索IPython命名空间。

![20210902110423](http://img.whfree.top/20210902110423.png)

### 2.5 %run命令

在IPython中可以使用`%run`命令运行任意Python程序，当然路径要对。比如`%run test.py`，运行后，文件中定义的所有变量（导入的、函数中的、全局定义的）都可以在IPython中使用。如果程序需要提供参数，则需要在命令行的文件路径后加上参数进行传递。

如果想将脚本导入到代码单元中，可以使用`%load`魔术函数，如`%load test.py`



### 2.6 执行剪贴板命令

在IPython中可以直接运行剪贴板中的代码，只需要使用`%paste`和`%cpaste`魔术函数。`%cpaste`与`%paste`不同的是，它可以让你剪贴多段代码并作一些修正，然后再运行。

而这两个魔术命令貌似在Jupyter中不能使用，会报错`UsageError: Line magic function %paste not found.`。只能在IPython控制台中使用。

### 2.7 终端快捷键

下表中总结了IPython常用的快捷键：

| 快捷键            | 描述                                 |
| ----------------- | ------------------------------------ |
| Ctrl-P 或向上箭头 | 以当前输入内容开始，向后搜索历史命令 |
| Ctrl-N 或向下箭头 | 以当前输入内容开始，向前搜索历史命令 |
| Ctrl-R            | 按行读取的反向历史搜索（部分匹配）   |
| Ctrl-Shift-V      | 从剪贴板粘贴文本                     |
| Ctrl-C            | 中断当前执行的代码                   |
| Ctrl-A            | 将光标移动到本行起始位置             |
| Ctrl-E            | 将光标移动到本行结束位置             |
| Ctrl-K            | 删除光标后本行的所有内容             |
| Ctrl-U            | 删除当前行                           |
| Ctrl-F            | 将光标向前移动一个字符               |
| Ctrl-B            | 将光标向后移动一个字符               |
| Ctrl-L            | 清除本屏内容                         |



### 2.8 魔术命令

IPython的特殊命令（在Python中不可用）被称为魔术命令。这些命令被设计用于简化任务。魔术命令的前缀符为`%`或`%%`。一个百分号的可以叫做行魔术命令（Line Magics），表示只作用于一行；而两个百分号的叫做单元魔术命令（Cell Magics），作用于一个单元格（Cell）。魔术命令可以看作是IPython系统内部的命令行程序，大多数魔术命令可以用?查看额外的命令行选项。

```python
In [1]: %pwd?
Docstring:
Return the current working directory path.

Examples
--------
::

  In [9]: pwd
  Out[9]: '/home/tsuser/sprint/ipython'
File:      d:\python39\lib\site-packages\ipython\core\magics\osm.py
```

此外，魔术函数也可以不加百分号%就使用，只要没有变量被定义为与魔术函数相同的名字。这种特性被称为自动魔术，通过`%automagic`进行启用或禁用。一些魔术函数也可以赋给一个变量。

```python
In [1]: %automagic
Automagic is OFF, % prefix IS needed for line magics.

In [2]: path = %pwd
In [3]: path
Out[3]: 'C:\\Users\\DELL\\Desktop\\learn'
```

IPython提供的魔术命令真的很多，可以使用`%quickref`或`magic`、`lsmagic`查看所有魔术命令。下面列举一些较为常用的命令：

| 命令        | 描述                                                         | 举例                             |
| ----------- | ------------------------------------------------------------ | -------------------------------- |
| %debug      | 从最后发生报错的底部进入交互式调试器                         |                                  |
| %hist       | 打印命令输入（也可以打印输出）历史                           |                                  |
| %timeit     | 多次运行语句，计算平均执行时间，也可加一个%计算单元的执行时间 | %timeit [i for i in range(1000)] |
| %reset      | 删除交互式命名空间中的所有变量/名称                          |                                  |
| %pwd        | 显示当前工作目录                                             |                                  |
| %cd         | 修改当前工作目录                                             |                                  |
| %matplotlib | 设置matplotlib以交互式方式工作                               | %matplotlib inline               |
| %load       | 从脚本文件中加载代码到前端                                   | %load test.py                    |
| %xdel       | 删除某个变量                                                 | %xdel a                          |
| %who、%whos | 展示命名空间中定义的变量                                     | %who int、<br />%whos            |

以下是用的不多的单元魔术方法，看到了也就列出来。

| 命令         | 描述                     | 举例                 |
| ------------ | ------------------------ | -------------------- |
| %%HTML       | 将单元格渲染为HTML输出   |                      |
| %%javascript | 运行JavaScript           |                      |
| %%latex      | 渲染为LaTeX              |                      |
| %%markdown   | 渲染为markdown           |                      |
| %%writefile  | 将单元格内容写入指定文件 | %%writefile test.txt |