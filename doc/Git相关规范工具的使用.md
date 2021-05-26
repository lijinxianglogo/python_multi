# Git相关规范工具的使用

---


> - commitizen-----用来代替git commit命令，可以按照制定的模版，生成commit message
> - cz-conventional-changelog-----Google团队的commit message模板，也可以使用自定义的模版
> - standard-version-----根据符合Google规范的commit message自动生成 CHANGELOG



## 安装与使用

### 1. 安装nodejs

可以到[官网](http://nodejs.cn/)，下载安装包，Windows可以直接下载安装包，Linux可以下载对应的软件包，也可以下载源代码自行编译，安装完成后，执行

`node -v`

显示了版本号，则安装成功了。由于nodejs默认的软件源在国外，为了加快软件安装速度，可以将源设置为淘宝源

`npm config set registry https://registry.npm.taobao.org --global`

`npm config set disturl https://npm.taobao.org/dist --global`

这两条命令在Linux环境下可能需要root权限运行。

### 2. 安装相关工具

可以使用命令行

`npm install -g commitizen cz-conventional-changelog standard-version`

来安装相关nodejs软件包。如果只是针对单个项目，不想全局安装，可以执行

`npm install -save commitizen cz-conventional-changelog standard-version`

来进行安装

### 3. 配置与使用

需要指定 commit message的模板，如果希望全局使用，可以在~目录下建立.czrc配置文件，执行以下命令行，可以直接创建文件，并指定cz-conventional-changelog作为模板文件。

`echo '{ "path": "cz-conventional-changelog" }' > ~/.czrc`

如果只希望在特定项目中使用，可以在项目根目录建立package.json文件，并加入以下内容

```
"config": {
    "commitizen": {
      "path": "cz-conventional-changelog"
    }
  }
```

完成后，就可以使用`git cz`命令来代替`git commit`命令。

如果需要生成`CHANGELOG.md`可以执行命令`standard-version`来自动生成。
