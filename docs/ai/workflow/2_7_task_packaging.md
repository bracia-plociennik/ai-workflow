# 2.7. FAZA TASK PACKAGING - Codex

Ta faza służy do grupowania tasków w pakiety przed specyfikacją.

Celem nie jest zmiana planu.
Celem jest przyspieszenie specyfikacji poprzez bezpieczne grupowanie tasków.

## Warunek wejścia do tej fazy

Do tej fazy przechodzimy tylko wtedy, gdy:

- plan przeszedł 2.5 (PASS)
- istnieje artefakt:
  `docs/projects/<what_we_doing>/planning/2_project_plan.md`

Brak PASS w 2.5:

- blokuje 2.7.

## Zasada ogólna

Task Packaging to:

- transformacja strukturalna planu
- bez zmiany jego treści

Nie wolno:

- zmieniać zakresu tasków
- usuwać tasków
- dodawać nowych tasków
- zmieniać kolejności globalnej

## Cel fazy

Celem jest stworzenie pakietów tasków, które:

- mogą być specyfikowane razem
- mogą być implementowane bez konfliktów
- nie maskują ryzyk ani zależności

## Kryteria grupowania

Taski mogą być w jednym pakiecie tylko jeśli:

- należą do tego samego obszaru systemu (komponent / moduł / feature)
- mają spójną odpowiedzialność
- nie mają konfliktów zakresu
- nie mają konfliktów odpowiedzialności
- nie mają konfliktów sequencing

## Zasady kolejności wykonywania (specyfikacja → implementacja):

- kolejność musi wynikać z zależności (dependencies), nie z typu (task vs package)
- package traktuj jak pojedynczy blok wykonawczy

Prawidłowa kolejność:

1. task bez zależności (foundation)
2. task zależny od poprzedniego
3. package, jeśli:
   - wszystkie jego zależności są już zamknięte
4. kolejne taski zależne od package
5. kolejne package, jeśli ich zależności są spełnione

Przykład:

1. task A (brak zależności)
2. task B (zależny od A)
3. package C (zależny od A i B)
4. task D (zależny od C)
5. package E (zależny od C i D)
6. package F (zależny od E)

Reguły:

- nie przeplataj implementacji wewnątrz package:
  - spec → QA → implementacja → QA dla całego package
- nie implementuj części package przed jego pełną specyfikacją
- nie zaczynaj taska, jeśli zależy od niezamkniętego package
- każdy element (task/package) musi przejść pełny cykl:
  - spec → QA → fix loop (jeśli FAIL) → implementacja → QA → fix loop → destylacja

## Twardy zakaz zależności wewnętrznych

Pakiet nie może zawierać tasków, które mają zależność między sobą.

W szczególności:

- task A zależy od task B → nie mogą być w jednym pakiecie
- task wymaga wyniku innego taska → nie mogą być w jednym pakiecie

Zależność wewnętrzna:

- FAIL

## Reguła niezależności pakietu

Pakiet musi być:

- niezależny wykonawczo
- możliwy do specyfikacji jako całość
- możliwy do implementacji bez czekania na wynik innego taska z tego pakietu

## Reguła wykrywania konfliktów

Codex musi wykryć:

- konflikty zależności
- konflikty zakresu
- konflikty odpowiedzialności
- konflikty sequencing

Każdy konflikt:

- blokuje utworzenie pakietu
- musi być jawnie zgłoszony

## Brak możliwości pakietyzacji

Jeśli tasków nie da się bezpiecznie pogrupować:

- nie twórz sztucznych pakietów
- zwróć:
  - brak pakietów
  - lista tasków solo

Brak pakietyzacji:

- jest poprawnym wynikiem tej fazy

## Output fazy

Codex musi zwrócić:

- listę pakietów
- dla każdego pakietu:
  - ID pakietu
  - zakres pakietu
  - lista tasków w pakiecie
- listę tasków niepakietyzowalnych
- listę wykrytych konfliktów lub none
- potwierdzenie aktualizacji sekcji `Tasks package` w pliku `docs/projects/<what_we_doing>/planning/2_project_plan.md`

## Reguła STOP

Jeśli:

- wykryto konflikty
- albo pakiety łamią zasady tej fazy

→ FAIL

Nie wolno:

- ignorować konfliktów
- tworzyć pakietów mimo konfliktów

## Reguła PASS

PASS jest możliwy tylko jeśli:

- wszystkie pakiety są bez konfliktów
- brak zależności wewnętrznych
- brak naruszenia zakresu planu
- output jest jednoznaczny i kompletny

## Artefakt wyjściowy fazy

Faza 2.7 nie tworzy osobnego artefaktu packagingu.

Wynik fazy 2.7 musi zostać zapisany przez aktualizację pliku:

- `docs/projects/<what_we_doing>/planning/2_project_plan.md`

Aktualizacja musi dodać lub zaktualizować sekcję:

- `Tasks package`

Sekcja `Tasks package` musi zawierać:

- listę pakietów
- dla każdego pakietu:
  - ID pakietu
  - zakres pakietu
  - lista tasków w pakiecie
- listę tasków niepakietyzowalnych
- listę wykrytych konfliktów lub none

Brak aktualizacji sekcji `Tasks package` w `docs/projects/<what_we_doing>/planning/2_project_plan.md`:

- blokuje przejście dalej z fazy 2.7.

## Reguła przejścia dalej

- PASS + utworzono co najmniej jeden pakiet → przejście do 2.9. (Packaging QA)
- PASS + nie utworzono żadnych pakietów → pomiń 2.9. i przejdź bezpośrednio do fazy 3. (Specyfikacja)
- FAIL → powrót do 2 jako osobnej fazy

Nie wolno uruchamiać 2.9. tylko po to, żeby potwierdzić brak pakietów.

Brak pakietów jest poprawnym wynikiem 2.7. i oznacza, że każdy task pozostaje solo execution block.

## Prompt bazowy

Prompt powinien brzmieć mniej więcej tak:

```json
Przeprowadź task packaging (2.7.).

Wejście:
- docs/projects/<what_we_doing>/planning/2_project_plan.md

Twoim celem nie jest zmiana planu.
Twoim celem jest bezpieczne pogrupowanie tasków w pakiety.

Wykonaj:

1. Zidentyfikuj taski możliwe do pogrupowania:
- wspólny obszar systemu
- wspólna odpowiedzialność
- brak konfliktów

2. Sprawdź dla każdego potencjalnego pakietu:
- brak zależności między taskami
- brak konfliktów zakresu
- brak konfliktów odpowiedzialności
- brak konfliktów sequencing

3. Wykryj konflikty:
- zależności
- zakres
- odpowiedzialność
- sequencing

Zasady:
- nie zmieniaj planu
- nie dodawaj tasków
- nie usuwaj tasków
- nie zmieniaj kolejności globalnej
- zależność wewnętrzna = FAIL
- konflikt = FAIL
- brak pakietyzacji jest poprawnym wynikiem

Na końcu zwróć:

- listę pakietów:
  - ID pakietu
  - zakres
  - lista tasków
- listę tasków niepakietyzowalnych
- listę kolejności wykonywania
- listę konfliktów lub none
- wynik końcowy: PASS / FAIL

DoD:
powstała jednoznaczna lista pakietów bez konfliktów albo brak pakietów
```

---
