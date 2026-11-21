# 本仓项目执行规范

适用仓库：hduhuh/zhuangxiudaishoufangyuanfenxi
全局协议唯一权威：hduhuh/ziwo-ai-os，V1.0，固定 Commit `75366992126779399aa66ad039431b3fd7d2f0fd`。
协议：https://github.com/hduhuh/ziwo-ai-os/blob/75366992126779399aa66ad039431b3fd7d2f0fd/control-center/github-sync-v1/GITHUB_SYNC_PROTOCOL.md
执行细则：https://github.com/hduhuh/ziwo-ai-os/blob/75366992126779399aa66ad039431b3fd7d2f0fd/control-center/github-sync-v1/EXECUTION_STANDARD.md
工具规则：https://github.com/hduhuh/ziwo-ai-os/blob/75366992126779399aa66ad039431b3fd7d2f0fd/control-center/github-sync-v1/tools/

保留本仓原有业务、安全和验收要求。本文件是项目执行入口，不另立全局协议副本。
开工核对唯一主仓、remote、分支、HEAD、状态、任务与唯一执行者；每工具独立分支及工作区。
正式成果必须真实测试、Commit、Push、Draft PR，运行本目录 verify_delivery.py 核验远端和同 SHA CI。
无权限交完整文件/补丁由获准集成者同步，标明代理来源；不能冒充该工具原生测试通过。
本次只更新治理文件，不修改业务、数据库或生产。不写 main/master/默认分支，不合并、不部署、不强推、不自动删除。
规则引用已分发不等于任一工具已安装、读取或具备原生写入能力。
公开仓库仅含本执行入口和通用校验代码，不复制私有全局知识、内部报告、客户资料或凭据。
