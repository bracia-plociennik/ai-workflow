# 5. FAZA JAKOŚCI - Codex

Ta faza służy do twardej walidacji, czy task / tasks package rzeczywiście spełnia warunki zakończenia.

Celem nie jest szukanie kolejnych ulepszeń.
Celem jest jednoznaczna odpowiedź, czy rozwiązanie przechodzi kontrolę jakości.

Wynik tej fazy musi być binarny:

- PASS
- FAIL

Nie używaj odpowiedzi typu:

- "raczej ok"
- "wygląda dobrze"
- "powinno działać"
- "w większości spełnia"

## Warunek wejścia do tej fazy

Do tej fazy przechodzimy po implementacji taska / tasks package i po wcześniejszej specyfikacji zadania / paczki zadań.

## Formalna definicja Quality Threshold

Task / tasks package przechodzi fazę jakości tylko wtedy, gdy łącznie spełnia wszystkie poniższe warunki:

- Definition of Done jest spełnione w 100%
- nie ma known bugs w zakresie taska / tasks package
- nie wykryto regresji w zakresie dotkniętym taskiem / paczką zadań i w bezpośrednich ścieżkach zależnych
- edge cases są:
  - pokryte
  - albo świadomie odrzucone z uzasadnieniem
- wynik PASS jest oparty na jawnych dowodach

Known limitations poza zakresem taska / tasks package:

- nie blokują PASS, jeśli są naprawdę poza zakresem
- nie naruszają nowego rozwiązania
- są jawnie oznaczone jako poza zakresem tego taska / tasks package

## Zasada dowodów jakości

PASS wymaga dowodu.

Codex nie może przyznać PASS wyłącznie na podstawie ogólnej oceny eksperckiej.

Dopuszczalne dowody:

- wykonane testy
- inspekcja kodu
- sprawdzone edge cases
- manual verification
- porównanie z Definition of Done
- porównanie z planem taska i wcześniejszą specyfikacją

Jeśli czegoś nie dało się zweryfikować:

- trzeba to jasno zaznaczyć
- brak istotnego dowodu oznacza FAIL

## Obowiązkowy zakres walidacji

Codex musi zawsze wykonać i zaraportować:

- walidację DoD
- check edge cases
- check regresji
- check zgodności z architekturą
- check known bugs

## **Zasada walidacji DoD**

DoD musi być sprawdzone 1:1 względem taska / tasks package.

Jeśli choć jeden element DoD nie został spełniony:

- wynik końcowy = FAIL

Nie traktuj częściowego spełnienia jako PASS.

## **Zasada edge cases**

Codex musi sprawdzić:

- czy edge cases z fazy specyfikacji zostały rzeczywiście obsłużone albo świadomie odrzucone
- czy podczas implementacji pojawiły się nowe istotne edge cases

Jeśli nowy istotny edge case pojawił się po implementacji i nie został oceniony:

- wynik = FAIL

## **Zasada regresji**

Check regresji obejmuje:

- zakres dotknięty taskiem / paczką zadań
- bezpośrednie ścieżki zależne

Nie rozszerzaj checku regresji na cały repo bez powodu.

Regresja oznacza:

- złamanie istniejącego zachowania w obszarze dotkniętym zmianą
- złamanie bezpośrednio zależnych ścieżek, które task mógł naruszyć
- pogorszenie kontraktu komponentu, API, przepływu danych lub UI, jeśli były objęte zakresem

## **Zasada known bugs**

Jeśli istnieje known bug w zakresie taska / tasks package:

- wynik = FAIL

Jeśli istnieje limitation poza zakresem taska / paczki zadań:

- nie blokuje PASS, jeśli:
  - jest naprawdę poza zakresem
  - nie narusza nowego rozwiązania
  - została jawnie oznaczona

## **Zasada zgodności z architekturą**

Codex musi sprawdzić zgodność rozwiązania z architekturą i planem taska / tasks package.

Jeśli rozwiązanie odbiega od architektury:

- nie blokuje to automatycznie PASS
- ale musi zostać oznaczone jako warning architektoniczny
- w takim przypadku:
  - zgodność z architekturą = PASS
  - oraz wymagane jest jawne wskazanie warningu architektonicznego w raporcie

Warning architektoniczny musi zawierać:

- na czym polega odejście
- czy wpływa na bieżący task / tasks package
- czy wymaga późniejszej decyzji lub korekty

Uwaga:

- warning architektoniczny nie może ukrywać znanego błędu, regresji ani niespełnionego DoD
- jeśli odejście od architektury powoduje known bug, regresję albo niespełnienie DoD, wynik = FAIL

## **Struktura raportu jakości**

Raport końcowy powinien zawierać:

- wynik końcowy: PASS / FAIL
- DoD: PASS / FAIL
- edge cases: PASS / FAIL
- regresja: PASS / FAIL
- zgodność z architekturą: PASS / FAIL (PASS oznacza zgodność lub kontrolowane odchylenie oznaczone jako warning; FAIL oznacza niezgodność wpływającą na DoD, regresję lub correctness)
- known bugs: PASS / FAIL
- dowody jakości
- known bugs lub none
- known limitations poza zakresem lub none
- warningi architektoniczne lub none
- decyzja końcowa:
  - task / tasks package może przejść do destylacji
  - task / tasks package nie może przejść do destylacji

## **Reguła przejścia do destylacji**

Tylko task / tasks package z wynikiem końcowym PASS może przejść do finalnej destylacji jako task / tasks package zakończony.

Jeśli wynik = FAIL:

- task / tasks package nie jest uznany za zamknięty
- task / tasks package nie przechodzi do finalnej destylacji
- można zapisać roboczą notatkę o przyczynie FAIL, ale nie finalną destylację zamkniętego zadania / paczki zadań

## Prompt bazowy

Prompt po implementacji powinien brzmieć mniej więcej tak:

```json
Sprawdź, czy task / tasks package przechodzi fazę jakości.

Wykonaj obowiązkowo:
- walidację Definition of Done
- check edge cases
- check regresji
- check zgodności z architekturą
- check known bugs

Zastosuj formalny Quality Threshold:
- DoD spełnione w 100%
- brak known bugs w zakresie taska / tasks package
- brak regresji w zakresie dotkniętym taskiem / paczką zadań i bezpośrednich ścieżkach zależnych
- edge cases pokryte lub świadomie odrzucone z uzasadnieniem
- wynik PASS oparty na jawnych dowodach

Known limitations poza zakresem taska / tasks package:
- nie blokują PASS, jeśli są naprawdę poza zakresem i nie naruszają nowego rozwiązania

Na końcu zwróć raport w formie:
- wynik końcowy: PASS / FAIL
- DoD: PASS / FAIL
- edge cases: PASS / FAIL
- regresja: PASS / FAIL
- zgodność z architekturą: PASS / FAIL (PASS oznacza zgodność lub kontrolowane odchylenie oznaczone jako warning; FAIL oznacza niezgodność wpływającą na DoD, regresję lub correctness)
- known bugs: PASS / FAIL
- dowody jakości
- known bugs lub none
- known limitations poza zakresem lub none
- warningi architektoniczne lub none
- decyzja końcowa: czy task / tasks package może przejść do destylacji

Jeśli rozwiązanie przechodzi Quality Threshold:
- zwróć PASS
- nie proponuj dalszych ulepszeń

Jeśli nie przechodzi:
- zwróć FAIL
- wskaż dokładnie, co nie przeszło
```

---
