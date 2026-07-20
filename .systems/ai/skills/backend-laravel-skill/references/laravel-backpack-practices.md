# Laravel And Backpack Practices

Use this reference for detailed Laravel/Backpack implementation, QA, and review decisions after `backend-laravel-skill` triggers.

## Backend Shape

- Current backend is Laravel with Backpack admin, Sanctum auth, DTO-heavy API responses, FormRequests, services/interfaces, migrations, factories, and Pest/PHPUnit tests.
- Strong local pattern: Backpack CRUD controller -> dedicated FormRequest -> Eloquent model -> optional DTO/service layer -> focused tests.
- Preserve current conventions unless an accepted spec requires a new domain namespace such as `App\Cht\...`.

## API Implementation Rules

- Implement non-trivial API behavior through `Controller -> FormRequest -> ServiceInterface -> Service -> DTO/API Resource`.
- Bind service interfaces in a service provider.
- Keep controllers limited to request receipt, service calls, and response construction.
- Normalize strings and defaults in `prepareForValidation()`.
- Put validation attributes and API-friendly validation errors in FormRequests.
- Return stable public payloads through DTOs/resources with frontend-facing naming.
- Do not let Backpack field config define API response shape.
- Every public API group must declare auth boundary, rate limit, and response shape.

## Backpack CRUD Rules

- Use one `*CrudController` per admin-managed model.
- Keep the controller skeleton predictable: `setup()`, `setupListOperation()`, `setupCreateOperation()`, `setupUpdateOperation()`.
- Use explicit Backpack operation traits. Do not import operations that are not needed.
- Use `CRUD::setValidation(FormRequest::class)`.
- Keep admin labels localized and field names aligned with migrations and model fillable/casts.
- Use Backpack only for admin surfaces; never infer public API contracts from Backpack.

## Models And Domain Logic

- Keep models focused on relationships, casts, scopes, and explicit mass-assignment boundaries.
- Use traits only for narrow, repeatable CMS/media concerns with understood side effects.
- For sensitive or domain-critical models, prefer explicit `$fillable` and service-level writes.
- Do not put request-dependent, provider-dependent, contract-dependent, or side-effectful behavior in Eloquent mutators.
- When a status appears in multiple layers, centralize it as an enum/constant plus label map.

## Migrations And Schema

- Schema changes must be migrations, never runtime model/controller/request logic.
- Prefer additive migrations by default.
- Keep `up()` and `down()` symmetric when reversibility is possible.
- Add indexes, unique constraints, foreign keys, and nullability that match domain rules.
- For irreversible migrations, require an explicit note, owner approval when risk requires it, and impact/rollback handling.
- Test schema changes on disposable local/test DB only unless owner explicitly approves another environment.

## Config, Secrets, And Integrations

- Application code reads `config()`, not `env()`.
- External integrations use services/adapters and Laravel fakes such as `Http::fake()`, `Mail::fake()`, and `Storage::fake()`.
- Do not use raw `curl_*` for new HTTP integrations.
- Never expose or persist secrets, provider tokens, private keys, seed phrases, KYC documents, raw provider payloads, auth headers, or unredacted traces.
- Do not let frontend/user input choose mail recipients, BCC recipients, provider callback URLs, chain IDs, contract addresses, or admin action targets without allowlists and authorization.

## Tests And Evidence

- Feature tests should assert status codes, JSON paths, validation errors, auth requirements, ownership, persistence, and side effects.
- Unit tests should cover reusable services, DTO mapping, cache behavior, status mapping, and edge cases.
- Use `RefreshDatabase`, `Storage::fake()`, `Mail::fake()`, and `Http::fake()` where relevant.
- For file uploads, validate MIME/size, disk, cleanup behavior, and SVG/user-supplied file risks.
- For API docs, keep Scribe annotations and response examples aligned with route/request changes.
- Do not mark PASS without concrete command/manual evidence.

## Negative Patterns To Avoid

- Runtime database schema mutation from models, traits, controllers, requests, observers, seeders, or admin actions.
- Direct `env()` calls outside config files.
- Raw `curl_*` instead of Laravel HTTP client.
- Raw Eloquent models as public API contracts.
- Business logic in controllers.
- Validation in controllers.
- Request-dependent model mutators for domain-critical behavior.
- Unredacted exception e-mails or full request/trace logging.
- Broad `logAll()` on sensitive domains without redaction.
- Backend-calculated CHT economics.
- Provider, cache, admin, or indexed state treated as smart-contract truth.

## Review Checklist

- Contract respected and response shape deterministic.
- FormRequest present for significant input.
- DTO/resource mapping complete.
- Controller thin and service/domain logic explicit.
- Migration reversible or explicitly gated.
- Auth, ownership, rate limits, validation, idempotency, and redaction covered where relevant.
- Tests and skipped-check impact recorded.

