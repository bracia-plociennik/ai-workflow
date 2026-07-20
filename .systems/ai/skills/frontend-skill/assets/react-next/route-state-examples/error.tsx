"use client";

export default function Error({ reset }: { reset: () => void }) {
  return (
    <main role="alert">
      <h2>Something went wrong.</h2>
      <button type="button" onClick={() => reset()}>Try again</button>
    </main>
  );
}
