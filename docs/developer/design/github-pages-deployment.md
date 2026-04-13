# 设计：GitHub Pages 文档部署

- `change slug`：`github-pages-deployment`
- 对应规范：`../specs/github-pages-deployment.md`

## 总体方案

采用单独的 `.github/workflows/docs.yml` 作为文档发布链路。工作流在 GitHub Actions 中安装项目开发依赖，执行 `mkdocs build` 生成 `site/`，再通过 GitHub 官方 Pages Actions 上传并部署该产物。

## 模块与文件落点

- 发布工作流：`.github/workflows/docs.yml`
- 文档站配置：`mkdocs.yml`
- 维护者约束：`AGENTS.md`
- 维护者规范与设计：
  - `docs/developer/specs/github-pages-deployment.md`
  - `docs/developer/design/github-pages-deployment.md`

## 调用流

1. `actions/checkout` 拉取仓库代码
2. `actions/setup-python` 固定 Python 3.11
3. `actions/configure-pages` 确保 GitHub Pages 使用 Actions 部署链路
4. 安装 `.[dev]` 依赖
5. 执行 `mkdocs build`
6. `actions/upload-pages-artifact` 上传 `site/`
7. `actions/deploy-pages` 发布到 `github-pages` 环境

## 为什么这样设计

- 将部署逻辑放进工作流文件后，配置可审查、可回滚、可复用，不需要每次依赖网页设置手工调整
- 直接部署 `site/` 可以保证远端站点与本地 MkDocs 构建一致，避免再次退回 Jekyll 渲染
- 在 `mkdocs.yml` 中显式写入 `site_url`，可以让项目页路径、canonical URL 与站点内部行为更稳定

## 备选方案与取舍

### 方案 A：继续使用 GitHub Pages 默认的 `docs/` / Jekyll 发布

不采用。因为这样发布出来的是 Jekyll 渲染结果，不是 MkDocs Material 站点，本地与远端会持续不一致。

### 方案 B：把 `site/` 提交到 `gh-pages` 分支

不采用。因为这会把生成产物纳入版本控制，增加分支维护与合并噪音，而 GitHub 官方 Pages Actions 已经提供了更直接的产物部署路径。

## 风险与缓解

- 风险：仓库 Pages 未启用或未切换到 Actions
  - 缓解：工作流中使用 `actions/configure-pages`，并开启 `enablement`
- 风险：项目页基础 URL 配置不完整，导致链接或 canonical 行为异常
  - 缓解：在 `mkdocs.yml` 中声明 `site_url`
- 风险：未来维护时误删文档部署工作流，导致远端再次退回默认发布方式
  - 缓解：在 `AGENTS.md` 与维护者规范中明确 `.github/workflows/docs.yml` 的职责

## 验证计划

- 运行 `ruff check .`
- 运行 `pytest`
- 运行 `mkdocs build`
- 确认工作流文件语义上包含 Pages 所需权限、构建步骤、产物上传与部署步骤
