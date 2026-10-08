# 2026-06-17 - Agent Tooling Balanced-Safety Setup

- Date: `2026-06-17`
- Category: `process`
- Status: `accepted`
- Source scope: `owner-approved capture`
- Privacy check: `confirmed no raw client data, client names, secrets, repo-specific facts, project-specific details, or production identifiers`
- Skill candidate: `yes`
- Suggested skill target: `AI_WORKFLOW_WORKSPACE_HOME/skills/agent-tooling-configuration`

## TEMAT

- `Proces - konfiguracja narzędzi agentowych`

## 0. SYGNAŁY

- Konfiguracja narzędzia agentowego powinna rozdzielać core safety, lokalną ergonomię, UI-only settings i instrukcje tekstowe.
- Clean template od zera jest lepszy do decyzji i wdrożenia niż pełny snapshot lokalnego configu.
- Legacy snapshot jest nadal wartościowy jako źródło lokalnych braków, rollbacku i selektywnego merge.
- Globalne custom instructions powinny być krótkim safety shimem, nie kopią repo workflow.
- Commit i PR instructions powinny wymuszać evidence, scope, risk i brak ukrytych skipów.
- MCP/tools powinny mieć domyślne stany zgodne z profilem, ale owner może jawnie zaakceptować wyjątki.
- Smoke test po wdrożeniu musi sprawdzać zarówno parse configu, jak i faktyczny stan narzędzi.

## 1. CO ZOSTAŁO FAKTYCZNIE ZROBIONE

- Utworzono clean balanced-safety config template.
- Zachowano pełny legacy snapshot jako materiał porównawczy.
- Przygotowano checklistę wdrożenia UI i config.
- Przygotowano zoptymalizowane commit instructions.
- Przygotowano zoptymalizowane pull request instructions.
- Przygotowano globalne custom instructions z zasadą supporting-context-only.
- Po owner-applied setup wykonano read-only smoke test.
- Zidentyfikowano i zaakceptowano owner-approved wyjątek dla jednego narzędzia MCP.

## 2. PROBLEMY (→ KONWERSJA)

| Problem | Przyczyna | Konwersja |
| --- | --- | --- |
| Pełny snapshot configu mieszał safety baseline z lokalnym stanem aplikacji. | Snapshot zawierał ścieżki, cache, pluginy, projekty i preferencje lokalne. | Twórz clean template jako aktywny baseline, a snapshot trzymaj jako legacy/rollback. |
| Nadpisanie configu może usunąć lokalną ergonomię. | Wdrożenie template'u bez merge pomija sekcje lokalne. | Po wdrożeniu sprawdzaj brakujące sekcje i decyduj selektywnie, co przywrócić. |
| Custom instructions mogą duplikować albo osłabiać repo contract. | Globalna personalizacja ładuje się szeroko i może wejść przed repo guidance. | Trzymaj custom instructions jako krótki safety shim; repo zasady zostaw w repo guidance. |
| Domyślne stany narzędzi mogą być zbyt restrykcyjne lub zbyt szerokie. | Różne przepływy pracy wymagają różnych integracji. | Zapisz default, a wyjątki rób jako jawne owner decisions. |

## 3. WZORCE

- Najpierw clean baseline, potem legacy comparison, potem owner decisions, potem smoke test.
- Instrukcje globalne powinny mówić jak pracować, a nie co repo konkretnie wymaga.
- Bezpieczne wdrożenie configu wymaga zarówno testu składni, jak i testu widocznego runtime state.

## 4. DECYZJE

| Treść | Wpływ |
| --- | --- |
| Clean balanced-safety template jest aktywnym baseline. | Upraszcza przyszłe wdrożenia i redukuje ryzyko kopiowania lokalnego bałaganu. |
| Legacy snapshot zostaje tylko jako comparison/rollback. | Zachowuje lokalną wiedzę bez mieszania jej z rekomendowanym baseline. |
| Custom instructions zostają krótkie. | Repo contracts i workflow gates nie są dublowane ani osłabiane globalną personalizacją. |
| Supporting context nigdy nie nadpisuje explicit instruction, repo state, AGENTS.md, safety policy ani evidence. | Zmniejsza ryzyko prompt injection i błędnej hierarchii źródeł. |
| Owner-approved wyjątki od defaultów narzędzi są dozwolone po smoke teście. | Pozwala zachować ergonomię bez udawania, że default nadal obowiązuje bez wyjątku. |

## 5. ZASADY NA PRZYSZŁOŚĆ

| Zasada | Kiedy stosować |
| --- | --- |
| Twórz clean config baseline niezależnie od legacy snapshotu. | Przy optymalizacji ustawień narzędzia, które już ma lokalny config. |
| Zachowuj legacy snapshot jako materiał porównawczy, nie jako aktywny template. | Gdy istnieją stare ustawienia z lokalnymi integracjami lub historią. |
| Globalne custom instructions ogranicz do stylu pracy, safety i source hierarchy. | Przy personalizacji narzędzi agentowych używanych w wielu repozytoriach. |
| Commit/PR instructions powinny wymagać scope, validation, risk i disclosure skipped checks. | Przy ustawianiu globalnego systemu commitów i PR-ów. |
| Każde realne wdrożenie ustawień kończ smoke testem runtime state. | Po zmianie configu, MCP, UI permissions, hooks, memory lub custom instructions. |
| Owner-approved wyjątek zapisuj jawnie jako wyjątek, nie jako niewykryty drift. | Gdy świadomie odchodzisz od rekomendowanego defaultu. |

## 6. OTWARTE LUKI

- Brak długoterminowej walidacji po kilku dniach realnej pracy.
- Brak decyzji, czy utworzyć dedykowany skill dla konfiguracji narzędzi agentowych.
- UI-only settings wymagają okresowej kontroli w aplikacji, nie tylko przez plik config.

## 7. ODRZUCONE JAKO SZUM

| Pominięte | Dlaczego |
| --- | --- |
| Konkretne lokalne ścieżki, nazwy projektów i plugin cache | Są lokalnym stanem, nie reusable operating lesson. |
| Pełna treść configu użytkownika | Zawiera szczegóły środowiska i nie jest potrzebna do zasady. |
| Screenshot-level detale UI | Nie są wymagane do odtworzenia procesu decyzyjnego. |

## 8. WALIDACJA OPERACYJNA

### co zostaje

- Clean baseline plus legacy snapshot jako para artefaktów.
- Smoke test obejmujący parse configu, runtime MCP state, hooks surface, repo cleanliness i instruction presence.
- Global custom instructions jako krótki safety shim.
- Commit/PR instructions z explicit evidence/risk/skipped-check rules.

### co poprawić / usunąć

- Nie kopiować pełnego legacy configu jako rekomendowanego template.
- Nie robić z lokalnych wyjątków cichych zmian baseline.
- Nie wkładać pełnego repo workflow contract do globalnych custom instructions.

### czego brakuje

- Obserwacja friction points po realnym użyciu.
- Decyzja, czy proces konfiguracji narzędzi agentowych powinien stać się lokalnym skillem.
- Periodic review checklist dla driftu między realnym configiem, clean baseline i owner-approved wyjątkami.
