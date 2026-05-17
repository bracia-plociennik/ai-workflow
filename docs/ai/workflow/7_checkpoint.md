# 7. CHECKPOINT PROJEKTU - Codex

Ta faza służy do synchronizacji stanu wiedzy projektowej, architektury i realnego stanu repo.

Celem nie jest mechaniczne scalanie notatek.
Celem jest:

- aktualizacja project memory i, jeśli trzeba, repo memory
- wykrycie driftu
- kompresja i deduplikacja wiedzy
- utrzymanie spójności między:
  - architekturą
  - implementacją
  - project memory
  - repo memory

## Zasada ogólna

Checkpoint jest obowiązkowym elementem utrzymania spójności projektu.

Checkpoint działa w dwóch trybach:

### 1. Checkpoint cykliczny

Powinien być wykonywany po każdych 3 taskach / paczkach zadań zakończonych wynikiem:

- PASS

### 2. Checkpoint warunkowy

Może zostać uruchomiony wcześniej, jeśli:

- pojawiła się ważna decyzja architektoniczna
- wykryto istotny drift
- zmienił się kierunek projektu
- powstało ryzyko utraty spójności między memory a repo

## Enforcement checkpointu

Po każdych 3 taskach / paczkach zadań zakończonych PASS Codex ma obowiązek przypomnieć o konieczności wykonania checkpointu.

Źródło prawdy dla licznika:

- licznik opiera się na liczbie plików X_task_or_package_name_distillation.md, które:
  - mają status taska / tasks package PASS
  - oraz memory_in_repo_memory: false
- każdy taki plik traktowany jest jako jeden zakończony task / tasks package wymagający checkpointu

Reguła:

- jeśli liczba takich plików >= 3 → Codex musi przypomnieć o checkpointcie

Uwagi:

- licznik nie opiera się na historii rozmowy ani pamięci modelu
- jedynym źródłem prawdy są pliki distillation
- ręczna edycja tych plików wpływa bezpośrednio na licznik

To jest miękki obowiązek z przypomnieniem:

- Codex powinien wyraźnie zasygnalizować, że checkpoint jest wymagany
- brak checkpointu nie blokuje automatycznie kolejnego taska / tasks package
- ale kontynuacja bez checkpointu zwiększa ryzyko driftu i powinna zostać jawnie oznaczona

## Lokalizacja artefaktu checkpointu

Checkpoint artifact should be written under:

`docs/projects/<what_we_doing>/checkpoints/7_checkpoint_YYYY-MM-DD_scope.md`

Do not store checkpoint artifacts in `distillations/`; distillations are inputs to checkpoint, while checkpoints are synchronization evidence.

## Wejście do checkpointu

Checkpoint powinien pracować na następujących źródłach:

- `docs/projects/<what_we_doing>/PROJECT-MEMORY.md`
- `docs/ai/REPO-MEMORY.md`
- wszystkie pliki `X_task_or_package_name_distillation.md`, w których:
  - `memory_in_repo_memory: false`
- aktualny stan repo
- aktualna architektura
- opcjonalnie aktualny plan projektu, jeśli wciąż istnieją otwarte taski

## Główne zadania checkpointu

Checkpoint musi wykonać trzy rzeczy:

1. przetworzyć nową wiedzę z niezsynchronizowanych distillation
2. zaktualizować `docs/projects/<what_we_doing>/PROJECT-MEMORY.md`
3. sprawdzić spójność między:
   - architekturą
   - implementacją
   - project memory
   - repo memory

`docs/ai/REPO-MEMORY.md` jest agregatem repo-level. Aktualizuj go tylko wtedy, gdy checkpoint wykrywa wiedzę globalnie istotną dla całego repo, a nie lokalny detal jednego projektu.

## **Minimalny kontrakt PROJECT-MEMORY.md i REPO-MEMORY.md**

Project Memory powinno zawierać wiedzę istotną dla danego projektu.

Repo Memory powinno zawierać tylko rzeczy globalnie istotne dla całego repo.

Nie zapisuj wszystkiego z distillation.

Zapisuj wyłącznie:

- kluczowe decyzje projektowe
- trwałe zasady implementacyjne
- ważne constraints
- ważne odchylenia od architektury
- wzorce, których należy pilnować w kolejnych taskach
- future-blockers lub trwałe ryzyka, jeśli nadal obowiązują

## **Zasada kompresji i deduplikacji**

Checkpoint nie może kopiować distillation 1:1.

Codex musi:

- scalać powtarzające się decyzje
- usuwać duplikaty
- aktualizować wcześniejsze wpisy, jeśli nowe taski zmieniają ich treść
- utrzymywać memory w formie krótkiej i operacyjnej

Memory ma być narzędziem operacyjnym, nie archiwum.

## **Zasada zgodności z rzeczywistością**

Checkpoint musi opierać się na realnym stanie repo.

Jeśli:

- memory mówi jedno
- architektura mówi drugie
- repo pokazuje trzecie

to:

- checkpoint musi jawnie wskazać rozjazd
- nie wolno cicho preferować wcześniejszego dokumentu nad realnym stanem kodu bez oznaczenia konfliktu

## **Walidacja zgodności z architekturą**

Checkpoint musi sprawdzić:

- czy implementacja pozostaje zgodna z aktualną architekturą
- czy istnieją odchylenia architektoniczne
- czy wcześniejsze warningi architektoniczne nadal obowiązują
- czy memory poprawnie odzwierciedla aktualny stan systemu
- czy repo memory nie przejęło lokalnych detali projektowych, które powinny zostać tylko w project memory

## **Klasyfikacja driftu**

Każdy rozjazd musi zostać oznaczony jako:

### **Critical**

Rozjazd istotny, który wpływa na:

- kolejne taski / tasks package
- poprawność architektury
- spójność repo memory
- bezpieczeństwo dalszego planowania

### **Warning**

Rozjazd lokalny albo kontrolowany, który:

- nie blokuje pracy natychmiast
- ale powinien zostać zapisany i monitorowany

### **Informational**

Różnica niskiego znaczenia operacyjnego, która:

- nie wpływa istotnie na dalsze taski / tasks package
- wymaga jedynie kosmetycznej synchronizacji

## **Konsekwencje driftu**

Jeśli checkpoint wykryje drift:

- critical -> oznacz to jawnie w raporcie i wskaż potrzebę decyzji lub korekty
- warning -> zapisz to w memory lub raporcie checkpointu
- informational -> zaktualizuj memory, jeśli to potrzebne

Uwaga:

- drift critical nie blokuje automatycznie dalszych tasków / tasks packages
- ale musi zostać wyraźnie oznaczony i nie może zostać przemilczany

Dodatkowa reguła:

- jeśli drift critical wpływa na:
  - zakres kolejnych tasków / tasks packages
  - poprawność architektury
  - lub interpretację repo memory

to:

- rozpoczęcie kolejnego taska / tasks package powinno zostać wstrzymane do momentu decyzji użytkownika

(miękki gate – nie blokuje automatycznie, ale wymaga jawnej akceptacji ryzyka)

## **Przetwarzanie distillation**

Checkpoint przetwarza wyłącznie te pliki distillation, w których:

- memory_in_repo_memory: false

Po poprawnym przetworzeniu wiedzy:

- Codex powinien zaktualizować te pliki i ustawić:
  - memory_in_repo_memory: true

Atomiczność checkpointu:

- checkpoint traktowany jest jako operacja logicznie atomowa

Jeśli wystąpi częściowe wykonanie:

- np.:
  - `PROJECT-MEMORY.md` albo `REPO-MEMORY.md` zostało zaktualizowane
  - ale nie wszystkie pliki distillation mają ustawione memory_in_repo_memory: true

wtedy:

- checkpoint uznaje się za NIEZAKOŃCZONY
- Codex w kolejnym uruchomieniu musi:
  - ponownie przetworzyć wszystkie pliki z memory_in_repo_memory: false
  - nadpisać lub skorygować project/repo memory, jeśli to konieczne

Reguła:

- źródłem prawdy są zawsze pliki distillation z memory_in_repo_memory: false
- `PROJECT-MEMORY.md` i `docs/ai/REPO-MEMORY.md` nie są źródłem prawdy, tylko wynikiem agregacji

Zabronione:

- zakładanie, że checkpoint był poprawny, jeśli checkboxy nie są zsynchronizowane

To jest źródło prawdy o tym, czy dana destylacja została już zsynchronizowana z Repo Memory.

## **Reguła tworzenia memory files**

Jeśli `docs/projects/<what_we_doing>/PROJECT-MEMORY.md` nie istnieje:

- checkpoint powinien go utworzyć
- nie traktuj tego jako błędu

Jeśli `docs/ai/REPO-MEMORY.md` nie istnieje:

- checkpoint może zaproponować jego utworzenie albo utworzyć go, jeśli checkpoint dotyczy wiedzy repo-level
- nie zapisuj lokalnej wiedzy projektowej do repo memory tylko dlatego, że repo memory istnieje

## **Zakaz mechanicznego merge**

Nie wolno:

- kopiować całych distillation do memory
- duplikować tych samych decyzji
- trzymać w memory informacji lokalnych, jednorazowych albo nieistotnych globalnie

## **Output kontrolny na końcu checkpointu**

Na końcu checkpointu Codex powinien krótko wypisać:

- które distillation zostały przetworzone
- które checkboxy zostały zmienione na true
- jakie decyzje, zasady lub constraints dodano albo zaktualizowano w `PROJECT-MEMORY.md`
- jakie decyzje, zasady lub constraints dodano albo zaktualizowano w `docs/ai/REPO-MEMORY.md`, jeśli dotyczy
- czy wykryto drift
- klasyfikację driftu:
  - critical
  - warning
  - informational
- czy projekt pozostaje spójny względem:
  - architektury
  - implementacji
  - memory
- czy potrzebna jest korekta architektury, memory lub planu projektu

## Prompt bazowy

Prompt checkpointu powinien brzmieć mniej więcej tak:

```json
Wykonaj checkpoint projektu.

Wejście:
- docs/projects/<what_we_doing>/PROJECT-MEMORY.md
- docs/ai/REPO-MEMORY.md
- wszystkie X_task_or_package_name_distillation.md z memory_in_repo_memory: false
- aktualny stan repo
- aktualna architektura
- opcjonalnie plan projektu, jeśli nadal jest aktywny

Wykonaj:
- agregację nowej wiedzy z distillation
- kompresję i deduplikację informacji
- aktualizację PROJECT-MEMORY.md
- aktualizację docs/ai/REPO-MEMORY.md tylko dla wiedzy repo-level
- walidację zgodności między:
  - architekturą
  - implementacją
  - project memory
  - repo memory

Oznacz każdy wykryty rozjazd jako:
- critical
- warning
- informational

Po poprawnym przetworzeniu distillation:
- ustaw w tych plikach:
  - memory_in_repo_memory: true

Na końcu zwróć:
- które distillation zostały przetworzone
- jakie decyzje lub zasady dodano albo zaktualizowano
- czy wykryto drift
- klasyfikację driftu
- czy projekt pozostaje spójny
- czy potrzebna jest korekta architektury, memory lub planu projektu
```

---
