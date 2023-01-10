import pygame, random

class Rush_hour():
    def __init__(self):
        pygame.init()
        #Peliruudukko jota muokataan ja joka tulostetaan pelaajalle
        self.peliruudukko = [[0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0],
                             [0, 0, "B", "b", 0, 0],
                             [0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0]]
  
        #Kuvat
        self.blue = pygame.image.load("blue2x1.png")
        self.orange = pygame.image.load("orange2x1.png")
        #Statusparametrit
        self.valmis = False
        self.pelaa_uusi_peli = False
        self.hiiri_painettuna = False
        self.klikattu_ruutu = (11, 11)
        self.klikatut_koordinaatit = (0, 0)
        self.hiiren_koordinaatit = (0, 0)
        #Aika
        self.aika_sekunteina = 0
        self.aika_minuutteina = 0
        #Näyttö
        self.korkeus = 6
        self.leveys = 6
        self.skaala = 100
        nayton_korkeus = self.skaala * self.korkeus
        nayton_leveys = self.skaala * self.leveys
        self.naytto = pygame.display.set_mode((nayton_leveys + 100, nayton_korkeus + 200))

        pygame.display.set_caption("Rush Hour")

        self.pelisilmukka()


    #Toistettava silmukka
    def pelisilmukka(self):
        kello = pygame.time.Clock()
        aika = 0
        while True:
            self.tutki_tapahtumat()
            self.debug()
            self.piirra_naytto()
            #self.testaa_ratkaisu()
            #if self.valmis and self.pelaa_uusi_peli:
            #    self.valitse_vaikeustaso()
            #Aika etenee jos peli ei ole valmis
            if not self.valmis:
                kello.tick(60)
                aika += 1
                if aika >= 60:
                    self.aika_sekunteina += 1
                    aika = 0
                if self.aika_sekunteina >= 60:
                    self.aika_sekunteina = 0
                    self.aika_minuutteina += 1
    
    def debug(self):
        for rivi in self.peliruudukko:
            print(rivi)
        


    def tutki_tapahtumat(self):
        for tapahtuma in pygame.event.get():
            #Jos painetaan peli-ikkunan rastia niin suljetaan ikkuna
            if tapahtuma.type == pygame.QUIT:
                exit()
            
            #Seurataan tapahtumia jos peli kesken
            if self.valmis == False:
                #Jos klikataan hiirellä autoa, kirjataan ylös että hiiri painettuna ja että mikä auto valittuna
                if tapahtuma.type == pygame.MOUSEBUTTONDOWN:
                    x, y = tapahtuma.pos
                    ruutu_x = (x - 50) // 100
                    ruutu_y = (y - 100) // 100
                    if 0 < ruutu_x < 6 and 0 < ruutu_y < 6:
                        if self.peliruudukko[ruutu_y][ruutu_x] != 0:
                            self.hiiri_painettuna = True
                            self.klikattu_ruutu = (ruutu_y, ruutu_x)
                            self.klikatut_koordinaatit = (x, y)
                    print(str(ruutu_x) + " " + str(ruutu_y))
                if tapahtuma.type == pygame.MOUSEBUTTONUP:
                    self.hiiri_painettuna = False
                
                #Jos hiiren painike on pohjassa, JA sitä klikattiin auton päällä
                if self.hiiri_painettuna:
                    if tapahtuma.type == pygame.MOUSEMOTION:
                        kohde_x = tapahtuma.pos[0]
                        kohde_y = tapahtuma.pos[1]
                        self.hiiren_koordinaatit = (kohde_x, kohde_y)

                #Jos tiputetaan auto ruutuun
                if tapahtuma.type == pygame.MOUSEBUTTONUP:
                    x, y = tapahtuma.pos
                    ruutu_x = (x - 50) // 100
                    ruutu_y = (y - 100) // 100
                    if 0 < ruutu_x < 6 and 0 < ruutu_y < 6:
                        if self.peliruudukko[ruutu_y][ruutu_x] == 0:
                            self.hiiri_painettuna = False
                            self.nollaa_ruudut("B")
                            self.peliruudukko[self.klikattu_ruutu[0]][ruutu_x] = "B"
                            self.peliruudukko[self.klikattu_ruutu[0]][ruutu_x + 1] = "b"



    def piirra_naytto(self):
        self.naytto.fill((255, 255, 255))

        #Piirrä pelilauta
        pygame.draw.rect(self.naytto, (150, 0, 0), (34, 84, 632, 632))
        pygame.draw.polygon(self.naytto, (255, 160, 160), [(34, 84), (664, 84), (34, 714)], 0)
        pygame.draw.rect(self.naytto, (220, 0, 0), (38, 88, 624, 624))
        pygame.draw.rect(self.naytto, (255, 160, 160), (43, 93, 614, 614))
        pygame.draw.polygon(self.naytto, (150, 0, 0), [(43, 93), (657, 93), (43, 706)], 0)
        pygame.draw.rect(self.naytto, (50, 50, 50), (48, 98, 604, 604))

        #Piirrä ruudut
        for y in range(self.korkeus):
            for x in range(self.leveys):
                ruutu = self.peliruudukko[y][x]
                pygame.draw.rect(self.naytto, (160, 160, 160), (x * self.skaala + 52, y * self.skaala + 102, 96, 96))
                pygame.draw.polygon(self.naytto, (240, 240, 240), [(x * self.skaala + 52, y * self.skaala + 102), (x * self.skaala + 52, y * self.skaala + 196), (x * self.skaala + 146, y * self.skaala + 102)], 0)
                pygame.draw.rect(self.naytto, (200, 200, 200), (x * self.skaala + 60, y * self.skaala + 110, 80, 80))
        #Uusi silmukka missä aiempien ruutujen päälle piirretään autot
        for y in range(self.korkeus):
            for x in range(self.leveys):
                ruutu = self.peliruudukko[y][x]
                #Piirrä Sininen 2x1 auto
                if ruutu == "B":
                    if self.hiiri_painettuna:
                        try:
                            if self.peliruudukko[self.klikattu_ruutu[0]][self.klikattu_ruutu[1]] == "B":
                                self.naytto.blit(self.blue, (self.hiiren_koordinaatit[0] - self.laske_erotus(self.klikatut_koordinaatit), y * self.skaala + 100))
                        except:
                            pass
                    else:
                        self.naytto.blit(self.blue, (x * self.skaala + 50, y * self.skaala + 100))
                elif ruutu == "b":
                    if self.hiiri_painettuna:
                        try:
                            if self.peliruudukko[self.klikattu_ruutu[0]][self.klikattu_ruutu[1]] == "b":
                                self.naytto.blit(self.blue, (self.hiiren_koordinaatit[0] - self.laske_erotus(self.klikatut_koordinaatit) - 100, y * self.skaala + 100))
                        except:
                            pass



        pygame.display.flip()


    
    def laske_erotus(self, koordinaatit: tuple):
        erotus = (koordinaatit[0] -50) % 100
        return erotus

    def nollaa_ruudut(self, auton_tunnus: str):
        for y in range(self.korkeus):
            for x in range(self.leveys):
                ruutu = self.peliruudukko[y][x]
                if ruutu == auton_tunnus or ruutu == auton_tunnus.lower():
                    self.peliruudukko[y][x] = 0



    #Nollaa aika
    def nollaa_aika(self):
        self.aika_sekunteina = 0
        self.aika_minuutteina = 0


    #Tarkistaa onko täytetty sudoku sääntöjen mukainen
    def testaa_ratkaisu(self):
        pass






if __name__ == "__main__":
    Rush_hour()


    