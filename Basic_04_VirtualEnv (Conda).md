# 最流行的Python环境——conda

前面的文章中，为大家介绍过Python下的虚拟环境和包管理。在实际中，更为流行的是用Conda来管理Python环境。今天这篇文章就为大家介绍这方面的相关内容。

## Conda环境

###  Conda简介

Conda是目前为止，最流行的Python软件包与管理环境。Conda分为 `miniconda` 与 `anaconda` 两种。前者从名字上就能猜出是精简版，后者预装了很多常用的功能，但比较臃肿。实际工程中，一般都使用 `miniconda`，按需安装软件包，本文的下面篇幅也以 `miniconda` 为例进行说明。

### Conda安装

首先利用`wget`下载安装脚本文件：
```
wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
```

> 如果速度较慢，可以换用`axel`或`aria2c`下载

利用`chmod`命令修改sh文件为可执行文件，然后运行安装脚本：

```
chmod 755 Miniconda3-latest-Linux-x86_64.sh
bash ./Miniconda3-latest-Linux-x86_64.sh
```

在出现的提示界面中，根据提示选择yes或no。一般来说，我们保持默认即可，但需要留意下最后一步会自动在`.bashrc`文件添加`conda`的`PATH`路径。如果`conda`的环境存在与你日常使用的程序有冲突的命令，就有可能会出现问题。

当然，还有一种方式是在添加`PATH`路径时选择no，然后在每次需要conda的时候手动找到conda下的`active`命令激活下。这种方式比较灵活，如果不嫌麻烦建议使用这种方式。

> 注意不要把激活conda与激活虚拟环境搞混。

### Conda常用命令

在`conda`环境中，常用的命令格式为：

```
conda [命令 [参数]] 
```

#### 包管理

与`python -m pip list`类似，conda可以列出当前环境下的所有包：

```
conda list
```

#### 版本与升级

`conda`有一套特别的机制，用于管理和维护依赖库之间的关系。在不同版本的`conda`中，我们可以直接使用的Python与依赖库的版本都不同，为了确定当前使用的`conda`版本，可以运行以下命令：

```
conda --version
```

有时，我们想用的某个库在`conda`中有问题，或者默认模块安装的版本比较旧，可以先尝试升级解决：

```
conda update conda
```

#### 环境管理

`conda`环境中的虚拟环境比起原生Python更为强大，**可以指定Python的版本**，并自动安装相关的C++依赖库（Windows下自动下载相关的c++ runtime）。


- 建立
 

建立虚拟环境命令：
```
conda create -n env_demo 
```
如果要指定python版本，同时指定虚拟环境生成的路径，可以这样：

```
conda create   python=3.6  -p /tmp/test
```

这样，Conda就为你生成了一个在`/tmp/`下叫`test`的虚拟环境，并且环境里的python版本是`3.6`。

> `conda create`默认并不会把基础环境的依赖复制给新建的虚拟环境。如果要实现类似的依赖复制，需要加参数`--clone`，例如`conda create -n test3 --clone base`

我们也看一下这个路径下的内容：

```
ls /tmp/test
bin  conda-meta  include  lib  share  ssl
```
在`bin`目录中，就存在`python`等常用的可执行命令：
```
2to3              idle3    pydoc3     python3.6-config   pyvenv-3.6  wish8.5
2to3-3.6          idle3.6  pydoc3.6   python3.6m         sqlite3     xz
c_rehash          openssl  python     python3.6m-config  tclsh8.5
easy_install      pip      python3    python3-config     unxz
easy_install-3.6  pydoc    python3.6  pyvenv             wheel
```

> 因为这里是虚拟环境的`bin`目录，所以没有`conda`、`activate`等命令。这些命令都在当前conda默认的`bin`目录中。

- 激活

激活一个虚拟环境，就需要用`bin`下的`activate`：
```
source venv_test/bin/activate
```
其中，`venv_test`是虚拟环境的名称。

激活后，可以用`which python`确认是否成功。如果成功，当前`python`应该指向的是`venv_test/bin/python`

- 安装依赖
  

激活一个Conda的虚拟环境后，安装依赖主要用以下命令：

```
conda install xxx
```

这条命令主要从默认的频道中去寻找xxx软件包。比如，我们可以用`conda install pandas`来安装`pandas`软件包。要注意，Conda里有频道的概念，类似电视机买回来一般都有个默认频道一样，默认的Conda有一个`defaults`的频道。如果我们需要更多的下载源，就需要和加入Ubuntu软件源类似，加入Conda频道：

```
conda config --add channels conda-forge
```

如果大家还记得上次文章，里面给大家介绍了Python的pip安装时怎么配置镜像地址来加速国内下载速度。同样的操作在Conda里面，则是通过配置频道来实现。比如，我们添加清华的Conda镜像：

```
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
```

配置完成后，可以通过下面命令来确认是否配置成功：

```
conda config --show
```

当然，更直接的是直接下载一个依赖库，看实际下载速度怎么样。另外，也可以在`conda install`的同时，显式的指定频道：

```
conda install --prefix=/tmp/miniconda3/pyenv/py36 --channel https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/pytorch/ pytorch torchvision cuda91 -c pytorch
```

Conda不仅仅可以用`conda install`安装软件，同时也可以继续用`pip`，就和普通Python环境下操作没太有什么区别：

```
python -m pip install  xxx
```
> 并不是所有的软件都可以用pip安装。最佳实践是只在conda找不到包时，才用`pip`安装。不要使用`user`参数，避免权限问题。

- 退出

直接运行`conda deactivate`，然后可以通过`which python`来确认。

### Conda环境导出与恢复

Conda支持直接导出环境，命令如下：

```
conda env export > env.yml
```

这里，推荐在熟悉的情况下，去掉二级依赖库(依赖的依赖)。一方面减少文件内容，第二有可能二级依赖在后面会被取消。

环境恢复使用命令：

```
conda env create -n revtest -f=/tmp/env.yml
```

这里比较关键是导出的yaml文件，通过编译器查看可知，其是一个标准的yaml文件。里面主要包括：

```
name: 环境名字
channels：
 - 频道urls
 ……
dependencies：
 - 软件名=版本号=编译环境
prefix：环境路径
```

- Conda环境包含pip依赖

上面的环境依赖都是conda自己就可以安装，如果所需要的依赖正好没有conda资源怎么办？其实，conda早就可以直接在环境里使用pip依赖：

```
name: hyperparam_example
channels:
  - defaults
dependencies:
  - python=3.6
  - numpy=1.14.3
  - pandas=0.22.0
  - scikit-learn=0.19.1
  - matplotlib=2.2.2
  - tensorflow-mkl==1.13.1
  - keras==2.2.2
  - pip:
    - mlflow>=1.0
    - Gpy==1.9.2
    - GpyOpt==1.2.5
    - pyDOE==0.3.8
    - hyperopt==0.1
```

这个环境文件参考自mlflow项目（https://github.com/mlflow/mlflow/blob/master/examples/hyperparam/conda.yaml），从这里我们就可以看到两点：

- 利用conda就可以同时管理好conda和pip依赖
- conda 的环境管理，已经成为一种标准，被mlflow这样的项目所使用。

那么最后一个问题，conda和pip到底有什么不同？

- conda还负责依赖检查和维护。Conda不仅仅安装Python库这么简单，他还能把Python库需要的外部依赖也同时安装进来，并且维护每个软件库对应的各种依赖版本关系，每次conda安装都要进行比较复杂的处理来维护好依赖关系。
- conda这个包管理命令不仅仅可以用在Python上，还可以用来管理R等其他语言。
- 不能提供egg或whl时，pip只能从源代码编译。而`conda install`一直都是安装编译好的二进制。
- conda默认就支持虚拟环境；而pip是靠`virtualenv`或`venv`来支持
- conda是Python的外部工具
- conda的托管网站是Anaconda，而pip的托管网站是PyPI（https://pypi.org/）