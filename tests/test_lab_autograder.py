import subprocess
import sys
from pathlib import Path


def test_analysis_script_exists():
    assert Path("eda_analysis.py").exists(), "eda_analysis.py not found"


def test_script_runs():
    """Run eda_analysis.py as a subprocess — should exit cleanly."""
    result = subprocess.run(
        [sys.executable, "eda_analysis.py"],
        capture_output=True, text=True, timeout=120
    )
    assert result.returncode == 0, f"Script failed:\n{result.stderr}"


def test_output_directory_exists():
    assert Path("output").is_dir(), "output/ directory not found"


def test_distribution_plots_exist():
    pngs = list(Path("output").glob("*.png"))
    assert len(pngs) >= 3, (
        f"Expected at least 3 PNG files in output/, found {len(pngs)}"
    )


def test_findings_report_exists():
    assert Path("Findings.md").exists(), "Findings.md not found"


def test_findings_has_substance():
    content = Path("Findings.md").read_text()
    assert len(content) > 500, (
        f"Findings.md appears too short ({len(content)} chars) — "
        "write a substantive analysis"
    )


def test_data_profile_exists():
    assert Path("output/data_profile.txt").exists(), "output/data_profile.txt not found"
