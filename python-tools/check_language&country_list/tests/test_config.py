from app.config import DEFAULT_CONFIG, _strip_json_comments, load_project_config


def test_default_json_loads_with_comments() -> None:
    config = load_project_config(DEFAULT_CONFIG)
    assert config.project == "X1102D"
    assert config.excel.data_start_row == 2
    assert config.excel.country_name_column == 1
    assert "settings_add_language" in config.screens


def test_strip_json_comments_keeps_string_content() -> None:
    text = """
    {
      // 说明
      "url": "https://example.com/path", // 行尾注释
      "name": "value"
    }
    """
    parsed = _strip_json_comments(text)
    assert "// 说明" not in parsed
    assert "https://example.com/path" in parsed
    assert "value" in parsed
