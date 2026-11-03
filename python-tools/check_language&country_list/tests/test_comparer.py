from app.models.schemas import StatusTexts
from app.services.comparer import compare_lists

TEXTS = StatusTexts()


def test_compare_exist_missing_extra() -> None:
    expected = ["English", "Français", "Deutsch"]
    actual = ["English", "Italiano", "Français"]
    results = compare_lists(expected, actual, TEXTS)
    mapping = {item.name: item.status for item in results}
    assert mapping["English"] == "存在"
    assert mapping["Français"] == "存在"
    assert mapping["Deutsch"] == "不存在"
    assert mapping["Italiano"] == "多余"


def test_compare_trims_and_deduplicates() -> None:
    expected = [" English ", "English"]
    actual = ["English", " English "]
    results = compare_lists(expected, actual, TEXTS)
    assert len(results) == 1
    assert results[0].status == "存在"


def test_compare_is_exact_match() -> None:
    results = compare_lists(["Cote d'Ivoire"], ["Côte d'Ivoire"], TEXTS)
    assert results[0].status == "不存在"
    assert results[1].name == "Côte d'Ivoire"
    assert results[1].status == "多余"
