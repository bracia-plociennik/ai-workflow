# 1.7. ARCHITECTURE FIX LOOP - Codex

Ta faza służy do naprawy problemów wykrytych w fazie 1.5. FAZA ARCHITEKTURY QA.

Celem nie jest stworzenie nowej architektury od zera.
Celem jest poprawienie dokładnie tych luk, ryzyk, sprzeczności i błędów, które zostały wykryte przez Architecture QA, tak aby architektura mogła ponownie przejść przez gate.

## Warunek wejścia do tej fazy

Do tej fazy przechodzimy tylko wtedy, gdy:

- faza 1.5 zakończyła się wynikiem FAIL
- istnieje raport z 1.5 zawierający listę problemów
- istnieje artefakt:
  `docs/projects/<what_we_doing>/architecture/1_architecture_phase.md`

Brak wyniku FAIL albo brak raportu z 1.5:

- blokuje 1.7.
- uniemożliwia wykonanie fixu architektury

## Zasada ogólna

1.7. działa jako:

- faza naprawcza po FAIL z 1.5
- poprawa tylko wskazanych problemów
- przygotowanie architektury do ponownej walidacji w 1.5

Codex nie może:

- rozszerzać scope poza problemy wskazane przez 1.5
- przepisywać całej architektury od zera, jeśli nie jest to konieczne do naprawy wskazanych błędów
- wykonywać optymalizacji ani uproszczeń „przy okazji”, jeśli nie wynikają bezpośrednio z FAIL
- przechodzić dalej bez ponownego QA

## Zakres fixu

Fix może obejmować wyłącznie:

- luki wykryte przez 1.5
- sprzeczności wykryte przez 1.5
- błędną klasyfikację unknowns
- ryzyka bez decyzji / ownera / warunku domknięcia
- brakujące elementy wymagane przez Architecture Gate
- decyzje użytkownika potrzebne do domknięcia architektury

Fix nie może obejmować:

- nowych elementów architektury niezwiązanych z FAIL
- rozszerzenia systemu poza aktualny zakres zmiany
- refactoru architektury „dla porządku”
- zmian planu projektu
- zmian w fazach dalszych niż 1.5, jeśli nie wynikają bezpośrednio z naprawy architektury

## Obsługa decyzji użytkownika

Jeśli naprawa architektury wymaga decyzji użytkownika:

- decyzja musi być jawnie wskazana
- należy wskazać:
  - co trzeba rozstrzygnąć
  - dlaczego blokuje PASS
  - 1 rekomendację
  - 1 sensowną alternatywę

Jeśli decyzja użytkownika nie została jeszcze podjęta, a wpływa na Architecture Gate:

- fix loop nie może uznać architektury za gotową
- należy to oznaczyć jako blocker do ponownego 1.5

## Reguła scope control

Jeśli w trakcie fixu okaże się, że naprawa wymaga:

- zmiany scope projektu
- zmiany założeń biznesowych
- zmiany granic systemu wykraczającej poza zakres FAIL
- powrotu do repo intake albo zmiany artefaktów wejściowych

wtedy:

- 1.7. kończy się STOP
- należy jawnie wskazać potrzebę powrotu do wcześniejszej właściwej fazy
- nie wolno ukrywać takiej zmiany jako zwykłego fixu architektury

## Retry limit

Fix loop ma ograniczony limit retry.

Limit zależy od ryzyka zmiany:

- low-risk:
  - 1 retry
- medium-risk:
  - 2 retry
- high-risk:
  - 2 retry

Po przekroczeniu limitu retry:

- nie uruchamiaj kolejnego automatycznego fixu
- wskaż potrzebę decyzji użytkownika albo powrotu do wcześniejszej fazy

## Retry count

Output fazy 1.7 musi jawnie zawierać:

- aktualny retry count
- maksymalny dopuszczalny retry count
- informację, czy limit został osiągnięty

## Output fazy

Codex musi zwrócić:

- które problemy z raportu 1.5 zostały naprawione
- których problemów nie naprawiono
- dlaczego nie zostały naprawione
- jakie decyzje użytkownika zostały uwzględnione
- jakie decyzje użytkownika są nadal potrzebne
- aktualny retry count
- maksymalny retry count
- czy limit retry został osiągnięty
- czy można wrócić do 1.5
- czy fix ujawnił problem wychodzący poza zakres 1.7.

## Reguła PASS tej fazy

Faza 1.7 sama nie nadaje końcowego PASS dla architektury.

Jedyny poprawny wynik tej fazy to:

- fix wykonany i gotowy do ponownego QA w 1.5
  albo
- STOP, jeśli naprawa wymaga wyjścia poza zakres 1.7.
  albo
- STOP, jeśli osiągnięto limit retry

## Reguła przejścia dalej

Po 1.7 możliwe są tylko trzy ścieżki:

- powrót do fazy 1.5. FAZA ARCHITEKTURY QA
- STOP z powodu scope escalation
- STOP z powodu osiągnięcia limitu retry

Nie wolno:

- przechodzić bezpośrednio do fazy 2. planu projektu
- poprawiać architektury poza zakresem błędów wykrytych w 1.5
- traktować 1.7 jako substytutu 1.5

## Prompt bazowy

Prompt powinien brzmieć mniej więcej tak:

```json
Napraw tylko błędy wykryte w fazie 1.5. FAZA ARCHITEKTURY QA.

Wejście:
- raport z 1.5 z wynikiem FAIL
- aktualna architektura
- aktualny retry count
- poziom ryzyka zmiany
- decyzje użytkownika, jeśli zostały już podjęte

Zasady:
- popraw tylko wskazane błędy krytyczne i luki wpływające na Architecture Gate
- nie rozszerzaj scope
- nie poprawiaj warningów, jeśli nie są częścią FAIL
- nie wykonuj optymalizacji ani refactoru „przy okazji”
- jeśli naprawa wymaga zmiany scope, założeń biznesowych albo wcześniejszej fazy:
  - zatrzymaj się
  - wskaż potrzebę powrotu do wcześniejszej fazy
- po zakończeniu fixu wróć do fazy 1.5
- jawnie podaj retry count i limit retry

Na końcu zwróć:
- które błędy naprawiono
- których nie naprawiono
- dlaczego
- jakie decyzje użytkownika uwzględniono
- jakie decyzje są nadal potrzebne
- retry count
- limit retry
- czy można wrócić do fazy 1.5
- czy fix ujawnił problem poza zakresem 1.7.

DoD fazy:
- poprawiono tylko błędy wskazane przez 1.5
- nie rozszerzono scope
- retry count został jawnie zaraportowany
- faza jest gotowa do ponownego QA albo jawnie zatrzymana
```

---
