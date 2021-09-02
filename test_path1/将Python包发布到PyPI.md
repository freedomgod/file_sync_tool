# 将Python包发布到PyPI

参考了很多网上的文章，发现要准备的文件或者说目录结构都有不同，除了核心代码那部分，不同文章中有的文件是没有的，而其他地方又需要这些。

所以我还不清楚具体需要准备什么，于是直接找到了官方的一个教程。以我自己的两个机器学习的程序为例，打包步骤整理如下：

1. 整理项目结构
   给出的例子是一个名为`example_pkg`的包，将包整理成如下的结构。具体的结构不需要和下例一样。

   ```python
   packaging_tutorial/
   └── src/
       └── example_pkg/
           └── __init__.py
   ```

   注意这里是需要`__init__.py`文件的，因为只有含有这个文件时Python才会把这个目录视为一个包。在最简单的情况下，`__init__.py`文件可以是空的，但是一般它被用来将包初始化或者设置`__all__`变量。

   如果没有`__init__.py`文件，可以参考下面文件的编写。

2. `__init__.py`文件的编写
   ①可以直接留空
   ②文件中定义`__all__`变量，为一字符串列表，用于说明使用`import *`时要导入的所有模块

3. 创建包文件
   创建其他发布包所需要的文件，如下：

   ```python
   packaging_tutorial/
   ├── LICENSE
   ├── pyproject.toml
   ├── README.md
   ├── setup.cfg
   ├── src/
   │   └── example_pkg/
   │       └── __init__.py
   └── tests/
   ```

4. 测试文件
   用于测试程序，可以自己写文件。

5. pyproject.toml文件
   这个文件到底是什么？官方文档中我看到的解释是：告诉构建工具（如pip和build）构建项目需要什么内容，一个示例是：

   ```python
   [build-system]
   requires = [
       "setuptools>=42",
       "wheel"
   ]
   build-backend = "setuptools.build_meta"
   ```

   关于这个文件我也不清楚。可以参考：https://python.freelycode.com/contribution/detail/1910

6. 配置元数据（metadata）
   元数据有两种：静态和动态

   - 静态（`setup.cfg`）：保证每次都是相同的。这种更简单，也更易于阅读，并且能避免很多一般的错误，如编码错误。
   - 动态（`setup.py`）：可能是非确定性的。任何动态或在安装时确定的项目以及扩展模块或setuptools的扩展，需要进入`setup.py`。

   具体的编写方法：

   - `setup.cfg`（static）
     `setup.cfg`是setuptools的配置文件，它告诉setuptools关于你的包（例如名称、版本）以及哪些代码文件包含在内。最终大部分这些配置可能会被移动到`pyproject.toml`文件
     以下是我编写的这个文件

     ```python
     [metadata]
     name = ML_example_packge
     version = 0.0.1
     author = wwhfree
     author_email = wwhfree@foxmail.com
     description = A small example package
     long_description = file: README.md
     long_description_content_type = text/markdown
     url = https://github.com/pypa/sampleproject
     project_urls =
         Bug Tracker = https://github.com/pypa/sampleproject/issues
     classifiers =
         Programming Language :: Python :: 3
         License :: OSI Approved :: MIT License
         Operating System :: OS Independent
     
     [options]
     package_dir =
         = src
     packages = find:
     python_requires = >=3.6
     
     [options.packages.find]
     where = src
     ```

     - name：包分发的名称。可以是任何包含字符、数字、下划线和`-`的名称。而且必须是在PyPI上还没使用的名称。

     - version：包的版本。有关版本的更多细节可以参阅[PEP 440](https://www.python.org/dev/peps/pep-0440)。

     - author、author_email：用于标识作者。

     - description：包的一个简短的摘要。

     - long_description：包的详细的描述。这会显示在PyPI的包的详细页面中。

     - long_description_content_type：告诉索引用于long_description的标记类型的标记，这种情况下是Markdown。

     - url：是项目的主页。

     - project_urls：可以列出任意链接展示在PyPI上。通常可能是文档链接之类的。

     - classifiers：分类器。分类器为索引和PIP提供一些关于包的额外元数据。在这种情况下，该包只与Python 3兼容，使用MIT许可，并且是与操作系统独立的。应该始终至少包含包可工作的Python版本，包可在哪个许可下使用，以及包将工作在哪个操作系统上。


       在options选项中，控制setuptools本身：

     - package_dir：包名称和目录的映射。 空包名称表示“root包” - 项目中包含包的所有Python源文件的目录 - 因此在这种情况下，src目录被指定为根包。

     - packages：应该包含在分发包中的所有Python导入包的列表。我们可以使用`find:`指令来自动发现所有的包和子包，并使用`options.packages.find`来指定要使用的包的目录，而不是手动列出每个包。

     - python_requires：提供了项目所支持的python版本。像pip这样的安装程序会回顾旧版本的包，直到找到匹配的Python版本。

   - `setup.py`（dynamic）
     `setup.py`是setuptools的编译脚本。它告诉setuptools关于包的一些信息。

     ```python
     import setuptools
     
     with open("README.md", "r", encoding="utf-8") as fh:
         long_description = fh.read()
     
     setuptools.setup(
         name="example-pkg-YOUR-USERNAME-HERE",
         version="0.0.1",
         author="Example Author",
         author_email="author@example.com",
         description="A small example package",
         long_description=long_description,
         long_description_content_type="text/markdown",
         url="https://github.com/pypa/sampleproject",
         project_urls={
             "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
         },
         classifiers=[
             "Programming Language :: Python :: 3",
             "License :: OSI Approved :: MIT License",
             "Operating System :: OS Independent",
         ],
         package_dir={"": "src"},
         packages=setuptools.find_packages(where="src"),
         python_requires=">=3.6",
     )
     ```

   7. 创建README.md文件
      这个文件想必就比较熟悉了，很多地方都能见到这个文件。主要是写一些对包的说明。由于配置加载README.md提供了long_description，因此必须在生成源分发时与代码一起包含README.md。 较新版本的stuptools会自动执行此操作。

   8. 创建LICENSE许可证文件
      许可证对于每个上传到PyPI的包都非常重要。 这告诉那些安装你的包的用户需要使用你的包的条款。 有关选择许可证的帮助，请参阅https://choosealicense.com/。 一旦选择许可证后，打开许可证并输入许可证文本。 

