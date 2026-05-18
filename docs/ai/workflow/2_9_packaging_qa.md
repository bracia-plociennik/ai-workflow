# 2.9. FAZA TASK PACKAGING QA - Codex

Ta faza służy do krytycznej walidacji pakietów tasków przed przejściem do specyfikacji.

Celem nie jest poprawianie pakietów ani tworzenie nowych.
Celem jest jednoznaczne określenie, czy pakiety są poprawne, bezkonfliktowe i zgodne z architekturą oraz planem projektu.

Wynik tej fazy musi być binarny:

- PASS
- FAIL

Nie używaj odpowiedzi typu:

- "raczej ok"
- "wydaje się bezpieczne"
- "można iść dalej"

## Warunek wejścia do tej fazy

Do tej fazy przechodzimy tylko wtedy, gdy:

- istnieje artefakt:
  `docs/projects/<what_we_doing>/planning/2_project_plan.md`
- została wykonana faza 2.7.
- istnieje output pakietyzacji, istnieje sekcja `Tasks package` w artefakcie `docs/projects/<what_we_doing>/planning/2_project_plan.md`
- sekcja `Tasks package` zawiera co najmniej jeden realny pakiet

Brak outputu pakietyzacji:

- blokuje 2.9.
- uniemożliwia wykonanie QA pakietów

## Przypadek braku pakietów

Jeśli wynik fazy 2.7. jest taki, że nie utworzono żadnych pakietów lub jeśli sekcja `Tasks package` w `docs/projects/<what_we_doing>/planning/2_project_plan.md` wskazuje, że nie utworzono żadnych pakietów::

- nie wchodź w fazę 2.9.
- przejdź bezpośrednio do fazy 3. dla kolejnego taska solo z planu projektu.
- odnotuj w statusie workflow:
  - brak pakietów
  - `2.9. PACKAGING QA` pominięte
  - następna faza: `3. FAZA SPECYFIKACJI`

To nie jest FAIL.
To nie jest PASS.
To jest pominięcie fazy z powodu braku pakietów.

## Zasada ogólna

2.9. działa jako:

- review krytyczne
- próba obalenia poprawności pakietów
- walidacja gate przed specyfikacją

Codex nie może:

- przepisywać pakietów
- proponować nowych pakietów jako wyniku tej fazy
- mieszać tej fazy z 2.7.
- poprawiać planu projektu

## Zakres walidacji

Codex musi obowiązkowo sprawdzić:

### 1. Spójność pakietów

Sprawdź, czy każdy pakiet:

- ma jeden logiczny zakres
- zawiera taski należące do tego samego obszaru systemu lub odpowiedzialności
- nie miesza niezależnych domen
- nie jest sztucznie połączonym zbiorem tasków bez wspólnego celu

Brak spójności pakietu:

- FAIL

---

### 2. Zależności między taskami

Sprawdź, czy w pakiecie nie istnieją zależności wewnętrzne.

W szczególności:

- task A zależy od taska B w tym samym pakiecie
- task wymaga wyniku innego taska z tego samego pakietu
- kolejność wykonania wewnątrz pakietu jest konieczna do correctness

Zależność wewnętrzna:

- FAIL

---

### 3. Konflikty między taskami

Sprawdź, czy w pakiecie nie istnieją konflikty:

- zakresu
- odpowiedzialności
- sequencing
- implementacyjne
- integracyjne

Każdy konflikt wpływający na wspólną specyfikację lub wspólne wykonanie:

- FAIL

---

### 4. Zgodność z planem projektu

Sprawdź, czy pakietyzacja:

- nie zmienia zakresu tasków
- nie usuwa tasków
- nie dodaje nowych tasków
- nie zmienia globalnej kolejności planu
- nie ukrywa tasków conditional albo blocked jako ready

Każde naruszenie planu projektu:

- FAIL

---

### 5. Zgodność z architekturą

Sprawdź, czy pakiety:

- nie łamią granic systemu
- nie łączą tasków, które powinny pozostać rozdzielone ze względu na architekturę
- nie maskują nierozstrzygniętych decyzji architektonicznych
- nie obejmują zakresu spoza architektury

Naruszenie architektury:

- FAIL

---

### 6. False independence

Sprawdź, czy pakiet nie wygląda na niezależny tylko pozornie.

W szczególności:

- czy taski nie współdzielą ukrytych zależności
- czy wspólna specyfikacja nie ukrywa ryzyka
- czy wspólna implementacja nie wymaga jednak podziału na osobne ścieżki

False independence:

- FAIL

---

## Cross-validation

2.9. musi zawierać drugi przebieg review.

Zasady:

- podważ założenia pakietyzacji
- szukaj false independence
- szukaj konfliktów, nie potwierdzeń
- szukaj ukrytych zależności i ukrytego scope creep

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
- lista konfliktów lub none
- lista zależności wewnętrznych lub none
- lista naruszeń architektury lub none
- lista warningów lub none
- decyzja:
  - czy można przejść do specyfikacji
  - czy trzeba wrócić do 2.7.

Jeśli po fazie 2.7. nie utworzono żadnych pakietów, nie uruchamiaj tej fazy.

Brak pakietów musi zostać obsłużony w fazie 2.7. jako przejście bezpośrednio do fazy 3.

## Reguła PASS

PASS jest możliwy tylko wtedy, gdy:

- wszystkie pakiety są spójne
- brak zależności wewnętrznych
- brak konfliktów
- brak naruszeń planu projektu
- brak naruszeń architektury
- brak false independence
- istnieje dowód, że Packaging Gate jest spełniony

## Reguła FAIL

FAIL jest obowiązkowy, jeśli:

- brakuje outputu pakietyzacji
- istnieje zależność wewnętrzna
- istnieje konflikt
- pakiet łamie plan projektu
- pakiet łamie architekturę
- istnieje false independence
- gate nie jest spełniony

## Reguła przejścia dalej

- PASS pozwala przejść do fazy specyfikacji
- FAIL wymusza powrót do 2.7. jako osobnej fazy
- brak pakietów blokuje wejście do tej fazy, ponieważ nie istnieje nic do walidacji

Nie wolno:

- poprawiać pakietów w tej samej fazie
- przechodzić dalej po FAIL
- traktować braku pakietów jako ukrytego PASS
- uruchamiać 2.9. przy braku pakietów

## Prompt bazowy

Prompt powinien brzmieć mniej więcej tak:

```json
Przeprowadź krytyczną walidację task packaging (2.9.).

Wejście:
- docs/projects/<what_we_doing>/planning/2_project_plan.md
- output fazy 2.7. Task Packaging, sekcja `Tasks package` z `docs/projects/<what_we_doing>/planning/2_project_plan.md`

Twoim celem nie jest poprawianie pakietów.
Twoim celem jest sprawdzenie, czy pakiety przechodzą Packaging Gate.

Najpierw sprawdź, czy istnieją pakiety.

Jeśli pakiety nie istnieją:
- STOP
- nie wykonuj Packaging QA
- wskaż, że zgodnie z workflow faza 2.9. jest pomijana i następną fazą jest 3. FAZA SPECYFIKACJI

Jeśli pakiety istnieją, wykonaj obowiązkowo:

1. Walidację spójności pakietów:
- czy każdy pakiet ma jeden logiczny zakres
- czy nie miesza niezależnych domen
- czy taski w pakiecie mają wspólny cel

2. Walidację zależności:
- czy nie istnieją zależności wewnętrzne
- czy taski nie wymagają wyników innych tasków z tego samego pakietu

3. Walidację konfliktów:
- zakres
- odpowiedzialność
- sequencing
- implementacja
- integracja

4. Walidację zgodności z planem:
- czy pakietyzacja nie zmienia zakresu
- czy nie usuwa tasków
- czy nie dodaje nowych tasków
- czy nie zmienia kolejności globalnej

5. Walidację zgodności z architekturą:
- czy pakiety nie łamią granic systemu
- czy nie maskują otwartych decyzji architektonicznych

6. Walidację false independence:
- czy pakiety nie wyglądają na niezależne tylko pozornie
- czy nie ukrywają ryzyk albo zależności

Następnie wykonaj drugi przebieg (cross-validation):
- podważ założenia pakietyzacji
- szukaj false independence
- szukaj konfliktów i ukrytych zależności

Na końcu zwróć:

- wynik końcowy: PASS / FAIL
- lista problemów
- lista konfliktów lub none
- lista zależności wewnętrznych lub none
- lista naruszeń architektury lub none
- lista warningów lub none
- lista decyzji, które użytkownik musi podjąć osobiście (zaproponuj do każdej decyzji po 1 rekomendacji + wpływ rekomendacji oraz 1 alternatywie + wpływ alterantywy)
- decyzja:
  - czy można przejść do specyfikacji
  - czy trzeba wrócić do 2.7.

Zasady:
- wynik musi być binarny, jeśli pakiety istnieją
- brak dowodu = FAIL
- nie poprawiaj pakietów
- nie twórz nowych pakietów
- nie przechodź dalej przy FAIL
- brak pakietów = STOP i przejście poza 2.9., ponieważ ta faza nie ma czego walidować

DoD:
jeśli pakiety istnieją -> jednoznaczna decyzja PASS / FAIL + lista problemów
jeśli pakiety nie istnieją -> 2.9. nie jest wykonywane
```

---
