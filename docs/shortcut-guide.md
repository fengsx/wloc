# 使用、迁移与排障

## 首次使用

先阅读 README 的兼容性状态，再安装对应客户端模块，启用 MITM 并信任客户端证书。模块匹配的主机包括 `gs-loc.apple.com`、`gs-loc-cn.apple.com`、`gsp-ssl.ls.apple.com` 及两种上游高德备用主机。

用 Safari 打开自己部署的选点网页，选点后点击「储存到设备」。网页查询的「当前生效坐标」是代理本地保存值，不是设备定位服务的独立测量结果。

## 从旧仓库迁移

1. 订阅本仓库对应模块，停用旧模块，避免重复脚本执行。
2. 保留客户端持久化键 `wloc_settings`；本分支没有改名。
3. 原网页收藏在旧站点的 localStorage 中，换站点不会自动迁移。请先记录收藏，不要清除旧浏览器数据。
4. 模块默认参数继续沿用上游值；自定义参数要手动核对。

## 快捷指令

在 iPhone 上直接安装：[WLOC设置位置](https://www.icloud.com/shortcuts/e0d3b9504c1541f182117fe328f68a5b)（[二维码](../shortcuts/WLOC设置位置-二维码.png)）、[WLOC恢复定位](https://www.icloud.com/shortcuts/fddd99ba529b457088243640b28ded6a)（[二维码](../shortcuts/WLOC恢复定位-二维码.png)）。

设置位置指令使用 `https://wloc.fengsx.workers.dev/api/parse?format=json` 解析地图链接，再通过手机代理模块拦截的 `https://gs-loc.apple.com/wloc-settings/save` 保存坐标。Apple 地图选点后点“共享 → WLOC设置位置”；高德地图可从“分享 → 更多”进入系统分享菜单。恢复指令清除保存值；若要确保停用虚拟位置，还需关闭 WLOC 模块。

## 排障顺序

| 现象 | 检查方向 |
| --- | --- |
| 模块下载失败 | GitHub raw 地址、仓库是否公开、网络可达性 |
| 地图空白 | Leaflet CDN、瓦片服务、浏览器网络 |
| 链接解析失败 | Worker 路由、原链接格式、地图服务响应 |
| 储存失败 | Safari 是否经过代理、模块规则和 MITM 证书 |
| 储存成功但定位不变 | 系统版本、locationd TLS 拒绝、GPS 覆盖、定位缓存 |
| 清除后仍改变位置 | 模块参数中是否另设了自定义经纬度，是否有重复模块 |

上游提出重启可能帮助清除缓存，但重启不能解决 TLS 证书校验限制。不要把反复切换飞行模式当成所有系统版本通用的解决方案。
