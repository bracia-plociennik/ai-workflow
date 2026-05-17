# 3.5. FAZA SPECYFIKACJI QA - Codex

Ta faza służy do krytycznej weryfikacji specyfikacji przed implementacją.

W normalnym workflow interaktywnym jest wymagana wtedy, gdy:

- użytkownik jawnie poprosi o `spec qa`, `qa specyfikacji`, `zweryfikuj specyfikację` albo równoważną komendę
- albo Codex wykryje blocking uncertainty / konflikt, którego nie wolno rozstrzygać przez implementację
- albo specyfikacja jest dependency-gated i została odświeżona po zakończeniu zależności

W autopilocie `3.5. SPEC QA` jest obowiązkowa przed każdą implementacją taska lub package. Autopilot nie może przejść z fazy 3 do fazy 4 bez Spec QA PASS.

Celem nie jest potwierdzenie poprawności.
Celem jest znalezienie błędów, luk i sprzeczności, które mogą spowodować rework lub błędną implementację.

## Warunek wejścia do tej fazy

Istnieje artefakt `docs/projects/<what_we_doing>/specs/3_<task_or_package_name>_specification.md`

Artefakt ten może być:

- nowo utworzony w fazie 3
- albo wcześniej istniejący i zaktualizowany w fazie 3
- jeśli wejście do `3.5. SPEC QA` następuje bezpośrednio po zaakceptowanym `/plan`, ale artefakt nie został jeszcze zapisany, najpierw trzeba zapisać go jako kopię 1:1 planu z `/plan`, a dopiero potem rozpocząć QA

## Zakres fazy

Faza obejmuje:

- zgodność specyfikacji z architekturą
- zgodność specyfikacji z planem projektu
- kompletność Implementation Gate (faza 3)
- poprawność logiczną specyfikacji
- wykrycie konfliktów, zależności i redundancji

## Out-of-scope

Faza nie obejmuje:

- zmiany specyfikacji
- rozszerzania scope
- proponowania nowych rozwiązań poza wykrytymi problemami

## Tryby działania

Faza działa w dwóch trybach:

### Tryb task

- standardowa walidacja specyfikacji pojedynczego taska

### Tryb package

Dodatkowo obowiązuje:

- pełne pokrycie wszystkich tasków w paczce
- brak zależności wewnętrznych (twardy warunek)
- brak konfliktów zakresu i odpowiedzialności
- brak ukrytego scope creep

Jeśli wykryta zostanie zależność wewnętrzna:

- FAIL
- powrót do fazy 2.7. lub 2.9.

## Reguła krytycznych błędów

PASS jest możliwy tylko jeśli:

- brak błędów krytycznych

Błędy krytyczne to:

- brak testów (twardy FAIL)
- naruszenie architektury
- naruszenie planu projektu
- ukryte zależności w package
- brak pokrycia zakresu
- brak Implementation Gate lub jego niepoprawność
- obecność blocking uncertainties bez decyzji

## Reguła warningów

Warningi:

- nie blokują PASS
- muszą być jawnie wypisane

## Walidacja kompletności specyfikacji

Specyfikacja musi zawierać:

- kroki implementacji
- potencjalne błędy
- edge cases (z oznaczeniem)
- testy (obowiązkowe)
- decyzje użytkownika (jeśli wymagane)
- założenia (jeśli istnieją)
- klasyfikację uncertainties

Brak któregokolwiek elementu:

- FAIL

## Walidacja Implementation Gate

QA musi sprawdzić:

- czy warunki startu są poprawnie ocenione
- czy blocking uncertainties są jawnie wskazane
- czy decyzja „może przejść do implementacji” jest uzasadniona

## Walidacja zgodności z architekturą

Sprawdź:

- czy spec nie łamie granic systemu
- czy nie wprowadza niezatwierdzonych zmian architektonicznych
- czy jest zgodna z decyzjami architektonicznymi

## Walidacja zgodności z planem projektu

Sprawdź:

- czy spec nie rozszerza scope
- czy nie pomija elementów planu
- czy nie dodaje ukrytych tasków

## Walidacja package (jeśli dotyczy)

Sprawdź:

- czy wszystkie taski są objęte specyfikacją
- czy nie ma zależności wewnętrznych (twardy warunek)
- czy nie ma konfliktów zakresu
- czy nie ma ukrytego scope creep

## Detekcja niespójności

Sprawdź:

- sprzeczne decyzje
- sprzeczne założenia
- duplikaty kroków
- niespójne testy

## Output fazy

Output musi zawierać:

- wynik: PASS / FAIL
- lista problemów:
  - błędy krytyczne
  - warningi

## Reguła FAIL → powrót

Jeśli wynik to FAIL:

- wróć do fazy 3
- popraw tylko wskazane problemy
- nie zmieniaj nic poza zakresem błędów

## Prompt bazowy

Prompt powinien brzmieć mniej więcej tak:

```json
Zweryfikuj specyfikację zadania / paczki zadań.

Warunek wejścia do tej fazy:
- istnieje artefakt `docs/projects/<what_we_doing>/specs/3_<task_or_package_name>_specification.md`

Sprawdź:
- zgodność z architekturą
- zgodność z planem projektu
- kompletność Implementation Gate
- obecność wszystkich wymaganych sekcji
- poprawność logiczną
- konflikty, zależności i redundancję

Jeśli pracujesz na package:
- sprawdź brak zależności wewnętrznych (twardy warunek)
- sprawdź pełne pokrycie paczki
- sprawdź brak konfliktów i scope creep

Zastosuj reguły:

FAIL jeśli:
- brak testów
- naruszenie architektury
- naruszenie planu
- ukryte zależności
- brak completeness
- blocking uncertainties bez decyzji

Na końcu zwróć:

- wynik: PASS / FAIL
- lista problemów:
  - błędy krytyczne
  - warningi
- lista decyzji, które użytkownik musi podjąć osobiście (zaproponuj do każdej decyzji po 1 rekomendacji + wpływ rekomendacji oraz 1 alternatywie + wpływ alterantywy)

DoD fazy:
	•	istnieje decyzja PASS / FAIL
	•	istnieje lista problemów
	•	brak false PASS
```

---
