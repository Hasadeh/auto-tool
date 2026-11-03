from app.models.schemas import CompareItem, StatusTexts


def compare_lists(
    expected: list[str],
    actual: list[str],
    status_texts: StatusTexts,
) -> list[CompareItem]:
    expected_names = _normalize(expected)
    actual_names = _normalize(actual)
    actual_set = set(actual_names)
    expected_set = set(expected_names)

    results = [
        CompareItem(
            name=name,
            status=status_texts.exist if name in actual_set else status_texts.missing,
        )
        for name in expected_names
    ]
    for name in actual_names:
        if name not in expected_set:
            results.append(CompareItem(name=name, status=status_texts.extra))
    return results


def _normalize(items: list[str]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for item in items:
        name = (item or "").strip()
        if not name or name in seen:
            continue
        result.append(name)
        seen.add(name)
    return result
