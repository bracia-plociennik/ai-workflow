# 2.6. PLAN FIX LOOP - ChatGPT

Ta faza służy do naprawy problemów wykrytych w fazie 2.5. FAZA PLANU PROJEKTU QA.

Celem nie jest stworzenie nowego planu od zera.
Celem jest poprawienie dokładnie tych błędów, braków, niespójności i ryzyk, które zostały wykryte przez Plan QA, tak aby plan projektu mógł przejść gate.

## Warunek wejścia do tej fazy

Do tej fazy przechodzimy tylko wtedy, gdy:

- faza 2.5 zakończyła się wynikiem FAIL
- istnieje raport z 2.5 zawierający listę problemów
- istnieje artefakt:
  `docs/projects/<what_we_doing>/planning/2_project_plan.md`

Brak wyniku FAIL albo brak raportu z 2.5:

- blokuje 2.6.
- uniemożliwia wykonanie fixu planu

## Zasada ogólna

2.6. działa jako:

- faza naprawcza po FAIL z 2.5
- poprawa tylko wskazanych problemów
- przygotowanie planu do ponownej walidacji w 2.5

ChatGPT nie może:

- rozszerzać scope poza problemy wskazane przez 2.5
- przepisywać całego planu od zera, jeśli nie jest to konieczne do naprawy błędów
- wykonywać optymalizacji ani zmian „przy okazji”
- przechodzić dalej bez ponownego QA

## Zakres fixu

Fix może obejmować wyłącznie:

- braki w taskach
- błędny podział tasków
- niespójności między taskami
- błędne zależności
- brakujące dependency
- brak pokrycia wymagań z architektury
- błędy w Definition of Done
- błędną klasyfikację ryzyka tasków
- brakujące decyzje użytkownika

Fix nie może obejmować:

- nowych feature'ów
- zmiany scope projektu
- zmian architektury (chyba że są bezpośrednio wymagane do naprawy FAIL i wtedy STOP)
- refactoru planu „dla porządku”
- zmian w fazach innych niż plan projektu

## Obsługa decyzji użytkownika

Jeśli naprawa planu wymaga decyzji użytkownika:

- decyzja musi być jawnie wskazana
- należy wskazać:
  - co trzeba rozstrzygnąć
  - dlaczego blokuje PASS
  - 1 rekomendację
  - 1 sensowną alternatywę

Jeśli decyzja użytkownika nie została podjęta, a wpływa na Plan Gate:

- fix loop nie może uznać planu za gotowy
- należy to oznaczyć jako blocker

## Reguła scope control

Jeśli w trakcie fixu okaże się, że naprawa wymaga:

- zmiany architektury
- zmiany scope projektu
- powrotu do wcześniejszych faz

wtedy:

- 2.6. kończy się STOP
- należy wskazać właściwą fazę powrotu
- nie wolno ukrywać tego jako zwykłego fixu planu

## Retry limit

Fix loop ma ograniczony limit retry.

Limit zależy od ryzyka:

- low-risk:
  - 1 retry
- medium-risk:
  - 2 retry
- high-risk:
  - 2 retry

Po przekroczeniu limitu retry:

- zatrzymaj proces
- wskaż potrzebę decyzji użytkownika albo powrotu do wcześniejszej fazy

## Retry count

Output fazy 2.6 musi zawierać:

- aktualny retry count
- maksymalny retry count
- informację, czy limit został osiągnięty

## Output fazy

ChatGPT musi zwrócić:

- które problemy z raportu 2.5 zostały naprawione
- których problemów nie naprawiono
- dlaczego
- jakie decyzje użytkownika uwzględniono
- jakie decyzje są nadal potrzebne
- retry count
- limit retry
- czy można wrócić do 2.5
- czy fix ujawnił problem poza zakresem 2.6

## Reguła PASS tej fazy

Faza 2.6 nie nadaje końcowego PASS.

Możliwe wyniki:

- fix wykonany i gotowy do ponownego QA w 2.5
- STOP (scope / architektura)
- STOP (limit retry)

## Reguła przejścia dalej

Po 2.6 możliwe są tylko:

- powrót do 2.5
- STOP

Nie wolno:

- przechodzić dalej do implementacji
- zmieniać architektury bez powrotu do fazy 1

## Prompt bazowy

```json
Napraw tylko błędy wykryte w fazie 2.5. FAZA PLANU PROJEKTU QA.

Wejście:
- raport z 2.5 z wynikiem FAIL
- aktualny plan projektu
- retry count
- poziom ryzyka
- decyzje użytkownika

Zasady:
- popraw tylko błędy wpływające na Plan Gate
- nie rozszerzaj scope
- nie poprawiaj warningów
- nie wykonuj optymalizacji
- jeśli potrzebna zmiana architektury:
  - STOP
- po fixie wróć do 2.5
- raportuj retry count

Na końcu zwróć:
- które błędy naprawiono
- których nie
- dlaczego
- decyzje użytkownika
- retry count
- limit retry
- czy można wrócić do 2.5

DoD:
- tylko fix błędów z QA
- brak rozszerzenia scope
- jawny retry count
```

---
