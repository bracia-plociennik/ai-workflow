# Contract Topology Map

## Purpose

The Contract Topology Map is an advisory inventory of relationships between
core contracts, routers, validators, smoke tests, templates, producers, and
consumers. It helps find partial or orphaned wiring without becoming a new
phase gate.

Generate it with:

```sh
.systems/scripts/report-contract-topology --output <workspace-or-tmp-path>
```

Each contract is classified as `linked`, `partial`, `orphaned`, or `unknown`.
The report identifies producers and consumers where a field or artifact crosses
a boundary. Topology findings are always advisory. A real conflict in
repository state, permissions, risk, evidence, or phase gates still follows
the existing stop conditions.
