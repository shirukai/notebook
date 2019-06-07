```
Sub CreateFile()
'定义变量
Dim PathG As String
Dim i As Integer
Dim str As String
Dim str_path As String
Dim FSO As Object
'定义路径
PathG = "D:\VBAtest\software"

'如果路径后面有 "\"
'类似于 "D:\VBAtest\software\"
'需要将后面的斜杠处理掉

If Right(PathG, 1) = "\" Then
    str = Left(PathG, Len(PathG) - 1)
Else
    str = PathG
End If

'无论有没有错都执行
On Error Resume Next
'得到一级目录
str_path = Split(PathG, "\")(0) & "\" & Split(PathG, "\")(1)
Debug.Print str_path

'判断目录是否存在

Set FSO = CreateObject("Scripting.FileSystemObject")

If FSO.FolderExists(str_path) = False Then
'如果不存在，创建
    MkDir (str_path)
End If

'遍历创建子目录

For i = 2 To UBound(Split(PathG, "\"))
    str_path = str_path & "\" & Split(PathG, "\")(i)
    If FSO.FolderExists(str_path) = False Then
    '如果不存在，创建
    MkDir (str_path)
    End If
Next
'创建一个名字为xml的目录
'然后创建一个test.xml的文件

Dim newDirect As String
Dim newPath As String
Dim FileName As String
Dim FilePath As String
Dim content As String
newDirect = "xml"
FileName = "test.xml"
newPath = PathG & "\" & newDirect

If FSO.FolderExists(newPath) = False Then
'如果不存在，创建
    MkDir (newPath)
End If
content = "这是我要插入的内容啊"

FilePaht = newPath & "\" & FileName

Open FilePaht For Output As #1
Print #1, content
Close #1
Debug.Print "创建完成"
End Sub

```

