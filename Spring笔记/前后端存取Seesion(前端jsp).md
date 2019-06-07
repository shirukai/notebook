# 前后端存取Seesion(前端jsp)

### 1.前端jsp获取session 

```
<%@ page import="java.util.Map" %>
<%@ page import="java.util.HashMap" %>
<%@ page import="java.util.Enumeration" %><%--
  Created by IntelliJ IDEA.
  User: shirukai
  Date: 2017/10/16
  Time: 19:19
  To change this template use File | Settings | File Templates.
--%>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head>
    <title>jspGetSession</title>
</head>
<body>
<h2>根据key获取session</h2>
<h3>
    <%=request.getSession().getAttribute("controllerSetSession1")%>
</h3>
<%
    Map<String, String> sessionMap = new HashMap<String, String>();
    //获取所有session名字
    Enumeration sessionEnum = request.getSession().getAttributeNames();
    while (sessionEnum.hasMoreElements()) {
        String sessionName = sessionEnum.nextElement().toString();
        sessionMap.put(sessionName, request.getSession().getAttribute(sessionName).toString());
    }
%>
<table border="1">
    <thead>
    <tr>
        <th>key</th>
        <th>value</th>
    </tr>
    </thead>
    <tbody>
    <%
        for (String key : sessionMap.keySet()
                ) { %>
    <tr>
        <td><%=key%>
        </td>
        <td><%=sessionMap.get(key)%>
        </td>
    </tr>

    <%
        }
    %>
    </tbody>
</table>
</body>
</html>
```

### 2.前端存入session 

```
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head>
    <title>jspSetSession</title>
</head>
<body>
<%
    request.getSession().setAttribute("jspSetSession","这是我通过jsp设置的session");
%>
</body>
</html>
```

### 3.后端获取Session 

```
//controller 获取session
@RequestMapping(value = "getSession")
@ResponseBody
public Map<String, String> getSession(
        HttpServletRequest request
) {
    Map<String, String> sessionMap = new HashMap<String, String>();
    //获取所有session名字
    Enumeration sessionEnum = request.getSession().getAttributeNames();
    while (sessionEnum.hasMoreElements()) {
        String sessionName = sessionEnum.nextElement().toString();
        sessionMap.put(sessionName, request.getSession().getAttribute(sessionName).toString());
        System.out.println("_______________sessionEnum______" + sessionName);
    }

    return sessionMap;
}
```

### 4.后端存入Session 

```
//controller 存入session
@RequestMapping(value = "/setSession")
@ResponseBody
public Map<String, String> setSession(
        HttpServletRequest request
) {
    request.getSession().setAttribute("controllerSetSession1", "这是我通过controller设置的session1");
    request.getSession().setAttribute("controllerSetSession2", "这是我通过controller设置的session2");
    Map<String, String> map = new HashMap<String, String>();
    map.put("info", "存入成功");
    return map;
}
```

