from main import generate_recommendations

def test_yazilim_analitik():
    results = generate_recommendations("yazılım", "analitik")
    assert len(results) > 0
    assert results[0][0] == "Yazılım Geliştirici"

def test_tasarim_yaratici():
    results = generate_recommendations("tasarım", "yaratici")
    careers = [r[0] for r in results]
    assert "Grafik Tasarımcı" in careers

def test_no_match():
    results = generate_recommendations("spor", "liderlik")
    assert results == []
