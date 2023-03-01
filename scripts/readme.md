# 第三方库编译说明
当前目录下的baseline.json文件中存放的是已通过本地编译的vcpkg中各个库对应的版本。

thirdparty.json文件中则是需要安装的包和对应的版本号。

## 库添加和版本修改
库添加直接在当前目录下thirdparty.json文件中添加所需的库和对应的版本即可（库和版本号可在vcpkg中通过[vcpkg search 库名称]命令查看）。

若是需要修改库对应的版本，只需手动修改thirdparty.json文件中库的版本。

## .py运行流程
1.在vcpkg中创建一个新分支{new_branch_name}，读取其versions/baseline.json文件中的库名称和版本，若其中的库在当前目录下的baseline.json文件中没有，则将其添加进当前目录下的baseline.json文件中；

2.读取当前目录下的baseline.json文件中库的名称和版本，并与thirdparty.json文件中库的版本进行对比，若不同，则修改当前目录下的baseline.json；

3.将vcpkg新创建的分支{new_branch_name}下的versions/baseline.json用当前目录下的baseline.json替换，以确保所有库的版本都是已通过本地编译对应的库版本；

4.将thirdparty.json文件中所需的库生成vcpkg.json文件(vcpkg将根据该文件编译所需的库)。
