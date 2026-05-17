# 6. FAZA DESTYLACJI - Codex

Ta faza służy do zamiany zakończonego taska / tasks package w trwałą wiedzę projektową.

Celem nie jest opis przebiegu pracy.
Celem jest zapisanie tylko tych informacji, które mają wartość operacyjną i mogą zostać użyte w kolejnych taskach lub checkpointach.

## Warunek wejścia do tej fazy

Do tej fazy może przejść tylko task / tasks package, który przeszedł fazę jakości z wynikiem:

- PASS

Task / tasks package z wynikiem:

- FAIL
  nie może przejść do finalnej destylacji jako task zakończony.

Można ewentualnie zapisać roboczą notatkę o przyczynie FAIL, ale nie jako standardową finalną destylację taska / paczki zadań zamkniętego.

## Zasada ogólna

Destylacja ma być rygorystyczna, konkretna i używalna.

To nie jest:

- log pracy
- narracja
- opis procesu
- dump notatek

To jest:

- kompresja wiedzy
- zapis decyzji
- zapis problemów z wnioskami
- zapis zasad możliwych do reuse

## Lokalizacja artefaktu

Destylacja powinna powstać jako plik:

`docs/projects/<what_we_doing>/distillations/X_task_or_package_name_distillation.md`

gdzie:

- `X` = numer taska / tasks package

## **Minimalny kontrakt pliku destylacji**

Każdy plik distillation musi zawierać co najmniej:

- co zostało zrobione
- problemy
- decyzje
- zasady na przyszłość
- status memory checkbox

Jeśli jakaś sekcja nie zawiera nowych informacji:

- należy to jawnie zaznaczyć
- nie wolno pomijać sekcji po cichu

## **Struktura logiczna destylacji**

### **1. Co zostało zrobione**

Zapisuj tylko faktyczny rezultat taska / tasks package.

Nie opisuj całego procesu dochodzenia.

### **2. Problemy**

Zapisuj tylko problemy realnie istotne dla jakości, architektury, implementacji lub przyszłych tasków / paczek zadań.

Każdy istotny problem powinien prowadzić do:

- decyzji
  albo
- zasady na przyszłość

Problem bez wniosku oznacza utratę wiedzy.

### **3. Decyzje**

Każdą istotną decyzję zapisuj w formie możliwej do reuse.

Decyzja powinna zawierać:

- co zdecydowano
- dlaczego
- kiedy to stosować
- kiedy nie stosować, jeśli ma to znaczenie

Jeśli nie było nowych decyzji:

- zaznacz to jawnie

### **4. Zasady na przyszłość**

Zapisuj tylko zasady operacyjne, które mogą pomóc w kolejnych taskach / paczkach zadań.

Zasada powinna być:

- konkretna
- krótka
- możliwa do ponownego użycia
- oparta na realnym doświadczeniu z taska

Jeśli coś było nieoczywiste:

- co najmniej jedna zasada reusable jest obowiązkowa

Jeśli nic istotnego się nie wydarzyło:

- dopuszczalna jest destylacja minimalna

### **5. Status Repo Memory**

Każdy plik musi zawierać jawny status:

- memory_in_repo_memory: false

Wartość domyślna:

- false

Destylacja nie trafia automatycznie do Repo Memory.

Agregacja do memory odbywa się dopiero przez checkpoint projektu.

## **Synchronizacja planu projektu podczas destylacji**

Podczas `6. FAZA DESTYLACJI` Codex musi zsynchronizować wynik taska / tasks package także z:

- `docs/projects/<what_we_doing>/planning/2_project_plan.md`

Jeśli task albo package:

- przeszedł fazę jakości z wynikiem `PASS`
- i jest objęty bieżącą destylacją

to Codex musi:

- zaktualizować status odpowiedniego taska / tasków na `completed`, jeśli status jest nieaktualny
- oraz zaktualizować sekcję:
  - `## **Lista kolejności wykonywania**`

W tej sekcji należy:

- odnaleźć odpowiadający wpis taska albo package
- oznaczyć go jako wykonany przez dodanie `✅`

Zasady:

- aktualizuj tylko wpisy będące w scope bieżącej destylacji
- nie oznaczaj przyszłych tasków ani package
- nie oznaczaj `✅` bez wcześniejszego quality `PASS`
- jeśli sekcja `## **Lista kolejności wykonywania**` nie istnieje albo mapping wpisu nie jest wiarygodny:
  - nie zgaduj
  - opisz to jawnie w odpowiedzi końcowej

## **Zakaz narracji**

Nie wolno tworzyć:

- opisów krok po kroku
- historii taska
- ogólnych podsumowań bez wartości operacyjnej
- tekstu “co się działo” bez decyzji, problemu albo zasady

## **Zasada konkretu**

Informacje w destylacji muszą być:

- konkretne
- operacyjne
- możliwe do użycia później

Nie używaj:

- ogólników
- pustych wniosków
- oczywistości bez wartości reuse

## **Zasada kompresji wiedzy**

Codex ma obowiązek zachować tylko to, co ma wartość operacyjną.

Nie kopiuj:

- całej specyfikacji taska / tasks package
- całego raportu jakości
- całej historii implementacji

Destylacja ma być wynikiem kompresji, nie archiwizacją wszystkiego.

## **Zasada zgodności z rzeczywistością**

Destylacja musi być zgodna z:

- planem taska / tasks package
- faktyczną implementacją
- wynikiem fazy jakości

Nie wolno zapisywać wniosków, decyzji ani problemów, które nie miały miejsca albo nie wynikają z taska / tasks package.

## **Minimalna destylacja**

Minimalna destylacja jest dozwolona tylko wtedy, gdy:

- task / tasks package przeszedł PASS
- nic istotnego ani nieoczywistego się nie wydarzyło
- nie pojawiły się nowe decyzje
- nie pojawiły się reusable zasady poza oczywistościami

W takim przypadku nadal trzeba jawnie zapisać:

- co zostało zrobione
- brak istotnych problemów lub decyzji
- brak nowych zasad
- memory_in_repo_memory: false

## **Output kontrolny na końcu fazy**

Na końcu destylacji Codex powinien krótko potwierdzić:

- czy wszystkie istotne decyzje zostały zapisane
- czy wszystkie istotne problemy mają wniosek
- czy powstały zasady na przyszłość, jeśli były potrzebne
- czy wiedza nie została utracona
- czy plik jest gotowy do późniejszego checkpointu

## Prompt bazowy

Prompt po zakończeniu taska powinien brzmieć mniej więcej tak:

```json
Stwórz destylację wiedzy z tego taska / tasks package.

Destylacja ma zawierać tylko informacje operacyjnie użyteczne.

Uwzględnij:
- co zostało faktycznie zrobione
- problemy, które wystąpiły
- decyzje, które zapadły
- zasady na przyszłość
- checkbox, czy wiedza została przeniesiona do Repo Memory

Zasady:
- nie twórz narracji
- nie lej wody
- zapisuj konkrety
- każdy istotny problem zamień w decyzję albo zasadę
- jeśli brak nowych decyzji lub zasad, zaznacz to jawnie
- jeśli coś było nieoczywiste, zapisz co najmniej jedną zasadę możliwą do reuse
- jeśli nic istotnego się nie wydarzyło, dopuszczalna jest destylacja minimalna

Ustaw:
- memory_in_repo_memory: false

DoD fazy:
powstał artefakt docs/projects/<what_we_doing>/distillations/X_task_or_package_name_distillation.md
```

---
