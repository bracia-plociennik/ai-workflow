# 3.7. FAZA SPEC FIX LOOP - Codex

Ta faza służy do naprawy problemów wykrytych w fazie 3.5. FAZA SPECYFIKACJI QA.

Celem nie jest stworzenie nowej specyfikacji od zera.
Celem jest poprawienie dokładnie tych błędów, braków, niespójności i ryzyk, które zostały wykryte przez QA, tak aby specyfikacja mogła przejść gate.

## Warunek wejścia do tej fazy

Do tej fazy przechodzimy tylko wtedy, gdy:

- faza 3.5 zakończyła się wynikiem FAIL
- istnieje raport QA z listą problemów
- istnieje aktualna specyfikacja taska / paczki

Brak FAIL albo brak raportu:

- blokuje 3.7

## Zasada ogólna

3.7 działa jako:

- faza naprawcza po FAIL z 3.5
- poprawa tylko wskazanych problemów
- przygotowanie specyfikacji do ponownego QA

Codex nie może:

- rozszerzać scope
- przepisywać całej specyfikacji bez potrzeby
- wykonywać optymalizacji ani zmian „przy okazji”
- przechodzić dalej bez QA

## Zakres fixu

Fix może obejmować wyłącznie:

- brakujące lub niejednoznaczne kroki implementacji
- brakujące testy
- brakujące edge cases
- niespójności logiczne
- błędy w Definition of Done
- brak oznaczeń niepewności (blocking / non-blocking)
- brak decyzji użytkownika
- aktualizacja artefaktu `docs/projects/<what_we_doing>/specs/3_<task_or_package_name>_specification.md`
- uzupełnienie wcześniej istniejącego artefaktu specyfikacji bez przepisywania go od zera

Fix nie może obejmować:

- zmiany scope
- zmian architektury
- zmian planu projektu
- refactoru specyfikacji „dla jakości”

## Obsługa decyzji użytkownika

Jeśli fix wymaga decyzji:

- wskazać ją jawnie
- podać:
  - problem
  - wpływ na PASS
  - rekomendację
  - alternatywę

Brak decyzji blokującej:

- oznaczyć jako blocking
- nie wolno uznać specyfikacji za gotową

## Reguła scope control

Jeśli naprawa wymaga:

- zmiany architektury
- zmiany planu
- zmiany scope

wtedy:

- STOP
- wskazać powrót do właściwej fazy

## Retry limit

- low-risk: 1 retry
- medium-risk: 2 retry
- high-risk: 2 retry

Po przekroczeniu limitu:

- STOP

## Retry count

Output musi zawierać:

- retry count
- limit retry
- status limitu

## Output fazy

Codex musi zwrócić:

- które błędy naprawiono
- których nie
- dlaczego
- decyzje użytkownika
- brakujące decyzje
- retry count
- limit retry
- czy można wrócić do 3.5
- czy pojawił się problem poza zakresem
- potwierdzenie aktualizacji artefaktu `docs/projects/<what_we_doing>/specs/3_<task_or_package_name>_specification.md`

## Reguła PASS tej fazy

Faza 3.7 nie nadaje PASS.

Możliwe wyniki:

- gotowe do ponownego QA
- STOP (scope / architektura / plan)
- STOP (limit retry)

## Reguła przejścia dalej

Po 3.7 możliwe są tylko:

- powrót do 3.5
- STOP

## Prompt bazowy

```json
Napraw tylko błędy wykryte w fazie 3.5.

Wejście:
- raport QA (FAIL)
- aktualna specyfikacja
- retry count
- poziom ryzyka
- decyzje użytkownika

Zasady:
- popraw tylko błędy krytyczne
- nie rozszerzaj scope
- nie poprawiaj warningów
- nie wykonuj optymalizacji
- jeśli potrzebna zmiana architektury lub planu:
  - STOP
- po fixie wróć do 3.5

Na końcu zwróć:
- które błędy naprawiono
- których nie
- dlaczego
- retry count
- limit retry
- czy można wrócić do QA
- potwierdzenie aktualizacji artefaktu `docs/projects/<what_we_doing>/specs/3_<task_or_package_name>_specification.md`

DoD:
- tylko fix błędów z QA
- brak rozszerzenia scope
- jawny retry count
```

---
