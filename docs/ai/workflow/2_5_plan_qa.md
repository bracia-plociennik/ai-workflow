# 2.5. FAZA PLANU PROJEKTU QA - ChatGPT

Ta faza służy do krytycznej walidacji planu projektu przed przejściem do specyfikacji tasków.

Celem nie jest poprawianie planu ani tworzenie nowego.
Celem jest jednoznaczne określenie, czy plan przechodzi gate i nadaje się do dalszej pracy bez ryzyka ukrytych luk, złej kolejności albo redundancji.

Wynik tej fazy musi być binarny:

- PASS
- FAIL

Nie używaj odpowiedzi typu:

- "raczej ok"
- "wydaje się kompletne"
- "można iść dalej"

## Warunek wejścia do tej fazy

Do tej fazy przechodzimy tylko wtedy, gdy istnieje artefakt:

`docs/projects/<what_we_doing>/planning/2_project_plan.md`

Brak artefaktu:

- blokuje 2.5.
- uniemożliwia wykonanie QA

## Zasada ogólna

2.5. działa jako:

- review krytyczne
- próba obalenia planu
- walidacja gate przed przejściem do specyfikacji tasków

ChatGPT nie może:

- przepisywać planu
- proponować pełnego nowego planu
- mieszać tej fazy z fazą 2.

## Zakres walidacji

ChatGPT musi obowiązkowo sprawdzić:

### 1. Pokrycie architektury

Sprawdź, czy plan pokrywa 100% istotnego zakresu architektury.

W szczególności sprawdź:

- czy każdy istotny komponent lub obszar zmiany z architektury ma odzwierciedlenie w taskach
- czy nie pominięto przepływów danych, integracji, walidacji albo decyzji wymagających implementacji
- czy nie istnieją luki między architekturą a planem

Brak pokrycia istotnego elementu architektury:

- FAIL

---

### 2. Sequencing i kolejność

Sprawdź, czy kolejność tasków:

- minimalizuje ryzyko
- ujawnia ryzyka możliwie wcześnie
- nie odkłada krytycznych zależności na późno
- nie powoduje późnego wykrycia problemów integracyjnych lub architektonicznych

Błędna kolejność wpływająca na ryzyko lub rework:

- FAIL

---

### 3. Redundancje

Sprawdź, czy plan nie zawiera:

- tasków duplikujących ten sam rezultat
- tasków pokrywających ten sam zakres bez uzasadnienia
- tasków rozbitych w sposób sztuczny, który nie poprawia kontroli ani wykonania

Redundancja:

- FAIL

Uwaga:

- redundancja nie jest warningiem
- redundancja wpływa na koszt, jakość planu i interpretację zakresu

---

### 4. Zgodność z architekturą

Sprawdź, czy taski:

- nie łamią granic systemu
- nie wprowadzają zakresu spoza architektury
- nie implementują rzeczy, które nie mają podstawy w architekturze
- nie zakładają nierozstrzygniętej decyzji architektonicznej jako zamkniętej

Task sprzeczny z architekturą:

- FAIL

---

### 5. Kompletność kontraktu tasków

Sprawdź, czy taski mają pełny kontrakt zgodny z fazą 2.

W szczególności:

- ID lub nazwę
- cel
- zakres
- out-of-scope
- DoD
- zależności wejściowe
- typ ryzyka
- główne ryzyko
- warunek startu
- warunek zakończenia
- status:
  - ready
  - conditional
  - blocked
- informację o decyzji użytkownika, jeśli jest wymagana

Task niezdefiniowany albo niekompletny:

- FAIL

---

### 6. Ukryte zależności

Sprawdź, czy plan nie zawiera ukrytych zależności.

W szczególności:

- czy task nie wymaga wcześniejszego wyniku, którego nie oznaczono jawnie
- czy kolejność nie opiera się na niejawnych założeniach
- czy nie istnieją decyzje lub artefakty, bez których task faktycznie nie może ruszyć

Ukryta zależność:

- FAIL

---

### 7. Statusy tasków

Sprawdź, czy statusy tasków są poprawne.

W szczególności:

- task wymagający decyzji użytkownika nie może być oznaczony jako ready
- task z blocking dependency nie może być oznaczony jako ready
- task bez pełnego kontraktu nie może być oznaczony jako ready

Błędny status wpływający na przejście dalej:

- FAIL

---

## Cross-validation

2.5. musi zawierać drugi przebieg review.

Zasady:

- podważ założenia planu
- szukaj false completeness
- szukaj braków i ukrytych zależności
- szukaj tasków zbędnych, a nie tylko brakujących

Domyślnie:

- drugi review wykonuje ChatGPT (drugi prompt)

Codex review:

- opcjonalny
- nie jest domyślny

---

## Output

ChatGPT musi zwrócić:

- wynik końcowy: PASS / FAIL
- lista problemów
- lista braków krytycznych
- lista redundancji lub none
- lista warningów lub none
- informację:
  - czy można przejść do specyfikacji tasków bez doprecyzowywania w trakcie implementacji

## Reguła PASS

PASS jest możliwy tylko wtedy, gdy:

- plan pokrywa architekturę
- brak błędów sequencingu wpływających na ryzyko
- brak redundancji
- brak tasków sprzecznych z architekturą
- brak ukrytych zależności
- brak tasków niezdefiniowanych
- istnieje dowód, że Plan Gate jest spełniony

## Reguła FAIL

FAIL jest obowiązkowy, jeśli:

- brakuje artefaktu planu
- plan nie pokrywa architektury
- istnieje redundancja
- kolejność tasków zwiększa ryzyko reworku
- istnieją taski sprzeczne z architekturą
- istnieją ukryte zależności
- istnieją taski niezdefiniowane
- gate nie jest spełniony

## Reguła przejścia dalej

- tylko PASS pozwala przejść do fazy specyfikacji zadania
- FAIL wymusza powrót do 2 jako osobnej fazy

Nie wolno:

- poprawiać planu w tej samej fazie
- przechodzić dalej po FAIL

## Prompt bazowy

Prompt powinien brzmieć mniej więcej tak:

```json
Przeprowadź krytyczną walidację planu projektu (2.5.).

Wejście:
- docs/projects/<what_we_doing>/planning/2_project_plan.md
- docs/projects/<what_we_doing>/architecture/1_architecture_phase.md

Twoim celem nie jest poprawianie planu.
Twoim celem jest sprawdzenie, czy plan przechodzi Plan Gate.

Wykonaj obowiązkowo:

1. Walidację pokrycia architektury:
- czy plan pokrywa 100% istotnego zakresu architektury
- czy nie pominięto komponentów, integracji, walidacji albo przepływów

2. Walidację kolejności:
- czy sequencing minimalizuje ryzyko
- czy nie odkłada krytycznych zależności na późno
- czy nie zwiększa ryzyka reworku

3. Walidację redundancji:
- czy plan nie zawiera tasków duplikujących rezultat
- czy nie zawiera sztucznego rozbicia bez wartości wykonawczej

4. Walidację zgodności z architekturą:
- czy taski nie wychodzą poza granice architektury
- czy nie zakładają zamkniętych decyzji, które nadal są otwarte

5. Walidację kompletności kontraktu tasków:
- cel
- zakres
- out-of-scope
- DoD
- zależności
- ryzyko
- warunki startu i zakończenia
- status
- decyzje użytkownika, jeśli wymagane

6. Walidację ukrytych zależności:
- czy wszystkie realne zależności są jawne
- czy nie ma niejawnych blockerów

7. Walidację statusów tasków:
- czy ready / conditional / blocked są przypisane poprawnie

Następnie wykonaj drugi przebieg (cross-validation):
- podważ założenia planu
- znajdź false completeness
- szukaj braków, redundancji i ukrytych zależności

Na końcu zwróć:

- wynik końcowy: PASS / FAIL
- lista problemów
- lista braków krytycznych
- lista redundancji lub none
- lista warningów lub none
- lista decyzji, które użytkownik musi podjąć osobiście (zaproponuj do każdej decyzji po 1 rekomendacji + wpływ rekomendacji oraz 1 alternatywie + wpływ alterantywy)
- decyzja:
  - czy można przejść do specyfikacji tasków bez doprecyzowywania w trakcie implementacji

Zasady:
- wynik musi być binarny
- brak dowodu = FAIL
- nie poprawiaj planu
- nie twórz nowego planu
- nie przechodź dalej przy FAIL
- redundancja = FAIL

DoD:
jednoznaczna decyzja PASS / FAIL + lista problemów
```

---
