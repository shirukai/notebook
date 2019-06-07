# 使用maven打包可执行jar

在项目中需要将一些算法打包成可执行的jar，然后上传算法。这里主要是用的是maven插件进行可执行jar打包，插件包括maven-shade-plugin和org.scala-tools（主要用来打包编译scala文件）。下面将从搭建普通项目到打包可执行jar详细讲解一下。

## 搭建maven项目

### 创建项目

在IDEA下创建一个普通的maven项目：File-->New -->Project-->Maven-->maven-archetype-quickstart

![](https://shirukai.gitee.io/images/201805041425_367.gif)

### 引入Maven打包插件

修改pom.xml文件

```
    <build>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-shade-plugin</artifactId>
                <version>2.4.3</version>
                <executions>
                    <execution>
                        <phase>package</phase>
                        <goals>
                            <goal>shade</goal>
                        </goals>
                        <configuration>
                            <transformers>
                                <transformer
                                        implementation="org.apache.maven.plugins.shade.resource.ManifestResourceTransformer">
                                    <!--main方法所在的类路径-->
                                    <mainClass>com.hollysys.App</mainClass>

                                </transformer>
                            </transformers>
                            <artifactSet>
                                <includes>
                                 	<!--需要一起打包的依赖jar包-->
                                    <include>com.alibaba:fastjson</include>
                                </includes>
                            </artifactSet>
                        </configuration>
                    </execution>
                </executions>
            </plugin>

            <plugin>
                <groupId>org.scala-tools</groupId>
                <artifactId>maven-scala-plugin</artifactId>
                <version>2.15.2</version>
                <executions>
                    <execution>
                        <id>scala-compile-first</id>
                        <goals>
                            <goal>compile</goal>
                        </goals>
                        <configuration>
                            <includes>
                                <include>**/*.scala</include>
                            </includes>
                        </configuration>
                    </execution>
                    <execution>
                        <id>scala-test-compile</id>
                        <goals>
                            <goal>testCompile</goal>
                        </goals>
                    </execution>
                </executions>
            </plugin>
        </plugins>
    </build>
```

## 打包测试

配置好相关插件之后，我们就可以进行打包测试了。在IDEA的工具栏，点击【Maven Projects】然后执行【package】

![](https://shirukai.gitee.io/images/201805041438_377.png)

执行完成后，会在项目的target目录下生成一个jar包，我们可以拿到这个jar包使用命令行执行以下。

![](https://shirukai.gitee.io/images/201805041505_513.png)

