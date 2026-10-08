# Synthetic Authorization Diff

Read-only fixture; no real application is present.

```diff
 function download(Document $document, User $actor): Response {
-    abort_unless($document->owner_id === $actor->id, 403);
     return Storage::download($document->path);
 }
```
