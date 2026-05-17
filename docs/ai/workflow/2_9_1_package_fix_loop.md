# 2.9.1. FAZA PACKAGE FIX LOOP - ChatGPT

Ta faza służy do naprawy problemów wykrytych w fazie 2.9. FAZA TASK PACKAGING QA.

Celem nie jest stworzenie nowego packagingu od zera.
Celem jest poprawienie dokładnie tych błędów, braków, niespójności i ryzyk, które zostały wykryte przez Packaging QA, tak aby paczka tasków mogła przejść gate.

## Warunek wejścia do tej fazy

Do tej fazy przechodzimy tylko wtedy, gdy:

- faza 2.9 zakończyła się wynikiem FAIL
- istnieje raport z 2.9 zawierający listę problemów
- istnieje sekcja `Tasks package` w artefakcie:
  `docs/projects/<what_we_doing>/planning/2_project_plan.md`

Brak wyniku FAIL albo brak raportu z 2.9:

- blokuje 2.9.1
- uniemożliwia wykonanie fixu packagingu

## Zasada ogólna

2.9.1 działa jako:

- faza naprawcza po FAIL z 2.9
- poprawa tylko wskazanych problemów
- przygotowanie packagingu do ponownej walidacji w 2.9

ChatGPT nie może:

- rozszerzać scope poza problemy wskazane przez 2.9
- przepisywać całego packagingu od zera, jeśli nie jest to konieczne
- wykonywać optymalizacji ani zmian „przy okazji”
- przechodzić dalej bez ponownego QA

## Zakres fixu

Fix może obejmować wyłącznie:

- błędny podział na paczki
- niepoprawne granice paczek
- zależności wewnętrzne między paczkami (naruszenie zasad)
- konflikty zakresu i odpowiedzialności
- brak zgodności z architekturą lub planem projektu
- brak zgodności z outputem Packaging QA
- brakujące taski w paczkach
- błędne przypisanie tasków do paczek
- brakujące lub błędne Definition of Done
- aktualizację sekcji `Tasks package` w `docs/projects/<what_we_doing>/planning/2_project_plan.md`

Fix nie może obejmować:

- nowych tasków spoza planu
- zmiany scope projektu
- zmian architektury (chyba że wymagane do naprawy FAIL → STOP)
- refactoru packagingu „dla porządku”
- zmian w innych fazach

## Obsługa decyzji użytkownika

Jeśli fix wymaga decyzji użytkownika:

- decyzja musi być jawnie wskazana
- należy wskazać:
  - co trzeba rozstrzygnąć
  - dlaczego blokuje PASS
  - 1 rekomendację
  - 1 sensowną alternatywę

Brak decyzji blokującej:

- oznaczyć jako blocker
- nie wolno uznać packagingu za gotowy

## Reguła scope control

Jeśli w trakcie fixu okaże się, że naprawa wymaga:

- zmiany architektury
- zmiany planu projektu
- zmiany scope

wtedy:

- 2.9.1 kończy się STOP
- wskazać właściwą fazę powrotu (1.x lub 2.x)

## Retry limit

- low-risk: 1 retry
- medium-risk: 2 retry
- high-risk: 2 retry

Po przekroczeniu limitu:

- STOP
- wskazać potrzebę decyzji lub powrotu

## Retry count

Output musi zawierać:

- aktualny retry count
- maksymalny retry count
- czy limit został osiągnięty

## Output fazy

ChatGPT musi zwrócić:

- które problemy z raportu 2.9 naprawiono
- których nie naprawiono
- dlaczego
- decyzje użytkownika uwzględnione
- decyzje nadal potrzebne
- retry count
- limit retry
- czy można wrócić do 2.9
- czy fix ujawnił problem poza zakresem 2.9.1
- potwierdzenie aktualizacji sekcji `Tasks package` w `docs/projects/<what_we_doing>/planning/2_project_plan.md`

## Reguła PASS tej fazy

Faza 2.9.1 nie nadaje końcowego PASS.

Możliwe wyniki:

- fix wykonany i gotowy do ponownego QA w 2.9
- STOP (scope / architektura / plan)
- STOP (limit retry)

## Reguła przejścia dalej

Po 2.9.1 możliwe są tylko:

- powrót do 2.9
- STOP

Nie wolno:

- przechodzić dalej do implementacji

## Prompt bazowy

```json
Napraw tylko błędy wykryte w fazie 2.9. FAZA TASK PACKAGING QA.

Wejście:
- raport z 2.9 z wynikiem FAIL
- aktualny task packaging, sekcja `Tasks package` z `docs/projects/<what_we_doing>/planning/2_project_plan.md`
- retry count
- poziom ryzyka
- decyzje użytkownika

Zasady:
- popraw tylko błędy wpływające na Packaging Gate
- nie rozszerzaj scope
- nie poprawiaj warningów
- nie wykonuj optymalizacji
- jeśli potrzebna zmiana architektury lub planu:
  - STOP
- po fixie wróć do 2.9
- raportuj retry count

Na końcu zwróć:
- które błędy naprawiono
- których nie
- dlaczego
- decyzje użytkownika
- retry count
- limit retry
- czy można wrócić do 2.9

DoD:
- tylko fix błędów z QA
- brak rozszerzenia scope
- jawny retry count
```

---
