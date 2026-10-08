import type { ReactNode } from "react";

type GuidedRecoveryPanelProps = {
  title: string;
  description: string;
  actionLabel: string;
  onAction: () => void;
  children?: ReactNode;
};

export function GuidedRecoveryPanel({ title, description, actionLabel, onAction, children }: GuidedRecoveryPanelProps) {
  return (
    <section aria-labelledby="recovery-title">
      <h2 id="recovery-title">{title}</h2>
      <p>{description}</p>
      {children}
      <button type="button" onClick={onAction}>{actionLabel}</button>
    </section>
  );
}
