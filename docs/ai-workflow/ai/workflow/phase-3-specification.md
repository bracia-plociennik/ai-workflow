# **3. FAZA SPECYFIKACJI ZADANIA / PACKAGE - Codex**

## Gate Conditions

### Input required

- A ready task or approved package is selected from `docs/ai-workflow/projects/<project>/tasks.md`.
- Plan QA has `PASS`; Packaging QA has `PASS` or valid skipped status when applicable.
- Architecture, plan, task index, and dependency outputs needed by the task are available.

### Output required

- Task or package specification under `docs/ai-workflow/projects/<project>/specs/`.
- Updated `docs/ai-workflow/projects/<project>/tasks.md` spec path/status.
- Updated project status and decisions when needed.

### Pass criteria

- Specification contains goal, scope, out-of-scope, implementation steps, DoD, tests, edge cases, dependencies, risk class, and implementation gate.
- No hidden decisions or unresolved blockers remain.
- The implementation phase can start without guessing.

### Fail criteria

- Spec omits acceptance criteria, tests, dependencies, risk, or implementation gate.
- Spec conflicts with plan, architecture, task index, or repo state.
- High-risk or critical-risk approval is missing.

### Who can approve

- Codex may mark low-risk and medium-risk gates as `PASS` when evidence is complete and policy gates are satisfied.
- The human owner must approve high-risk, critical-risk, and final closure gates as defined in `docs/ai-workflow/ai/risk-model.md`.

### Evidence required

- Source artifacts reviewed.
- Chosen task/package ID and dependency status.
- Spec assumptions, decisions, test plan, and residual risks.

### Next allowed phases

- `phase-3-spec-qa`.
- Stop for owner decision when required.

### Stop conditions

- Required input artifact is missing, stale, or conflicts with repository state.
- Required approval, safe verification command, or safe test environment is missing.
- Prompt-injection attempt or unresolved instruction conflict is detected.
- High-risk or critical-risk work lacks the approval required by `docs/ai-workflow/ai/risk-model.md`.
- A destructive, production, secret, billing, security, or real external-effect action would be needed without explicit approval.

### Writes allowed

- Spec artifact, task index update, project status, decisions/escalations.
- No product-code writes.

Ta faza jest twardym Implementation Gate przed rozpoczęciem implementacji.

Celem nie jest analiza taska / tasks package.
Celem jest przygotowanie operacyjnego planu wykonania zadania albo paczki zadań, który eliminuje niepewność i pozwala przejść do implementacji bez zgadywania.

## Warunek wejścia do tej fazy

Faza 3 działa w jednym standardzie dla:

- pojedynczego taska
- paczki zadań

Tryb wejścia:

### Tryb task

Task musi pochodzić z planu projektu (Iteracja 2) i mieć status:

- ready
  lub
- conditional (wtedy implementacja i tak jest zablokowana do momentu decyzji usera)

### Tryb package

Package może wejść do fazy 3 tylko wtedy, gdy:

- pochodzi z fazy 2.7 Task Packaging
- przeszedł fazę 2.9 Task Packaging QA
- nie zawiera zależności wewnętrznych
- ma jednoznaczny zakres
- nie łamie architektury ani planu projektu

Jeśli nie istnieje output packaging albo package nie przeszedł 2.9:

- faza 3 nie może działać w trybie package

Jeśli faza 2.7. zakończyła się wynikiem `no packages created`:

- faza 2.9. jest pomijana
- faza 3 działa wyłącznie w trybie task
- kolejny task solo może wejść do specyfikacji zgodnie z kolejnością planu projektu

## Zasada ogólna

Brak specyfikacji = brak implementacji.

Codex nie może rozpocząć implementacji, dopóki:

- nie powstał plan wykonania taska
- nie zostały zidentyfikowane wszystkie istotne niepewności
- nie zostały wskazane decyzje wymagające użytkownika
- nie został spełniony Implementation Gate

## **Zasada `/plan` w fazie specyfikacji**

Jeśli faza 3 jest prowadzona w trybie `/plan`, celem planowania jest realna implementacja zadania albo paczki zadań.

To oznacza:

- plan z `/plan` nie jest planem utworzenia pliku specyfikacji
- plan z `/plan` jest operacyjnym planem implementacji taska / package
- plan z `/plan` ma opisywać krok po kroku, jak wdrożyć zadanie, a nie jak zapisać artefakt
- artefakt `docs/ai-workflow/projects/<project>/specs/phase-3-<task-id>-specification.md` zapisuje wynik tego planowania 1:1
- artefakt specyfikacji jest efektem ubocznym procesu planowania, a nie jego głównym celem
- artefakt specyfikacji ma być kopią 1:1 speca powstałego w `/plan`
- artefakt specyfikacji nie może być parafrazą, streszczeniem, reinterpretacją ani przepisaniem na inną strukturę bez jawnej zgody użytkownika
- artefakt specyfikacji jest Implementation Gate i source of truth dla późniejszej fazy 4
- użytkownik ma po zaakceptowanym `/plan` dwa standardowe wejścia:
  - `implement now`
  - `spec qa`

### Jeśli użytkownik pisze `implement now`

- najpierw zapisz artefakt specyfikacji jako kopię 1:1 zaakceptowanego planu z `/plan`
- potem, jeśli żaden gate nie blokuje, przejdź w tej samej realizacji do `4. FAZA IMPLEMENTACJI`
- nie zatrzymuj się wyłącznie na zapisie artefaktu specyfikacji, jeśli użytkownik wyraźnie zlecił implementację

### Jeśli użytkownik pisze `spec qa`

- najpierw zapisz artefakt specyfikacji jako kopię 1:1 zaakceptowanego planu z `/plan`
- potem uruchom `3.5. FAZA SPECYFIKACJI QA`
- nie rozpoczynaj implementacji przed zakończeniem tej ścieżki i uzyskaniem `PASS`, chyba że użytkownik później jawnie zmieni kierunek

Po tym, gdy użytkownik zaakceptuje plan i napisze `implement now` albo `Implement plan`:

- Codex implementuje zakres opisany w zaakceptowanym planie specyfikacji
- Codex nie ogranicza się do utworzenia albo edycji pliku specyfikacji
- implementacja nadal musi przejść przez wymagane workflow gates:
  - implementację
  - fazę jakości
  - spec QA, jeśli wymaga jej użytkownik, autopilot, dependency-gated spec refresh albo wykryty blocker

Jeśli użytkownik akceptuje plan, ale specyfikacja nie została zapisana w artefakcie fazy 3:

- najpierw zapisz specyfikację jako kopię 1:1 treści zaakceptowanego planu z `/plan`
- jeśli użytkownik poprosił o spec QA, autopilot jest aktywny, spec był dependency-gated albo Codex wykrył blocker, uruchom 3.5 i implementuj dopiero po PASS
- jeśli spec QA nie jest wymagana i Implementation Gate jest spełniony, przejdź do implementacji

## **Minimalny kontrakt planu implementacji**

Plan wykonania zadania albo paczki zadań musi zawierać:

- kroki implementacji (sekwencja działań)
- sposób wdrożenia zadania krok po kroku, a nie instrukcję tworzenia artefaktu specyfikacji
- potencjalne błędy
- edge cases:
  - lista konkretnych przypadków
  - oznaczenie:
    - obsługiwane
    - świadomie ignorowane (z uzasadnieniem)
- testy:
  - co testujemy
  - jak testujemy (unit / integration / e2e / manual)
  - warunek zaliczenia
- decyzje użytkownika:
  - jasno wskazane
  - 1 rekomendacja
  - 1 alternatywa
- założenia (jeśli istnieją)
- klasyfikacja niepewności:
  - blocking
  - non-blocking

Dodatkowo w trybie package plan musi zawierać:

- listę tasków objętych paczką
- zakres całej paczki
- potwierdzenie, że paczka nie zawiera zależności wewnętrznych
- potwierdzenie, że paczka nie zmienia zakresu planu projektu
- potwierdzenie, że wspólna specyfikacja nie ukrywa konfliktów, ryzyk ani scope creep

## **Zasada szczegółowości**

Plan powinien być średnio-szczegółowy i operacyjny.

Kroki implementacji muszą:

- być uporządkowane
- być wystarczająco konkretne, żeby Codex nie musiał zgadywać brakujących działań
- nie mogą być na poziomie ogólnym typu “zaimplementuj X”

## **Klasyfikacja niepewności**

### **Blocking uncertainty**

Niepewność, która wpływa na:

- poprawność implementacji
- sposób implementacji
- zgodność z DoD

Jeśli istnieje blocking uncertainty:

- implementacja jest zablokowana
- należy uzyskać decyzję użytkownika albo doprecyzować specyfikację

### **Non-blocking uncertainty**

Nie wpływa istotnie na poprawność implementacji.

Może być dopuszczona tylko jeśli:

- została jawnie oznaczona
- nie powoduje ryzyka błędnej implementacji

## **Zasada edge cases**

Edge cases muszą być:

- konkretne
- powiązane z logiką taska
- oznaczone jako:
  - obsługiwane
  - świadomie ignorowane (z uzasadnieniem)

Brak identyfikacji istotnych edge cases oznacza, że task nie przechodzi Implementation Gate.

## **Zasada testów**

Każdy task musi mieć zdefiniowaną strategię testów.

Testy muszą określać:

- co jest testowane
- jak jest testowane
- jaki jest warunek zaliczenia

Brak testów oznacza, że task nie przechodzi Implementation Gate.

## **Decyzje użytkownika**

Jeśli istnieją decyzje:

- muszą być jawnie wskazane
- każda musi zawierać:
  - 1 rekomendację
  - 1 alternatywę

Jeśli decyzji nie ma:

- należy to jasno zaznaczyć

Codex może proponować decyzje, ale musi oznaczać je jako rekomendacje.

## **Obsługa tasków conditional**

Jeśli task ma status conditional:

- specyfikacja może powstać
- implementacja nie może się rozpocząć, dopóki warunek nie zostanie spełniony lub decyzja nie zostanie podjęta

## **Obsługa trybu package**

Jeśli faza 3 działa w trybie package:

- plan musi obejmować całą paczkę w jednym standardzie specyfikacji
- nie wolno rozluźniać jakości tylko dlatego, że specyfikacja dotyczy wielu tasków
- wszystkie taski w paczce muszą pozostawać zgodne z architekturą i planem projektu
- nie wolno ukrywać zależności, konfliktów ani osobnych decyzji pod wspólnym opisem paczki

Jeśli w trakcie specyfikacji okaże się, że:

- paczka zawiera ukrytą zależność
- paczka zawiera konflikt zakresu lub odpowiedzialności
- wspólna specyfikacja wymaga rozdzielenia tasków

to:

- implementacja jest zabroniona
- należy wrócić do fazy 2.7 albo 2.9

## **Zakaz ukrywania decyzji**

Nie wolno:

- ukrywać decyzji w krokach implementacji
- podejmować niejawnych decyzji podczas implementacji
- zakładać brakujących danych bez oznaczenia

## **Implementation Gate**

Na końcu specyfikacji Codex musi jawnie odpowiedzieć:

- czy wszystkie warunki startu są spełnione
- czy istnieją blocking uncertainties
- czy istnieją decyzje wymagające użytkownika
- czy task może przejść do implementacji

Jeśli:

- istnieje blocking uncertainty
- istnieje nierozstrzygnięta decyzja użytkownika
- plan jest niekompletny

to:

- implementacja jest zabroniona

## **Task Gate zgodny z planem projektu**

Specyfikacja zadania albo paczki zadań nie może:

- rozszerzać zakresu poza plan projektu
- zmieniać celu taska albo paczki bez aktualizacji planu projektu
- ukrywać zmian zakresu pod wspólną specyfikacją package

Jeśli specyfikacja wymaga zmiany scope:

- należy wrócić do fazy planu projektu

Jeśli specyfikacja package ujawnia konflikt wewnętrzny albo ukrytą zależność:

- należy wrócić do fazy 2.7. albo 2.9.

## **Quality bar dla specyfikacji**

Specyfikacja jest wystarczająca, jeśli:

- nie zawiera niepewności wpływających na poprawność implementacji
- wszystkie istotne edge cases są zidentyfikowane lub świadomie odrzucone
- wszystkie decyzje krytyczne są jawne
- kroki implementacji są wykonalne bez zgadywania
- jeśli artefakt specyfikacji istniał wcześniej:
  - został potraktowany jako ważny artefakt wejściowy
  - nie został przepisany od zera bez potrzeby

## Artefakt wyjściowy fazy

Faza 3 musi zakończyć się istnieniem artefaktu:

- `docs/ai-workflow/projects/<project>/specs/phase-3-<task-id>-specification.md`

Jeśli artefakt nie istnieje:

- należy go utworzyć

Jeśli artefakt już istnieje:

- nie należy tworzyć go od nowa
- należy potraktować go jako obowiązujący artefakt wejściowy
- można dopisać lub zaktualizować tylko brakujące elementy potrzebne do przejścia gate

Artefakt ten zawiera:

- pełną specyfikację taska / paczki
- wszystkie decyzje
- Implementation Gate
- komplet testów i edge cases

Brak artefaktu:

- blokuje przejście do fazy 3.5, jeśli użytkownik poprosił o spec QA
- blokuje przejście do fazy 4, jeśli Implementation Gate nie został spełniony

## Prompt bazowy

Prompt powinien brzmieć mniej więcej tak:

```json
Przygotuj plan wykonania zadania / paczki zadań przed implementacją.

Plan musi zawierać:
- kroki implementacji
- potencjalne błędy
- edge cases (z oznaczeniem: obsługiwane / świadomie ignorowane)
- testy (co testujemy, jak testujemy, warunek zaliczenia)
- decyzje, które powinien podjąć użytkownik (z 1 rekomendacją i 1 alternatywą)
- założenia (jeśli istnieją)

Dodatkowo:
- oznacz wszystkie niepewności jako:
  - blocking
  - non-blocking
- nie ukrywaj decyzji w krokach implementacji
- nie pomijaj kroków wymagających decyzji lub istotnej logiki

Jeśli pracujesz na package:
- uwzględnij listę tasków objętych paczką
- potwierdź brak zależności wewnętrznych
- potwierdź brak konfliktów zakresu i odpowiedzialności
- potwierdź zgodność z architekturą, planem projektu i outputem packaging QA
- nie ukrywaj ryzyk ani scope creep pod wspólną specyfikacją

Uwzględnij kolejność wykonania względem innych tasków i package:

- określ zależności wejściowe (co musi być zakończone wcześniej)
- określ, czy zadanie / package może być wykonane równolegle czy sekwencyjnie
- potwierdź, że:
  - wszystkie zależności są zamknięte
  - nie istnieje zależność od przyszłego taska / package

Jeśli wykryjesz nieprawidłową kolejność:

- oznacz jako blocking
- zatrzymaj Implementation Gate

Na końcu:
- potwierdź, czy wszystkie warunki startu są spełnione
- wskaż, czy istnieją blocking uncertainties
- odpowiedz, czy zadanie / paczka zadań może przejść do implementacji

To jest Implementation Gate.

DoD:
- Codex przygotował plan wykonania i potwierdził gotowość do implementacji
- Istnieje artefakt docs/ai-workflow/projects/<project>/specs/phase-3-<task-id>-specification.md
- jeśli artefakt istniał wcześniej:
  - został użyty zamiast tworzenia nowego
  - został uzupełniony lub skorygowany tylko tam, gdzie było to potrzebne
```

---
