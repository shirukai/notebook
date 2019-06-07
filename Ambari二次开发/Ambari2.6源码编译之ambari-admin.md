# Ambari源码编译之ambari-admin

ambari-admin 使用的是angularjs + bower + gulp 

## 1.准备 

### 1.1下载源码 

#### 安装wget

```
yum -y install wget
```

#### 下载源码

将源码下载到/opt目录下

```
wget http://www.apache.org/dist/ambari/ambari-2.6.0/apache-ambari-2.6.0-src.tar.gz -O /opt/apache-ambari-2.6.0-src.tar.gz
```

### 1.2配置编译环境

#### 1.2.1安装node.js

下载

```
wget https://nodejs.org/dist/v8.5.0/node-v8.5.0-linux-x64.tar.gz /usr/lib/node-v8.5.0-linux-x64.tar.gz
```

解压

```
tar zxvf node-v8.5.0-linux-x64.tar.gz
```

配置环境变量

```
export NODE_HOME="/usr/lib/node-v8.5.0-linux-x64"
export PATH=$PATH:$NODE_HOME/bin
```

使修改后的文件生效

```
source /etc/profile 或者 . /etc/profile
```

查看安装情况

```
node -v
npm -v
```

#### 1.2.2安装bzip2

```
yum install bzip2
```

#### 1.2.3安装git

```
yum -y install git
```

## 2.编译

ambari-admin使用的是angularjs + bower +gulp

### 2.1修改 .bowerrc配置

#### 2.1.1切换目录

```
cd /opt/ambari-admin/src/main/resources/ui/admin-web
```

#### 2.1.2修改 .bowerrc

```
vim .bowerrc
```

#### 2.1.3内容 

```
{
    "directory": "app/bower_components",
    "allow_root": true
}
```

说明：添加一行`  "allow_root": true` 允许以root用户执行bower命令。也可以在执行命令的时候通过参数设定 如：bower install --allow-root    

### 2.2安装npm依赖包 

```
npm install
```

### 2.3安装全局gulp 

```
npm install -g gulp
```

### 2.4 安装全局bower

```
npm install -g bower
```

### 2.5 安装bower的依赖包 

```
bower install
```

### 2.6 安装gulp-webserver 

```
npm install gulp-webserver --save-dev
```

### 2.7 修改gulpfile.js文件

注释//+的地方是需要新增或者修改的地方

```
'use strict';

var gulp = require('gulp');
var $ = require('gulp-load-plugins')();
var webserver = require('gulp-webserver');//+

//+ 这个地方current如果为test就以webserver的方式启动，如果为build直接构建
var current = "test";
var config = {
    start_task:{
        test:"webserver",
        build:"build"
    }
};

//+
gulp.task('webserver', function(){
    gulp.src('app').pipe(webserver({
        port: 8000,//端口
        host: '192.168.162.127',//域名
        livereload: true,//实时刷新代码。不用f5刷新
        directoryListing: true,
        //fallback:'index.html',
        open:true
    }))
});


gulp.task('styles', function () {
  return gulp.src('app/styles/*.css')
    .pipe($.order([
      'app/styles/main.css',
      'app/styles/custom-admin-ui.css'   // This should always be the last stylesheet. So it can be dropped and be effective on build time
    ], { base: './' }))
    .pipe($.concat('main.css'))
    .pipe($.autoprefixer('last 1 version'))
    .pipe(gulp.dest('.tmp/styles'))
    .pipe($.size());
});

gulp.task('html', ['styles'], function () {
  var jsFilter = $.filter('**/*.js');
  var cssFilter = $.filter('**/*.css');

  return gulp.src('app/*.html')
    .pipe($.plumber())
    .pipe($.useref.assets({searchPath: '{.tmp,app}'}))
    .pipe(jsFilter)
    .pipe(jsFilter.restore())
    .pipe(cssFilter)
    .pipe(cssFilter.restore())
    .pipe($.useref.restore())
    .pipe($.useref())
    .pipe(gulp.dest('dist'))
    .pipe($.size());
});

gulp.task('views', function () {
  return gulp.src('app/views/**/*.html')
    .pipe(gulp.dest('dist/views'));
});

//+
gulp.task('xml',function(){
  return gulp.src('app/view.xml')
  .pipe(gulp.dest('dist'))
});

gulp.task('images', function () {
  return gulp.src('app/img/**/*')
    .pipe(gulp.dest('dist/img'))
    .pipe($.size());
});

gulp.task('fonts', function () {
  return $.bowerFiles()
    .pipe($.filter('**/*.{eot,svg,ttf,woff}'))
    .pipe($.flatten())
    .pipe(gulp.dest('dist/fonts'))
    .pipe($.size());
});

gulp.task('extras', function () {
  return gulp.src(['app/*.*', '!app/*.html'], {dot: true})
    .pipe(gulp.dest('dist'));
});

gulp.task('clean', function () {
  return gulp.src(['.tmp', 'dist'], {read: false}).pipe($.clean());
});
//+
gulp.task('build', ['html', 'views', 'images', 'fonts','xml', 'extras']);

//+
gulp.task('default', ['clean'], function () {
  gulp.start(config.start_task[current]);
});
```

## 3.编译

gulp提供两种方式编译，一种是webserver的方式，单独启动一个web服务，来测试修改后的ambari-Admin。另一种是直接编译后软链接到ambari-server以真实环境来测试。

### 3.1以webserver方式启动

#### 3.1.1修改gulpfile.js文件 

```
var current = "test";
```

#### 3.1.2启动gulp

```
gulp
```

#### 3.1.3测试 

访问http://192.168.162.127:8000/index.html#/ 即可查看效果。

### 3.2 以ambari-server服务真实环境启动

#### 3.2.1 修改gulpfile.js文件 

```
var current = "test";
```

#### 3.2.2启动gulp 

```
gulp
```

#### 3.2.3建立软链接

切换到ambari-server对应admin页面的目录下

```
cd /var/lib/ambari-server/resources/views/work
```

备份 ADMIN_VIEW{2.6.0.0} 

```
mv ADMIN_VIEW\{2.6.0.0\} ADMIN_VIEW\{2.6.0.0\}.bak
```

建立软链接

```
ln -s /opt/apache-ambari-2.6.0-src/ambari-admin/src/main/resources/ui/admin-web/dist ADMIN_VIEW\{2.6.0.0\}
```

复制ADMIN_VIEW\{2.6.0.0\}.bak里的view.xml文件到ADMIN_VIEW\{2.6.0.0\}

```
cp view.xml ../ADMIN_VIEW\{2.6.0.0\}
```

复制ADMIN_VIEW\{2.6.0.0\}.bak里的view.xml文件到/opt/apache-ambari-2.6.0-src/ambari-admin/src/main/resources/ui/admin-web/app

```
cp view.xml /opt/apache-ambari-2.6.0-src/ambari-admin/src/main/resources/ui/admin-web/app
```

#### 3.2.4重启ambari-server 

```
ambari-server restart
```

#### 3.2.5  测试 

访问http://192.168.162.127:8080 查看效果