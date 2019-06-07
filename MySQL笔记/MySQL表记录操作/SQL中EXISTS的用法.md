# SQL中EXISTS的用法

EXISTS用于检查子查询是否至少会返回一行数据，如果有数据返回，则给exists一个true值，否则false。where条件后，如果exists返回一个true，则继续执行查询语句。

EXISTS 指定一个子查询，检测行的存在。

语法：

EXISTS subquery

参数：subquery是一个首先的SELECT语句（不允许compute子句和into关键字）

结果类型：Boolean 如果子查询包含行，则返回true，否则返回flase