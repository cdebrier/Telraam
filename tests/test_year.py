import datetime as dt
import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from extract_year import aggregate, tranches   # noqa: E402
from extract_profile import parse_profile      # noqa: E402


def raw(car_days, v85, op, cars_h, pie):
    return {"pie": pie, "v85": {"speed_v85": v85, "speed_histogram_opacity": op}, "h24": {"car": cars_h},
            "days": {"car": car_days}}


class Year(unittest.TestCase):
    def test_tranches_contigues(self):
        t = tranches(dt.date(2026, 9, 28))
        self.assertEqual(len(t), 4)
        self.assertEqual(t[-1][1], dt.date(2026, 9, 28))
        for (s, e), (s2, _) in zip(t, t[1:]):
            self.assertEqual((s2 - e).days, 1)
        self.assertEqual((t[0][1] - t[0][0]).days, 90)

    def test_somme_et_ponderation(self):
        pie = {"car": 100, "heavy": 10, "bike": 5, "pedestrian": 5, "night": 20}
        a = raw([10, 10, 0], [50, 60, 0], [1, 1, 1], [100, 300, 50], pie)
        b = raw([10], [40, 0], [1, 1], [100, 0], pie)
        r = aggregate([a, b], 364)
        self.assertEqual(r["modes"]["car"], 200)
        self.assertEqual(r["days_with_data"], 3)
        # (50*100 + 60*300 + 40*100) / 500 = 54.0 ; heure sans voiture ou V85 nulle ignorée
        self.assertEqual(r["v85"], 54.0)
        self.assertEqual(r["v85_hours"], 3)
        self.assertEqual(r["per_day"]["vehicles"], round(220 / 3))

    def test_heure_peu_fiable_ignoree(self):
        a = raw([5], [50, 90], [1, 0.2], [100, 100], {"car": 1})
        self.assertEqual(aggregate([a], 364)["v85"], 50.0)

    def test_capteur_sans_donnees(self):
        a = {"pie": [], "v85": [], "h24": [], "days": []}
        r = aggregate([a], 364)
        self.assertIsNone(r["v85"])
        self.assertEqual(r["days_with_data"], 0)
        self.assertNotIn("per_day", r)


class Profile(unittest.TestCase):
    def test_fixture(self):
        p = parse_profile(open(os.path.join(ROOT, "tests/fixtures/profile_9000007509.html"), encoding="utf-8").read())
        self.assertEqual(p["road_width_m"], 5.0)
        self.assertEqual(p["footpath_m"], [1.4, 1.4])
        self.assertFalse(p["bike_lane"])
        self.assertFalse(p["bus"])
        self.assertEqual(p["max_speed"], 30.0)
        self.assertEqual(p["safety_10"], 3.0)

    def test_page_inattendue(self):
        self.assertIsNone(parse_profile("<html><body>Faq & Support</body></html>"))


if __name__ == "__main__":
    unittest.main()
