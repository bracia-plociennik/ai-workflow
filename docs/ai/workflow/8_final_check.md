# **8. FINAL CHECK - Codex**

Ta faza służy do końcowej walidacji całego etapu.

Celem nie jest analiza pojedynczego taska.
Celem jest ocena spójności całego systemu po zakończeniu etapu.

Final Check decyduje technicznie, czy etap może zostać przedstawiony ownerowi do zamknięcia.

Final Check nie może samodzielnie zamknąć etapu pełnym `PASS` bez jawnej zgody ownera.

## Warunek wejścia do tej fazy

Do tej fazy przechodzimy tylko wtedy, gdy:

- etap jest zakończony
- aktywny plan tematyczny lub plan projektu dla tego etapu jest zakończony
- wszystkie taski wchodzące w zakres etapu są:
  - zakończone
  - albo jawnie odroczone
- nie istnieją otwarte blocking issues wpływające na correctness etapu

Dodatkowo:

- checkpoint musi być wykonany

Jeśli checkpoint nie istnieje:

- wynik = FAIL
- nie wolno przejść dalej

Jeśli w aktywnym planie tematycznym nadal istnieją taski:

- otwarte
- blocked
- ready, ale niewykonane
- albo niejawnie pominięte

to:

- nie wolno uruchamiać Final Check
- nie wolno sugerować Final Check jako następnego kroku
- należy wrócić do dalszej realizacji tego planu

## Definicja zakończonego etapu

Etap jest zakończony tylko wtedy, gdy:

- jego zakres jest jawnie określony
- odpowiadający mu plan tematyczny jest domknięty w całości
- `8. FINAL CHECK` nie wykrył błędów technicznych
- owner jawnie zatwierdził finalne zamknięcie
- `8. FINAL CHECK` został dopiero wtedy oznaczony jako PASS

Jeśli Final Check nie wykrył błędów, ale owner nie zatwierdził jeszcze zamknięcia:

- wynik techniczny = `AWAITING_OWNER_FINAL_YES`
- aktywny plan nie jest jeszcze zamknięty
- kolejne side taski nie stają się jeszcze automatycznie optional

Po PASS dla `8. FINAL CHECK`:

- aktywny plan dla tego katalogu docs uznaje się za zamknięty
- kolejne side taski nie są automatycznie objęte pełnym workflow
- pełny workflow staje się opcjonalny aż do pojawienia się nowego planu projektu lub jawnego żądania użytkownika
- taski należące do etapu mają status zamknięty albo jawnie odroczony
- brak otwartych blockerów wpływających na correctness etapu

Bez spełnienia tych warunków:

- Final Check nie może dać wiarygodnego wyniku

## Zakres walidacji

Final Check musi zweryfikować:

- zgodność systemu z architekturą
- zgodność systemu z planem etapu
- brak sprzeczności między:
  - repo
  - architekturą
  - `docs/projects/<what_we_doing>/PROJECT-MEMORY.md`
  - `docs/ai/REPO-MEMORY.md`
  - `docs/ai/EXTERNAL-MEMORY.md`, jeśli etap promował uniwersalne lekcje workflow
  - checkpointami
- czy rzeczywisty system odpowiada deklarowanemu stanowi
- czy etap realizuje zamierzony cel systemowy

## Reguła warningów

Każdy warning blokuje PASS.

Jeśli istnieje choć jeden warning systemowy:

- wynik = FAIL

Nie wolno:

- ignorować warningów
- klasyfikować warningów jako "nieistotne" w tej fazie

## Reguła sprzeczności

FAIL jeśli:

- repo jest sprzeczne z architekturą
- plan etapu nie zgadza się z rzeczywistym stanem systemu
- project memory utrwala nieprawdziwy stan projektu
- repo memory utrwala nieprawdziwy stan repo-level
- external memory utrwala repo-specific albo project-specific wiedzę jako uniwersalną zasadę workflow
- istnieją niespójności między komponentami wpływające na correctness

## Relacja do checkpointu

Final Check zakłada, że:

- checkpoint został wykonany
- `docs/projects/<what_we_doing>/PROJECT-MEMORY.md` jest zsynchronizowany
- `docs/ai/REPO-MEMORY.md` jest zsynchronizowany, jeśli checkpoint dotyczył wiedzy repo-level
- `docs/ai/EXTERNAL-MEMORY.md` jest zsynchronizowany, jeśli checkpoint dotyczył uniwersalnej wiedzy workflow

Jeśli checkpoint nie istnieje:

- wynik = FAIL

Jeśli checkpoint istnieje, ale:

- memory jest niespójne z repo

→ wynik = FAIL

## Obsługa package

Jeśli etap zawierał package execution:

Final Check musi dodatkowo sprawdzić:

- czy paczki nie wprowadziły ukrytych sprzeczności
- czy łączenie tasków nie spowodowało dryfu względem:
  - architektury
  - planu projektu
- czy brak zależności wewnętrznych został utrzymany

## Zasada działania

Final Check:

- nie naprawia systemu
- nie proponuje implementacji
- nie zmienia architektury
- nie zmienia planu

Final Check:

- tylko ocenia
- tylko wskazuje problemy
- kończy się decyzją PASS albo FAIL

## Output fazy

Output musi zawierać:

- wynik końcowy: PASS / FAIL
- zgodność z architekturą: PASS / FAIL
- zgodność z planem etapu: PASS / FAIL
- spójność repo / memory / checkpointów: PASS / FAIL
- lista sprzeczności lub none
- lista warningów lub none
- decyzja:
  - etap może zostać uznany za zamknięty
  - etap nie może zostać uznany za zamknięty

## Reguła przejścia dalej

Jeśli wynik = PASS:

- etap może zostać zamknięty

Jeśli wynik = FAIL:

- należy wrócić do odpowiedniej fazy:
  - architektury
  - planu
  - specyfikacji
  - implementacji
  - QA

Nie wolno:

- zamknąć etapu z wynikiem FAIL

## Cross-check (opcjonalny)

Domyślnie Final Check wykonuje Codex.

Opcjonalnie:

- drugi przegląd może wykonać ChatGPT

Celem drugiego przeglądu jest:

- wykrycie ukrytych sprzeczności
- podważenie wyniku PASS
- wykrycie false closure

## Prompt bazowy

Prompt powinien brzmieć mniej więcej tak:

```json
Zweryfikuj cały etap jako system.

Zasady:
- oceń zgodność z architekturą
- oceń zgodność z planem etapu
- oceń spójność repo, PROJECT-MEMORY.md, docs/ai/REPO-MEMORY.md, docs/ai/EXTERNAL-MEMORY.md jeśli dotyczy, i checkpointów
- sprawdź brak sprzeczności systemowych

Reguły:
- jeśli checkpoint nie istnieje → FAIL
- jeśli istnieje choć jeden warning → FAIL
- jeśli istnieje sprzeczność wpływająca na correctness → FAIL

Nie:
- naprawiaj systemu
- proponuj implementacji
- zmieniaj architektury ani planu

Na końcu zwróć:
- wynik końcowy: PASS / FAIL
- zgodność z architekturą: PASS / FAIL
- zgodność z planem: PASS / FAIL
- spójność repo / memory / checkpointów: PASS / FAIL
- lista sprzeczności lub none
- lista warningów lub none
- decyzja: czy etap może zostać zamknięty

DoD:
- wynik PASS albo FAIL
- brak ukrytych sprzeczności
- decyzja o zamknięciu etapu
```
