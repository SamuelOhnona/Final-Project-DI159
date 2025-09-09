from agents.keyword_agent import KeywordAgent

def test_keyword_category_detection():
    k = KeywordAgent()
    assert k._detect_category("Assurance TNS in Rhône-Alpes") == "Assurance"
    assert k._detect_category("Banque loan for SMEs") == "Banque"
    assert k._detect_category("Travaux plumber Lyon") == "Travaux"
    assert k._detect_category("Immobilier apartment Paris") == "Immobilier"
