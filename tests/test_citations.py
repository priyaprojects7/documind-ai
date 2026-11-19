from app.generation.citation_checker import validate_citations

def test_citation_checker_flags_unknown_labels():
    result = validate_citations("Claim [S1] and unsupported [S9].", [{"label":"S1"}])
    assert result['valid'] == ['S1']
    assert result['unknown'] == ['S9']
