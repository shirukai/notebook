# hadoop FileSystem Shell

http://hadoop.apache.org/docs/r2.7.4/hadoop-project-dist/hadoop-common/FileSystemShell.html

文件系统（FS）shell包括各种类似shell的命令，可直接与Hadoop分布式文件系统（HDFS）以及Hadoop支持的其他文件系统（如本地FS，HFTP FS，S3 FS等）进行交互。FS shell 是通过以下方式调用的：

```
bin / hadoop fs <args>
```

### appendToFile

用法: 

```
hadoop fs -appendToFile <localsrc> ... <dst>
```

将本地的一个或多个文件追加到目标文件系统，如果目标文件系统的文件不存在，会自动创建。

如：

将本地的addfiletest.txt 文件 追加到 hdfs中的/test/todayTest文件中(如果文件不存在会自动创建)

```
[root@Master ~]# hadoop fs -appendToFile addfiletest.txt /test/todayTest
```

追加addfiletest.txt 和 hahah.cfg 文件到hdfs中的/test/todayTest文件中

```
[root@Master ~]# hadoop fs -appendToFile hahah.cfg /test/todayTest
```

### cat

用法：

```
hadoop fs -cat [-ignoreCrc] URI [URI ...]
```

查看目标文件

```
hadoop fs -cat hdfs://nn1.example.com/file1 hdfs://nn2.example.com/file2
```

### checksum 

用法：

```
hadoop fs -checksum URI
```

返回文件的检验和信息

例如：

```
[root@Master ~]# hadoop fs -checksum /test/todayTest
/test/todayTest	MD5-of-0MD5-of-512CRC32C	000002000000000000000000bb4b6ae665bd919e3ed68c9fa3974d20
```

### chgrp 

用法：

```
fs -chgrp [-R] GROUP URI [URI ...]
```

更改文件的组，-R是递归更改

### chmod

用法：

```
hadoop fs -chmod [-R] <MODE [，MODE] ... | OCTALMODE> URI [URI ...]
```

更改文件的权限。使用-R，递归地通过目录结构进行更改。用户必须是文件的所有者，否则是超级用户。其他信息在“ [权限指南”中](http://hadoop.apache.org/docs/r2.7.4/hadoop-project-dist/hadoop-hdfs/HdfsPermissionsGuide.html)。

选项

- -R选项将通过目录结构递归地进行更改。

### chown

用法：

```
hadoop fs -chown -R [：[GROUP]] URI [URI]
```

更改文件的所有者。用户必须是超级用户。其他信息在“ [权限指南”中](http://hadoop.apache.org/docs/r2.7.4/hadoop-project-dist/hadoop-hdfs/HdfsPermissionsGuide.html)。

选项

- -R选项将通过目录结构递归地进行更改。

### copyFromLocal

用法：

```
hadoop fs -copyFromLocal <localsrc> URI
```

与`fs -put`命令类似，只是源限制为本地文件引用。

选项：

- `-p`：保留访问和修改时间，所有权和权限。（假设权限可以跨文件系统传播）
- `-f`：覆盖目标，如果它已经存在。
- `-l`：允许DataNode延迟地将文件保存到磁盘，强制复制因子为1.此标志将导致减少的持久性。小心使用。
- `-d`：跳过创建后缀为`._COPYING_`的临时文件。

### copyToLocal

用法：

```
hadoop fs -copyToLocal -ignorecrc URI <localdst>
```

与get命令类似，只是目标被限制为本地文件引用。

### count

用法：

```
hadoop fs -count -q [-v] <路径>
```

统计与指定文件模式匹配的路径下的目录，文件和字节数。带有-count的输出列是：DIR_COUNT(目录)，FILE_COUNT（文件），CONTENT_SIZE（大小），PATHNAME（路径名）

如：

```
[root@Master ~]# hadoop fs -count /test
           1            2               2610 /test
```

带有-count -q的输出列为：QUOTA（配额），REMAINING_QUATA（剩余配额），SPACE_QUOTA（空间配额），REMAINING_SPACE_QUOTA（剩余空间配额），DIR_COUNT，FILE_COUNT，CONTENT_SIZE，PATHNAME

如：

```
[root@Master ~]# hadoop fs -count -q /test
        none             inf            none             inf            1            2               2610 /test
```

-h选项以可读格式显示大小。

```
[root@Master ~]# hadoop fs -count -h /test
           1            2              2.5 K /test
```

-v选项显示标题行。

例：

- `hadoop fs -count hdfs：//nn1.example.com/file1 hdfs：//nn2.example.com/file2`
- `hadoop fs -count -q hdfs：//nn1.example.com/file1`
- `hadoop fs -count -q -h hdfs：//nn1.example.com/file1`
- `hdfs dfs -count -q -h -v hdfs：//nn1.example.com/file1`

### cp

用法：

```
hadoop fs -cp -f] URI [URI ...] <dest>
```

将文件从源文件复制到目的地。这个命令允许多个源，在这种情况下，目标必须是一个目录。

如果（1）源和目标文件系统支持它们（仅限于HDFS），（2）所有源和目标路径名都在/.reserved/raw层次结构中，则保留'raw。*'命名空间扩展属性。确定raw。*命名空间xattrs是否保存与-p（preserve）标志无关。

选项：

- 如果它已经存在，-f选项将覆盖目标。
- -p选项将保留文件属性[topx]（时间戳，所有权，权限，ACL，XAttr）。如果-p指定为不带*arg*，则保留时间戳，所有权和权限。如果指定了-pa，则还会保留权限，因为ACL是超级权限。确定是否保留原始名称空间扩展属性与-p标志无关。

例：

- `hadoop fs -cp / user / hadoop / file1 / user / hadoop / file2`
- `hadoop fs -cp / user / hadoop / file1 / user / hadoop / file2 / user / hadoop / dir`

如：将/test/todayTest文件复制到/input目录下

```
[root@Master ~]# hadoop fs -cp /test/todayTest /input/todayTest
```

### createSnapshot

请参阅“ [HDFS快照指南”](http://hadoop.apache.org/docs/r2.7.4/hadoop-project-dist/hadoop-hdfs/HdfsSnapshots.html)。

### deleteSnapshot

请参阅“ [HDFS快照指南”](http://hadoop.apache.org/docs/r2.7.4/hadoop-project-dist/hadoop-hdfs/HdfsSnapshots.html)。

### df

用法：

```
hadoop fs -df [-h] URI [URI ...]
```

显示可用空间。

选项：

- -h选项将以“可读的”方式格式化文件大小（例如，64.0m而不是67108864）

例：

- `hadoop dfs -df / user / hadoop / dir1`

```
[root@Master ~]# hadoop fs -df -h /input
Filesystem                   Size    Used  Available  Use%
hdfs://Master.Hadoop:9000  17.0 G  32.0 M      3.2 G    0%
```

### du 

用法：

```
hadoop fs -du [-s] [-h] URI [URI ...]
```

显示给定目录中包含的文件和目录的大小，或者文件的长度，以防文件的大小。

选项：

- -s选项将导致显示文件长度的汇总摘要，而不是单个文件。
- -h选项将以“可读的”方式格式化文件大小（例如，64.0m而不是67108864）

例：

- `hadoop fs -du / user / hadoop / dir1 / user / hadoop / file1 hdfs：//nn.example.com/user/hadoop/dir1`

```
[root@Master ~]# hadoop fs -du -h /input
1.3 K  /input/todayTest
```

### expunge 

用法：

```
hadoop fs -expunge
```

永久删除比垃圾目录中的保留阈值更早的检查点中的文件，并创建新的检查点。

当创建检查点时，垃圾桶中最近删除的文件将在检查点下移动。早于`fs.trash.checkpoint.interval的`检查点中的文件将在下次调用`-expunge`命令时被永久删除。

如果文件系统支持该功能，则用户可以配置为通过以`fs.trash.checkpoint.interval`（在core-site.xml中）存储的参数定期创建和删除检查点。该值应该小于或等于`fs.trash.interval`。

有关[HDFS的](http://hadoop.apache.org/docs/r2.7.4/hadoop-project-dist/hadoop-hdfs/HdfsDesign.html#File_Deletes_and_Undeletes)垃圾功能的更多信息，请参阅[HDFS体系结构指南](http://hadoop.apache.org/docs/r2.7.4/hadoop-project-dist/hadoop-hdfs/HdfsDesign.html#File_Deletes_and_Undeletes)。

### find 

用法：

```
hadoop fs -find <path> ... <expression> ...
```

查找与指定表达式匹配的所有文件，并将选定的操作应用于它们。如果没有指定*路径*，则默认为当前工作目录。如果没有指定表达式，则默认为-print。

以下主要表达式被识别：

- -name

  -iname

  如果文件的基本名称与使用标准文件系统匹配的模式匹配，则评估为true。如果使用-iname，则匹配不区分大小写。

- -print 
  -print0Always

  评估为真。使当前路径名写入标准输出。如果使用-print0表达式，则会附加ASCII NULL字符。

以下运营商被认可：

- 表达式 -a 表达式
  表达式  -and 表达式 
  表达式 表达式 

  用于连接两个表达式的逻辑AND运算符。如果两个子表达式都返回true，则返回true。由两个表达式的并置所暗示，因此不需要明确指定。如果第一个表达式失败，则不会应用第二个表达式。

例：

```
[root@Master ~]# hadoop fs -find / -name test -print
/hiveLearn/foreign_path_hiveDB/test
/test
```

### get 

用法：

```
hadoop fs -get -ignorecrc -p <src> <localdst>
```

将文件复制到本地文件系统。CRC校验失败的文件可以用-ignorecrc选项复制。文件和CRC可以使用-crc选项复制。

例：

- `hadoop fs -get / user / hadoop / file localfile`
- `hadoop fs -get hdfs：//nn.example.com/user/hadoop/file localfile`

选项：

- `-p`：保留访问和修改时间，所有权和权限。（假设权限可以跨文件系统传播）
- `-f`：覆盖目标，如果它已经存在。
- `-ignorecrc`：跳过下载的文件的CRC校验。
- `-crc`：为下载的文件写入CRC校验和。



## getfacl

用法：

````
hadoop fs -getfacl [-R] <path>
````

显示文件和目录的访问控制列表（ACL）。如果目录具有默认ACL，则getfacl也会显示默认ACL。

选项：

- -R：递归列出所有文件和目录的ACL。
- *路径*：列出的文件或目录。

例子：

- `hadoop fs -getfacl /file`
- `hadoop fs -getfacl -R / dir`

```
[root@Master ~]# hadoop fs -getfacl -R /input
# file: /input
# owner: root
# group: supergroup
getfacl: The ACL operation has been rejected.  Support for ACLs has been disabled by setting dfs.namenode.acls.enabled to false.
```

### getfattr

用法：

````
hadoop fs -getfattr [-R] -n name | -d [-e en] <path>
````

显示文件或目录的扩展属性名称和值（如果有）。

选项：

- -R：递归列出所有文件和目录的属性。
- -n name：转储指定的扩展属性值。
- -d：转储与路径名关联的所有扩展属性值。
- -e encoding：检索值后进行编码。有效的编码是“文本”，“十六进制”和“base64”。编码为文本字符串的值用双引号（“）括起来，编码为十六进制和base64的值分别以0x和0作为前缀。
- *路径*：文件或目录。

例子：

- `hadoop fs -getfattr -d / file`
- `hadoop fs -getfattr -R -n user.myAttr / dir`

```
[root@Master ~]# hadoop fs -getfattr -d /input/todayTest
# file: /input/todayTest
```



### getmerge

用法：

```
hadoop fs -getmerge [-nl] <src> <localdst>
```

将源目录和目标文件作为输入，并将src中的文件连接到目标本地文件。可选项 -ln，可以设置-nl以在每个文件的末尾添加换行符（LF）。

例子：

- `hadoop fs -getmerge -nl / src /opt/output.txt`
- `hadoop fs -getmerge -nl /src/file1.txt /src/file2.txt /output.txt`

如：将hdfs中/input/todayTest文件 内容 以及 本地/root/addfiletest.txt的内容合并并保存到addfiletest.txt中

```
[root@Master ~]# hadoop fs -getmerge -nl /input/todayTest /root/addfiletest.txt 
```

### help 

用法：

````
hadoop fs -help
````



### ls 

用法：

```
hadoop fs -ls [-d] [-h] [-R] <args>
```

选项：

- -d：目录被列为纯文件。
- -h：以人类可读的方式格式化文件大小（例如，64.0m而不是67108864）。
- -R：递归列出遇到的子目录。

### mkdir

用法：

```
hadoop fs -mkdir [-p] <路径>
```

以路径uri作为参数并创建目录。

选项：

- -p选项行为与Unix mkdir -p非常相似，沿路径创建父目录。

例：

- `hadoop fs -mkdir / user / hadoop / dir1 / user / hadoop / dir2`

### moveFromLocal

用法：

```
hadoop fs -moveFromLocal <localsrc> <dst>
```

与put命令类似，区别在于源localsrc在复制后被删除。

### moveToLocal 

用法：

````
hadoop fs -moveToLocal [-crc] <src> <dst>
````

将hdfs中的文件移动到本地

### mv 

用法：

```
hadoop fs -mv URI [URI ...] <dest>
```

将文件从源移动到目标。这个命令允许多个源，在这种情况下，目标需要是一个目录。在文件系统中移动文件是不允许的。

例：

- `hadoop fs -mv / user / hadoop / file1 / user / hadoop / file2`
- `hadoop fs -mv hdfs：//nn.example.com/file1 hdfs：//nn.example.com/file2 hdfs：//nn.example.com/file3 hdfs：//nn.example.com/dir1`

### put 

用法：

````
hadoop fs -put [-f][-p] [-l][-d] [ - | <localsrc1> ..]。<DST>
````

将单个src或多个srcs从本地文件系统复制到目标文件系统。如果源设置为“ - ”，还从stdin读取输入并写入目标文件系统

如果文件已经存在，复制失败，除非给出-f标志。

选项：

- `-p`：保留访问和修改时间，所有权和权限。（假设权限可以跨文件系统传播）
- `-f`：覆盖目标，如果它已经存在。
- `-l`：允许DataNode延迟地将文件保存到磁盘，强制复制因子为1.此标志将导致减少的持久性。小心使用。
- `-d`：跳过创建后缀为`._COPYING_`的临时文件。

例子：

- `hadoop fs -put localfile / user / hadoop / hadoopfile`
- `hadoop fs -put -f localfile1 localfile2 / user / hadoop / hadoopdir`
- `hadoop fs -put -d localfile hdfs：//nn.example.com/hadoop/hadoopfile`
- `hadoop fs -put - hdfs：//nn.example.com/hadoop/hadoopfile` 从标准输入读取输入。

### rm

用法：

````
hadoop fs -rm [-f][-r | -R] [-skipTrash] URI [URI ...]
````

删除指定为args的文件。

如果已启用垃圾箱，则文件系统会将已删除的文件移至垃圾目录（由[FileSystem＃getTrashRoot指定](http://hadoop.apache.org/docs/r2.7.4/api/org/apache/hadoop/fs/FileSystem.html)）。

目前，垃圾功能默认是禁用的。用户可以通过为参数`fs.trash.interval`（在core-site.xml中）设置一个大于零的值来启用垃圾箱。

请参阅[删除](http://hadoop.apache.org/docs/r2.7.4/hadoop-project-dist/hadoop-common/FileSystemShell.html#expunge)垃圾桶中的文件。

选项：

- -f 如果文件不存在，-f选项将不显示诊断消息或修改退出状态以反映错误。
- -R选项递归删除目录及其下的任何内容。
- -r选项相当于-R。
- 如果启用，-skipTrash选项将绕过垃圾箱，并立即删除指定的文件。当需要从超配额目录中删除文件时，这会很有用。

例：

- `hadoop fs -rm hdfs：//nn.example.com/file/user/Hadoop/emptydir`

### rmdir 

用法：

````
hadoop fs -rmdir [--ignore-fail-on-non-empty] URI [URI ...]
````

删除一个目录。

选项：

- `--ignore-fail-on-non-empty`：使用通配符时，如果目录仍包含文件，则不要失败。

例：

- `hadoop fs -rmdir / user / hadoop / emptydir`



### setfacl

用法：

````
hadoop fs -setfacl [-R][-b | -k -m | -x  ] | [ - set <acl_spec> <path>]
````

设置文件和目录的访问控制列表（ACL）。

选项：

- -b：删除除基本ACL条目以外的所有条目。为了与许可位兼容，保留用户，组和其他的条目。
- -k：删除默认的ACL。
- -R：递归地将操作应用于所有文件和目录。
- -m：修改ACL。新的条目被添加到ACL，并保留现有条目。
- -x：删除指定的ACL条目。其他ACL条目被保留。
- `--set`：完全替换ACL，丢弃所有现有的条目。所述*acl_spec*必须包括用户，组条目和其他用于与权限位兼容性。
- *acl_spec*：逗号分隔的ACL条目列表。
- *路径*：要修改的文件或目录。

例子：

- `hadoop fs -setfacl -m用户：hadoop：rw- /文件`
- `hadoop fs -setfacl -x用户：hadoop /文件`
- `hadoop fs -setfacl -b / file`
- `hadoop fs -setfacl -k / dir`
- `hadoop fs -setfacl --set user :: rw-，user：hadoop：rw-，group :: r - ，other :: r-- / file`
- `hadoop fs -setfacl -R -m用户：hadoop：rx / dir`
- `hadoop fs -setfacl -m default：user：hadoop：rx / dir`



### setfattr 

用法：

````
hadoop fs -setfattr -n name [-v value] | -x名称<路径>
````

为文件或目录设置扩展属性名称和值。

选项：

- -b：删除除基本ACL条目以外的所有条目。为了与许可位兼容，保留用户，组和其他的条目。
- -n名称：扩展的属性名称。
- -v value：扩展的属性值。有三种不同的编码方法的值。如果参数用双引号引起来，那么值就是引号内的字符串。如果参数以0x或0X为前缀，则将其视为十六进制数字。如果参数以0或0S开始，则将其视为base64编码。
- -x名称：删除扩展属性。
- *路径*：文件或目录。

例子：

- `hadoop fs -setfattr -n user.myAttr -v myValue / file`
- `hadoop fs -setfattr -n user.noValue / file`
- `hadoop fs -setfattr -x user.myAttr / file`



### setrep 

用法：

````
hadoop fs -setrep [-R][-w] <numReplicas> <path>
````

更改文件的复制因子。如果*path*是一个目录，那么该命令会递归地更改以*path为*根的目录树下的所有文件的复制因子。

选项：

- -w标志请求该命令等待复制完成。这可能需要很长时间。
- -R标志被接受为向后兼容。它没有效果。

例：

- `hadoop fs -setrep -w 3 / user / hadoop / dir1`

### stat

用法：

````
hadoop fs -stat [format] <path> ...
````

以指定的格式打印关于<path>处的文件/目录的统计信息。格式接受块（％b），类型（％F），所有者组名（％g），名称（％n），块大小（％o），复制（％r），所有者用户名（％ u）和修改日期（％y，％Y）。％y将UTC日期显示为“yyyy-MM-dd HH：mm：ss”，％Y显示1970年1月1日以来的毫秒。如果未指定格式，则默认使用％y。

例：

- `hadoop fs -stat“％F％u：％g％b％y％n”/ file`

退出代码：成功时返回0，错误时返回-1。

### tail 

用法：

````
hadoop fs -tail [-f] URI
````

显示文件的最后一个千字节到标准输出。

选项：

- 在Unix中，-f选项会随着文件的增长而输出附加的数据。

例：

- `hadoop fs -tail路径名`

退出代码：成功时返回0，错误时返回-1。

### test 

用法：

````
hadoop fs -test - [defsz] URI
````

选项：

- -d：f路径是一个目录，返回0。
- -e：如果路径存在，则返回0。
- -f：如果路径是一个文件，则返回0。
- -s：如果路径不为空，则返回0。
- -z：如果文件长度为零，则返回0。

例：

- `hadoop fs -test -e文件名`

### text 

用法：

```
hadoop fs -text <src>
```

采用源文件并以文本格式输出文件。允许的格式是zip和TextRecordInputStream。

## touchz

用法：

````

````

创建一个零长度的文件。如果文件的长度非零，则返回错误。

例：

- `hadoop fs -touchz路径名`

退出代码：成功时返回0，错误时返回-1。

### truncate 

用法：

```
hadoop fs -truncate [-w] <length> <paths>
```

将与指定文件模式匹配的所有文件截断为指定的长度。

选项：

- 该`-w`标志的要求，对块恢复命令如有必要，等待完成。没有-w标志的文件可能会保持一段时间，而恢复正在进行中。在此期间文件不能重新打开追加。

例：

- `hadoop fs -truncate 55 / user / hadoop / file1 / user / hadoop / file2`
- `hadoop fs -truncate -w 127 hdfs：//nn1.example.com/user/hadoop/file1`

### usage 

用法：

````
hadoop fs -usage 命令
````

返回单个命令的帮助。