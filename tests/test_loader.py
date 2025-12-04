from src.ingest.loader import load_content


def test_load_content_reads_file(tmp_path):
    file_path = tmp_path / "example.md"
    file_path.write_text("hello world", encoding="utf-8")

    raw = load_content(str(file_path))

    assert raw.text == "hello world"
    assert raw.path == str(file_path)
