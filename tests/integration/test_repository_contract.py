from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_docs_tree_matches_spec_driven_layout() -> None:
    required_paths = {
        "docs/index.md",
        "docs/getting-started.md",
        "docs/tutorials/index.md",
        "docs/tutorials/geometry-normalization-workflow.md",
        "docs/tutorials/point-cloud-metrics-workflow.md",
        "docs/api/index.md",
        "docs/api/geometry.md",
        "docs/api/metrics.md",
        "docs/concepts/index.md",
        "docs/concepts/architecture.md",
        "docs/concepts/spec-driven-development.md",
        "docs/developer/specs/index.md",
        "docs/developer/specs/feature-template.md",
        "docs/developer/specs/github-pages-deployment.md",
        "docs/developer/specs/repository-layout-and-workflow.md",
        "docs/developer/specs/geometry-normalization.md",
        "docs/developer/specs/point-cloud-distance-metrics.md",
        "docs/developer/design/index.md",
        "docs/developer/design/feature-template.md",
        "docs/developer/design/github-pages-deployment.md",
        "docs/developer/design/repository-layout-and-workflow.md",
        "docs/developer/design/geometry-normalization.md",
        "docs/developer/design/point-cloud-distance-metrics.md",
    }

    missing_paths = sorted(path for path in required_paths if not (ROOT / path).exists())
    assert not missing_paths, f"missing paths: {missing_paths}"


def test_mkdocs_nav_keeps_developer_hidden() -> None:
    mkdocs_text = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
    nav_text = mkdocs_text.split("nav:", maxsplit=1)[1]

    assert "developer/" not in nav_text
    assert "开发者" not in nav_text


def test_local_doc_portal_exposes_hidden_developer_entries() -> None:
    portal = (ROOT / "open-docs.html").read_text(encoding="utf-8")

    assert "./site/developer/specs/index.html" in portal
    assert "./site/developer/design/index.html" in portal


def test_spec_driven_skill_and_check_script_exist() -> None:
    assert (ROOT / ".agents/skills/qrlib-spec-driven-change/SKILL.md").exists()
    assert (ROOT / "scripts/check.sh").exists()


def test_agents_reference_spec_and_design_paths() -> None:
    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")

    assert "docs/developer/specs" in agents
    assert "docs/developer/design" in agents


def test_docs_workflow_deploys_mkdocs_site_to_pages() -> None:
    workflow = (ROOT / ".github/workflows/docs.yml").read_text(encoding="utf-8")

    assert 'branches: ["main", "master"]' in workflow
    assert "workflow_dispatch:" in workflow
    assert "actions/configure-pages@v5" in workflow
    assert "enablement: true" in workflow
    assert "mkdocs build" in workflow
    assert "path: site" in workflow
    assert "actions/deploy-pages@v4" in workflow
    assert "github.event_name == 'push'" not in workflow
