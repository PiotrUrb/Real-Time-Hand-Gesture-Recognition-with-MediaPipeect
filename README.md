# Hand Gesture Recognition with MediaPipe

## Cel projektu

Celem projektu jest opracowanie systemu opartego na bibliotece **MediaPipe**, który umożliwia zaawansowane rozpoznawanie gestów dłoni w czasie rzeczywistym. System ten ma za zadanie:

- **Rozpoznawanie lewej i prawej dłoni** na obrazie z kamery.
- **Identyfikację strony dłoni** (wewnętrznej lub zewnętrznej) przy użyciu analizy landmarków dłoni.
- **Liczenie liczby wyprostowanych palców** i wizualizację wyników w czasie rzeczywistym.
- **Interpretację gestów dłoni w różnych orientacjach**, co może stanowić podstawę do zastosowań takich jak sterowanie urządzeniami za pomocą gestów czy monitorowanie ruchów rąk w aplikacjach zdrowotnych i sportowych.

## Opis działania programu

Program został zaimplementowany w języku **Python** z wykorzystaniem bibliotek **MediaPipe** i **OpenCV**. Jego działanie obejmuje następujące kroki:

### Inicjalizacja systemu

1. **Inicjalizacja kamery:**  
   Kamera jest konfigurowana za pomocą OpenCV, a obraz z niej pobierany jest w czasie rzeczywistym.
   
2. **Inicjalizacja MediaPipe Hands:**  
   Moduł ten pozwala na wykrycie dłoni oraz identyfikację 21 charakterystycznych punktów (landmarków) na jej powierzchni.

### Rozpoznawanie dłoni

1. **Wykrycie dłoni na obrazie:**  
   Moduł MediaPipe Hands analizuje obraz i identyfikuje obszary odpowiadające dłoniom.

2. **Identyfikacja strony dłoni:**  
   Strona dłoni (wewnętrzna lub zewnętrzna) określana jest na podstawie pozycji najniższego punktu kciuka względem nadgarstka. Taka metoda eliminacji błędów związanych z nietypowymi orientacjami dłoni zapewnia większą precyzję.

3. **Rozróżnienie lewej i prawej dłoni:**  
   MediaPipe Hands dostarcza klasyfikację dłoni jako lewej lub prawej z perspektywy użytkownika. W przypadku użycia kamery wymagane jest odwrócenie interpretacji, aby odpowiadała rzeczywistemu widokowi dłoni na ekranie.

### Analiza palców

1. **Liczenie wyprostowanych palców:**  
   Wykorzystując pozycje landmarków końcówek palców oraz punktów zgięcia, program analizuje, które palce są wyprostowane.

2. **Rozpoznanie kciuka:**  
   Specjalne algorytmy analizują orientację kciuka w zależności od strony dłoni. Inna logika stosowana jest dla strony wewnętrznej i zewnętrznej, co pozwala dokładnie rozróżniać jego położenie i wyprostowanie.

### Wizualizacja wyników

- Na obrazie wyświetlane są **landmarki dłoni** oraz **linie łączące poszczególne punkty**.
- Wyświetlane są informacje tekstowe, takie jak:
  - Rozpoznana dłoń (lewa/prawa).
  - Strona dłoni (wewnętrzna/zewnętrzna).
  - Liczba wyprostowanych palców.
- System umożliwia **śledzenie ruchów dłoni w czasie rzeczywistym** z minimalnym opóźnieniem.
