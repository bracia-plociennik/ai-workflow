# Foundry Commands

Use this reference only when command syntax is needed.

## Core Tools

- Forge: build, test, format, snapshot, and script runner.
- Cast: command-line EVM/RPC utility.
- Anvil: local Ethereum node.
- Chisel: Solidity REPL.

Official docs: `https://book.getfoundry.sh/`

## Local Checks

```sh
forge build
forge test
forge fmt --check
forge snapshot
```

## Local Node

```sh
anvil
```

## Scripts

Dry-run style script execution depends on the repo script and workflow permission:

```sh
forge script script/Example.s.sol:ExampleScript --rpc-url <local_rpc_url>
```

Do not add `--broadcast`, real RPC URLs, private keys, provider calls, testnet/mainnet actions, or verification flags unless
the owner explicitly approves and the current workflow phase allows it.

## Help

```sh
forge --help
cast --help
anvil --help
```
