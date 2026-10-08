# 2026-06-23 - Quality Review Intent Compliance

- Date: `2026-06-23`
- Category: `quality`
- Status: `accepted`
- Source scope: `owner-approved capture`
- Privacy check: `confirmed no raw client data, client names, secrets, repo-specific facts, project-specific details, or production identifiers`
- Skill candidate: `yes`
- Suggested skill target: `AI_WORKFLOW_WORKSPACE_HOME/skills/quality-review-skill`

## TEMAT

- `Jakość - zgodność z intencją`

## 0. SYGNAŁY

- Review techniczny może przepuścić wykonanie, które rozwiązuje niewłaściwy problem.
- Przechodzące testy nie dowodzą zgodności z poleceniem, zakresem ani acceptance criteria.
- Brak jawnego porównania z intencją zwiększa ryzyko overbuild, underbuild i scope creep.

## 1. CO ZOSTAŁO FAKTYCZNIE ZROBIONE

- Wprowadzono osobną soczewkę jakościową dla zgodności wykonania z intencją, planem, specyfikacją, zakresem i acceptance criteria.
- Rozdzielono statusy advisory review od formalnej bramki jakości.
- Dodano walidację, która blokuje narrację, że techniczne checks wystarczają bez sprawdzenia zgodności z intencją.

## 2. PROBLEMY (→ KONWERSJA)

| Problem | Przyczyna | Konwersja |
| --- | --- | --- |
| Review może być zbyt techniczny | Brak osobnej soczewki na intencję i scope | Każdy jakościowy review powinien porównać wynik z poleceniem, zaakceptowanym zakresem i acceptance criteria |
| Testy mogą przejść mimo złego kierunku | Testy sprawdzają implementację, nie zawsze cel biznesowy lub operacyjny | PASS jakościowy wymaga evidence technicznego oraz zgodności z intencją |
| Scope creep może wyglądać jak dodatkowa wartość | Brak wymogu wskazania overbuild i unapproved scope | Review musi jawnie oznaczać scope creep, overbuild i underbuild |

## 3. WZORCE

- Warto oddzielać `technical correctness` od `intent/scope correctness`.
- Najlepszy review zaczyna od pytania, czy wykonano właściwe zadanie, a dopiero potem czy wykonano je dobrze technicznie.

## 4. DECYZJE

| Treść | Wpływ |
| --- | --- |
| Review jakościowy ma sprawdzać zgodność z intencją i zaakceptowanymi źródłami zakresu | Zmniejsza ryzyko zaakceptowania technicznie poprawnego, ale merytorycznie błędnego wyniku |
| Formalny PASS jakościowy nie powinien opierać się wyłącznie na testach | Wymusza porównanie z acceptance criteria i scope |

## 5. ZASADY NA PRZYSZŁOŚĆ

| Zasada | Kiedy stosować |
| --- | --- |
| Najpierw sprawdź, czy rozwiązano właściwy problem | Każdy review, QA, final review, handoff albo odbiór zadania |
| Oddziel status techniczny od zgodności z intencją | Gdy testy przechodzą, ale istnieje ryzyko mismatchu z poleceniem lub zakresem |
| Oznacz overbuild, underbuild i scope creep jako findings | Gdy wykonanie wychodzi poza zaakceptowany zakres albo pomija wymagane elementy |

## 6. OTWARTE LUKI

- Brak aktywnego skilla jakościowego, który formalizuje tę checklistę poza kontraktem workflow.

## 7. ODRZUCONE JAKO SZUM

| Pominięte | Dlaczego |
| --- | --- |
| Konkretne nazwy repo, commity i ścieżki | To są repo-specific facts, nie przenośna lekcja operacyjna |
| Szczegóły implementacyjne walidatora | Nie są potrzebne do zastosowania zasady w innych projektach |

## 8. WALIDACJA OPERACYJNA

### co zostaje

- Jakościowy review musi sprawdzać zgodność z intencją, planem, specyfikacją, zakresem i acceptance criteria.
- Same testy techniczne nie wystarczają do potwierdzenia jakości, jeśli rezultat nie odpowiada zaakceptowanemu celowi.

### co poprawić / usunąć

- Usuwać wording sugerujący, że review techniczny jest wystarczający bez porównania z intencją.

### czego brakuje

- Kandydat na skill jakościowy z checklistą intent/scope compliance dla różnych typów pracy.
