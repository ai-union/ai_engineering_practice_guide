# 万万没想到，用Shell脚本做AI批处理，真香

前面两篇文章已经为大家介绍了Linux的Shell命令相关的知识，我们已经可以在命令行下单独的完成一些操作。但在实际工作中，我们通常还需要利用这些命令，结合一些逻辑控制编写AI批处理脚本。

本篇文章就来介绍Shell脚本编程。因为bash是目前最常见的Shell环境，下文都将以bash为例进行介绍。

## 脚本基础

###  编写脚本文件

Shell脚本文件本质就是一个纯文本文件，只要把我们常用的txt文件的后缀名改成sh，甚至不改（只要你自己不混淆就可以）就可以作为脚本文件来用。一般，sh脚本应注意以下几点：
首行的`shebang`符号：
```
#！/bin/bash
```
保存文件后，为方便脚本文件能直接和命令一样运行，需要执行`chmod +x file`。`shebang`的可执行权限的内容可以回顾专栏里的Linux命令（上）这篇文章（请插入链接）。

### 变量

- 定义赋值

定义Shell变量的形式为：变量名=变量值。例如：
```
PATH1="/tmp"
```
这里，注意变量名不能以数字开头，中间不能有空格和标点符号，以及Shell里面的一些关键字。变量值可以通过一条命令的结果动态赋值，例如：
```
PATH1=$(pwd)
```
注意，`pwd`是查看当前路径的命令，通过`$()`的形式，把里面`pwd`的结果直接赋值给`PATH1`。

- 使用变量

Shell中需要用`$变量名`的形式使用变量。结合前面所讲的定义赋值，我们可以使用一个已有变量的值，直接赋给另一个变量：
```
PATH1=$PWD
```
注意，`$PWD`是系统维护的环境变量，和`pwd`效果一致。

- 命令行参数

与很多命令行环境相似，Shell脚本需要对多个参数进行处理。我们编写脚本时，可以通过一些特殊的变量获取命令行参数。首先，我们先写一个脚本`testpara.sh`，内容如下：
```
#!/bin/bash

param1=$1
param2=$2
echo "Running :$0"
echo "Parameter1: $param1"
echo "Parameter1: $param2"
```
当我们运行`./testpara.sh p1 p2`后，显示结果如下：
```
Running:./testpara.sh
Parameter1: p1
Parameter1: p2
```
请注意，如果参数很多时，脚本最好支持缺省参数，这样就不用每个参数都必须写全。我们可以把`testpara.sh`略微改造下，支持缺省参数:
```
#!/bin/bash
param1=${1:-para1}
param2=${2:-para2}
echo "Running :$0"
echo "Parameter1: $param1"
echo "Parameter1: $param2"
```
我们直接运行命令`./testpara.sh`，看看不给参数值的效果：
```
Running :./testpara.sh
Parameter1: para1
Parameter1: para2
```
可以看到，参数的缺省值已经发挥作用。
>在实际的AI批处理脚本中，缺省参数也很实用。例如，一些超参数的设置经常会有一些默认的经验值，常见的训练集、验证集和测试集划分是`6:2:2`，tensorflow常用的版本号是`1.13.2`（因为1.14.0的`tf.keras`的卷积函数有一点Bug）。在这些场合灵活运用缺省参数，会提高我们的工作效率。

- 退出状态码

基本上所有命令在退出时，都会返回一个状态值，表示这条命令是否成功。类似于c里面的` int function`的`return 1`或`return 0`一样。在Linux中，一般定义0表示成功，非0表示失败。在Shell环境里，可以用`$?`获取上条命令的状态。例如，我们在成功执行`testpara.sh`后，可以运行`echo $?`，Shell这时返回了`0`，提示我们命令成功。

> 常见的非0码包括：127表示命令没找到，126表示不可执行。

###  逻辑控制

- if

Shell的if语句与其他语言的很类似，唯一需要注意的是语法，以及**与if成对的关键字fi**。我们通过`pip`命令来举例：
```
sudo pip3 install numpy

  if [ $? = 0 ]; then
    echo "Installation Successfully"
  else
    echo "Problems to install Essential packages, check this!"
    exit 1
  fi

```
注意，Shell脚本的语句段不需要括号包围。

> pip3 是指明使用与系统中python3想关联的pip命令安装。一般系统默认的pip指向pip2，即python2对应的pip命令。一种更推荐的的使用方式是`python -m pip install numpy`，这样可以避免混淆`python`和`pip`的关系。

- case

Shell中的case语句与其他语言的case也很相似，是多分支选择结构。注意，**与case对应的结束关键字是esac**。 我们来看一个判断输入数字的例子：
```
echo 'Please press a number to select options'
read num
case $num in
    1)  echo 'option 1'
    ;;
    2)  echo 'option 2'
    ;;
    3)  echo 'option 3'
    ;;
    *)   echo 'Other'
    ;;
esac
```
注意，`read`读取键盘输入，并保存在变量`num`中。同时，注意`case`语句选项的写法。

> 也许读者们已经发现，Shell的条件选择命令的结束词，都是该命令反过来拼写。比如`if`和`fi`，`case`和`esac`。

- 循环

上面的例子为我们展示了Shell中的多分支结构，但我们注意到这个脚本只能执行一次选择就退出。在其他语言中，我们可以使用循环不断重复这个选择过程。同样，Shell中可以这样实现：
```
echo 'Input a number（press q to quit）'
read num
while [ $num != "q" ];do
    case $num in
        1)  echo 'option 1'
            ;;
        2)  echo 'option 2'
            ;;
        3)  echo 'option 3'
            ;;
        *)   echo 'Other'
            ;;
    esac
    echo 'Input a number'
    read num
done
```
这里特别注意，`while`中的`do`其实需要另起一行，上面的例子是通过`;`把两行合并在一行，显的紧凑。同时，为了脚本不会死循环，设置了`q`作为退出键。最后的`done`是`while ;do`的结束词。

编程语言中还有`for`循环，适合迭代执行：
```
for ((i=1;i<=5;i++))
do   
    echo $i
done
```
另外，`for`语句更好用的是后面跟一个数组形式的参数，类似python中的list。数组可以是数字组成的序列：
```
for i in $(seq 1 5) 
do   
   echo $i
done   
```
这里的`seq`命令可以生成`1`到`5`的序列，等价于`{1..5}`。在批处理时，我们经常需要对多个文件进行处理，可以使用`ls`返回一个文件名的序列，作为`for`的参数：
```
for i in `ls`
do   
   echo $i 
done  
```
当我们知道一个路径的一部分，还可以通过通配符进行遍历，迭代每个符合的路径：
```
for file in /tmp/*  
do  
    echo $file  
done  
```
> `for in`这种形式，非常类似python中的形式。可以利用各种函数或命令来构造循环迭代。另外，循环命令的执行体是`do`开头，`done`结尾，这点需要与`if`和`case`的反写结尾区分开。

### 函数

Shell中支持用户自定义函数，形式如下：
```
[ function ] funname [()]

{

    XXXXX;

    [return int;]

}
```
这里，方括号表示可选内容。即`function`关键词可以省略，直接写`函数名()`就可以定义：
```
test(){
 echo hello
}

test
```
特别注意的是，函数也支持参数，使用`$1`、`$2`等变量进行处理。

## 应用示例

### 配置python环境

开发环境中的配置，是个琐碎机械的工作。使用批处理进行环境配置，是脚本编程最常使用的场景。这里我引用一个小的项目`prashant2018/MLSetup`中的脚本，可以通过下面命令下载：
```
wget https://raw.githubusercontent.com/prashant2018/MLSetup/master/MLSetup_python3.sh
```
该脚本的使用方法很简单，可以给出一个模块的名字,单个安装；也可以直接给`all`，进行批量的全部安装：
```
./MLSetup_python3.sh numpy
./MLSetup_python3.sh pandas
./MLSetup_python3.sh all
```
这个脚本提供了一键安装包括`numpy`等多种常用python库的功能，综合运用了本篇文章讲解的命令行参数、退出状态码、`case`和函数多个知识点。请读者仔细研究，模仿其中写法。

### 文本标注

这里介绍作者以前实际工作中涉及到的一个小实验。我们使用CRF对地址文本进行识别，把相应的省、市、区、街道等等实体提取出来。在NLP中，这种任务属于命名实体识别（NER），完成NER任务所使用的模型是条件随机场（CRF）。

> CRF是统计机器学习中的经典序列标注方法。关于CRF的更多介绍可以查阅文末给出的参考资料。若需要更多相关理论方面的介绍可以直接阅读李航老师的《统计机器学习》一书。

- 安装依赖库

我使用的CRF工具来源于`taku910/crfpp`项目。crfpp本身是C++库，也通过Swig提供了Python的封装库，但是安装过程复杂。为了方便起见，我将其重新封装成标准的扩展模块`crfpy`，可以通过`pip install crfpy`直接安装好。除了`crf_test`命令暂时没加进来，其他都与原`crfpp`相同。

整个脚本文件在文末给出的代码仓库中的`src/basic-02-shell/crf/`位置，文件名为`
do.sh`

- 数据处理

首先，为了让脚本出错后就终止运行，方便查看问题，需要在脚本的起始位置（`shebang`行后的第一个非注释行）设置：
```
set -e
```
我使用了`libpostal`项目中分享的部分中文地址开源数据，从中截取了1000条记录作为整个数据集 ( 就是用的`head`命令 )，另存为了`allchina_addr.txt`。在这个文件里面，前两列都是国家和语言，只有最后一列才是需要的标注信息。通过`awk`命令对原数据进行提取：
```
cat allchina_addr.txt| awk '{$1=""}{$2=""}1'> input.data
```
通过`shuf`命令对数据集进行打散：
```
shuf input.data > shuffled_input
```
- 划分数据集

按照7:3的比例，对数据集划分训练集和测试集：
```
split -l $[ $(wc -l shuffled_input|cut -d" " -f1) * 70 / 100 ] \
	shuffled_input crfdata_
mv crfdata_aa train.txt
mv crfdata_ab test.txt
```
因为这个数据集的标注格式和`crfpp`要求的不同，所以我准备了`make_crfpp_data.py`这个脚本进行转换:
```
echo converting
./make_crfpp_data.py -i train.txt -o  train.data
./make_crfpp_data.py -i test.txt -o  test.data
```
- 模型训练

最后，调用`crf_learn`命令训练模型：
```
echo training
time crf_learn -p 30 template train.data model.crf 2>&1 | tee  train.log
```
注意，`time`是显示命令执行时间。其中的`template`是`crfpp`需要的特征模板文件，后面的`2>&1 | tee train.log`整个实现了屏幕上打印日志信息，又同时保存在`train.log`中。读者们可以自己试验，通过拆解各部分来体会各个作用。

> 目前在`crfpy`中还没有封装`crf_test`命令，所以暂时没法直接进行验证集测试。在后面的文章中，会配合python模块封装技术的讲解，带着大家去实战一下，怎么样把这个命令也封装进来，让大家都学会如何自己把一个C++库封装为python模块。

## 后记

本篇文章首先简单介绍了一些Shell编程最常需要的一些基础知识，然后提供了两个例子。

- 第一个例子是通过批处理自动配置Python环境，把前面几个知识进行了串联。但有个问题是，这个**脚本直接把模块安装到了系统的python中，在实际工作中，不一定合适**。下一篇文章会为大家介绍**一种更推荐的方式——虚拟环境**。
- 第二个例子，是通过基于CRF的NER任务实战脚本，演示了Shell脚本的批处理。我们特别注意，在第二个例子中，除了转换标签格式部分额外写了Python脚本，模型训练使用了`crf_learn`命令，其余都是利用Linux常用的shell命令就完成了。特别是最后的模型训练的**日志记录**，模型训练的**计时**，**都没有额外编程**。同时，**Shell脚本完成了比Python更高一层的“胶水语言”，把Python和C++实现的Shell命令与其他内部命令很好的衔接起来，完成一整套pipeline**。

PS: 本文所需代码和演示数据，可通过[ai-union/ai_engineering_practice_guide](https://github.com/ai-union/ai_engineering_practice_guide) 中的`src`文件夹获得。本篇文章的代码文件夹是`basic-02-shell`，CRF的相关代码文件在`crf`中。

## 参考资料

- [prashant2018/MLSetup](https://github.com/prashant2018/MLSetup) 
- [如何轻松愉快地理解条件随机场（CRF）？ - 简书](https://www.jianshu.com/p/55755fc649b1) 