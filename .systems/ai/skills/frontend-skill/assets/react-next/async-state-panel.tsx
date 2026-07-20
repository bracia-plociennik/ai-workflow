import type { ReactNode } from "react";

type AsyncStatePanelProps = {
  loading?: boolean;
  error?: string | null;
  empty?: boolean;
  children?: ReactNode;
  onRetry?: () => void;
};

export function AsyncStatePanel({ loading, error, empty, children, onRetry }: AsyncStatePanelProps) {
  if (loading) return <p role="status" aria-live="polite">Loading...</p>;
  if (error) return <section role="alert"><p>{error}</p>{onRetry ? <button type="button" onClick={onRetry}>Try again</button> : null}</section>;
  if (empty) return <p>No results yet.</p>;
  return <>{children}</>;
}
