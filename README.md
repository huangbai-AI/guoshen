# 过审 · guoshen

给 AI 一条视频，按 **通用规则 + 单平台规则** 检查语音、字幕与画面，给出可回看的时间点、依据和改法。支持 **小红书、抖音、B站、视频号**。

过审是一套开放的审核预检流程，不是永久有效的禁词表，也不连接平台内部审核系统。规则会变，案例有语境；我们把来源、时间和不确定性一起保留下来。

[使用指南](docs/usage.md) · [文档导航](docs/README.md) · [规则入口](rules/README.md) · [案例区](cases/README.md) · [共建流程](docs/community.md) · [贡献指南](CONTRIBUTING.md)

![视频、语音、字幕与画面一起检查](assets/illustrations/01-review.png)

## 开始使用

将仓库放入 Codex 技能目录；已有同名目录时先备份：

```sh
git clone https://github.com/huangbai-AI/guoshen.git ~/.codex/skills/guoshen
```

新建对话，发送视频并说：

> 用 $guoshen 检查这条视频在小红书、抖音、B站、视频号的发布风险，标出原文、时间点、依据和改法。

也可以只指定一个平台，或补充“这是商业合作”“只是加热失败”。审核结果分别标记：明确风险、需复核、按你的要求修改、未发现明显问题、未检查。不会给虚构的通过率。

本地提取需要 Python 3、FFmpeg、whisper.cpp 的 whisper-cli 与多语言模型；全画面文字和二维码识别使用 macOS Vision 与 Swift。模型不随仓库发布，其他系统不会自动切换工具。依赖、命令与采样范围见 [使用指南](docs/usage.md) 和 [提取说明](references/extraction.md)。

**脚本提取证据、召回线索，AI 助手结合完整上下文复核并写报告。** 独立运行脚本的接入方需要自行提供复核步骤，见 [完整审核流程](docs/ai-review.md)。

## 规则与依据

![通用规则与四个平台规则叠加](assets/illustrations/02-rules.png)

| 层级 | 内容 | 入口 |
| --- | --- | --- |
| 通用规则 | 违法危险、隐私、真实性、版权、广告、AI标识等58项检查问题 | [通用清单](rules/common/checklist.md) |
| 平台规则 | 平台社区规则、导流、官方入口与专项场景 | [小红书](rules/platforms/xiaohongshu.md) · [抖音](rules/platforms/douyin.md) · [B站](rules/platforms/bilibili.md) · [视频号](rules/platforms/wechat_channels.md) |
| 来源与时间 | 官方正文、入口、二手资料分开；记录适用期与复核日期 | [来源台账](references/sources.json) · [版本治理](docs/rule-lifecycle.md) |
| 个人要求 | 可选的更保守发布偏好，不冒充官方禁令 | [公开默认](references/user-profile.json) · [配置说明](profiles/README.md) |

当前有26条结构化检查规则、28个来源记录。来源记录不等于28份已取得的官方全文；**视频号运营规范正文已核实，外链、直播、电商等专项仍须按场景补查**。来源缺口必须输出需复核，各条核查日期单独记录，整理仓库不会刷新旧来源的核查日期。

不把“小红书/抖音出现任何网址必违规”或“B站任何网址都允许”写成统一结论。需结合实际导流目的、官方挂载权限、商业场景和当期条款。严格地址模式只是用户可选要求。

## 案例与共建

**这是一个共建项目。大家运行技能，在各个平台拿到实际反馈后，把结果回传给助手，一起完善真实案例库。**

![运行技能、获得平台反馈、匿名回传、自动提交PR，复核后进入案例库并帮助下一次审核](assets/illustrations/03-cases.png)

**运行技能 → 平台反馈 → 匿名回传 → 助手自动提交 PR → 维护者复核入库 → 帮助下一次审核。**

在运行技能的对话中回传通过、拒审或申诉结果，补充平台通知、日期、修改与重试记录。助手整理匿名案例、展示待公开内容；你确认有权公开并授权提交后，助手自动向本仓库创建案例修改提案（PR）。需要可用的 GitHub 登录与提交环境，具体步骤见 [共建流程](docs/community.md)。案例经维护者复核合并进入 `cases/records/`，模拟填写示例仍单独保留。

可以直接说：

> 这是上次视频在抖音的实际反馈。请整理匿名案例给我确认，确认后自动提交到 guoshen，完善案例库。

案例帮助复核后续判断；修改规则仍需另走 [版本治理](docs/rule-lifecycle.md)，不会自动生效。

- [案例区与填写说明](cases/README.md)：把事实、平台通知、AI推断和干扰因素分开。
- [提交案例](https://github.com/huangbai-AI/guoshen/issues/new?template=case.yml)：先匿名化，上传即公开，请勿包含私人原片、联系方式或未获授权截图。
- [提议规则修订](https://github.com/huangbai-AI/guoshen/issues/new?template=rule-change.yml)：补来源、日期、适用场景和反例。
- [贡献指南](CONTRIBUTING.md)：欢迎新增平台、提取工具、规则和分析方法。

当前提供5个**模拟填写示例**，真实案例区尚待社区贡献。模拟示例不计入统计、不作为规则证据。“删掉一个内容后通过”只能支持假设，不能单独证明它就是拒审原因。

## 仓库导航

| 目录 / 文件 | 用途 |
| --- | --- |
| [SKILL.md](SKILL.md) · [agents/](agents/) | 技能执行入口与助手展示配置 |
| [docs/](docs/README.md) | 使用、审核流程、版本治理和开发验证 |
| [scripts/](scripts/README.md) | 证据提取、规则上下文、候选扫描与现有测试 |
| [rules/](rules/README.md) | 通用规则、四平台规则、注册表和历史存档 |
| [references/](references/README.md) | 来源台账、提取方法、验收场景与参考记录 |
| [profiles/](profiles/README.md) | 可选个人要求；默认配置保留原路径 |
| [cases/](cases/README.md) | 模拟示例、真实记录和待复核共性 |
| [schemas/](schemas/README.md) | 规则与案例的数据格式 |
| [assets/illustrations/](assets/illustrations/README.md) | 配图与来源说明 |
| [.github/](.github/) | 案例表单、规则修订表单、贡献模板与自动校验 |

维护前运行现有检查，命令见 [开发与验证](docs/development.md)。项目版本见 [VERSION](VERSION)，变化见 [更新记录](CHANGELOG.md)，类似项目见 [开源参考](references/github-projects.md)。

原创代码和文档使用 [MIT 许可](LICENSE)；第三方规则及引用的权利说明见 [NOTICE](NOTICE)。
