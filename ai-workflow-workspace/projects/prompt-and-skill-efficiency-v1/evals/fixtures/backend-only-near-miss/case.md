# Synthetic Laravel Review Target

Read-only fixture. Neither class belongs to a deployed application.

```php
final class TransferRequest extends FormRequest
{
    public function authorize(): bool { return $this->user() !== null; }

    public function rules(): array
    {
        return [
            'account_id' => ['required', 'integer'],
            'amount' => ['required', 'integer', 'min:1'],
        ];
    }
}

final class TransferService
{
    public function execute(User $actor, array $validated): void
    {
        $account = Account::findOrFail($validated['account_id']);
        $account->balance -= $validated['amount'];
        $account->save();
        Transfer::create([
            'actor_id' => $actor->id,
            'account_id' => $account->id,
            'amount' => $validated['amount'],
        ]);
    }
}
```
