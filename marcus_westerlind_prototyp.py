'''
Marcus Westerlind
2024-05-12
KTH Programmeringsteknik DD100N
Prototyp, Musée-katalog

Detta är ett program som fungerar som katalog för en samling föremål på Moderna Muséet.
Programmet läser in föremål från en textfil samt sparar gjorda ändringar till den samma.
Programmet tillhandahåller funktioner för att söka, lägga till, radera och ändra föremål i samlingen.

Programmet är uppbyggt av två klasser: 

Föremål: Klass som beskriver ett föremål. Har metoder för att skriva ut ett föremål, ändra attribut samt sortera föremål
Katalog: Klass som fungerar som katalog för instanser av klassen Föremål. Läser in föremål från fil till katalogens lista.
Klassen har metoder för att söka på föremål i katalogen, skapa/radera föremål, ändra attribut på föremål & spara ändringar

Datastrukturer: I filen 'föremål.txt' sparas varje föremål på en egen rad. Föremålets attribut separeras med '|'-symbolen.
metoden .läsFöremål() skapar instanser av Föremål från filen och sparar de i en lista i den skapade katalogen. Det går att lägga
till nya föremål rätt i filen genom att skriva in de attribut man önskar enligt:
Titel|Konstnär|Årtal|Beskrivning|Kontext|Tillhörighet (vilket muséeum föremålet finns på)|Antal sökningar (0)

I metoden .fritextSök() nyttjas ett lexikon {dict} med key:value = föremål:träffar


Funktioner:
Programmets funktioner kontrollerar filens existens, presenterar programmet, huvudemenyn, submenyer
samt tillåter användaren nyttja katalogens metoder.

Externa resurser:
Kontroll av fils existens: https://www.geeksforgeeks.org/python-check-if-a-file-or-directory-exists/
Sortering av dict på value för metoden .fritextSök(): https://www.freecodecamp.org/news/sort-dictionary-by-value-in-python/
Omvandling av lista (kontext) till str mha .join(): https://www.w3schools.com/python/ref_string_join.asp
Ignorera värden mha '_' https://www.datacamp.com/tutorial/role-underscore-python

VIKTIGT: Ändra konstanterna SÖKVÄG och FILNAMN till rätt filnamn och sökväg till filen för programmet.
'''


#----------Importerade bibliotek----------------------------
import os.path

#----------KONSTANTER----------------------------------------

FILNAMN = 'föremål.txt'
SÖKVÄG = 'C:/Users/Marcus/Project 1/föremål.txt'

#----------------------KLASSER & METODER---------------------------------------------------------------

class Föremål:
    '''En klass som beskriver föremålet.

    titel = föremålets titel (str)
    konstnär = föremålets upphovsman (str)
    årtal = när föremålet skapades (str)
    kontext = föremålets kontext i lista ex: ['Vikingatiden', 'Romarriket'] [lista]
    beskrivning = beskrivning av föremålet (str)
    tillhörighet = vilket museum har föremålet (str)
    antalSökningar = hur många gånger föremålet sökts i katalogen (int)
    '''
    def __init__(self, titel, konstnär, årtal, beskrivning, kontext, tillhörighet, antalSökningar):
        self.titel = titel
        self.konstnär = konstnär
        self.årtal = årtal
        self.kontext = kontext
        self.beskrivning = beskrivning
        self.tillhörighet = tillhörighet
        self.antalSökningar = antalSökningar

    def __str__(self):
        '''Returnerar en sträng som beskriver föremålet
        Inparameter: self
        Returvärde: sträng som beskriver föremålet
        '''
        return f"Titel: {self.titel}, Konstnär: {self.konstnär}, År: {self.årtal}\nBeskrivning: {self.beskrivning}\nKontext: {', '.join(self.kontext)}\nTillhörighet: {self.tillhörighet}\nAntal sökningar: {self.antalSökningar}"

    def ändraBeskrivning(self, nyBeskrivning):
        '''Ändrar beskrivning av föremålet
        Inparameter: nyBeskrivning (str), self
        Returvärde: Uppdaterar self.beskrivning'''
        self.beskrivning = nyBeskrivning
    
    def ändraKontext(self, nyKontext):
        '''Ändrar föremålets kontext
        Inparameter: nyKontext (str), self
        Returvärde: Uppdaterar self.kontext'''
        self.kontext.clear()
        self.kontext.append(nyKontext)

    def ökaAntalSökningar(self):
        '''Ökar self.antalSökningar med =+1
        Inparameter: self
        Returvärde: uppdaterar self.antalSökningar med +1'''
        self.antalSökningar += 1
    
    def __lt__(self, other): #NYTTJAS I .allaFöremål()
        '''Sorterar föremålen efter popularitet (antalSökningar)
        Inparameter: self, other
        Returvärde: True om lt (bool)'''
        if self.antalSökningar < other.antalSökningar:
            return True

    def kontrollUtlåning(self):
        '''Kontrollerar om ett objekt är utlånat till ett annat museeum än Moderna Museet
        Inparameter: self
        Returvärde: True om utlånat (bool)'''
        if self.tillhörighet != 'Moderna Museet, Stockholm':
            return True

class Katalog:
    '''En klass för katalogfunktionen i programmet med metoder för att söka och radera/lägga till Föremål i katalogen
    samt ändra attribut hos föremål i katalogen.'''

    def __init__(self):
        '''Skapar en tom lista för att spara föremål i'''
        self.föremålsLista = []

    def läsFöremål(self, filnamn):
        """ Läser föremål från filen föremål.txt till attributet föremålsLista & presenterar användaren med antal föremål som lästs in.
    Inparametrar: self, filnamn (str)
    Returnerar: - """
        try:
            with open(filnamn, 'r', encoding='utf-8') as fil:
                i = 0
                for rad in fil:
                    rad = rad.strip().split('|')
                    titel = rad[0]
                    konstnär = rad[1]
                    årtal = rad[2]
                    beskrivning = rad[3]
                    kontext = rad[4].split(',')
                    tillhörighet = rad[5]
                    antalSökningar = int(rad[6])
                    föremål = Föremål(titel, konstnär, årtal, beskrivning, kontext, tillhörighet, antalSökningar)
                    self.föremålsLista.append(föremål)
                    i +=1
            print(f"Föremål inlästa från fil {filnamn}\nAntal föremål i katalogen: {i}\n")
        except:
            pass
    def allaFöremål(self):
        '''Metod för att visa samtliga föremål i katalogen sorterat på flest antal sökningar i fallande ordning.
        Inparameter: self
        Returvärde: -'''
        allaFöremål = self.föremålsLista
        allaFöremål = sorted(allaFöremål, reverse=True)
        print(f"\nSamtliga föremål i katalogen:\n")
        for föremål in allaFöremål:
            print(f"{föremål}\n")

    def utlånadeFöremål(self):
        '''Metod för att visa de föremål som är utlånade till andra museeum
        Inparameter: self
        Returvärde: -'''
        print('Föremål utlånade till andra museeum: \n')
        for föremål in self.föremålsLista:
            if föremål.kontrollUtlåning():
                print(f"{föremål}\n")
            else:
                pass

    def titelSök(self, titel):
        '''Metod för att söka på titel på Föremål
        Inprameter: titel (str)
        Returvärde: första föremålet med matchande self.titel [Föremål]'''
        for föremål in self.föremålsLista: #jämför self.titel på föremålen i katalogen mot sökordet (titel)
            if föremål.titel.lower() == titel.lower():
                return föremål
    
    def kontextSök(self, kontext):
        '''Metod för att söka på kontext på Föremål
        Inparamter: kontext (str)
        Returvärde: Lista med matchande Föremål [lista]'''
        matchandeFöremål = []
        for föremål in self.föremålsLista:
            for kontexter in föremål.kontext:
                if kontexter.lower() == kontext.lower():
                    matchandeFöremål.append(föremål)
        return matchandeFöremål
    
    def fritextSök(self):
        '''Metod för att söka med flera olika sökord, resultat presenteras med flest träffar/Föremål först.

        Fritext görs om till lista som sedan matchas mot samtliga attribut. En räknare (träffar) ökar +=1 
        för varje match i attributen. Föremål med > 0 träffar läggs till i matchandeFöremål {dict} enligt:
        {'föremål':'träffar'} som sedan sorteras.
        Inparameter: -
        Returvärde: -'''

        matchandeFöremål = {}
        fritext = input('Ange dina sökord, mellanslag " " för att separera: ')
        sökord = fritext.split()  # skapar en lista av söksträngen, ' ' = separator

        for föremål in self.föremålsLista:
            träffar = 0
            for attribut in [föremål.titel.lower(), föremål.konstnär.lower(), föremål.årtal, föremål.beskrivning.lower(), ''.join(föremål.kontext).lower(), föremål.tillhörighet.lower()]:
                for ordet in sökord:
                    if ordet in attribut:
                        träffar += 1
            if träffar > 0:
                matchandeFöremål[föremål] = träffar
        
        matchandeFöremål = sorted(matchandeFöremål.items(), key=lambda x:x[1], reverse=True) #sorterar dict {key:value} till list [(key,value)]
        matchandeFöremål = [föremål for föremål, _ in matchandeFöremål] #Gör om sorterad lista [(key,value)] till lista med enbart föremål [key]

        if matchandeFöremål:
            print('Matchande föremål: ')
            for föremål in matchandeFöremål:
                föremål.ökaAntalSökningar()
                print(f"{föremål}\n")
        else:
            print('Inga föremål hittades.')

    def raderaFöremål(self):
        '''Metod för att radera föremål från katalogen
        Inparameter: -
        Returvärde: -'''
        titel = input('Ange titeln för föremålet du vill radera: ')
        föremål = self.titelSök(titel)
        if föremål:
            self.föremålsLista.remove(föremål)
            print(f"Föremålet: '{föremål.titel}' Har raderats från katalogen.")
        else:
            print(f"Inget föremål med titeln: '{titel}' kunde hittas i katalogen.")
    
    def ändraKontextFöremål(self):
        '''Metod där användaren kan ersätta kontexten på ett föremål i katalogen, anropar metoden .ändraKontext() & .titelSök()
        för det valda föremålet (Föremål)
        Inparameter: self
        Returvärde: -'''
        titel = input('Ange titeln för föremålet du vill ändra kontext på: ')
        föremål = self.titelSök(titel)
        if föremål:
            nyKontext = input(f"Ange ny kontext for {föremål.titel} (nuvarande kontext {','.join(föremål.kontext)}):  ")
            föremål.ändraKontext(nyKontext)
            print(f"Ny kontext för {föremål.titel}:\n{','.join(föremål.kontext)}\n")
        else:
            print(f"Inget föremål med titeln: '{titel}' hittades i katalogen")

    def ändraBeskrivningFöremål(self):
        '''Metod där användaren kan ersätta beskrivningen på ett föremål i katalogen, anropar metoden .ändraBeskrivning() & .titelSök()
        för det valda föremålet (Föremål)
        Inparameter: self
        Returvärde: -'''
        titel = input('Ange titeln för föremålet du vill ändra beskrivning på: ')
        föremål = self.titelSök(titel)
        if föremål:
            nyBeskrivning = input(f"Ange ny beskrivning för {föremål.titel}:  ")
            föremål.ändraBeskrivning(nyBeskrivning)
            print(f"Ny beskrivning för {föremål.titel}:\n{föremål.beskrivning}\n")
        else:
            print(f"Inget föremål med titeln: '{titel}' hittades i katalogen")
    
    def läggTillFöremål(self):
        '''Metod där användaren kan skapa och lägga till föremål i katalogen (self.föremålsLista)
        Inparameter: self
        Returvärde: -'''
        titel = input('Titel: ')
        konstnär = input('Konstnär: ')
        årtal = input('Årtal: ')
        kontext = input('Kontext: ')
        tillhörighet = input('Tillhörighet: ')
        beskrivning = input('Beskrivning: ')
        nyttFöremål = Föremål(titel, konstnär, årtal, beskrivning, [kontext], tillhörighet, 0)
        self.föremålsLista.append(nyttFöremål)
        print(f"'{titel}' har lagts till\n")

    def sparaTillFil(self, filnamn):
        with open(filnamn, 'w', encoding='utf-8') as fil:
            for föremål in self.föremålsLista:
                kontexter = ','.join(föremål.kontext)
                fil.write(f"{föremål.titel}|{föremål.konstnär}|{föremål.årtal}|{föremål.beskrivning}|{kontexter}|{föremål.tillhörighet}|{föremål.antalSökningar}\n")

# ------------------------FUNKTIONER--------------------------------------------------
def kontrollFil():
    '''Kontrollerar att filen föremål.txt existerar på sökvägen enligt konstanten SÖKVÄG
    Inparameter: -
    Returvärde: True om filen finns'''
    filFinns = os.path.isfile(SÖKVÄG)
    if filFinns:
        return True

def sökTitel(katalog):
    '''Funktion för att söka på titel och visa resultat, nyttjar sig av metoden .titelSök()
    Inparameter: katalog (Katalog)
    Returvärde: -'''
    titel = input('Ange titel på föremålet du vill visa: ')
    föremål = katalog.titelSök(titel)
    if föremål:
        föremål.ökaAntalSökningar()
        print(f"Resultat:\n {föremål}")
    else:
        print(f"Inget föremål med titeln: '{titel}' hittades i katalogen")

def sökKontext(katalog):
    '''Funktion för att söka på titel och visa resultat, nyttjar sig av metoden .titelSök()
    Inparameter: katalog (Katalog)
    Returvärde: -'''
    kontext = input('Ange kontext du vill söka på: ')
    matchandeFöremål = katalog.kontextSök(kontext)
    if matchandeFöremål:
        print(f"Föremål som matchar '{kontext}':")
        for föremål in matchandeFöremål:
            föremål.ökaAntalSökningar()
            print(f"{föremål}\n")
    else:
        print(f"Inget föremål som matchar kontexten '{kontext}' hittades.")

def sökMeny(katalog):
    '''Submeny för programmets sökfunktioner
    Inparameter: katalog (Katalog)
    Returvärde: -
    '''
    while True:
        print('1. Sök på titel')
        print('2. Sök utifrån kontext')
        print('3. Fritextsök')
        print('4. Visa samtliga föremål i katalogen')
        print('5. Visa utlånade föremål')
        print('6. Återgå till huvudmenyn')

        val = input('Ange val 1-6: ')
        if val == '1':
            sökTitel(katalog)
        elif val == '2':
            sökKontext(katalog)
        elif val == '3':
            katalog.fritextSök()
        elif val == '4':
            katalog.allaFöremål()
        elif val == '5':
            katalog.utlånadeFöremål()
        elif val == '6':
            break
        else: 
            print('Felaktigt val!')
    
def ändraAttributMeny(katalog):
    '''Submeny för ändring av beskrivning/kontext på föremål
    Inparameter: katalog (Katalog)
    Returvärde: -'''
    while True:
        print('1. Ändra beskrivning:\n2. Ändra kontext:\n3. Återgå till huvudmenyn')
        val = input('Val: ')
    
        if val == '1':
            katalog.ändraBeskrivningFöremål()
        elif val == '2':
            katalog.ändraKontextFöremål()
        elif val == '3':
            break
        else:
            print('Felaktigt val!')

def huvudmeny(katalog):
    '''Programmets huvudmeny
    Inparameter: katalog (Katalog)
    Returvärde: -'''
    while True:
        print('1. Sök efter föremål')
        print('2. Lägg till föremål')
        print('3. Radera föremål')
        print('4. Ändra beskrivning/kontext på ett föremål')
        print('5. Spara ändringar & avsluta programmet')

        val = input('Ange val 1-5: ')
        if val == '1':
            sökMeny(katalog)
        elif val == '2':
            katalog.läggTillFöremål()
        elif val == '3':
            katalog.raderaFöremål()
        elif val == '4':
            ändraAttributMeny(katalog)
        elif val == '5':
            print(f"Sparar ändringar till filen {FILNAMN}...\nProgrammet avslutas...")
            katalog.sparaTillFil(FILNAMN)
            break
        else: 
            print('Felaktigt val')

def huvudprogram():
    '''
    1. Kontrollerar att filen existerar mha. kontrollFil() om True returneras --> steg 2. annars skickas felmeddelande och programmet avslutas.
    2. Skapar en instans 'katalog' av Klassen Katalog
    3. Läser in museeumets föremål från filen (FILNAMN) som läggs till i listan self.föremålsLista i katalogen, meddelar användaren antal inlästa föremål.
    4. Presenterar programmet för användaren.
    5. Anropar huvudmenyn där användaren i sin tur kan anropa metoderna för den skapade katalogen och avsluta programmet.'''

    if kontrollFil() != True:
        print(f"Filen med namn {FILNAMN} hittades inte, kontrollera att den finns i mappen {SÖKVÄG}\nAvslutar programmet....")
        #AVLSUTA PROGRAMMET (sys.exit?)
    katalog = Katalog()
    katalog.läsFöremål(FILNAMN)
    print('Välkommen till Moderna Museets katalogprogram!\n')
    huvudmeny(katalog)

huvudprogram()