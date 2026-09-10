# 腾讯云官网部署

## 当前状态（2026-09-10）

- 北京轻量服务器 `lhins-09a023c0`，公网 IP `58.87.96.124`。
- 已按“备份后重装”提交并完成 Ubuntu Server 24.04 LTS 重装。实例名称仍为 `CentOS-YIMZ`，不代表当前系统。
- Nginx 已安装并运行，仅监听 `127.0.0.1:8080`，未开放公网 HTTP/HTTPS。
- 配置文件：服务器 `/etc/nginx/sites-available/powerclaw`。
- 网站目录：服务器 `/srv/powerclaw/current`，指向 `/srv/powerclaw/releases/34459610109-1`。
- 首版包含 17 个公开文件，8 个中英文页面通过 HTTP 逐字节核对；首页返回 200。
- 首版压缩包 SHA-256：`16bad0df6a1da0b8b84a11d2d463a8e078a6720fc8e06d82e53c6da4f7319529`。
- 已通过 GitHub Actions 完成首次发布：[运行 34459610109](https://github.com/xiaozhijiankang/powerclaw-web/actions/runs/34459610109)，结果 success，8 页逐字节校验通过；前一版 20260910-1 保留。
- 当前 GitHub 账号已获 admin 权限。旧 Pages 已从 legacy 改为 workflow，停止 main 分支的自动 Pages 发布；保留旧站现有部署和 powerclaw.app 域名。

## 发布流程

`.github/workflows/deploy-tencent.yml` 仅提供手动触发，使用 `tencent-server` environment。
脚本打包 8 个页面及 9 个样式/图片文件，排除内部文档、Git 信息及部署脚本。
发布包传输后校验 SHA-256，解压到新的版本目录，切换 `current` 符号链接。
通过服务器内部 HTTP 对全部页面逐字节比较，失败自动恢复之前的目录链接。
各历史目录保留，当前无自动清理。

这份流程已完成本地打包、shell 语法检查，并在服务器上执行了同一份发布脚本的首次成功发布。
已创建 powerclaw-deploy 专用账号，无 sudo 权限，仅对官网目录及自身目录有写权限；SSH 已实测通过，主机公钥通过腾讯云控制台核对。tencent-server 环境已创建并限制为 main 分支。用户已明确授权将专用私钥保存到环境 Secrets，5 项配置已完成；Actions 完整流程已实跑成功。本机临时部署私钥在验证后清理。

## 已完成的配置与维护参考

以下配置均已完成，重新搭建时可参考：

1. 检查 Settings → Pages 的发布分支。在国内版代码合并 main 前停用旧 Pages 自动发布，提前确认旧域名访问的切换安排。
2. 创建 `tencent-server` environment，并限定允许部署的分支。
3. 建立专用服务器部署账号，仅授予 `/srv/powerclaw` 和自身上传目录写权限，不授予 sudo。配置 SSH 密钥登录；密钥内容不得提交到仓库。
4. 在该 environment 设置 Secrets：

| Secret | 内容 |
| --- | --- |
| `DEPLOY_HOST` | `58.87.96.124` |
| `DEPLOY_PORT` | `22` |
| `DEPLOY_USER` | `powerclaw-deploy` |
| `DEPLOY_SSH_KEY` | 专用账号对应的 SSH 私钥 |
| `DEPLOY_KNOWN_HOSTS` | 通过可信腾讯云控制台核对的 SSH 主机公钥 known_hosts 行 |

不要用未经核对的 `ssh-keyscan` 结果替代主机身份验证。
若 Actions 到 SSH 的连接被现有防火墙阻止，先确认具体原因与最小访问范围，再调整；当前未修改防火墙。

5. 将 workflow 合并到默认分支后，从 Actions 手动运行并验证发布结果。

## 备案后对外上线

当前 8080 仅用于内部验证，Actions 运行成功也不会开放公网。
备案通过后再配置域名解析、HTTPS、公网监听、正式备案号和搜索索引策略。
保留内部 8080 校验入口供后续发布使用。公网配置单独添加，避免改变发布验证地址。
