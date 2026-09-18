import tempfile
from pathlib import Path

from core.autonomy.codebase_intelligence import CodebaseIntelligence
from core.autonomy.model_adapter import ModelAdapter

def test_model_adapter_is_safe_when_unconfigured(monkeypatch):
    for key in ("PREM_LLM_ENDPOINT","PREM_LLM_MODEL","PREM_LLM_API_KEY"):
        monkeypatch.delenv(key, raising=False)
    assert not ModelAdapter().configured()

def test_codebase_intelligence_scans_python():
    with tempfile.TemporaryDirectory() as d:
        p=Path(d)/"sample.py"
        p.write_text("class Demo:\n    pass\n", encoding="utf-8")
        data=CodebaseIntelligence(d).scan()
        assert "sample.py" in data["python_files"]
        assert "Demo" in data["symbols"]["sample.py"]
