# 万万没想到，命令行也能玩数据分析？

在大数据时代，很多领域都越来越重视数据分析，越来越多的朋友也开始学习数据分析。有的朋友喜欢用图形化软件，还有很多喜欢用Python或 R写脚本进行更灵活的数据分析。但你有没有想过，其实Linux命令行也可以玩数据分析？

# AI 项目的 Linux 命令基础 (下篇)

本篇是Linux命令基础的下篇。在今天的文章里，我通过一个数据分析的实例，为大家演示一些Linux命令行下可以帮助数据分析的经典命令。今天的示例一共有两个，分别是著名的机器学习 iris 数据分析，以及莎士比亚文本分析。

##  iris 数据分析

今天第一个示例就是 iris 数据集。该数据集里一共有 150 条记录，五个字段 。字段含义分别是花萼长度，花萼宽度，花瓣长度，花瓣宽度和鸢尾花类别（Setosa，Versicolour，Virginica ）

### 数据获取

数据从UCI 数据集上直接下载，使用命令`wget` :
```
cd /tmp
wget http://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data
```

`wget` 是Linux下最常用的下载数据的命令之一， 其通常用法是：
```
 wget -c  -t 0  xxxxx 
```
其中，`-c`表示断点续传，`-t 0`表示无限重试，在Linux下还有`curl -OL xxx `命令同样也可以下载数据。
> 无论是`wget`还是`curl`都只是单线程，我们可以安装其他更快的命令，比如`aria2c`或`axel`命令，都是默认支持断点续传，并能多线程下载的命令。我们可以用`apt`进行安装这些命令。但在实际中，我们看到的很多网站数据很难直接得到下载地址，一般都是通过专门的爬虫去爬取数据。**关于这部分内容，读者们可以参考学习AI派公众号的爬虫专栏系列文章。**

### 文件操作

下载完数据后，我们经常要移动或复制数据到指定位置，下面简单介绍一下几个最常见的文件操作命令。

- 移动/重命名

使用`mv`命令：
```
mv file1 file2 dir  # 将file1和file2 移动到dir下
mv dir1 dir2 # 如果dir2不存在，则表示目录重命名
mv file1 file2 # file2存在时会覆盖file2；否则，会重命名file1为file2
```
- 复制文件/文件夹

使用`cp`命令
```
cp file1 file2 # 将file1复制为file2
cp -r dir1/*    dir2/  将dir1目录下的所有内容复制到dir2目录下
cp -r dir1   dir3   将dir1目录整个复制为dir3（含所有文件和子文件夹）
```
>复制文件夹内部内容，经常需要`-r`参数

- 删除文件或文件夹

Linux下的命令是`rm`，**特别注意大部分情况无法撤销`rm`的删除**。传说中的破坏力极大的命令：
```
rm -rf xxxx
```
> 上述表示强制删除xxx和xxx下的所有文件夹和子目录，生产环境里面**用不好就等于删库跑路，一定要谨慎**。

- 创建文件夹

命令是`mkdir`，在工作中常用到建立好几级的目录结构，比如：
```
mkdir -p data/raw
```
参数`-p`的优点是，在`data`，`raw`目录均不存在时，命令可以直接创建这些目录，而不需要挨个创建。

### 数据检查

- 打印/拼接

获取数据后，第一步是检查数据，简单说是显示数据里的内容。我们这里介绍这些命令主要是处理文本类型的数据，所以显示数据就是打印文本文件。读者很容易想到用`cat`打印，通过该命令能打印一个csv文件里的全部信息：
```
cat iris.data
```
另外，`cat`还有拼接文件的功能，可以用`cat`快速实现两个csv的拼接:
```
cat iris.data iris.data > data_all.csv
```
或者是csv数据的添加：
```
cat newdata.csv >>  data_all.csv
```
- 交互式检查

如果文件行数很多，`cat`会导致刷屏。这时，**`cat`结果更多是作为管道符的一个输入，传递给后续命令进行筛选或处理，**而不是直接显示出来。如果真的想检索所有数据，Linux有一个`less`命令，可以实现快捷的交互式数据检查：
```
less -S iris.data
```
这里的`less`会显示一个交互式的可操作文本界面。内容是文件的所有内容，我们使用键盘上的方向键可以上下观察，发现该数据是一个**没有表头**的逗号分隔的数据表格文件。注意`-S`参数，对数据分析很有用。**该参数保证数据文件的每行内容不会随终端窗口的宽度限制而换行**，让我们不会混淆数据行的位置。

> 在大数据量的初步检查时，`less`更能体现出其作用。因为**`less`不会将所有数据一次性都读入内存**；此外，在`less`返回的操作界面中，还可以直接使用vim的方向操作键位。比如`ijkl`的四方向操作，以及`shift+G` 和 `gg` 的快捷操作，如果有不知道作用的同学可以亲自试验一下。**在Linux中，很多命令的结果操作，都支持vim键位。**从中我们也可以感受到，在Linux或Unix中，这些小的技术点都是互相联系浑然一体，而不是像Windows那样，大部分都是孤立并很容易废弃。

### 数据筛选

#### 行筛选

- 头部行筛选

数据筛选操作中，最常见的是查看前几条记录。假设数据下载位置就是当前目录，可以用命令`head`查看数据中前5条记录:
```
head -n 5 iris.data
```
返回结果：
```
5.1,3.5,1.4,0.2,Iris-setosa
4.9,3.0,1.4,0.2,Iris-setosa
4.7,3.2,1.3,0.2,Iris-setosa
4.6,3.1,1.5,0.2,Iris-setosa
5.0,3.6,1.4,0.2,Iris-setosa
```
- 尾部行筛选

也可以查看数据中最后5条记录：
```
tail -n 5 iris.data
```
返回结果：
```
6.3,2.5,5.0,1.9,Iris-virginica
6.5,3.0,5.2,2.0,Iris-virginica
6.2,3.4,5.4,2.3,Iris-virginica
5.9,3.0,5.1,1.8,Iris-virginica
```
> 熟悉Python或R的同学们，可能会觉得对这两条命令觉得眼熟，因为pandas和R里都有`head`和`tail`函数，起到的作用也是一样。**Python和R还有许许多多与Linux保持一致的细节（比如路径分隔符，注释），如果你只用或只熟悉Windows是很难了解这些内容的。

- 指定行筛选

我们想只显示特定的一行，比如显示第5行记录：
```
sed -n 5p iris.data 
```
返回结果：
```
5.0,3.6,1.4,0.2,Iris-setosa
```
如果，我们想显示从A行到第B行的数据，比如从第1行到第3行数据：
```
sed -n 1,3p iris.data
```
返回结果为
```
5.1,3.5,1.4,0.2,Iris-setosa
4.9,3.0,1.4,0.2,Iris-setosa
4.7,3.2,1.3,0.2,Iris-setosa
```
通过`sed`，很容易实现`head`相同的效果。另外，`sed`可以显示多个指定行，比如显示前3行数据还可以用下面的命令：
```
sed -n -e 1p -e 2p -e 3p  iris.data
```
从结果可以发现，这里实际是显示了第1行，第2行和第3行数据。

- 随机行筛选

在数据分析中，我们经常需要对数据进行随机打乱顺序的操作。并且可能需要随机取出几条数据，这时可利用`shuf`命令完成。比如，我们想用Linux命令直接从数据中随机抽取3行记录：
```
shuf -n 3 iris.data
```
返回的记录为（**因为是随机，每次都不同**）：
```
6.4,2.8,5.6,2.1,Iris-virginica
5.0,3.5,1.3,0.3,Iris-setosa
4.6,3.1,1.5,0.2,Iris-setosa
```
- 行统计
Linux中可以使用`wc`命令统计csv中的数据记录数：
```
wc -l iris.data
```
其中，`-l`表示统计的行数。但这条命令返回的行数多算了一个空行，我们可以利用以下的复合命令，统计不含空行的行数：
```
cat iris.data | sed -e '/^$/d' | wc -l   
```
这里，`^\s*$ `匹配 空行、空格、tab。也可以使用`grep`实现同样效果：
```
cat iris.data | grep -v ^$|wc -l 
```

#### 列筛选

- 显示列名

```
cat iris.csv |  sed -e 's/,/\n/g;q'
```
这里通过`sed`命令，将第一行的逗号都替换为换行。注意，**`sed`是逐行执行**，不加后面的`;q`，会继续处理表头之外的其余行。命令返回csv表头的字段名：
```
sepal_length
sepal_width
petal_length
petal_width
species
```

- 指定列筛选

Linux的`cut`命令，原本是用于文本分割。我们这里灵活运用，将`cut`用于筛选显示csv中第几列的数据。例如，用`cut`命令显示`iris.data`的第5列类型：
```
cut -d ',' -f 5 iris.data
```
命令返回了类型。
>这里灵活运用了逗号分隔符。逗号分隔符常用于csv中。如果我们拿到一个数据是csv文件，或文件是用逗号分割的文本格式，我们就可以直接使用这条命令查看某列信息，节省了很多调用Python或R的时间。

由于上面的`cut`是全部打印了所有行，命令行被刷屏了。我们结合上一篇文章所讲的管道，和本篇文章前面所介绍的`head`组合使用：
```
cut -d ',' -f 5 iris.data | head -n 3
```
命令则只返回了我们想要的前3行第5列：
```
Iris-setosa
Iris-setosa
Iris-setosa
```

- 字段唯一值

数据分析中经常要查看某字段的唯一值，你可能马上想到pandas的`unique`函数。Linux里也有`uniq`能实现类似效果，比如我们想查看第5列的唯一值：
```
cut -d ',' -f 5 iris.data  | uniq
```
- 搜索字段内容所在行

如果想查找`data.csv`中特定值在第几行，可以用：
```
grep -rn iris.data -e "Iris-setosa"
```
结果会返回`iris.data`含有`Iris-setosa`的每一行内容和行号，高亮显示搜索的关键词`Iris-setosa`。上面的`iris.data`也可以换成通配符，比如`*.csv`,**实现多文件的内容搜索**。

> 我们可以使用更强大的文本处理命令`awk`来完成更多的文本处理操作。当然`awk`相对也更复杂一些，几乎可以看成是一个独立的编程语言。

### 数据转换

- 添加表头

我们发现，下载的数据和通常看到的csv不同，第一行是数据，不是表头。直接操作这样的数据，我们需要记忆每个字段的索引位置。我们也可以通过拼接操作，为数据增加一行表头。假设我们知道字段名分别是`sepal_length`,`sepal_width`,`petal_length`,`petal_width`和`species`，可以利用`cat`将表头和数据拼接起来：
```
echo "sepal_length,sepal_width,petal_length,petal_width,species" | cat -  iris.data  >  iris.csv
```
这里的`cat -` 部分是把管道符前面的打印内容和后面的`iris.data`进行拼接，然后利用重定向符`>`输出到文件`iris..csv`。

- 列统计

已经有表头的数据，可以利用以下命令统计列数：
```
head -1 iris.csv | sed 's/[^,]//g' | wc -c
```
这里通过sed命令，将`head`的结果过滤为字段分隔符`,`， 然后利用`wc`统计字符个数。特别注意，**这里因为正好多统计了换行，所以恰好等于字段个数**。
> 可能有的读者会不理解，明明直接用`head`一目了然多少列，为什么还要用命令去数。其实，在实际数据分析中拿到的数据，经常有几十个字段名，有些代码中需要知道列的个数，这时快速统计列数就很有用。

- 列排序

Linux下的排序命令是`sort`，可以用`sort`对数据第1列的大小进行排序：
```
sort -t , -k 1  iris.data | head
```
这里的`-t ,`表示用逗号作为字段的分隔符。

- 数据连接

了解数据分析的同学一定知道数据库中`left join`的作用。Linux下可用`join`命令实现类似逻辑。首先，先新建一个新文件`iris_key.csv`:
```
Iris-setosa,1
```
再利用上面介绍的`sort`命令做`join`的预处理。这里，因为使用类型字段进行连接，所以排序的字段也是类型字段：
```
 sort -t , -k 5  iris.data > iris_sorted.csv 
 sort -t , iris_types.csv  > iristype_sorted.csv
 join -t , iris_sorted.csv iristype_sorted.csv -1 5 -2 1 > testjoin.csv
```
第一条`sort`命令的`-k 5`表示按照第5行进行排序。第二条是因为待排序文件本身就只有一条，所以没有指定排序字段。第三条的`join`参数`-1 5`表示，第一个待连接的数据` iris_sorted.csv`使用第5列进行关联，`-2 1`表示第二个数据`iristype_sorted.csv`使用第1列进行关联。
> `join`可实现很多SQL中类似的效果，具体可查询命令帮助`join --help`

## 莎士比亚文本分析

前面的例子是关于csv的表格数据的分析，第二个例子是文本分析相关的例子。我们用莎士比亚的小说文本为例，介绍Linux命令行下如何做基本的文本分析。

### 数据获取

首先依然是下载数据，这次我换用`curl`命令进行下载：
```
cd /tmp
curl -L  https://ocw.mit.edu/ans7870/6/6.006/s08/lecturenotes/files/t8.shakespeare.txt  -o  shakes.txt
```
这里，注意`curl`如果后面直接跟地址，就会在屏幕直接打印出文本的内容，相当于下载（`wget`）并显示（`cat`）的组合效果。`-o`参数表示把在文件的文件名改为后面的形式。

### 数据检查

前面，我们检查主要介绍是查看文件内容。这里为大家介绍如何在Linux下方便的查看下载的文件情况。

- 查看文件大小

```
ls -lah shakes.txt
```
这里的`-l`参数表示结果中显示文件类型，所有者和组，大小，日期和文件名等。`-a`参数表示显示**包含隐藏文件的所有文件**。`-h`是一个对用户很友好的一个参数，能将文件大小换为人类方便阅读的形式返回：
```
-rw-r--r--@ 1 sabber  staff   5.6M Jun 15 09:35 shakes.txt
```

- 查看文本内容

在文本分析中，原始文件经常存在我们不需要的内容。为了观察这些内容所在的行数，我们可以用这条命令：
```
less -N shakes.txt
```
这里的`-N`参数表示在结果每行首加上行号。我们通过观察，发现前141行，14926到 149689行的内容似乎并不是莎士比亚的小说内容。

### 文本处理

- 删除文本行

经过以上观察，我们发现一些文本行不是正文，需要删除。我们可以使用以下命令：
```
cat shakes.txt | sed -e '149260,149689d' | sed -e '1,141d' > shakes_new.txt
``` 
这里，我们使用几个命令的组合完成这个数据清理的操作。`sed -e  xxxd`是删除行的作用，为了不需要重新算后面的行数，所以先删除后面的行，再删除行首的141行。处理结果通过重定向另存为新文件`shakes_new.txt`。

> 特别注意，这里**我们在对源文件修改后，并不覆盖源文件，而是把处理结果另存为新文件**，这是数据处理的一个最重要的**基本原则**。

- 文本清洗

文本分析的数据清洗比数据表格要更繁杂，主要包括大小写转换、去除标点符号、停用词。此外，根据不同具体目的，还可能会有其他处理操作。这里只介绍以上提到的一些最基本文本清洗：
```
cat shakes_new.txt | tr 'A-Z' 'a-z' | tr -d [:punct:] |  tr -d [:digit:] > shakes_new_cleaned.txt
```
这里，`tr`分别实现了大写转换为小写、删除数字和标点的操作。

- 分词

自然语言处理中，分词（Tokenization）是最基本的预处理，可以在词或句子上进行。这里，我们演示如何对一个文档进行分词：
```
cat shakes_new_cleaned.txt | tr -sc ‘a-z’ '[\012*]'  > shakes_tokenized.txt
```
这里，`tr`把`cat`传入的文本的每个词转换为行。

- 删除停用词

停用词的删除，在NLP中是非常关键的一步预处理。这里我们使用Gist上一份NLTK的英文停用词表：
```
curl -o stop_words.txt -L  "https://gist.githubusercontent.com/sebleier/554280/raw/7e0e4a1ce04c2bb7bd41089c9821dbcf6d0c786c/NLTK's%2520list%2520of%2520english%2520stopwords"
```

通过`awk`命令，删除这里面定义的停用词：
```
 awk 'FNR==NR{for(i=1;i<=NF;i++)w[$i];next}(!($1 in w))'  stop_words.txt shakes_tokenized.txt > shakes_stopwords_removed.txt
```

> 删除停用词的意义，请看下面文本分析中的词频统计。

### 文本分析

- 字数统计

文本分析中最基本的是统计文本的字符数，我们可以用以下命令：
```
cat shakes_new_cleaned.txt| wc | awk '{print "Lines: " $1 "\tWords: " $2 "\tCharacter: " $3 }'
```
以上命令中，`cat`先打印出所有文本，然后通过管道符传递给`wc`命令。`wc`统计出行数、字和字符数后，后面的`awk`命令负责将这三个数字前面加上提示文字，类似于其他语言中的格式化输出：
```
Lines: 124315	Words: 898977	Character: 5204131
```
- 词频统计

词频统计可以告诉我们，莎士比亚小说中最常出现或最少出现的词是哪个？为了实现词频统计，我们需要在前述分词的文本基础上，用以下的管道命令实现词频的降序排列：
```
cat shakes_tokenized.txt | sort | uniq -c | sort -nr > shakes_sorted_desc.txt
```
我们也可以将词频升序排列：
```
cat shakes_tokenized.txt | sort | uniq -c | sort -n > shakes_sorted_asc.txt
```
这里的两条命令很类似。`sort`首先对文本先排序，然后`uniq -c`将每个词出现的频率统计出来（类似分组统计）。最后，`sort`通过参数具体控制是降序还是升序。这里通过`head`命令查看高频词：
```
head -n 5  shakes_sorted_desc.txt
```
发现结果中的高频词多数都是没有意义的介词、代词等虚词：
```
 27607 the
 26702 and
 20681 i
 19171 to
 18143 of
```
但如果我们在删除停用词后统计的词频，会更加符合我们想要的效果：
```
cat shakes_stopwords_removed.txt | sort | uniq -c | sort -nr > shakes_sorted_desc.txt
cat shakes_stopwords_removed.txt | sort | uniq -c | sort -n > shakes_sorted_asc.txt
```
这时的高频词为：
```
5485 thou
   4032 thy
   3591 shall
   3178 thee
   3059 lord
```
我们发现，这里的高频词中还有没去掉的停用词，我们可以把`thou`、`shall`，`thee`和`thy`（主要是旧式用法的代词）都添加到停用词表中，然后再次统计：
```
echo "thou\nshall\nthee\nthy\n" >> stop_words.txt
awk 'FNR==NR{for(i=1;i<=NF;i++)w[$i];next}(!($1 in w))'  stop_words.txt shakes_tokenized.txt > shakes_stopwords_removed.txt
cat shakes_stopwords_removed.txt | sort | uniq -c | sort -nr > shakes_sorted_desc.txt
cat shakes_stopwords_removed.txt | sort | uniq -c | sort -n > shakes_sorted_asc.txt
head -n 4  shakes_sorted_desc.txt
```
这里我们可以看到这4个高频词：
```
   3059 lord
   2861 king
   2812 good
   2754 sir
```
我们可以通过一些对文学的基本了解，和更多的背景知识去解释。

### 语言模型

在NLP中，我们经常简单的假设一个词只和他前面出现的n-1个词相关（隐马尔可夫假设）。此时，整个句子的概率等于每个词的概率乘积，我们可以用N-Gram（N元语言模型）模型来描述。当n取1,2,3时的ngram，分别叫unigram、bigram和trigram。

例如，当我们假设下一个词依赖前一个词时，需要计算bigram：
```
   cat shakes_tokenized.txt | awk -- 'prev!="" { print prev,$0; } { prev=$0; }' | \
  sort | uniq -c | sort -nr | \
  head 
```

如果假设下一个词依赖前面两个词，则用trigram。
```
 cat shakes_tokenized.txt |  awk -- 'first!=""&&second!="" { print first,second,$0; } { first=second; second=$0; }' | \
  sort | uniq -c | sort -nr | \
  head
```
## 总结

今天的文章通过两个实例，向大家介绍了一些Linux常见的数据处理相关命令的用法。这里想总结和强调几个方面：
- Linux命令比较擅长处理文本表格数据（`csv`）和文本分析
- 在管道组合命令中，`cat` 常负责传给下个命令全部文本。
- 在很多操作中，`sort`都是重要的前处理步骤，务必重点掌握。
- 文本编辑中，`tr`，`sed`和`awk`是三个很重要的处理命令。

本篇文章介绍的只是Linux许多命令中的一部分，其他的命令以及许多需要额外安装的更多更强大的命令，还需要读者们多多去挖掘。此外，Linux命令下的数据处理和分析，可以作为一种额外的辅助手段，让我们能在服务器上不安装什么软件就能做基本处理，也可以作为我们熟悉和锻炼Linux命令的一种方式。对于大部分场景下的复杂数据处理和计算，还是应该使用更专业的框架和软件包去处理，才是主流。

## 相关资源

- [命令行中的数据科学](https://www.datascienceatthecommandline.com)
- [鳥哥的 Linux 私房菜](http://linux.vbird.org/) 
- [Text mining on the command line - Towards Data Science](https://towardsdatascience.com/text-mining-on-the-command-line-8ee88648476f)
- [语言模型的基本概念 - Dream_Fish - 博客园](https://www.cnblogs.com/Dream-Fish/p/3963028.html) 