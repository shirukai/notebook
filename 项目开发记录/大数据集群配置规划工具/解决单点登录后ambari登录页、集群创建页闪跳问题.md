# 解决单点登录后ambari登录页、集群创建页闪跳问题

### 登录页闪跳 

注释掉一下内容,大约在app.js 93006行

      /*
      connectOutlets: function (router, context) {
                $('title').text(Em.I18n.t('app.name'));
                router.get('applicationController').connectOutlet('login');
            },
    
            serialize: function (router, context) {
                // check for login/local hash
                var location = router.get('location.location.hash');
                return {
                    suffix: location === '#' + router.get('localUserAuthUrl') ? '/local' : ''
                };
            }*/
### 集群页闪跳

设置    clusterInstallCompleted的值为true ,大约在app.js 92259行

```
clusterInstallCompleted: true,
```