# ScrapydManagement
Scrapyd 自带的后台管理页面功能太简单，无法满足业务需求，自己尝试性的写一个

### 2018-1-9
  1、初始化项目结构,开始填坑<br>
  2、创建虚拟环境fvenv<br>
  3、创建数据库models<br>
  4、初始化app文件夹内__init__.py文件以及scdMain内__init__.py文件<br>
  5、初始化config.py 文件结构<br>
  6、修改manager.py启动文件结构<br>

### 2018-1-10
  1、新增view内容,含登录/注册/首页/登出/邮件发送/登录步骤处理等方法<br>
  2、新增一套html模板并修改适应项目需求

### 2018-1-11
  1、新增scrapyd API配置<br>
  2、新增utils.urllibfunc 工具包,后续urllib相关内容添加在这里<br>
  3、新增spiderinfo.py 存储spider相关操作<br>
  4、新增APScheduler依赖, 用于完成任务调度   （调度器简介）[http://jinbitou.net/2016/12/19/2263.html]<br>
  5、新增redis依赖, 用作APScheduler JobStore.<br>
  6、完成SchedUtilis模块基本功能

### 2018-1-12
  1、新增pymysql依赖,mysql作为项目主要数据库, redis仅保存任务信息<br>
  2、新增spiMain路由,spider相关操作转移到该路由下<br>
  3、增加apsched调度页面模板和flash消息模板<br>
  
### 2018-1-16
  1、新增apsched页面模板
  2、着手添加flash消息支持
  3、完善任务调度相关api

### 2018-1-17
  1、努力构思编写前端模板


  