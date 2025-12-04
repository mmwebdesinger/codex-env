# TourVideo-Script-Factory 项目计划

## 一、项目愿景与范围
- **目标**：从多格式旅游线路文档（PDF/Word/Markdown/纯文本等）自动解析，生成三类脚本：
  - 抖音 40 秒口播脚本
  - 视频号 60–90 秒口播脚本
  - 剪映导演脚本（含镜头、旁白、字幕、画面建议）
- **语言/技术栈**：Python 3，模块化、可测试，偏重文本处理与可扩展的模板化生成。
- **输入约束**：仅文本代码文件，不在仓库生成任何二进制示例文件；测试时用纯文本/Markdown 样例。

## 二、系统总体架构
```
+---------------------+
| 输入层/导入层       | <-- PDF/Word/Markdown/纯文本 (路径/URL/字符串)
+---------------------+
            |
            v
+---------------------+      +-------------------+
| 文档解析/标准化层   | ---> | 结构化行程模型    |
| (格式解析、清洗、   |      | (目的地/天数/     |
| 正则+LLM补全)       |      | 景点/交通/预算等) |
+---------------------+      +-------------------+
            |                           |
            |                           v
            |               +----------------------+
            |               | 生成层               |
            |               | - 模板引擎           |
            |               | - 风格/时长约束      |
            |               | - 口播/导演脚本生成  |
            |               +----------------------+
            |                           |
            v                           v
+---------------------+      +----------------------+
| 质量控制与评估层    | ---> | 输出层              |
| (一致性/时长/术语)  |      | (文本+结构化 JSON) |
+---------------------+      +----------------------+
```

### 模块设计（Python 包）
- `ingest/`
  - `loaders.py`：文件/字符串输入抽象，支持本地文件、URL、stdin；统一返回文本或中间表示。
  - `parsers.py`：按格式解析（Markdown/纯文本/预留 PDF、DOCX 钩子）；使用可插拔策略，返回统一的段落列表。
- `normalization/`
  - `cleaning.py`：去噪、正则分段、表格/列表转文本、去除水印和无关页眉页脚。
  - `structure.py`：规则+可选 LLM 提示，抽取“天数-景点-交通-餐宿-备注”结构；定义 `Itinerary` 数据类。
- `domain/`
  - `models.py`：核心数据模型（`Itinerary`, `DayPlan`, `Poi`, `SceneCue`, `NarrationSegment`）。
  - `constraints.py`：时长、节奏、口播语速、品牌/安全合规词表。
- `generation/`
  - `templates.py`：三类脚本的可配置模板片段（开头钩子、亮点、行动号召）。
  - `stylers.py`：语气/人设/口播节奏调整器（短句化、口语化、Emoji/禁用列表）。
  - `timing.py`：根据目标时长和语速估算字数分配，切分段落。
  - `renderers.py`：组合结构化行程与模板，生成抖音/视频号口播稿；生成剪映导演脚本（镜头、字幕、画面建议）。
- `quality/`
  - `validators.py`：字段完整性、敏感词/禁用词检测、长度校验、CTA 必备元素检测。
  - `review.py`：可选 LLM self-check 提示；规则评分（信息覆盖率、节奏、可听度）。
- `io/`
  - `exporters.py`：输出为纯文本或 JSON；支持多稿并列导出。
- `cli.py`
  - CLI 入口：支持 `parse`, `generate`, `validate`, `full-pipeline` 子命令；便于本地测试。

### 运行流程（管线）
1. **导入**：加载文件/字符串 → 识别格式 → 调用对应解析器。
2. **解析/标准化**：清洗文本，抽取结构化行程（规则+LLM 补全）。
3. **生成**：基于行程模型、模板与时长约束，产出口播稿与导演脚本。
4. **质量控制**：规则校验 + 可选 LLM 复核；给出提示或自动修正。
5. **导出**：输出多种格式（文本/JSON），支持同时导出三种脚本。

## 三、数据模型草案
```python
@dataclass
class Poi:
    name: str
    highlights: list[str] = field(default_factory=list)
    timing_hint: str | None = None

@dataclass
class DayPlan:
    day: str
    title: str | None
    activities: list[Poi]
    transport: str | None
    meals: str | None
    lodging: str | None

@dataclass
class Itinerary:
    title: str
    days: list[DayPlan]
    duration: str | None
    audience: str | None
    theme: str | None
```

## 四、质量与风格规则
- **时长/字数**：抖音约 110–140 字，视频号约 180–260 字；剪映导演脚本按镜头拆分，每镜头旁白 10–20 字。
- **语气**：口语化、行动导向、首句钩子；避免堆砌形容词，强调“做什么/怎么玩/怎么省钱”。
- **安全/合规**：敏感词和禁止承诺（如“包过”“零风险”）；涉政涉黄涉暴过滤。
- **结构**：开头钩子 → 行程亮点（按天/场景） → 交通/省心点 → 行动号召。

## 五、测试策略
- **单元测试**：
  - parsers/cleaning/structure：用 Markdown/纯文本样例验证分段与行程抽取。
  - generation/timing：字数分配与分镜切分。
  - validators：敏感词检测、长度校验。
- **集成测试**：
  - CLI `full-pipeline` 在示例文本上生成三类脚本并校验输出结构。
- **无需二进制样例**：测试输入以 Markdown/纯文本字符串或临时文件生成。

## 六、里程碑与阶段任务（可渐进交付）
1. **M1：基础解析与数据模型**
   - 建立包结构与 `Itinerary`/`DayPlan` 数据类。
   - 支持纯文本/Markdown 解析，输出段落列表。
   - 清洗与简单规则抽取行程结构（不依赖 LLM）。
2. **M2：模板化生成**
   - 定义三类脚本模板与字数分配逻辑。
   - 实现抖音/视频号口播稿生成器。
   - 引入风格化处理（短句化、CTA）。
3. **M3：导演脚本与质量控制**
   - 剪映导演脚本渲染器（镜头/旁白/字幕/画面建议）。
   - 规则校验与敏感词/长度检查。
   - CLI 子命令贯通单端到端流程。
4. **M4：LLM 增强与评估**
   - LLM 辅助抽取与 self-check 提示。
   - 评分与多稿对比输出。
   - 性能优化（缓存/可配置语速）。

## 七、下一步开发任务（分解）
- **任务 A：初始化包结构与数据模型**
  - 创建包目录 `src/tourvideo/`，编写 `domain/models.py` 和最小 `__init__.py`。
  - 添加 `Itinerary/DayPlan/Poi` 数据类及类型检查。
  - 建立基础测试样例（pytest）。
- **任务 B：解析与清洗模块（Markdown/纯文本）**
  - 在 `ingest/parsers.py` 添加纯文本/Markdown 解析函数，输出段落列表。
  - 在 `normalization/cleaning.py` 实现去噪、分段、简单正则抽取日程行（如“D1/Day 1/第1天”）。
  - 为上述函数补充单元测试，使用内联字符串作为输入。
- **任务 C：行程结构抽取（规则版）**
  - 在 `normalization/structure.py` 将分段转换为 `Itinerary` 对象，支持基础字段填充。
  - 支持缺省字段回退策略（未提供住宿/交通时填 `None`）。
  - 增加覆盖解析边界案例的测试。
- **任务 D：模板和时长分配**
  - 在 `generation/templates.py` 定义三个脚本模板片段；在 `generation/timing.py` 根据目标时长返回建议字数分配。
  - 在 `generation/stylers.py` 处理短句化与 CTA 拼接。
  - 单元测试验证字数分配与模板占位替换。
- **任务 E：渲染器与导出**
  - 在 `generation/renderers.py` 组合行程与模板生成抖音/视频号文案，生成剪映导演脚本（分镜+字幕+画面描述）。
  - 在 `io/exporters.py` 支持文本/JSON 导出，确保无二进制输出。
  - 集成测试：给定 Markdown 行程文本，产出三种脚本并校验字段。
- **任务 F：质量校验与 CLI**
  - 在 `quality/validators.py` 添加敏感词、长度、CTA 检查；在 `quality/review.py` 预留 LLM 检查接口。
  - 实现 `cli.py`，提供 `parse`, `generate`, `validate`, `full-pipeline`。
  - 编写 CLI 集成测试，使用纯文本样例。
- **任务 G：LLM 增强与持续改进**
  - 增加 LLM 辅助抽取与 self-check 提示（配置化 API 调用/占位）。
  - 增加多稿对比、打分与选择逻辑。
  - 性能/缓存与可配置语速优化。

## 八、风险与对策
- **多格式解析复杂**：先覆盖 Markdown/纯文本，PDF/DOCX 通过可插拔解析器逐步迭代。
- **时长控制**：通过字数预估与短句化策略，必要时在生成后二次截断/压缩。
- **敏感内容**：维护禁用词表，规则优先；LLM 仅作为补充，避免 hallucination。
- **测试稳定性**：全部使用文本样例，避免外部依赖；CI 跑 pytest。

