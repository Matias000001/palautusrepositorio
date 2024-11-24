import unittest
from unittest.mock import Mock, ANY, call
from kauppa import Kauppa
from viitegeneraattori import Viitegeneraattori
from varasto import Varasto
from tuote import Tuote

class TestKauppa(unittest.TestCase):
    def setUp(self):
        self.pankki_mock = Mock()
        self.viitegeneraattori_mock = Mock()
        self.varasto_mock = Mock()

        # viitegeneraattori palauttaa aina 42
        self.viitegeneraattori_mock.uusi.return_value = 42

        # varaston saldo-metodi
        def varasto_saldo(tuote_id):
            if tuote_id == 1:
                return 10
            if tuote_id == 2:
                return 5
            return 0

        # varaston hae_tuote-metodi
        def varasto_hae_tuote(tuote_id):
            if tuote_id == 1:
                return Tuote(1, "maito", 5)
            if tuote_id == 2:
                return Tuote(2, "leipä", 3)
            return None

        self.varasto_mock.saldo.side_effect = varasto_saldo
        self.varasto_mock.hae_tuote.side_effect = varasto_hae_tuote

        # alustetaan kauppa
        self.kauppa = Kauppa(self.varasto_mock, self.pankki_mock, self.viitegeneraattori_mock)

        # palautetaan uusi viitenumero jokaiselle kutsulle
        self.viitegeneraattori_mock.uusi.side_effect = [42, 43]

    def test_ostoksen_paaytyttya_pankin_metodia_tilisiirto_kutsutaan(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")

        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "12345", ANY, 5)

    def test_kaksi_eri_tuotetta_kutsuu_tilisiirtoa_oikein(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(2)
        self.kauppa.tilimaksu("matti", "67890")

        self.pankki_mock.tilisiirto.assert_called_with("matti", 42, "67890", ANY, 8)

    def test_kaksi_samaa_tuotetta_kutsuu_tilisiirtoa_oikein(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("teemu", "54321")

        self.pankki_mock.tilisiirto.assert_called_with("teemu", 42, "54321", ANY, 10)

    def test_yksi_varastossa_ja_yksi_loppu_kutsuu_tilisiirtoa_oikein(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(3)  # Ei varastossa
        self.kauppa.tilimaksu("liisa", "98765")

        self.pankki_mock.tilisiirto.assert_called_with("liisa", 42, "98765", ANY, 5)

    def test_aloita_asiointi_nollaa_edellisen_ostoksen_tiedot(self):
        # Aloitetaan ensimmäinen ostos
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)  # 5 euroa
        self.kauppa.lisaa_koriin(2)  # 3 euroa
        self.kauppa.tilimaksu("pekka", "12345")

        # Tarkistetaan, että summa on oikein
        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "12345", ANY, 8)

        # Aloitetaan uusi asiointi
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(2)  # 3 euroa
        self.kauppa.tilimaksu("matti", "67890")

        # Tarkistetaan, että edellisen ostoksen tietoja ei ole mukana ja summa on oikein
        self.pankki_mock.tilisiirto.assert_called_with("matti", 43, "67890", ANY, 3)

    def test_pyydetaan_uusi_viite_jokaiseen_maksuun(self):
        # Luodaan pankki_mock
        pankki_mock = Mock()

        # Luodaan Viitegeneraattori mockilla, mutta sen oikeaa toimintaa käytetään
        viitegeneraattori_mock = Mock(wraps=Viitegeneraattori())

        # Luodaan Kauppa oikeilla riippuvuuksilla
        kauppa = Kauppa(self.varasto_mock, pankki_mock, viitegeneraattori_mock)

        # Ensimmäinen ostotapahtuma
        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(1)  # Tuote 1 lisätään
        kauppa.tilimaksu("pekka", "12345")

        # Tarkistetaan, että viitegeneraattori pyysi uuden viitenumeron
        self.assertEqual(viitegeneraattori_mock.uusi.call_count, 1)

        # Toinen ostotapahtuma
        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(2)  # Tuote 2 lisätään
        kauppa.tilimaksu("matti", "67890")

        # Tarkistetaan, että viitegeneraattori pyysi viitenumeron uudelleen
        self.assertEqual(viitegeneraattori_mock.uusi.call_count, 2)

        # Varmistetaan viitenumerot jokaisessa kutsussa
        viitegeneraattori_mock.uusi.assert_has_calls([call(), call()])
