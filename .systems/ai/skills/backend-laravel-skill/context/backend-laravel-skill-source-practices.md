# Backend Laravel Skill Source Practices

## Metadata

| Field | Value |
| --- | --- |
| `project` | `backend-update` |
| `artifact-purpose` | Source material for a future `backend-laravel-skill` |
| `date` | `2026-06-16` |
| `source-root` | `backend/` |
| `product-code-changed` | `no` |
| `smartcontracts-artifacts-changed` | `no` |

## Scope Reviewed

Reviewed current backend source and support files as evidence for reusable Laravel/Backpack practices:

- `backend/app/**`: DTOs, API controllers, admin CRUD controllers, requests, middleware, mail, models, model traits, providers, services.
- `backend/routes/**`: API, web, Backpack custom routes, console.
- `backend/config/**`: application, Backpack, content/API key, Scribe, service provider config.
- `backend/database/**`: migrations, factories, seeders.
- `backend/tests/**`: feature and unit tests.
- `backend/resources/**`: Backpack custom views/fields, mail view, frontend/vendor views, language files.
- `backend/composer.json`, `backend/package.json`, `backend/phpunit.xml`, `backend/README.md`, `backend/.env.example`.

Not reviewed as source of best-practice guidance:

- `backend/.env`: real local secrets/config, intentionally not read.
- `backend/vendor/**`: third-party generated dependency code.
- `backend/storage/**`, `backend/bootstrap/cache/**`, `.scribe` generated cache/output, `backend/public/uploads/**`: generated/runtime artifacts.

High-level source shape:

- 38 admin controller files under `backend/app/Http/Controllers/Admin`.
- 37 first-party model files under `backend/app/Models`.
- 46 request files under `backend/app/Http/Requests`.
- 50 DTO files under `backend/app/DTO`.
- 13 service/interface files under `backend/app/Services`.
- 44 migration files under `backend/database/migrations`.
- 10 test files under `backend/tests`.

## Executive Summary

The strongest reusable backend pattern is:

```text
Backpack CRUD controller
  -> dedicated FormRequest
  -> Eloquent model with small reusable traits for CMS/media concerns
  -> optional DTO/service layer for API-facing reads and writes
  -> Feature/Unit tests with fake storage/mail/http where side effects exist
```

This backend is good source material for a skill because it has consistent Backpack CRUD structure, clear admin route registration,
localized admin labels, reusable model traits, API controllers that delegate to services, DTOs that stabilize API payloads,
FormRequests that normalize and validate input, Scribe documentation annotations, and focused tests for auth/profile/contact/wallet flows.

The future skill should preserve those strengths, but it must explicitly prohibit the unsafe legacy patterns that also exist here:
dynamic schema mutation from model traits, direct `env()` usage outside config, direct `curl_*`, unredacted exception e-mails, broad
`logAll()` in sensitive domains, request-dependent model mutators, and unvalidated legacy mail paths.

## Practices To Keep

### 1. Backpack Admin CRUD Structure

Good pattern:

- one `*CrudController` per admin-managed model;
- `setup()` defines model, route, and entity labels;
- `setupListOperation()` defines visible admin columns;
- `setupCreateOperation()` defines fields and attaches validation;
- `setupUpdateOperation()` usually delegates to `setupCreateOperation()`;
- only required operations are imported through Backpack operation traits.

Evidence:

- `WalletCrudController` uses `CreateOperation`, `ListOperation`, `UpdateOperation`, `BulkDeleteOperation`, `ReorderOperation`,
  `MinorUpdateOperation`, `DeleteOperation`, `CRUD::setValidation(WalletRequest::class)`, relationship field for user, `select_from_array`
  status labels, and explicit reorder config.
- `UserCrudController` keeps admin user fields explicit and uses `UserRequest`.
- `PageCrudController` uses `editable_switch`, slug field, custom `description` field, reorder, clone/delete/bulk delete operations.
- `SettingCrudController` uses tabs, repeatable phone/e-mail fields, upload fields, URL fields, and CMS-oriented long form layout.
- `ActivityLogCrudController` is read/show oriented and adds a custom CSV export button.

Skill rule:

```text
For every Backpack CRUD, generate a predictable controller skeleton:
setup -> setupListOperation -> setupCreateOperation -> setupUpdateOperation.
Use explicit operation traits. Use CRUD::setValidation(FormRequest::class).
Keep admin labels localized and field names aligned with migrations/models.
```

### 2. FormRequest Per Boundary

Good pattern:

- API and admin validation live in dedicated request classes.
- API requests normalize input in `prepareForValidation()`.
- API requests expose human-readable validation attributes.
- Admin requests authorize through Backpack auth when appropriate.
- Uniqueness constraints use `Rule::unique(...)->ignore(...)` and scoped uniqueness when needed.

Evidence:

- `RegisterUserRequest` trims name, lowercases e-mail, validates unique e-mail, confirmed complex password, and localized attributes.
- `LoginUserRequest` lowercases e-mail before validation.
- `UpdateCurrentUserRequest` normalizes wallet arrays, trims user fields, has `withValidator()` to reject empty updates, and requires
  `current_password`.
- `StoreCurrentUserWalletRequest` defaults wallet status to connected and normalizes wallet strings.
- `WalletRequest` enforces wallet uniqueness by `wallet_address` plus `network`.
- `ApiFormRequest` centralizes JSON validation errors and localized base messages.

Skill rule:

```text
Never validate significant API/admin payloads in controllers.
Create a FormRequest, normalize strings in prepareForValidation, localize attributes, and keep failed JSON shape consistent.
```

### 3. Thin API Controllers With Services

Good pattern:

- API controllers receive service interfaces through constructor injection.
- Controllers keep response composition and HTTP status handling.
- Business actions live in services.
- `AppServiceProvider` binds interfaces to implementations.

Evidence:

- `AuthController` delegates register/login/logout to `UserAuthServiceInterface`.
- `UserController` delegates profile/wallet/delete flows to `UserProfileServiceInterface`.
- `StaticContentController`, `FirstContentController`, `PageController`, `LoginController`, and `DashboardController` use service interfaces.
- `AppServiceProvider` binds `StaticContentServiceInterface`, `PageServiceInterface`, `LoginServiceInterface`,
  `DashboardServiceInterface`, `UserAuthServiceInterface`, and `UserProfileServiceInterface`.

Skill rule:

```text
For non-trivial API behavior: Controller -> FormRequest -> ServiceInterface -> Service -> DTO.
Keep controllers free of database orchestration, storage cleanup, token generation, and provider calls.
```

### 4. DTOs For Stable API Payloads

Good pattern:

- DTOs isolate API response shape from Eloquent internals.
- Auth DTOs implement `Arrayable` and expose `toArray()`.
- Content DTOs use `final readonly class` where mutability is not needed.
- DTO factories use `fromModel()` and handle naming conversion to frontend-friendly camelCase.

Evidence:

- `UserDTO`, `UserWalletDTO`, and `AuthResponseDTO` expose typed constructor properties and `toArray()`.
- `SettingDTO`, `SectionsDTO`, and other content DTOs map CMS fields to stable response names.
- `StaticContentService` and dashboard/login/page services return arrays/collections of DTOs instead of raw models.

Skill rule:

```text
Expose API payloads through DTOs or resources.
Do not return raw Eloquent models for public API contracts unless explicitly intended.
```

### 5. Reusable Model Traits For CMS Concerns

Good pattern to keep carefully:

- `PhotoTrait` centralizes image upload, resizing, cleanup, and optional WebP creation.
- `FileTrait` centralizes common file upload mutators.
- `MutatorTrait` centralizes repeatable/gallery image processing.
- `LogTrait` centralizes Spatie Activitylog options.

Why this is useful:

- CRUD controllers remain focused on fields and operations.
- Models with similar media fields do not duplicate upload handling.
- CMS editors get consistent image/file behavior.
- Audit logging is attached uniformly to content models.

Skill rule:

```text
Use traits for narrow, repeatable CMS/model concerns only when the trait has one responsibility and documented side effects.
For sensitive domains, prefer explicit services over model mutator traits.
```

### 6. API Security And Abuse Controls

Good pattern:

- Public content/auth/user API routes are grouped behind `ApiKeyMiddleware` and rate limiting.
- Auth uses Laravel Sanctum tokens.
- Login/register/delete have named rate limiters in `AppServiceProvider`.
- Contact form uses honeypot field, reCAPTCHA verifier, mail fake tests, and service-unavailable response when mailbox is missing.

Evidence:

- `routes/api.php` wraps content/auth/user routes in `ApiKeyMiddleware` and `throttle:60,1`.
- Auth register/login use `throttle:auth-register` and `throttle:auth-login`.
- User delete uses `throttle:user-delete`.
- `RecaptchaVerifier` uses Laravel `Http` facade and configurable score threshold.
- `ContactSubmitRequest` rejects honeypot `company`.

Skill rule:

```text
Every public API group must declare its auth boundary, rate limit, and response shape.
Use Laravel HTTP client/fakes for external verification, not raw cURL.
```

### 7. Test Shape Worth Reusing

Good pattern:

- Feature tests use `RefreshDatabase`.
- API tests assert status codes, JSON paths, validation errors, auth requirements, and database side effects.
- Tests fake storage, mail, and external HTTP when side effects exist.
- `phpunit.xml` configures in-memory SQLite, array cache/session/mail, sync queues, and low bcrypt rounds for fast tests.

Evidence:

- `AuthTest` covers API key requirement, register, login, invalid credentials, Polish validation errors.
- `CurrentUserTest` covers profile read/update/delete, token revocation, storage fake, password update, e-mail verification reset.
- `StoreCurrentUserWalletTest` and `CurrentUserWalletUniquenessTest` cover auth and wallet uniqueness.
- `ContactSubmitTest` covers recaptcha success/failure with `Http::fake()` and `Mail::fake()`.
- `StaticContentServiceCacheTest` checks cache usage.

Skill rule:

```text
For every backend feature, add Feature tests around public behavior and Unit tests around reusable services.
Use Storage::fake, Mail::fake, Http::fake, RefreshDatabase, and explicit JSON assertions.
```

### 8. Documentation Pattern

Good pattern:

- API endpoints use Scribe docblocks with `@group`, auth notes, headers, body params, and response files.
- `config/scribe.php` defines auth, API key explanation, `/api/docs`, Postman/OpenAPI output, and included API route prefixes.
- Generated docs are visible under `/api/docs`.

Skill rule:

```text
For API endpoints, update Scribe annotations alongside controller/request changes.
Docs should describe auth headers, body params, response files, and examples.
```

## Practices To Improve Or Remove

### 1. Remove Dynamic Schema Changes From Models

Problem:

- `DatabaseTrait` runs on `creating` and `updating`.
- It checks the current request and creates missing columns in the model table.
- It can create tables or columns at runtime based on request keys.

Why this is dangerous:

- Database schema becomes mutable from HTTP/admin input.
- Changes bypass migrations, review, rollback, tests, and deployment planning.
- Request field mistakes become production columns.
- This is unacceptable for financial/blockchain/KYC/provider domains.

Replace with:

- explicit migrations;
- JSON columns for flexible CMS content when needed;
- reviewed schema changes with tests;
- admin field config that maps only to known columns.

Skill rule:

```text
Never create or alter database schema from a model, trait, request, controller, observer, or runtime admin action.
Only migrations may define schema.
```

### 2. Limit Request-Dependent Model Mutators

Problem:

- `PhotoTrait` and `MutatorTrait` call `request()->getSchemeAndHttpHost()`.
- `DatabaseTrait` reads `request()->except(...)`.
- Traits query settings directly from DB inside mutators.

Why this is fragile:

- Models become coupled to HTTP runtime.
- CLI jobs, queues, tests, imports, seeders, and future indexers can behave differently.
- Side effects are hidden inside assignment.

Keep only for current low-risk CMS media if needed. For new backend-update blockchain/provider work, use explicit services/actions.

Skill rule:

```text
Do not put request-dependent or provider-dependent behavior in Eloquent mutators for domain-critical models.
Use services with explicit input/output and tests.
```

### 3. Replace `env()` Outside Config

Problem evidence:

- `MailController` reads `env('GOOGLE_RECAPTCHA_SECRET')`.
- `ContactMail` reads `env('MAIL_FROM_ADDRESS')` and `env('APP_NAME')`.
- `SeoCrudController` uses `env('APP_URL')`.
- `Handler` sends to `env('DEV_EMAIL')`.

Why this is weak:

- Laravel config caching can make direct `env()` calls unreliable.
- It spreads secret/config access across app code.
- It is harder to test and override cleanly.

Replace with:

- `config('services.recaptcha.secret')`;
- `config('mail.from.address')`;
- `config('app.name')`;
- dedicated `config('content.*')` or `config('ops.*')` values.

Skill rule:

```text
Use env() only in config files. Application code reads config().
```

### 4. Retire Legacy Mail/Helper Paths

Problem evidence:

- `MailController` validates manually, uses raw `Request`, calls `Helper::validReCaptcha`, allows request-provided recipient/BCC,
  and may return nothing when blacklist rejects an e-mail.
- `Helper::validReCaptcha` uses raw `curl_*`.
- `ContactController` and `RecaptchaVerifier` are the better replacement pattern.

Replace with:

- `ContactSubmitRequest`;
- `RecaptchaVerifier` using Laravel `Http`;
- explicit recipient from trusted config/CMS only;
- queued mail if production traffic grows;
- response tests for every branch.

Skill rule:

```text
Do not create new generic Helper-based request flows.
Use FormRequest + service + Laravel facade/client with fakes in tests.
```

### 5. Sanitize Error Reporting

Problem evidence:

- `Handler::sendErrorEmail()` includes exception message, file, line, full trace, and `request()` object.
- It sends directly to `env('DEV_EMAIL')`.
- Subject still says `Budmat`, which looks like copied legacy naming.

Risk:

- PII, auth headers, API keys, wallet data, or provider payloads could be exposed in e-mail.
- Direct mail inside exception reporting can fail or amplify incidents.

Replace with:

- Laravel logging channels / Sentry-like provider / queued sanitized notifications;
- redaction rules for headers, tokens, provider payloads, KYC, wallets, and request bodies;
- config-based recipient;
- tests for redaction if custom reporting remains.

Skill rule:

```text
Never e-mail raw request objects, full traces, headers, secrets, KYC payloads, wallet payloads, provider payloads, or private data.
```

### 6. Align PHP Version And Syntax

Problem evidence:

- `composer.json` requires `"php": "^8.2"`.
- README says PHP 8.4.
- Service interfaces use typed class constants such as `CONST STRING CACHE_KEY`, which require newer PHP support than plain PHP 8.2.

Fix:

- choose one runtime baseline;
- make composer, README, CI, deployment, and syntax match;
- if PHP 8.2 is required, use untyped constants: `public const CACHE_KEY = '...'`.

Skill rule:

```text
Generated code must fit the project's declared PHP version, not the developer's local version.
```

### 7. Tighten Migrations And Rollbacks

Problem evidence:

- `2026_05_08_000000_add_profile_fields_to_users_table.php` adds `referral_code` and `photo_webp`, but `down()` does not drop them.
- `2025_07_20_164743_create_footer_link_table.php` creates `footer_links` but drops `footer_link`.
- Some CMS tables use broad `text` fields for many scalar values.

Fix:

- keep `up()` and `down()` symmetric;
- test migration rollback on disposable DB;
- use column types that match semantics;
- add unique/index/foreign constraints where domain rules require them.

Skill rule:

```text
Every migration must have a safe rollback or an explicit irreversible-migration note.
Rollback table/column names must exactly match.
```

### 8. Prefer Explicit Mass Assignment On Sensitive Models

Good current exceptions:

- `User` and `Wallet` define explicit `$fillable`.

Weak legacy pattern:

- many CMS models use `protected $guarded = ['id'];`.

Guidance:

- `guarded` can be acceptable for low-risk CMS-only models when admin fields are tightly controlled.
- New auth, KYC, wallet, blockchain, transaction, provider, audit, and evidence models must use explicit `$fillable` or controlled write methods.

Skill rule:

```text
For sensitive or domain-critical models, never use broad guarded-only mass assignment.
Use explicit fillable fields and service-level writes.
```

### 9. Standardize Statuses And Magic Integers

Problem evidence:

- `kyc_status` values `0..3` and `wallet_status` values `0..1` are repeated across CRUD controllers, requests, DTOs, services, tests,
  and Scribe docs.

Fix:

- introduce PHP enums or constants with labels;
- centralize admin options and API serialization labels;
- keep database values stable but stop duplicating the meaning everywhere.

Skill rule:

```text
When a status appears in more than one layer, define it once as enum/constant plus label map.
```

## Missing Best Practices To Add

- Policies/abilities for admin operations beyond `is_admin`; especially needed before KYC/provider/wallet/blockchain admin work.
- API Resources or a consistent DTO/resource convention across all endpoints; current DTOs are good, but not uniformly shaped.
- Explicit OpenAPI/Scribe generation check in CI or release workflow.
- Static analysis (`phpstan`/Larastan or Psalm) and stricter Pint/style checks.
- Admin CRUD tests or at least smoke tests for route access, validation, and file upload fields.
- Service-level tests for `UserAuthService`, `UserProfileService`, contact flow, DTO mapping edge cases, and cache invalidation.
- Queue boundaries for mail and future provider/webhook side effects.
- Central file upload policy: allowed MIME/extensions, image dimensions, disk, cleanup, SVG handling, virus scanning if uploads become user-facing.
- Redaction policy for logs, activity logs, error reports, provider webhooks, KYC state, wallet addresses, API keys, and auth tokens.
- Cache invalidation strategy for CMS content; current version/TTL pattern exists, but admin save invalidation is not visible.
- Domain folders/namespaces for future CHT integration, e.g. `App\Domains\Cht\...`, to avoid mixing blockchain/provider code into CMS services.
- Reusable API response envelope/helper to avoid manually repeating `data` and `version`.
- Consistent current-user authorization and ownership checks for nested resources.
- Migration rollback tests on disposable DB before schema-heavy backend-update packages.

## Negative Practices: Do Not Do This

These should become hard rules in the future skill:

- Do not read or write real `.env` values into docs, artifacts, logs, tests, or generated code.
- Do not use `env()` outside config files.
- Do not mutate database schema from models, traits, controllers, requests, observers, seeders, or admin runtime.
- Do not let request keys create database columns.
- Do not put provider calls, contract reads/writes, wallet signing, or KYC authority inside Eloquent mutators.
- Do not store issuer/admin private keys, seed phrases, provider secrets, KYC documents, or raw provider payloads in app tables unless a spec explicitly allows and secures it.
- Do not e-mail full request objects, full traces, headers, tokens, or private data.
- Do not use raw `curl_*` for HTTP integrations when Laravel `Http` client can be faked and tested.
- Do not let frontend/user input choose mail recipients, BCC recipients, provider callback URLs, chain IDs, contract addresses, or admin action targets without allowlists and authorization.
- Do not use broad `logAll()` on sensitive domains without redaction.
- Do not treat provider state, cache state, admin form state, or indexed state as contract truth.
- Do not create backend-calculated CHT economics; future CHT backend must preserve contract-derived truth.
- Do not introduce admin/provider/blockchain work without tests for auth, authorization, validation, idempotency, provenance, and failure paths.
- Do not rely on generated docs, generated caches, uploads, logs, or vendor code as source-of-truth for implementation.

## Skill Seed: Recommended Rules

Use these as direct seed rules for `backend-laravel-skill`:

1. For admin CRUD, prefer Backpack `CrudController` with explicit operation traits, localized labels, `CRUD::setValidation`, and separate list/create/update methods.
2. For API features, use `Controller -> FormRequest -> ServiceInterface -> Service -> DTO/API Resource -> Feature tests`.
3. For request validation, always create FormRequests, normalize input in `prepareForValidation`, and centralize API validation JSON through a base API request.
4. For responses, return a consistent envelope: `data` plus metadata such as `version` when already established by the app.
5. For services, bind interfaces in a service provider and keep side effects explicit and testable.
6. For external integrations, use adapter/service classes and Laravel fakes (`Http::fake`, `Mail::fake`, `Storage::fake`).
7. For models, use explicit `$fillable` for sensitive domains; use traits only for narrow CMS/media concerns.
8. For file uploads, validate MIME/size, use configured disks, clean up old files, and test with `Storage::fake`.
9. For migrations, write reversible migrations with exact rollback names and test on disposable DB.
10. For docs, keep Scribe annotations and response examples current with route/request changes.
11. For tests, cover auth, API key, validation, ownership, persistence, side effects, and failure paths.
12. For secrets/config, application code reads `config()`, never direct `env()`.
13. For backend-update/CHT work, separate CMS patterns from financial/blockchain patterns: no runtime schema mutation, no backend custody, no provider-state-as-truth.

## Evidence

- artifacts-reviewed: PASS - current backend source, routes, config, migrations, resources, tests, README, and `.env.example` were reviewed.
- manual-checks: PASS - reusable strengths, improvement areas, missing practices, and negative practices were derived from current code examples.
- command: PASS - `find backend/app -type f`, `find backend/routes backend/config backend/database backend/tests -type f`, and targeted `rg` searches were used to cover first-party source areas.
- command: PASS - real `backend/.env` was intentionally not read.

## Suggested Next Use

Use this artifact as raw source material for a future `backend-laravel-skill` intake. The skill should not blindly copy the current backend;
it should preserve the strong CRUD/API/testing patterns and convert the weaknesses above into explicit "never do" and "prefer this" rules.
