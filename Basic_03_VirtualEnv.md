# 如何管理多个python环境才不会乱

前面的文章中，为大家介绍过一个脚本，可以自动安装一些数据分析常用的Python依赖。但是，为了让系统里面的Python环境不会变得越来越乱，一般我们会把依赖库安装到Python虚拟环境里面。今天的这篇文章就简单介绍下，Python下的虚拟环境和包管理。

## Python环境

###  Python环境的不同级别

一般我们默认安装Ubuntu后，在系统上就有Python2和Python3两种不同版本。Python2主要是用来运行系统相关或历史遗留的一些工具，而Python3是我们以后真正会使用的版本。通过`which python3`可以得知目前系统里安装的Python3的版本。

系统级别的Python3可执行程序在`/usr/bin/`下，对应账户`root`。依赖库安装的路径是`/usr/lib/python3/dist-packages`，而当前用户目录下也有`~/.local/lib/python3.6/site-packages`。根据我们用什么用户安装库，Python也会安装到对应账户路径下。
> 特别注意，`dist-packages`是Debian/Ubuntu下使用的命名，表示其中的库属于系统使用，一般通过系统的命令进行安装和卸载，与Python下管理的`site-packages`区别开。

除了上述的Python环境外，还可以使用的Python环境就是虚拟环境（Virtual environment）。虚拟环境是对Python环境进行隔离的机制，通过每个互相不影响的Python虚拟环境，我们可以让系统的Python环境尽量少的去安装各个项目所特有的依赖，避免系统Python环境受到污染。

### Python虚拟环境

因为以后大家都只会用Python3，Python的虚拟环境就是`pyvenv`（命令是`venv`）。下面简单介绍虚拟环境相关的操作。

- 建立

建立虚拟环境命令：
```
python3 -m venv venv_test
```
这里，`python3 -m`是启用某个Python3模块命令，命令中的第一个`venv`表示使用`venv`这个命令来建立虚拟环境。`venv_test`是虚拟环境的名字，这里只为简单演示。实际工作中，建议起的名字符合一定规律，比如`venv_projectname_os`,具体可以是`venv_crftest_lin`。后面的操作系统是为不混淆不同系统下的虚拟环境。因为不同系统的可执行文件和运行机制完全不同，所以相应虚拟环境也不可能通用。

我们可以观察，命令会自动建立一个`venv_test`的文件夹，下面内容有：
```
ls venv_test 
bin  include  lib  lib64  pyvenv.cfg  share
```
在`bin`目录中，就存在`python`等常用的可执行命令：
```
activate      activate.fish  easy_install-3.6  pip3    python
activate.csh  easy_install   pip               pip3.6  python3
```

- 激活

激活一个虚拟环境，就需要用`bin`下的`activate`：
```
source venv_test/bin/activate
```
其中，`venv_test`是虚拟环境的名称。

> 很多文章里面还一直提`virtualenv`，这个虚拟环境工具的主要优势是支持Python2，劣势是建立环境比较慢。

激活后，可以用`which python`确认是否成功。如果成功，当前`python`应该指向的是`venv_test/bin/python`

- 安装依赖

激活一个环境后，安装依赖就和普通Python环境下操作没太有什么区别：
```
python -m pip install  xxx
```
这里有个细节，只要是相对虚拟环境操作，就不需要用`python3`，而应该是`python`。另外，就是`python -m pip`比直接敲`pip`更规范，有保障，可以明确当前`python`和当前执行的`pip`的对应关系。不注意这方面，就特别容易导致一些环境中装的很杂乱的依赖。

- 退出

直接运行`deactivate`，然后可以通过`which python`来确认。

## 实践

### 依赖库镜像

众所周知，安装Python依赖库的速度不快。我们需要设置镜像。Linux建立文件` ~/.pip/pip.conf `，输入内容如下：
```
[global]
trusted-host=mirrors.ustc.edu.cn
                pypi.tuan.tsinghua.edu.cn
                mirrors.aliyun.com
                pypi.douban.com
                pypi.python.org
index-url=https://pypi.tuna.tsinghua.edu.cn/simple
extra-index-url=http://mirrors.aliyun.com/pypi/simple
            https://mirrors.ustc.edu.cn/pypi/web/simple/
            http://pypi.douban.com/simple/
            https://pypi.python.org/pypi/
timeout = 20
require-virtualenv = false
format=columns 

[install]
use-mirrors = true
mirrors = http://pypi.douban.com/simple/
```
这里的配置启用了多个镜像服务器，可有效加速依赖安装速度。

> Windows下同样可以使用相同配置，但要在 user 目录中创建一个 pip 目录，如：`C:\Users\xx\pip`，新建文件 pip.ini，内容同`pip.conf`

如果不想设置文件，也可以通过命令临时使用镜像。例如，`python -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple xxx`

### 文件夹结构

一个好的项目结构，会让使用者心情愉悦头脑清晰。通过观察许多开源项目，以及自己工作实践，和Python环境相关的一些常见的习惯如下：

- requirements文件

如果只有一个`requirements.txt`， 可以直接放在项目根目录下，比较容易找到。如果有多个，建议放在`deps`文件夹。同时，考虑一些习惯命名，比如开发者使用`requirements-dev.txt`。

另外，多个`requirements`之间可以存在引用关系。一般来说，普通用户需要的依赖，开发者也需要。这时的`requirements-dev.txt`可以这样写：
```
-r requirements.txt

# development specific requirements
...
sphinx
sphinx-rtd-theme
wheel
...
```
此时，我们只需要在相应文件里更新各自考虑的特殊需求，只写上自己独有的那部分依赖即可。

### 虚拟环境导出

虚拟环境直接拷贝使用，经常会有问题出现。需要虚拟环境可以把当前依赖信息导出，命令如下：
```
python -m pip freeze  > requirements.txt 
```
这里，推荐在熟悉的情况下，去掉二级依赖库(依赖的依赖)。一方面减少文件内容，第二有可能二级依赖在后面会被取消。

通过Python的原生生态，我们可以很方便的管理环境和依赖。但因为Python安装软件时缺少对版本和冲突的严格控制，而这方面`anaconda`的包管理采取了很多措施去解决这种问题。下一篇，我们将介绍`anaconda和`conda下的虚拟环境。
