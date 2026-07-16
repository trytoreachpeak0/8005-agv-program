# RCS介绍
## RCS是什么
RCS 是负责统一管理和调度一群 AGV/AMR 的“大脑

## 斯坦德RCS
RIoT 是 RobotInternet of Things 的缩写，以下简称为“RIoT”。RIoT 是一个设备互联管理平台，通过标准的通信协议，实现对整厂所涉及硬件的连接和控制。软件具备低代码编程能力，可通过配置化的方式，快速搭建适配不同用户场景的搬运和控制流程，降低业务系统的开发和部署成本，让给更多的业务人员通过“托拉拽”的方式构建符合自身需求的业务流程。

## 本项目如何使用RIoT
1. 通过网页端访问RIoT，使用RIoT网页端功能，主要是给是实施和运维人员使用
2. 通过RIoT API，可以实现部分网页端功能，但大部分主要功能都可以通过API直接控制，主要是给app使用

## 如何通过网页端访问RIoT
1. 打开chrome
2. 访问链接: RIoT所在ip+端口号8888，例如http://172.19.206.222:8888/
3. 输入账号密码登录(账号admin,密码admin)
4. 登入RIoT，可使用RIoT各项管理功能

## 如何通过API访问RIoT
1. 通过用户登录API获得bearer token
2. 放在HTTP请求头里，访问其他RIoT API

## 如何获取RIoT API
1. 可看文档
2. 可看RIoT的swagger(RIoT所在ip+端口号8888/swagger-ui/index.html#/)
例如http://172.19.206.222:8888/swagger-ui/index.html#/

## 本仓库相关资料

- [`riot_swagger/`](./riot_swagger/)：RIoT OpenAPI 原始快照，用于查询静态接口契约。
- [`riot_ithing_model/`](./riot_ithing_model/)：设备物模型快照，用于查询属性、事件、服务和枚举。
- [`riot-sdk/`](./riot-sdk/)：C# / Python 调用客户端。
- [`riot-behavior-lab/`](./riot-behavior-lab/)：通过现场实验验证真实接口行为、可观测状态变化和异常语义。

