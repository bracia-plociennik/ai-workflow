# 1.5. FAZA ARCHITEKTURY QA - Codex

Ta faza służy do krytycznej walidacji architektury przed przejściem do planu projektu.

Celem nie jest poprawianie architektury ani tworzenie nowej.
Celem jest jednoznaczne określenie, czy architektura spełnia warunki przejścia dalej.

Wynik tej fazy musi być binarny:

- PASS
- FAIL

Nie używaj odpowiedzi typu:

- "raczej ok"
- "wydaje się poprawne"
- "można iść dalej"

## Warunek wejścia do tej fazy

Do tej fazy przechodzimy tylko wtedy, gdy istnieje artefakt:

`docs/projects/<what_we_doing>/architecture/1_architecture_phase.md`

Brak artefaktu:

- blokuje 1.5.
- uniemożliwia wykonanie QA

## Zasada ogólna

1.5. działa jako:

- review krytyczne
- próba obalenia architektury
- walidacja gate przed planem projektu

Codex nie może:

- przepisywać architektury
- proponować pełnej nowej architektury
- mieszać tej fazy z fazą 1.

## Zakres walidacji

Codex musi obowiązkowo sprawdzić:

### 1. Kompletność architektury

Czy architektura zawiera:

- cele systemu lub zmiany
- granice systemu i out-of-scope
- komponenty i ich odpowiedzialności
- zależności między komponentami
- główne przepływy danych lub integracji
- decyzje architektoniczne podjęte
- decyzje architektoniczne do podjęcia
- ryzyka architektoniczne
- assumptions
- unknowns:
  - blocking
  - non-blocking
- wpływ architektury na plan projektu

Brak któregokolwiek elementu wpływającego na plan projektu:

- FAIL

---

### 2. Spójność wewnętrzna

Sprawdź:

- sprzeczności między sekcjami
- konflikt granic i zakresu
- konflikt odpowiedzialności komponentów
- konflikt między decyzjami i unknowns
- konflikt między ryzykami i rekomendacją

Sprzeczność wpływająca na plan projektu:

- FAIL

---

### 3. Unknowns i klasyfikacja

Sprawdź:

- czy wszystkie unknowns są jawne
- czy klasyfikacja blocking / non-blocking jest poprawna
- czy istnieją ukryte unknowns blocking
- czy non-blocking mają:
  - ownera
  - opis wpływu
  - warunek domknięcia

Błąd w klasyfikacji lub brak jawności:

- FAIL

---

### 4. Ryzyka architektoniczne

Sprawdź:

- czy każde istotne ryzyko ma:
  - decyzję
  - albo ownera
  - albo warunek domknięcia

Brak jednego z powyższych:

- FAIL

---

### 5. Architecture Gate

Sprawdź, czy można przejść do planu projektu bez ryzyka reworku.

Jeśli:

- istnieją unknowns blocking
- istnieją nierozstrzygnięte decyzje wpływające na implementację
- architektura jest zbyt ogólna

→ FAIL

---

### 6. Proporcjonalność architektury

Sprawdź:

- czy architektura nie jest zbyt ogólna
- czy nie jest przeładowana
- czy odpowiada skali zmiany

Jeśli poziom szczegółowości uniemożliwia planowanie:

- FAIL

---

### 7. Uproszczenia

Sprawdź:

- czy istnieją zbędne komponenty
- czy istnieje pseudo-złożoność
- czy można uprościć bez utraty correctness

To nie blokuje PASS, chyba że:

- wpływa na Architecture Gate

---

## Cross-validation

1.5. musi zawierać drugi przebieg review.

Zasady:

- podważ założenia
- szukaj false completeness
- szukaj braków, nie potwierdzeń

Domyślnie:

- drugi review wykonuje Codex (drugi prompt)

Codex review:

- opcjonalny
- nie jest domyślny

---

## Output

Codex musi zwrócić:

- wynik końcowy: PASS / FAIL
- lista problemów
- lista braków krytycznych
- lista warningów (jeśli istnieją)
- informację:
  - czy można przejść do planu projektu bez ryzyka reworku

## Reguła PASS

PASS jest możliwy tylko wtedy, gdy:

- brak unknowns blocking
- brak istotnych ryzyk bez decyzji / ownera / warunku domknięcia
- architektura jest kompletna
- brak sprzeczności wpływających na plan projektu
- istnieje dowód, że Architecture Gate jest spełniony

## Reguła FAIL

FAIL jest obowiązkowy, jeśli:

- brakuje artefaktu architektury
- architektura jest niekompletna
- istnieją sprzeczności wpływające na plan
- istnieją ukryte unknowns
- gate nie jest spełniony

## Reguła przejścia dalej

- tylko PASS pozwala przejść do fazy planu projektu
- FAIL wymusza powrót do 1. jako osobnej fazy

Nie wolno:

- poprawiać architektury w tej samej fazie
- przechodzić dalej po FAIL

## Prompt bazowy

Prompt powinien brzmieć mniej więcej tak:

```json
Przeprowadź krytyczną walidację architektury (1.).

Wejście:
- docs/projects/<what_we_doing>/architecture/1_architecture_phase.md

Twoim celem nie jest poprawianie architektury.
Twoim celem jest sprawdzenie, czy architektura przechodzi Architecture Gate.

Wykonaj obowiązkowo:

1. Walidację kompletności:
- cele systemu lub zmiany
- granice systemu i out-of-scope
- komponenty i odpowiedzialności
- zależności
- przepływy danych / integracje
- decyzje podjęte i do podjęcia
- ryzyka
- assumptions
- unknowns (blocking / non-blocking)
- wpływ na plan projektu

2. Walidację spójności:
- sprzeczności między sekcjami
- konflikty zakresu i granic
- konflikty odpowiedzialności
- konflikty decyzji i unknowns
- konflikty ryzyk i rekomendacji

3. Walidację unknowns:
- czy wszystkie są jawne
- czy klasyfikacja blocking / non-blocking jest poprawna
- czy istnieją ukryte unknowns blocking
- czy non-blocking mają ownera, wpływ i warunek domknięcia

4. Walidację ryzyk:
- czy każde istotne ryzyko ma decyzję / ownera / warunek domknięcia

5. Walidację Architecture Gate:
- czy można przejść do planu projektu bez ryzyka reworku

6. Walidację proporcjonalności:
- czy architektura nie jest zbyt ogólna ani przeładowana

Następnie wykonaj drugi przebieg (cross-validation):
- podważ założenia
- znajdź false completeness
- szukaj braków

Na końcu zwróć:

- wynik końcowy: PASS / FAIL
- lista problemów
- lista braków krytycznych
- lista warningów lub none
- lista decyzji, które użytkownik musi podjąć osobiście (zaproponuj do każdej decyzji po 1 rekomendacji + wpływ rekomendacji oraz 1 alternatywie + wpływ alterantywy)
- decyzja:
  - czy można przejść do planu projektu bez ryzyka reworku

Zasady:
- wynik musi być binarny
- brak dowodu = FAIL
- nie poprawiaj architektury
- nie twórz nowej architektury
- nie przechodź dalej przy FAIL

DoD:
jednoznaczna decyzja PASS / FAIL + lista problemów
```

---
