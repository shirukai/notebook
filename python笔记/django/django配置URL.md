# django配置URL

之前配置url是直接修改url.py如下图：

```
from django.conf.urls import url
from django.contrib import admin
import blog.views as bv
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/', bv.index)
]
```

这样是可行的，但是如果我们的网站过于庞大，会有好多应用，而且url也很多。这时候，我们写到一个文件里，会显得特别乱，不容易管理，而且，容易出现重名的现象。

所以官方提示：

```
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
```

引入其他的url配置



### 一、引入include这个方法：

```
from django.conf.urls import url,include
```

### 二、修改之前的url配置

```
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^blog/', include('blog.urls'))
]
```

### 三、在应用目录下创建urls.py文件

```
from django.conf.urls import url, include
import blog.views as bv

urlpatterns = [
    url(r'^index/', bv.index)
]
```

访问blog/index即可