from KiviPaperiSakset import Pelitehdas

def main():
    while True:
        print("Valitse pelataanko"
              "\n (a) Ihmistä vastaan"
              "\n (b) Tekoälyä vastaan"
              "\n (c) Parannettua tekoälyä vastaan"
              "\nMuilla valinnoilla lopetetaan"
              )

        vastaus = input()

        if vastaus == "a":
            peli = Pelitehdas.luo_peli("kaksinpeli")
        elif vastaus == "b":
            peli = Pelitehdas.luo_peli("helppo_tekoaly")
        elif vastaus == "c":
            peli = Pelitehdas.luo_peli("parempi_tekoaly")
        else:
            print("Lopetetaan.")
            break

        print("Peli loppuu, kun pelaaja antaa virheellisen siirron (jokin muu kuin 'k', 'p', 's').")
        peli.pelaa()

if __name__ == "__main__":
    main()
