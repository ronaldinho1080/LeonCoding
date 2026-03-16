from playwright.sync_api import sync_playwright
import google.generativeai as genai
import json
import time

# ==========================================
# 1. KONFIGURACIJA I LISTE
# ==========================================

genai.configure(api_key="AIzaSyDVErIrBkqFZB205PPskv8bBKucSNB_DmM")

DOZVOLJENE_VRSTE_ODLUKA = ["Rješenje", "Presuda", "Presuda i rješenje", "Odluka", "Zaključak"]

DOZVOLJENE_VRSTE_POSTUPAKA = [
    "Građanski - prvostupanjski", "Kazneni - prvostupanjski", "Građanski - drugostupanjski",
    "Kazneni - drugostupanjski", "Građanski - zahtjev za zaštitu zakonitosti", "Građanski - revizija",
    "Kazneni - drugostupanjski pritvori", "Kazneni - mjesna nadležnost i sukob nadležnosti",
    "Kazneni - izvanredno preispitivanje presude", "Kazneni - produljenje pritvora",
    "Kazneni - drugostupanjski žalbeni", "Kazneni - izvanredno ublažavanje kazne",
    "Kazneni - zahtjev za zaštitu zakonitosti", "Kazneni - neslaganja",
    "Građanski - delegacija ili sukob nadležnosti", "Građanski - revizija iz trgovačkog spora",
    "Građanski - izvanredno preispitivanje - prekršaj", "Upravni spor protiv rješenja tijela državne uprave",
    "Nepoznata vrsta predmeta u SuPri", "Kazneni - zahtjev za izručenje",
    "Istraga za predmete iz nadležnosti općinskih sudova", "Kazneni - prvostupanjski (županijski)",
    "Trgovački spor", "Građanski", "Kazneni - zaštita prava na suđenje u razumnom roku - zahtjev",
    "Sudska uprava", "Prekršajni - javni red i mir i javna sigurnost - drugostupanjski",
    "Prekršajni - sigurnost prometa - drugostupanjski", "Građanski - razno",
    "Prekršajni - gospodarstvo - drugostupanjski", "Građanski - drugostupanjski - ovrha",
    "Kazneni - žalbe u predmetima protiv mlađih punoljetnika i odraslih počinitelja na štetu djece i maloljetnika",
    "Prekršajni - financijski prekršaj - drugostupanjski", "Kazneni - drugostupanjski maloljetnički predmeti",
    "Građanski - drugostupanjski - naknada štete", "Građanski - drugostupanjski - razvod braka, povjeravanje djece, uzdržavanje",
    "Prekršajni - supletorni zatvor - drugostupanjski", "Trgovački spor - drugostupanjski",
    "Kazneni - trećestupanjski žalbeni", "Kazneni", "Zahtjev za zaštitom prava zajamčenih Ustavom RH",
    "Sudska uprava - županijski sud", "Parnični predmet", "Kazneni - priziv na odluke Višeg disciplinskog suda HOK",
    "Građanski - parnični", "Građanski-parnični", "Kazneni - priziv odvjetnika",
    "Građanski - štrajk, poništenje izbora za radničko vijeće, nezakonite radnje",
    "Građanski - zaštita prava na suđenje u razumnom roku - žalba", "Građanski - zaštita prava na suđenje u razumnom roku - zahtjev",
    "Upravni - zaštita prava na suđenje u razumnom roku - zahtjev", "Kazneni - pravno shvaćanje - sudska uprava",
    "Građanski - pravno shvaćanje - sudska uprava", "Kazneni - zaštita prava na suđenje u razumnom roku - žalba",
    "Građanski - zahtjev za jedinstvenu primjenu zakona u građanskim stvarima", "Prekršajni postupak – izavnredni pravni lijekovi",
    "Radni spor – revizija", "Radni spor – drugostupanjski", "Građanski - drugostupanjski žalbeni",
    "Građanski - zaštita zakonitosti u upravnim predmetima", "Nepoznato", "Građanski - revizija (predmeti stariji od 10 godina)",
    "Kazneni - vijeća za izvršenje kazne zatvora", "Građanski - naknada štete",
    "Kazneni - zahtjev za jedinstvenu primjenu zakona u kaznenim stvarima", "Istražni predmet - razno",
    "Građanski - razno - pismena", "Kazneni - drugostupanjski predmeti iz čl. 21. Zakona o USKOK-u",
    "Građanski - drugostupanjski - zemljišnoknjižni", "Građanski - zaštita prava na suđenje u razumnom roku",
    "Građanski - drugostupanjski - mediji (tisak)", "Građanski - izvanparnični", "Kazneni - optužno vijeće",
    "Građanski - ovrha", "Građanski - najam stanova", "Izvanraspravno kazneno vijeće - za kazneni odjel I. stupnja",
    "Građanski - parnični predmeti", "Trgovački - stečaj", "Trgovački - predmeti proslijeđeni od javnog bilježnika po prigovoru na rješenje o ovrsi na temelju vjerodostojne isprave",
    "Kazneni - županijski sud", "Građanski - drugostupanjski zemljišnoknjižni predmeti",
    "Prekršajni - devizni - drugostupanjski", "Kazneni - prvostupanjski (općinski)", "Trgovački - ovrha",
    "Upravni - Upisnik za drugostupanjske predmete povodom žalbe", "Građanski - statusni sporovi",
    "Građanski - isplate", "Upravni - ocjena zakonitosti odluka javnopravnih tijela",
    "Građanski - prigovor na ovrhu temeljem vjerodostojne isprave", "Upravni - upisnik za ocjenu zakonitosti pojedinačne odluke...",
    "Upravni - ocjena zakonitosti općih akata", "Građanski - smetanje posjeda", "Kazneni - europski uhidbeni nalog (županijski)",
    "Kazneni - europski uhidbeni nalog", "Građanski - drugostupanjski ovršni predmeti",
    "Upravni - izvanredno preispitivanje zakonitosti pravomoćne presude upravnog i Visokog upravnog suda RH",
    "Kazneni - prvostupanjski - odrasli počinitelj za kaznena djela na štetu djece i maloljetnika",
    "Građanski - stambeno", "Građanski - drugi stupanj - razumni rok", "Građanski - prvi stupanj - razumni rok",
    "Građanski - sporovi male vrijednosti", "Kazneni prvostupanjski - USKOK-a", "Građanski - obvezni",
    "Upravni - upisnik za upravne sporove", "Građanski - mediji", "Kazneni - prvostupanjski - ratni zločin",
    "Građanski - predmeti stariji od 15 godina", "Upravni - upisnik radnih i službeničkih sporova",
    "Upravni - razni upravni predmeti", "Kazneni - drugostupanjski kazneni predmeti za kaznena djela kaznenopravne zaštite djece",
    "Prekršajni - predmeti iz područja gospodarstva", "Građanski - obiteljski sporovi",
    "Kazneni - izvanraspravno kazneno vijeće - za mladež", "Kazneni - za maloljetnike", "Građanski - ostavine",
    "Kazneni - kaznena djela kaznenopravne zaštite djece", "Kazneni - drugostupanjski - izvanraspravno kazneno vijeće za istražne predmete i predmete općinskih sudova",
    "Kazneni - drugostupanjski predmeti izvršavanja kazne zatvora", "Obiteljski – drugostupanjski",
    "Građanski - radni statusni", "Građanski - isplate iz radnog odnosa", "Kazneni - prvostupanjski - maloljetnik",
    "Trgovački - pobijanje predstečajne nagodbe", "Građanski-pomoćni upisnik za ovršne vrste postupaka",
    "Kazneni - prvostupanjski - maloljetnici", "Upravni - upisnik predmeta iz područja mirovinskog osiguranja",
    "Građanski - upisnik za razne građanske predmete", "Upravni - upisnik predmeta iz područja financijsko-poreznog sustava-porezi",
    "Građanski - utvrđenje izvanbračne zajednice, oduzimanje roditeljskog prava...", "Upravni - upisnik predmeta u kojima vrijednost predmeta spora ne prelazi 100.000,00 kuna",
    "Kazneni - drugostupanjski kazneni predmeti mlađih punoljetnika", "Upravni - upisnik predmeta iz područja graditeljstva i prostornog uređenja",
    "Upravni - upisnik predmeta iz područja financijsko-poreznog sustava-porezni nadzori", "Upravni - upisnik predmeta iz područja zdravstvenog i socijalnog osiguranja",
    "Upravni - upisnik predmeta javne nabave i koncesija", "Upravni - upisnik predmeta iz područja katastra",
    "Upravni - upisnik predmeta naknade za oduzete imovine", "Upravni - upisnik predmeta iz područja financijsko-carinskog sustava",
    "Građanski-pomoćni upisnik za ostavinske vrste postupaka", "Kazneni - upisnik za predmete po ostalim oblicima pravosudne suradnje u kaznenim stvarima s državama članica EU",
    "Kazneni - izdane i primljene potvrde – priznanje i izvršenje odluka o novčanoj kazni između članica EU (općinski)",
    "Kazneni - upisnik za drugostupanjske kaznene predmete ratnih zločina", "Kazneni - upisnik za drugostupanjske kaznene predmete za kaznena djela kaznenopravne zaštite djece",
    "Kazneni - prvostupanjski - mlađi punoljetnik", "Prekršajni - žalbe na rješenja o oduzimanju predmeta, na nalog za zadržavanje i dr.",
    "Građanski - drugostupanjski povodom žalbi na predmete europskog postupka za sporove male vrijednosti",
    "Prekršajni - predmeti iz područja javnog reda i mira i javne sigurnosti", "Prekršajni - izvanredno ublažavanje kazne",
    "Kazneni - izdane i primljene potvrde – priznanje i izvršenje odluka o novčanoj kazni između članica EU (županijski)",
    "Kazneni - upisnik za predmete iz članka 21. Zakona o USKOK-u za izvanraspravno vijeće", "Kazneni - upisnik priziva na odluke Višeg disciplinskog suda HOK",
    "Građanski-upisnik za ovrhu po Obiteljskom zakonu", "Prekršajni - predmeti iz područja sigurnosti prometa na cestama i prijevoza",
    "Kazneni - upisnik odluka drugostupanjskog disciplinskog vijeća za javne bilježnike", "Kazneni-upisnik za predmete iz članka 21. Zakona o USKOK-u za izvanraspravno vijeće",
    "Kazneni - upisnik za drugostupanjske kaznene predmete iz članka 21. Zakona o USKOK-u", "Upravni - upisnik predmeta izvlaštenja-izvlaštenje, deposedacija, eksproprijacija",
    "Građanski - predmeti prema Zakonu o zaštiti osoba s duševnim smetnjama", "Prekršajni - predmeti iz područja financija",
    "Prekršajni - pomoćni upisnik za predmete iz područja sigurnosti prometa na cestama", "Građanski - prijedlog za dopuštenje revizije",
    "Građanski - ogledni postupak", "Građanski-upisnik za stečaj potrošača", "Izvršenje kazni",
    "Prekršajni - povodom žalbi - o priznavanju i izvršenju odluka o novčanoj kazni između članica EU",
    "Upravi - upisnik za sklapanja, raskidanja i izvršavanje ...", "Upisnik za prekršajni postupak",
    "Prekršajni upisnik za drugostupanjske predmete", "Kazneni - postupak prenošenja nadležnosti i rješavanje sukoba nadležnosti",
    "Kazneni - drugostupanjski žalbeni na uvjetne otpuste", "Kazneni - drugostupanjski žalbeni europski uhidbeni nalog",
    "Kazneni - drugostupanjski žalbeni istražni zatvori iz čl. 21. Zakona o USKOK-u", "Obiteljski – drugostupanjski",
    "Kazneni - drugostupanjski žalbeni na maloljetnike", "Prekršajni - izdane i primljene potvrde u svrhu priznanja i izvršenja odluka o novčanoj kazni između članica EU",
    "Prekršajni - razni prekršajni zahtjevi", "Kazneni - drugostupanjski žalbeni po ostalim oblicima pravosudne suradnje u kaznenim stvarima s državama članicama EU",
    "Kazneni - drugostupanjski žalbeni iz čl. 21. Zakona o USKOK-u", "Upravni - upisnik za izvršenje sudskih odluka",
    "Kazneni - drugostupanjski žalbeni za kaznena djela kaznenopravne zaštite djece", "Kazneni - drugostupanjski žalbeni ratni zločin",
    "Kazneni - upisnik drugostupanjskog državnoodvjetničkog stegovnog vijeća", "Trgovački - ovrha temeljem vjerodostojne isprave",
    "Upravni - upisnik za ocjenu zakonitosti postupanja jav.prav.", "Građanski - platni nalog",
    "Prekršajni - razni prekršajni predmeti", "Trgovački - Upisnik za žalbe protiv rješenja u skraćenom stečajnom postupku",
    "Trgovački - upisnik za predmete ovrhe i osiguranja na temelju odluka donesenih u državama članicama Europske unije",
    "Trgovački - upisnik za predmete europskog platnog naloga i europskog postupka za sporove male vrijednosti",
    "Građanski - upisnik za izdavanje potvrda, priznanje i ovrhu sudskih odluka iz država članica Europske unije",
    "Kazneni - povodom žalbe na rješenje u istrazi", "Prekršajni - predmeti izvršenja prekršajnih sankcija",
    "Građanski - predmeti mirenja", "Upisnik za predmete europskog platnog naloga i europskog postupka za sporove male vrijednosti",
    "Upravni spor – izvanredni pravni lijekovi", "Radni spor – prvostupanjski", "Trgovački – izvanparnični",
    "Obiteljski – izvanparnični", "Građanski - izvanredno preispitivanje - upravni postupak",
    "Građanski - drugostupanjski radni predmeti", "Građanski-upisnik za drugostupanjske obiteljske predmete",
    "Kazneni - predmeti izvršavanja kazne zatvora za kaznena djela kaznenopravne zaštite djece",
    "Građanski-pomoćni upisnik za parnične vrste postupaka"
]

DOZVOLJENA_PODRUCJA_PRAVA = [
    "010101 Trgovačka društva, osnivanje i statusne promjene", "010102 Sudski registar, upis i promjene", "010103 Predstavništva inozemnih trgovačkih društava", "010104 Preuzimanje dioničkih društava", "010105 Poslovna tajna", "010106 Stečaj i predstečajna nagodba", "010201 Obrt", "010202 Zadruge", "010301 Sloboda pružanja usluga", "010302 Zaštita tržišnog natjecanja", "010303 Mjere kontrole cijena", "010401 Financijsko poslovanje", "010501 Elektronički potpis, elektronička isprava", "010601 Poticanje gospodarstva, ulaganja, izvoza, inovacija i dr. gospodarske mjere", "010701 Poduzetnička infrastruktura", "010801 Komore (Hrvatska gospodarska komora, Hrvatska obrtnička komora)", "020101 Radni odnosi (ugovor o radu, pravilnik o radu, plaća i dr.)", "020201 Državni službenici i službenici i namještenici u tijelima jedinica lokalne i područne (regionalne) samouprave", "020202 Državni (stručni) ispit", "020203 Plaće, naknade i materijalna prava u javnom sektoru", "020301 Prava radnika u slučaju stečaja poslodavca", "020401 Zaštita života i zdravlja na radu", "020402 Zaštita prijavitelja nepravilnosti, zaštita dostojanstva", "020501 Kolektivni ugovori", "020502 Sindikati, udruge poslodavaca", "020601 Volonterstvo", "020701 Posredovanje pri zapošljavanju, profesionalna rehabilitacija", "020801 Obvezno mirovinsko osiguranje, mirovine", "030101 Obvezni odnosi, zatezne kamate", "030102 Posebna odgovornost RH za štetu", "030103 Mjenica, ček", "030201 Vlasništvo i druga stvarna prava, izvlaštenje i komasacija", "030301 Ovršni postupak", "040101 Autorsko i srodna prava", "040201 Patenti, žigovi, industrijski dizajn i dr.", "040301 Naknade u području intelektualnog vlasništva", "050101 Platni promet", "050102 Sprječavanje pranja novca", "050103 Financijski inspektorat", "050104 Financijska agencija (FINA)", "050105 Zaštita u poslovanju s gotovim novcem i vrijednostima", "050106 Devizno poslovanje", "050201 Računovodstvo poduzetnika i neprofitnih organizacija", "050202 Revizija financijskih izvještaja društava i drugi poslovi revizije", "050301 Porezi i porezni sustav općenito", "050302 Porez na dohodak, paušalno oporezivanje djelatnosti", "050303 Porez na dodanu vrijednost, trošarine", "050304 Porez na promet nekretnina", "050305 Porez na dobit", "050306 Lokalni porezi (županijski, gradski i općinski porezi)", "050307 Porezna uprava", "050308 Porezno savjetništvo", "050401 Doprinosi za financiranje obveznih osiguranja", "050501 Carinski propisi", "050502 Carinska služba", "050503 Slobodne zone, zastupanje u carinskom postupku", "050504 Posebne pristojbe na uvezenu robu", "060101 Normizacija, akreditacija", "060102 Mjeriteljstvo", "060201 Tehnički zahtjevi za proizvode", "060202 Nadzor predmeta od plemenitih kovina", "060301 Opća sigurnost proizvoda", "060302 Zdravstvena ispravnost predmeta opće uporabe", "060401 Inspekcije (osim građevinske, upravne, prosvjetne i sportske inspekcije, inspekcije cesta i cestovog prometa i financijskog inspektorata)", "070101 Poljoprivreda i ruralni razvoj, općenito", "070201 Potpore poljoprivredi, ruralnom razvoju i ribarstvu", "070301 Biljna proizvodnja, biljno zdravstvo, GMO", "070401 Vinogradarstvo, vinarstvo", "070501 Gnojiva i poboljšivači tla", "070601 Stočarstvo, zaštita životinja, zoo vrtovi", "070602 Veterinarstvo, veterinarski proizvodi", "070701 Ekološka proizvodnja, oznake izvornosti, zemljopisnog podrijetla i tradicionalnih specijaliteta", "070702 Sigurnost i standardi u proizvodnji hrane", "070801 Šumarstvo", "070901 Divljač - uzgoj, zaštita, lov i korištenje", "070902 Ribarstvo - morsko i slatkovodno", "080101 Rudarstvo i geološka istraživanja", "080201 Ugljikovodici - istraživanje i eksploatacija", "080301 Energija, općenito", "080302 Obnovljivi izvori energije, kogeneracija", "080303 Nafta, plin", "080401 Industrija, općenito", "090101 Održivi razvitak", "090201 Zaštita okoliša", "090202 Zaštita prirode", "090203 Zaštita od štetnog utjecaja kemikalija i biocidnih pripravaka", "090204 Zaštita od buke i svjetlosnog onečišćenja", "090205 Zaštita od eksplozija", "090206 Zaštita od elementarnih nepogoda, hidrometeorološki i seizmološki poslovi", "090301 Vode i vodno gospodarstvo", "090302 Komunalno gospodarstvo, komunalni red", "090303 Gospodarenje otpadom", "100101 Prostorno uređenje i gradnja", "100201 Obnova", "110101 Katastar nekretnina, geodetska djelatnost", "110102 Zemljišne knjige", "110201 Stanovanje, poslovni prostori", "110202 Posredovanje u prometu nekretnina", "110203 Procjena vrijednosti nekretnina", "120101 Trgovina na domaćem tržištu i s inozemstvom", "120201 Elektronička trgovina", "120301 Zaštita potrošača, potrošačko kreditiranje", "130101 Promet općenito", "130201 Pomorsko dobro, morske luke", "130202 Pomorski promet, lučke kapetanije", "130301 Unutarnja plovidba", "130401 Hrvatski registar brodova", "130501 Hidrografska djelatnost", "130601 Zračne luke i zračni promet", "130701 Željeznice i željeznički promet", "130801 Žičare", "130901 Javne i nerazvrstane ceste", "130902 Prijevoz putnika i tereta u cestovnom prometu", "130903 Sigurnost prometa na cestama, homologacija vozila, HAK", "131001 Poštanske i kurirske usluge", "140101 Ugostiteljstvo", "140201 Turizam", "150101 Elektroničke komunikacije, IKT", "150201 Digitalni sadržaji i usluge", "150301 Zaštita osobnih podataka (GDPR)", "160101 Hrvatska narodna banka", "160102 Banke, kreditne institucije", "160201 Leasing", "160202 Faktoring", "160301 Društva za osiguranje, poslovi osiguranja", "160302 Obvezna osiguranja u prometu", "160401 Mirovinski fondovi, mirovinska osiguravajuća društva, dokup mirovine, REGOS", "160501 Investicijski fondovi i društva za upravljanje", "160502 Novčani fondovi", "160503 Privatizacijski investicijski fondovi i ostali investicijski fondovi", "160601 Tržište kapitala (burza) i tržište novca", "160701 Nadzor financijskih usluga i društava (HANFA)", "170101 Obrazovanje i znanost, općenito", "170201 Predškolski odgoj i obrazovanje", "170301 Školstvo i obrazovanje, općenito", "170401 Osnovno, srednje, srednje strukovno i umjetničko obrazovanje", "170501 Obrazovanje odraslih", "170601 Visoko obrazovanje i znanost", "170701 Obrazovne kvalifikacije", "170801 Ostale djelatnosti i područja u obrazovanju", "180101 Kultura i umjetnost, općenito", "180102 Kulturna dobra", "180103 Arhivi", "180104 Knjižnice", "180105 Muzeji", "180106 Kazališta", "180107 Audiovizualne djelatnosti", "180201 Sport", "180301 Igre na sreću i nagradne igre", "180401 Mediji, općenito", "180402 Elektronički mediji", "190101 Zdravstvena zaštita, općenito", "190102 Zaštita od zaraznih bolesti", "190103 Zaštita pacijenata, zaštita zdravstvenih podataka", "190104 Prevencija bolesti i ovisnosti", "190201 Djelatnosti u zdravstvu, opće odredbe", "190202 Stomatološka djelatnost", "190203 Fizioterapeutska djelatnost", "190204 Psihološka djelatnost i djelatnosti psihoterapije", "190205 Medicinsko-biokemijska djelatnost", "190206 Transfuzijska djelatnost", "190207 Hitna medicina", "190208 Primjena ljudskih tkiva i stanica", "190209 Presađivanje ljudskih organa", "190210 Medicinski pomognuta oplodnja", "190211 Ostale djelatnosti i područja u zdravstvu", "190301 Liječništvo", "190302 Sestrinstvo", "190303 Primaljstvo", "190401 Zdravstvene ustanove", "190501 Obvezno i dobrovoljno zdravstveno osiguranje", "190601 Ljekarništvo, lijekovi", "190602 Medicinski proizvodi", "190701 Socijalna skrb i rad, općenito", "190702 Prognanici, povratnici i izbjeglice", "190703 Branitelji, invalidi rata, nestale osobe", "190704 Humanitarna pomoć i solidarnost", "190705 Edukacijsko-rehabilitacijska djelatnost", "190706 Udomiteljstvo", "190707 Novčane naknade i prava rodilja, roditelja, djece i omladine, zaslužnih osoba", "190708 Prava osoba s invaliditetom i djece s poteškoćama u razvoju", "190709 Djelatnost dadilje", "200101 Nacionalna sigurnost RH, općenito", "200201 Obrana", "200202 Oružje i vojna oprema", "200301 Policija", "200302 Državna granica", "200401 Sigurnosno-obavještajni sustav", "200402 Tajnost podataka, informacijska sigurnost", "200501 Radiološka i nuklearna sigurnost", "200601 Zaštita od požara, vatrogastvo", "200701 Hrvatska gorska služba spašavanja", "200801 Privatna zaštita osoba i imovine, detektivska djelatnost", "210101 Ustanove, općenito", "210201 Udruge i civilno društvo", "210301 Političke stranke", "210401 Vjerske zajednice", "210501 Zaklade", "220101 Ustav RH i ljudska prava", "220102 Ustavni sud", "220103 Konvalidacija i ništetnost pravnih propisa", "220104 Državna znamenja, odlikovanja i priznanja", "220105 Domovinski rat", "220106 Računanje vremena", "220107 Javno okupljanje, građanska inicijativa", "220108 Nacionalne manjine", "220109 Izborni sustav", "220201 Predsjednik RH", "220202 Vlada RH", "220203 Hrvatski sabor", "220301 Državna uprava, općenito", "220302 Pečati i žigovi", "220303 Upravna inspekcija", "220304 Službena statistika", "220401 Lokalna i područna (regionalna) samouprava, općenito", "220402 Potpomognuta područja, razvojne posebnosti", "220501 Strateško planiranje i upravljanje razvojem RH", "220601 Dužnosnici, saborski zastupnici", "220701 Državna imovina (dionice, nekretnine i dr.)", "220702 Javno-privatno partnerstvo", "220703 Koncesije", "220801 Pravo na pristup informacijama", "230101 Državni proračun, proračunsko računovodstvo", "230102 Izvršavanje Državnog proračuna - Državni zajmovi i krediti (zaduživanje i otplata)", "230201 Državne potpore, općenito", "230301 Javna nabava", "230401 Robne zalihe RH", "230501 Unutarnja kontrola i revizija u javnom sektoru, državna revizija", "240101 Pravosuđe, općenito", "240201 Sudovi, komunikacija sa sudovima", "240202 Sudske pristojbe", "240301 Državno odvjetništvo, USKOK, sprječavanje korupcije", "240401 Pravobraniteljstvo", "240501 Javno bilježništvo", "240502 Javnobilježničke pristojbe i tarifa", "240601 Odvjetništvo", "250101 Državljanstvo, javne isprave", "250102 Stranci u RH, azil", "250201 Upravni postupak", "250202 Upravni spor", "250203 Upravne pristojbe", "250301 Nasljeđivanje", "250401 Obiteljsko pravo, zaštita od nasilja", "250402 Životno partnerstvo", "250501 Parnični postupak", "250601 Arbitraža, mirenje", "250701 Kazneno pravo, postupak i oprost", "250702 Kaznene sankcije, izvršavanje", "250801 Prekršaji i prekršajni postupak", "250901 Kolizijski propisi, mjerodavno pravo", "260101 Vanjski poslovi, diplomatska i konzularna predstavništva", "260201 Europska unija i RH", "260301 Međunarodna suradnja RH", "260401 Hrvati izvan RH", "270101 Međunarodne organizacije (Međunarodno pravo)", "270201 Međunarodni ugovori (Međunarodno pravo)", "270301 Sukcesija država i ugovora (Međunarodno pravo)", "270401 Lokalna samouprava (Međunarodno pravo)", "270501 Diplomatski i konzularni odnosi (Međunarodno pravo)", "270502 Zaštita klasificiranih podataka (Međunarodno pravo)", "270601 Granice, vize, prihvat i predaja osoba (Međunarodno pravo)", "270701 Rad, zapošljavanje (Međunarodno pravo)", "270702 Socijalno osiguranje (Međunarodno pravo)", "270801 Gospodarska suradnja, općenito (Međunarodno pravo)", "270802 Industrija, energetika, resursi (Međunarodno pravo)", "270803 Poljoprivreda, šumarstvo i ribarstvo (Međunarodno pravo)", "270804 Turizam (Međunarodno pravo)", "270805 Trgovina i carine (Međunarodno pravo)", "270901 Tehnički propisi (Međunarodno pravo)", "271001 Promet, općenito (Međunarodno pravo)", "271002 Željeznički promet (Međunarodno pravo)", "271003 Cestovni promet (Međunarodno pravo)", "271004 Pomorski i riječni promet, more (Međunarodno pravo)", "271005 Zračni promet (Međunarodno pravo)", "271006 Svemirsko pravo (Međunarodno pravo)", "271007 Pošta i komunikacije (Međunarodno pravo)", "271101 Zaduživanje, tehnička i financijska pomoć (Međunarodno pravo)", "271102 Oporezivanje, platni sporazumi (Međunarodno pravo)", "271103 Ulaganja (Međunarodno pravo)", "271201 Zdravlje (Međunarodno pravo)", "271301 Obrazovanje, kultura, znanost, tehnologija, sport (Međunarodno pravo)", "271401 Zaštita okoliša (Međunarodno pravo)", "271402 Meterologija, prirodne i civilizacijske katastrofe (Međunarodno pravo)", "271501 Mirno rješavanje sporova (Međunarodno pravo)", "271502 Rat i obrana, vojna suradnja, humanitarno pravo (Međunarodno pravo)", "271601 Ljudska prava, manjine (Međunarodno pravo)", "271701 Građanskopravni status i odnosi, obitelj (Međunarodno pravo)", "271801 Intelektualno vlasništvo (Međunarodno pravo)", "271901 Kaznena djela, policijska suradnja (Međunarodno pravo)", "272001 Pravna pomoć i suradnja, izručenje, sudske odluke (Međunarodno pravo)", "00 Nedefinirano", "250502 Izvanparnični postupak", "190801 Demografija"
]

DOZVOLJENI_GRADOVI = [
    "Bjelovar", "Crikvenica", "Dubrovnik", "Đakovo", "Gospić", "Karlovac", "Koprivnica", "Kutina", "Makarska", "Metković", "Novi Zagreb", "Osijek", "Pazin", "Požega", "Rijeka", "Sesvete", "Pula", "Sisak", "Slavonski Brod", "Split", "Šibenik", "Varaždin", "Velika Gorica", "Vukovar", "Vinkovci", "Virovitica", "Zadar", "Zlatar", "Strasbourg", "Luxembourg", "Nedefinirano", "Zabok", "Zaprešić", "Zagreb", "Imotski", "Buje", "Korčula", "Krapina", "Našice", "Sinj", "Novom Zagrebu", "Bjelovaru", "Crikvenici", "Dubrovniku", "Gospiću", "Karlovcu", "Koprivnici", "Kutini", "Makarskoj", "Metkoviću", "Osijeku", "Pazinu", "Požegi", "Puli", "Rijeci", "Sesvetama", "Sisku", "Slavonskom Brodu", "Splitu", "Varaždinu", "Velikoj Gorici", "Vinkovcima", "Virovitici", "Vukovaru", "Zadru", "Zlataru", "Čakovec", "Čakovcu", "Đakovu", "Šibeniku", "Zagrebu", "Čazma", "Daruvar", "Garešnica", "Grubišno polje", "Križevci", "Pakrac", "Krk", "Rab", "Senj", "Prelog", "Blato", "Lastovo", "Gračac", "Otočac", "Duga Resa", "Ogulin", "Slunj", "Đurđevac", "Novska", "Ploče", "Vrgorac", "Jastrebarsko", "Samobor", "Beli Manastir", "Donji Miholjac", "Valpovo", "Labin", "Poreč", "Umag", "Rovinj", "Delnice", "Mali Lošinj", "Opatija", "Dugo Selo", "Sveti Ivan Zelina", "Vrbovec", "Glina", "Hrvatska Kostajnica", "Petrinja", "Nova Gradiška", "Stari Grad", "Supetar", "Trogir", "Knin", "Ivanec", "Novi Marof", "Ivanić Grad", "Županja", "Slatina", "Benkovac", "Biograd na Moru", "Pag", "Donja Stubica", "Klanjec"
]

MJESECI = {
    "1": "Siječanj", "2": "Veljača", "3": "Ožujak", "4": "Travanj",
    "5": "Svibanj", "6": "Lipanj", "7": "Srpanj", "8": "Kolovoz",
    "9": "Rujan", "10": "Listopad", "11": "Studeni", "12": "Prosinac",
    "01": "Siječanj", "02": "Veljača", "03": "Ožujak", "04": "Travanj",
    "05": "Svibanj", "06": "Lipanj", "07": "Srpanj", "08": "Kolovoz",
    "09": "Rujan"
}

UPUTE_ZA_GEMINI = f"""
Ti si stručni pravni asistent urednika portala sudske prakse.
Tvoj zadatak je analizirati tekst sudske presude i vratiti JSON sa sljedećim ključevima:
- "broj_odluke": Poslovni broj odluke iz teksta.
- "vrsta_odluke": Smiješ koristiti SAMO jednu od ovih opcija: {DOZVOLJENE_VRSTE_ODLUKA}
- "vrsta_postupka": Smiješ koristiti SAMO jednu od ovih opcija, prepoznaj točan oblik: {DOZVOLJENE_VRSTE_POSTUPAKA}
- "naziv_suda": Točan naziv suda kako stoji u zaglavlju.
- "grad": Prepoznaj grad u kojem se nalazi sud prema zaglavlju presude (npr. 'Općinski sud u Šibeniku' -> 'Šibenik'). Smiješ koristiti SAMO jednu opciju s ovog popisa: {DOZVOLJENI_GRADOVI}
- "ecli": ECLI broj, ako izričito postoji u tekstu. Ako ne postoji, ostavi prazno.
- "podrucje_prava": Smiješ koristiti SAMO jednu od ovih opcija: {DOZVOLJENA_PODRUCJA_PRAVA}
- "kljucne_rijeci": Ključni pravni pojmovi odvojeni zarezom (npr. 'nedozvoljene igre na sreću, oduzimanje predmeta').
- "sazetak": Vrlo detaljan i stručan pravni sažetak. Mora uključivati: tko je i zašto proglašen krivim/oslobođenim, točan opis radnje/spora, izrečenu sankciju (npr. uvjetna osuda, kazna zatvora) i sporedne mjere (npr. oduzimanje predmeta).
"""


# ==========================================
# 2. OBRADA PREKO UMJETNE INTELIGENCIJE
# ==========================================

def analiziraj_presudu(tekst_presude):
    print("Šaljem presudu Gemini modelu na analizu...")
    model = genai.GenerativeModel(
        model_name="gemini-2.5-pro",
        system_instruction=UPUTE_ZA_GEMINI,
        generation_config={"response_mime_type": "application/json"}
    )

    odgovor = model.generate_content(tekst_presude)
    podaci = json.loads(odgovor.text)

    podaci["naslov"] = podaci.get("broj_odluke", "")
    return podaci


# ==========================================
# 3. KONTROLE ZA LING.HR
# ==========================================

def upisi_tekst(page, selektor, tekst):
    """
    Upisuje tekst u standardno input/textarea polje.

    React overridea value setter pa Playwright .fill() ne aktivira onChange.
    Koristimo native setter za TOČAN element tip (Input vs Textarea).
    """
    if tekst:
        try:
            polje = page.locator(selektor)
            polje.click()
            time.sleep(0.2)

            page.evaluate('''(args) => {
                const [sel, val] = args;
                const el = document.querySelector(sel);
                if (!el) return;

                // KLJUČNO: koristiti setter od TOČNOG prototipa za tip elementa
                const proto = el.tagName.toLowerCase() === 'textarea'
                    ? window.HTMLTextAreaElement.prototype
                    : window.HTMLInputElement.prototype;
                const nativeSetter = Object.getOwnPropertyDescriptor(proto, 'value')?.set;

                if (nativeSetter) {
                    nativeSetter.call(el, val);
                } else {
                    el.value = val;
                }

                el.dispatchEvent(new Event('input', { bubbles: true }));
                el.dispatchEvent(new Event('change', { bubbles: true }));
            }''', [selektor, tekst])

            time.sleep(0.2)
            page.keyboard.press("Tab")
            time.sleep(0.3)
        except Exception as e:
            print(f"  [!] Greška pri unosu teksta u {selektor}: {e}")
            try:
                page.locator(selektor).fill(tekst)
                page.keyboard.press("Tab")
                time.sleep(0.3)
            except:
                pass


def unesi_datum(page, naziv_polja, datum_string):
    """
    Popunjava datum putem react-datepicker komponente.

    HTML struktura datumskog polja:
      div (kontejner)
        div (zaglavlje - klikabilno, sadrži label + SVG ikonu)
          div "Datum odluke"   ← label
          div                  ← prikaz odabranog datuma
          svg                  ← ikona kalendara
        div (popup s kalendarom)
          div.react-datepicker
            div[width="100px"]  ← trigger za godinu
            div[width="130px"]  ← trigger za mjesec
            div.react-datepicker__day ← dani
    """
    if not datum_string:
        return
    try:
        dijelovi = datum_string.strip('.').split('.')
        if len(dijelovi) != 3:
            print(f"  [!] Neispravan format datuma: {datum_string}")
            return

        dan = str(int(dijelovi[0].strip()))
        mjesec = dijelovi[1].strip()
        godina = dijelovi[2].strip()
        naziv_mjeseca = MJESECI.get(mjesec)

        if not naziv_mjeseca:
            print(f"  [!] Nepoznat mjesec: {mjesec}")
            return

        print(f"  -> Odabirem u kalendaru: {dan}. {naziv_mjeseca} {godina}. (za polje '{naziv_polja}')")

        # 1. Klik na zaglavlje datumskog polja (parent div labela) da se otvori kalendar
        zaglavlje = page.locator(
            f'xpath=//div[text()="{naziv_polja}"]/parent::div'
        ).first
        zaglavlje.click(force=True)
        time.sleep(1)

        # 2. Pronađi react-datepicker unutar najbližeg ancestor kontejnera
        kalendar = page.locator(
            f'xpath=//div[text()="{naziv_polja}"]'
            f'/ancestor::div[.//div[contains(@class,"react-datepicker")]][1]'
        ).first.locator('.react-datepicker').first
        kalendar.wait_for(state="visible", timeout=5000)

        # 3. Odaberi godinu - klik na dropdown trigger (width="100px")
        kalendar.locator('div[width="100px"]').first.click(force=True)
        time.sleep(0.5)

        god_opcija = kalendar.locator(f'div.css-114bz43[title="{godina}"]').first
        god_opcija.scroll_into_view_if_needed()
        time.sleep(0.2)
        god_opcija.click(force=True)
        time.sleep(0.5)

        # 4. Odaberi mjesec - klik na dropdown trigger (width="130px")
        kalendar.locator('div[width="130px"]').first.click(force=True)
        time.sleep(0.5)

        mj_opcija = kalendar.locator(f'div.css-114bz43[title="{naziv_mjeseca}"]').first
        mj_opcija.scroll_into_view_if_needed()
        time.sleep(0.2)
        mj_opcija.click(force=True)
        time.sleep(0.5)

        # 5. Odaberi dan - iteriraj po danima koji NISU outside-month
        dani = kalendar.locator(
            '.react-datepicker__day:not(.react-datepicker__day--outside-month)'
        ).all()
        dan_kliknut = False
        for d in dani:
            if d.inner_text().strip() == dan:
                d.click(force=True)
                dan_kliknut = True
                break

        if not dan_kliknut:
            print(f"  [!] Dan {dan} nije pronađen u kalendaru za {naziv_polja}")

        time.sleep(0.5)

    except Exception as e:
        print(f"  [!] Greška pri unosu datuma {datum_string} za {naziv_polja}: {e}")
        page.keyboard.press("Escape")
        time.sleep(0.3)


def odaberi_iz_padajuceg_izbornika(page, naziv_polja, trazena_vrijednost):
    """
    Odabire vrijednost iz custom dropdown izbornika.

    Koristi više strategija otvaranja dropdowna jer React komponenta
    ne reagira uvijek na isti tip klika (posebno nakon zatvaranja
    prethodnog dropdowna).
    """
    if not trazena_vrijednost:
        return
    try:
        print(f"  -> Biram iz izbornika '{naziv_polja}': {trazena_vrijednost}")

        # Zatvori bilo koji prethodno otvoreni dropdown
        page.keyboard.press("Escape")
        time.sleep(0.5)

        trigger = page.locator(
            f'xpath=//div[text()="{naziv_polja}"]'
            f'/following-sibling::div[*[local-name()="svg"]]'
        ).first
        trigger.scroll_into_view_if_needed()
        time.sleep(0.3)

        opcija = page.locator(f'div.css-114bz43[title="{trazena_vrijednost}"]').first
        otvoren = False

        # Strategija 1: dispatch_event('click') - šalje DOM event
        trigger.dispatch_event('click')
        time.sleep(1.5)
        if opcija.is_visible():
            otvoren = True

        # Strategija 2: page.mouse.click na koordinatama triggera
        if not otvoren:
            page.keyboard.press("Escape")
            time.sleep(0.3)
            box = trigger.bounding_box()
            if box:
                page.mouse.click(
                    box['x'] + box['width'] / 2,
                    box['y'] + box['height'] / 2
                )
                time.sleep(1.5)
                if opcija.is_visible():
                    otvoren = True

        # Strategija 3: klik na SVG strelicu unutar triggera
        if not otvoren:
            page.keyboard.press("Escape")
            time.sleep(0.3)
            svg = trigger.locator('svg').first
            svg.dispatch_event('click')
            time.sleep(1.5)
            if opcija.is_visible():
                otvoren = True

        # Strategija 4: JavaScript native click na trigger
        if not otvoren:
            page.keyboard.press("Escape")
            time.sleep(0.3)
            page.evaluate('''(labelText) => {
                const divs = document.querySelectorAll('div');
                for (const d of divs) {
                    if (d.textContent.trim() === labelText &&
                        d.nextElementSibling &&
                        d.nextElementSibling.querySelector('svg')) {
                        d.nextElementSibling.click();
                        return;
                    }
                }
            }''', naziv_polja)
            time.sleep(1.5)
            if opcija.is_visible():
                otvoren = True

        if not otvoren:
            print(f"  [!] Dropdown '{naziv_polja}' se ne otvara nakon 4 pokušaja.")
            return

        opcija.scroll_into_view_if_needed()
        time.sleep(0.2)
        opcija.click(force=True)
        time.sleep(0.8)

    except Exception as e:
        print(f"  [!] Greška za padajući izbornik '{naziv_polja}': {e}")
        page.keyboard.press("Escape")
        time.sleep(0.3)


def odaberi_checkbox_podrucje_prava(page, trazena_vrijednost):
    """
    Označava checkbox u izborniku "Područje prava".

    Koristi čisti JavaScript pristup: otvori dropdown, scrollaj do
    checkboxa, klikni ga. Izbjegava Playwright visibility probleme
    jer dropdown opcije su skrivene CSS-om do otvaranja.
    """
    if not trazena_vrijednost:
        return
    try:
        print(f"  -> Označavam područje prava: {trazena_vrijednost}")

        page.keyboard.press("Escape")
        time.sleep(0.5)

        # Korak 1: Otvori dropdown klikom na trigger putem JS
        page.evaluate('''() => {
            const divs = document.querySelectorAll('div');
            for (const d of divs) {
                if (d.textContent.trim() === 'Područje prava' &&
                    d.nextElementSibling &&
                    d.nextElementSibling.querySelector('svg')) {
                    d.nextElementSibling.click();
                    return;
                }
            }
        }''')
        time.sleep(2)

        # Korak 2: Pronađi checkbox i klikni ga putem JS
        rezultat = page.evaluate('''(searchText) => {
            // Pronađi sve checkbox redove
            const rows = document.querySelectorAll('.e1xea2lb6');
            for (const row of rows) {
                const label = row.querySelector('.e1xea2lb5, .css-1d193z1');
                if (label && label.textContent.trim() === searchText) {
                    row.scrollIntoView({ block: 'center' });
                    const cb = row.querySelector('input[type="checkbox"]');
                    if (cb) {
                        cb.click();
                        return { found: true, checked: cb.checked };
                    }
                }
            }
            // Fallback: parcijalno podudaranje po kodu (npr. "180301")
            const code = searchText.split(' ')[0];
            for (const row of rows) {
                const label = row.querySelector('.e1xea2lb5, .css-1d193z1');
                if (label && label.textContent.includes(code)) {
                    row.scrollIntoView({ block: 'center' });
                    const cb = row.querySelector('input[type="checkbox"]');
                    if (cb) {
                        cb.click();
                        return { found: true, checked: cb.checked };
                    }
                }
            }
            return { found: false, checked: false };
        }''', trazena_vrijednost)

        if rezultat and rezultat.get('found'):
            print(f"  -> Checkbox kliknut: {trazena_vrijednost} (checked={rezultat.get('checked')})")
        else:
            print(f"  [!] Područje prava '{trazena_vrijednost}' nije pronađeno u listi.")

        time.sleep(0.5)
        page.keyboard.press("Escape")
        time.sleep(0.3)

    except Exception as e:
        print(f"  [!] Greška pri odabiru područja prava: {e}")
        page.keyboard.press("Escape")
        time.sleep(0.3)


def popuni_lexical_editor(page, tekst_html, tekst_plain):
    """
    Upisuje tekst u Lexical rich-text editor (#editor-output).

    Prima i HTML i plain-text verziju teksta presude.
    Koristi ClipboardEvent s text/html za očuvanje formatiranja
    (paragrafi, bold, struktura) iz originalne presude.

    Fallback: insertHTML execCommand, pa insertText za plain tekst.
    """
    if not tekst_html and not tekst_plain:
        return
    try:
        print("  -> Upisujem tekst presude u editor...")

        editor = page.locator('#editor-output')
        editor.click(force=True)
        time.sleep(0.5)

        page.keyboard.press("Control+A")
        time.sleep(0.2)
        page.keyboard.press("Backspace")
        time.sleep(0.3)

        if tekst_html:
            # Metoda 1: ClipboardEvent paste s HTML sadržajem
            # Lexical obrađuje paste evente i čuva HTML formatiranje
            uspjeh = page.evaluate('''(html) => {
                try {
                    const el = document.querySelector('#editor-output');
                    el.focus();
                    document.execCommand('selectAll', false, null);
                    document.execCommand('delete', false, null);

                    const dt = new DataTransfer();
                    dt.setData('text/html', html);
                    dt.setData('text/plain', html.replace(/<[^>]*>/g, ''));
                    const pasteEvent = new ClipboardEvent('paste', {
                        clipboardData: dt,
                        bubbles: true,
                        cancelable: true,
                        composed: true
                    });
                    el.dispatchEvent(pasteEvent);
                    return true;
                } catch(e) {
                    return false;
                }
            }''', tekst_html)

            if uspjeh:
                time.sleep(1)
                sadrzaj = editor.inner_text().strip()
                if len(sadrzaj) > 50:
                    print("  -> Tekst (HTML) uspješno unesen u editor.")
                    return
                print("  [!] HTML paste nije unio tekst, pokušavam insertHTML...")

            # Metoda 2: insertHTML execCommand
            page.evaluate('''(html) => {
                const el = document.querySelector('#editor-output');
                el.focus();
                document.execCommand('selectAll', false, null);
                document.execCommand('delete', false, null);
                document.execCommand('insertHTML', false, html);
            }''', tekst_html)

            time.sleep(1)
            sadrzaj = editor.inner_text().strip()
            if len(sadrzaj) > 50:
                print("  -> Tekst (insertHTML) uspješno unesen u editor.")
                return
            print("  [!] insertHTML nije unio tekst, pokušavam plain text...")

        # Metoda 3: Fallback na plain text s insertText/insertParagraph
        tekst = tekst_plain or tekst_html
        if tekst:
            page.evaluate('''(text) => {
                const el = document.querySelector('#editor-output');
                el.focus();
                document.execCommand('selectAll', false, null);
                document.execCommand('delete', false, null);

                const lines = text.split('\\n');
                for (let i = 0; i < lines.length; i++) {
                    if (i > 0) {
                        document.execCommand('insertParagraph', false, null);
                    }
                    if (lines[i].length > 0) {
                        document.execCommand('insertText', false, lines[i]);
                    }
                }
            }''', tekst)
            time.sleep(0.5)
            print("  -> Tekst (plain) uspješno unesen u editor.")

    except Exception as e:
        print(f"  [!] Greška pri unosu teksta u editor: {e}")


def klikni_dalje(page, opis_koraka):
    """
    Klikne gumb 'Dalje' i VERIFICIRA da je navigacija uspjela.

    Problem: .click(force=True) dispatchira DOM evente ali React handler
    ne reagira. Razlog može biti pointer-events, React synth event system,
    ili form validacija.

    Koristi više strategija klika i provjerava je li Step 1 sadržaj nestao.
    """
    print(f"  -> Klikam 'Dalje' ({opis_koraka})...")

    dalje = page.locator('div[role="button"]:text-is("Dalje")').last
    dalje.scroll_into_view_if_needed()
    time.sleep(0.5)

    strategije = [
        ("JavaScript native click", lambda: page.evaluate('''() => {
            const buttons = document.querySelectorAll('div[role="button"]');
            for (const btn of buttons) {
                if (btn.textContent.trim() === 'Dalje') {
                    btn.click();
                    return true;
                }
            }
            return false;
        }''')),
        ("dispatch_event click", lambda: dalje.dispatch_event('click')),
        ("mouse.click na koordinatama", lambda: _mouse_click_element(page, dalje)),
        ("pointerdown + pointerup + click", lambda: _pointer_click(page, dalje)),
        ("Playwright click bez force", lambda: dalje.click(timeout=3000)),
        ("Playwright click force", lambda: dalje.click(force=True)),
    ]

    for naziv, akcija in strategije:
        try:
            akcija()
        except Exception:
            pass
        time.sleep(3)

        try:
            page.wait_for_load_state("networkidle", timeout=5000)
        except:
            pass

        # Provjeri je li navigacija uspjela - na Step 1 postoji input[name="title"]
        if not page.locator('input[name="title"]').is_visible():
            print(f"    ✓ Navigacija uspjela (strategija: {naziv})")
            return True

        print(f"    ✗ Strategija '{naziv}' nije pokrenula navigaciju, pokušavam sljedeću...")

    print("  [!] Nijedna strategija nije uspjela pokrenuti navigaciju!")
    return False


def _mouse_click_element(page, locator):
    box = locator.bounding_box()
    if box:
        page.mouse.click(box['x'] + box['width'] / 2, box['y'] + box['height'] / 2)


def _pointer_click(page, locator):
    locator.dispatch_event('pointerdown')
    time.sleep(0.1)
    locator.dispatch_event('pointerup')
    time.sleep(0.1)
    locator.dispatch_event('click')


def klikni_dalje_korak(page, opis, provjera_selektor=None):
    """Klikne 'Dalje' na koraku koji NIJE Step 1 (nema input[name=title] provjeru)."""
    print(f"  -> Klikam 'Dalje' ({opis})...")

    dalje = page.locator('div[role="button"]:text-is("Dalje")').last
    dalje.scroll_into_view_if_needed()
    time.sleep(0.5)

    for naziv, akcija in [
        ("JS click", lambda: page.evaluate('''() => {
            const buttons = document.querySelectorAll('div[role="button"]');
            for (const btn of buttons) {
                if (btn.textContent.trim() === 'Dalje') { btn.click(); return; }
            }
        }''')),
        ("dispatch", lambda: dalje.dispatch_event('click')),
        ("mouse", lambda: _mouse_click_element(page, dalje)),
        ("force", lambda: dalje.click(force=True)),
    ]:
        try:
            akcija()
        except:
            pass
        time.sleep(3)

        try:
            page.wait_for_load_state("networkidle", timeout=5000)
        except:
            pass

        if provjera_selektor:
            try:
                page.wait_for_selector(provjera_selektor, timeout=5000)
                print(f"    ✓ Navigacija uspjela (strategija: {naziv})")
                return True
            except:
                print(f"    ✗ '{naziv}' nije pokrenula navigaciju...")
                continue
        else:
            print(f"    ✓ Klik izvršen ({naziv})")
            return True

    print("  [!] 'Dalje' klik nije uspio!")
    return False


# ==========================================
# 4. GLAVNI ROBOT
# ==========================================

def glavni_proces():
    url_pretrage_sudova = "https://odluke.sudovi.hr/Document/DisplayList?q=zakon%20o%20igrama%20na%20sre%C4%87u&sort=dat&prm=pravomocna"
    url_ling_editora = "https://ling.hr/backoffice/jurisprudence/add/step-one"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=50)
        context = browser.new_context()
        context.grant_permissions(['clipboard-read', 'clipboard-write'])
        page = context.new_page()

        print("Otvaram ling.hr. Molim Vas, prijavite se ako već niste. Imate 15 sekundi...")
        page.goto("https://ling.hr")
        time.sleep(15)

        # --- KORAK A: Prikupljanje linkova ---
        print("Spajam se na e-Sudove i tražim sve presude...")
        page.goto(url_pretrage_sudova)

        sve_veze = []
        broj_stranice = 1

        while True:
            page.wait_for_selector('.search-result')
            time.sleep(2)

            elementi_presuda = page.locator('a.search-result').all()
            for el in elementi_presuda:
                href = el.get_attribute('href')
                if href:
                    sve_veze.append("https://odluke.sudovi.hr" + href)

            print(f"Prikupljena {broj_stranice}. stranica (Trenutno linkova: {len(sve_veze)})")

            next_btn = page.locator('a[aria-label="Next"]')
            if next_btn.count() > 0:
                roditelj_li = next_btn.locator('xpath=..')
                klase_roditelja = roditelj_li.get_attribute('class') or ""
                if "disabled" in klase_roditelja:
                    break
                else:
                    next_btn.click(force=True)
                    broj_stranice += 1
            else:
                break

        # TESTIRANJE: Samo prva presuda
        sve_veze = sve_veze[:1]
        print(f"Pronađeno UKUPNO presuda za obradu: {len(sve_veze)}")

        # --- KORAK B: Obrada ---
        for redni_broj, link in enumerate(sve_veze, 1):
            try:
                print(f"\n{'='*60}")
                print(f"[{redni_broj}/{len(sve_veze)}] Otvaram presudu: {link}")
                page.goto(link)

                page.wait_for_selector('.decision-text')

                datum_odluke = ""
                try:
                    datum_odluke = page.locator(
                        '.metadata-item[data-metadata-type="decision-date"] .metadata-content'
                    ).first.inner_text().strip()
                except:
                    pass

                datum_objave = ""
                try:
                    datum_objave = page.locator(
                        '.metadata-item[data-metadata-type="publication-date"] .metadata-content'
                    ).first.inner_text().strip()
                except:
                    pass

                elementi_zakona = page.locator(
                    '.view-sidebar .metadata-item[data-metadata-type="zakonsko-kazalo-index"] li.law-title a'
                ).all()
                popis_zakona = [el.inner_text().strip() for el in elementi_zakona if "NN" not in el.inner_text()]

                tekst_presude = page.locator('.decision-text').inner_text()
                tekst_presude_html = page.locator('.decision-text').inner_html()

                podaci = analiziraj_presudu(tekst_presude)
                print(f"Pripremljen unos za broj: {podaci.get('naslov', 'Nepoznato')}")

                # --- KORAK C: Unos na ling.hr - Step 1 ---
                page.goto(url_ling_editora, wait_until="networkidle")
                time.sleep(4)

                # Aktivacija kartice "Sudska odluka"
                # Stranica automatski prelazi na "Sentenca" nakon ~1s,
                # pa moramo kliknuti "Sudska odluka" i provjeriti ostaje li aktivna.
                print("  -> Aktiviram karticu 'Sudska odluka'...")
                for pokusaj_tab in range(5):
                    gumb_sudska = page.locator('div[role="button"]:text-is("Sudska odluka")').first
                    gumb_sudska.click()
                    time.sleep(2)

                    if page.locator('input[name="title"]').is_visible():
                        print("  -> Kartica 'Sudska odluka' aktivna.")
                        break
                    print(f"  [!] Pokušaj {pokusaj_tab+1}: prebacilo se, klikam ponovno...")

                # Tekstualna polja
                upisi_tekst(page, 'input[name="title"]', podaci.get('naslov', ''))
                upisi_tekst(page, 'input[name="decisionNumber"]', podaci.get('broj_odluke', ''))
                if podaci.get('ecli'):
                    upisi_tekst(page, 'input[name="ecli"]', podaci['ecli'])
                upisi_tekst(page, 'input[name="keywords"]', podaci.get('kljucne_rijeci', ''))
                upisi_tekst(page, 'textarea[name="abstract"]', podaci.get('sazetak', ''))

                # Kalendari
                unesi_datum(page, "Datum odluke", datum_odluke)
                unesi_datum(page, "Datum objave", datum_objave)

                # Padajući izbornici
                if podaci.get("vrsta_odluke"):
                    odaberi_iz_padajuceg_izbornika(page, "Vrsta odluke", podaci["vrsta_odluke"])
                if podaci.get("vrsta_postupka"):
                    odaberi_iz_padajuceg_izbornika(page, "Vrsta postupka", podaci["vrsta_postupka"])
                if podaci.get("naziv_suda"):
                    odaberi_iz_padajuceg_izbornika(page, "Naziv suda", podaci["naziv_suda"])
                if podaci.get("grad"):
                    odaberi_iz_padajuceg_izbornika(page, "Grad / Ispostava", podaci["grad"])

                # Checkbox - Područje prava
                if podaci.get("podrucje_prava"):
                    odaberi_checkbox_podrucje_prava(page, podaci["podrucje_prava"])

                # Tekst editor (Lexical) - šaljemo HTML za očuvanje formatiranja
                popuni_lexical_editor(page, tekst_presude_html, tekst_presude)

                # Provjeri jesu li ključna polja popunjena prije klika na Dalje
                print("  -> Provjera popunjenosti polja...")
                naslov_val = page.evaluate('document.querySelector(\'input[name="title"]\')?.value || ""')
                broj_val = page.evaluate('document.querySelector(\'input[name="decisionNumber"]\')?.value || ""')
                print(f"    Naslov: '{naslov_val}' | Broj: '{broj_val}'")
                if not naslov_val:
                    print("  [!] Naslov je prazan! Pokušavam ponovo upisati...")
                    polje = page.locator('input[name="title"]')
                    polje.click()
                    time.sleep(0.2)
                    polje.fill(podaci.get('naslov', podaci.get('broj_odluke', '')))
                    time.sleep(0.2)
                    page.keyboard.press("Tab")
                    time.sleep(0.5)
                    naslov_val = page.evaluate('document.querySelector(\'input[name="title"]\')?.value || ""')
                    print(f"    Naslov nakon ponovnog unosa: '{naslov_val}'")

                # --- Step 1 → Step 2 ---
                if not klikni_dalje(page, "Step 1 → Step 2"):
                    print("  [!] PRESKAĆEM ovu presudu - navigacija Step 1→2 nije uspjela.")
                    continue

                # --- KORAK D: Step 2 (Prošle odluke) ---
                print("  -> Step 2: Prošle odluke - preskačem...")
                time.sleep(2)
                page.wait_for_load_state("networkidle")
                time.sleep(1)

                # --- Step 2 → Step 3 ---
                if not klikni_dalje_korak(page, "Step 2 → Step 3"):
                    print("  [!] Navigacija Step 2→3 nije uspjela, nastavljam...")

                # --- KORAK E: Step 3 (Propisi) ---
                print("  -> Step 3: Unosim povezane propise...")
                time.sleep(2)
                page.wait_for_load_state("networkidle")
                time.sleep(1)

                for zakon in set(popis_zakona):
                    try:
                        trazilica = page.locator('input[placeholder="Pretraži..."]')
                        if trazilica.count() == 0:
                            print(f"    [!] Nema polja za pretragu, preskačem propise.")
                            break

                        trazilica.first.click()
                        time.sleep(0.3)
                        trazilica.first.fill("")
                        time.sleep(0.2)
                        trazilica.first.fill(zakon)
                        time.sleep(2)

                        prvi_rezultat = page.locator('table tbody tr:first-child td span')
                        if prvi_rezultat.count() > 0 and prvi_rezultat.first.is_visible():
                            prvi_rezultat.first.click(force=True)
                            print(f"    - Dodan: {zakon}")
                        else:
                            print(f"    [!] Nema rezultata za: {zakon}")
                    except Exception as e_zakon:
                        print(f"    [!] Greška pri dodavanju zakona '{zakon}': {e_zakon}")

                    time.sleep(0.5)

                # --- Step 3 → Step 4 ---
                klikni_dalje_korak(page, "Step 3 → Step 4")

                # --- KORAK F: Završni korak ---
                print("  -> Završni korak: Pregled...")
                time.sleep(2)
                page.wait_for_load_state("networkidle")
                time.sleep(1)

                pregled = page.locator('div[role="button"]:has-text("Pregled")')
                if pregled.count() > 0:
                    pregled.first.click(force=True)
                else:
                    print("  [!] Gumb 'Pregled' nije pronađen.")

                print(f"==== Unos dovršen za: {podaci.get('naslov', '')} ====")
                time.sleep(3)

            except Exception as e:
                print(f"[!!!] Neočekivana greška na presudi {link}: {e}")
                import traceback
                traceback.print_exc()

        print(f"\n{'='*60}")
        print("SVE PRESUDE SU USPJEŠNO OBRAĐENE!")
        time.sleep(10)
        browser.close()


if __name__ == "__main__":
    glavni_proces()
