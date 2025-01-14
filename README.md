# Modelowanie dyskretne
<p align="justify">
Bitmapowanie, lab 2 i lab 3 realizują edycje obrazów i podstawowe operacje (erozje, dylatacje, operacje otwarcia, zamknięcia ...). Nie są one obszernie opisane ponieważ zawierają pliki *.bmp obrazujące działanie funkcji. W realizacji wykorzystano biblioteki:</p>

- PIL
- numpy
- matplotlib.pyplot


## Gra w życie:
<p align="justify">
Projekt "Gra w życie" realizuje automat komórkowy Conway'a. W implementacji posłużyłem się biblioteką pygame 2.4.1 do wizualizacji i stworzenia prostego GUI (zdjęcie poniżej). Zaimplementowałem możliwość dodawania w czasie rzeczywistym podstawowych wzorów oraz zmiane warunków brzegowych</p>

<div align="center">
  <img src="Gra_W_Zycie/img.png" alt="GUI Gry w Życiu" width="500">
</div>

## Labirynt
<p align="justify">
Projekt Implementuje symulacje labiryntu, w którym użytkownik może:</p>

- samemu stowrzyć przestrzeń labiryntu wraz z łowcami
- wybrać już istniejącą mapę (zdjęcie poniżej) 

<div align="center">
  <img src="Labirynt/default.png" alt="GUI Gry w Życiu" width="250">
</div>

<p align="justify">
Dalej z bazy danych użytkownik wgrywa uciekinierów umieszczając ich w opdowiednich miejscach w Labiryncie. Zarówno uciekinierzy (kolor złoty), jak i łowcy (kolor czerwony) do osiągnięcia celu używają algortymu astar, natomiast uciekinierzy dodatkowo mają dodany element podstawowego q-learningu w czasie trwania symulacji. Celem łowcy jest złapanie najbliższefo uciekiniera, a uciekiniera unikanie łowców i dotarcie do wyjścia (kolor zielony). Oboje mogą poruszać się tylko i wyłącznie po korytarzach (kolor biały). Baza danych obsługiwana jest na localhost z kontenera docker-owego. GUI zaimplementowane przy użyciu pygame:</p>

<div align="center">
  <img src="Labirynt/GUI.png" alt="GUI Gry w Życiu" width="500">
</div>

## LGA:
<p allign="center">
W folderze zawarta jest implementacja nie tylko LGA, ale również dyfuzji LBM oraz przepływu LBM. O ile do realizacji LGA podszedłem w inny sposób - tworząc klasę środowiska i cząsteczek - to dyfuzje LBM zdefiniowałem jako macierz 3 wymiarową - x,y,tablica gęstości zmierzającej w odpowiednich kierunkach z sąsiedztwa von Neumanna, natomiast przepływ LBM dziedziczy z dyfuzji ale rozszerza tablicę gęstości do 9 kierunków zgodnie z sąsiedztwem Moore'a. W obu przypadkach LBM użyłem biblioteki Numba w celu zrównoleglenia obliczeń. Wyniki dla każdego z algorytmów po kolei:</p>

- LGA
  <div align="center">
  <img src="LGA/LGA.png" alt="GUI Gry w Życiu" width="500">
</div>

- LBM dyfuzja
  <div align="center">
  <img src="LGA/LBM_d.png" alt="GUI Gry w Życiu" width="500">
</div>

- LBM przepływ
  <div align="center">
  <img src="LGA/LBM_f.png" alt="GUI Gry w Życiu" width="500">
</div>
