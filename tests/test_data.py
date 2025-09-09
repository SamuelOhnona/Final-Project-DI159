import os
def test_structure():
    assert os.path.exists('campaigns'), 'campaigns folder missing'
    assert os.path.exists('data/keywords_seed.csv'), 'keywords seed missing'
