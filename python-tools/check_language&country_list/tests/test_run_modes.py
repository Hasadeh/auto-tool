from app.models.run_modes import RUN_MODES, get_run_mode


def test_all_modes_defined() -> None:
    assert set(RUN_MODES) == set(range(8))


def test_mode_1_is_full_check() -> None:
    mode = get_run_mode(1)
    assert mode.check_oobe_language
    assert mode.check_oobe_country
    assert mode.skip_oobe
    assert mode.check_settings_language


def test_mode_4_country_only() -> None:
    mode = get_run_mode(4)
    assert not mode.check_oobe_language
    assert mode.check_oobe_country
    assert not mode.skip_oobe
    assert not mode.check_settings_language
    assert "国家" in mode.start_hint


def test_mode_5_settings_only() -> None:
    mode = get_run_mode(5)
    assert mode.check_settings_language
    assert not mode.skip_oobe
    assert not mode.check_oobe_language


def test_unknown_mode_raises() -> None:
    try:
        get_run_mode(9)
    except ValueError as exc:
        assert "0-7" in str(exc)
    else:
        raise AssertionError("expected ValueError")
