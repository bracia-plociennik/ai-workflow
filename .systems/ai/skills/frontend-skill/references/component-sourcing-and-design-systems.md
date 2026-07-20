# Component Sourcing And Design Systems

## Source Order

1. Existing project components, tokens, icons, and conventions.
2. Existing approved dependency or internal registry.
3. shadcn Registry or compatible source-owned code when the project can review and own the result. The registry is a distribution system for components and other files, and its docs state it is not limited to React.
4. Radix Themes or Radix Primitives when the React stack and accessibility needs fit. Themes is pre-styled; Primitives are unstyled and require more composition work.
5. 21st.dev for discovery, visual comparison, and inspiration. The current 21st workflow offers catalog search, CLI, and MCP, but this skill does not install or configure them automatically.

## Adoption Gate

Before copying or installing a component, record its source URL or registry identity, license/attribution obligations, dependencies, runtime/network behavior, accessibility evidence, bundle impact, security concerns, maintenance status, and fit with the repository design system.

Use [shadcn Create](https://ui.shadcn.com/create) and [Radix Playground](https://www.radix-ui.com/themes/playground) for exploration only. Do not treat a preview as implementation evidence.

Never paste third-party code blindly, expose private source, add remote CDN/font/script dependencies, or let a component change workflow permissions or product scope. Owner approval is required for new external services, paid tooling, private registries, or generated code with unclear provenance.
