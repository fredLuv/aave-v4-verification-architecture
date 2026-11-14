# Aave V4 Architecture & Verification Methodology

An interactive architecture explorer and compositional formal verification methodology for [`aave/aave-v4`](https://github.com/aave/aave-v4#architecture).

## Reports

1. **[Interactive Architecture Explorer (`index.html`)](https://fredluv.github.io/aave-v4-verification-architecture/)** ([source](index.html))
   - Clickable Hub-and-Spoke topology diagram (`Hub`, `Spoke`, `BabylonSpoke`, `TokenizationSpoke`, `LiquidationLogic`, `Premium`, `SharesMath`, `PositionManager`, `AaveV4ConfigEngine`, `AccessManagerEnumerable`).
   - Function-level inspector with line-verified links directly into [`aave/aave-v4`](https://github.com/aave/aave-v4).
   - Interactive **Risk Premium** greedy collateral coverage calculator and **Dutch-Auction Liquidation Bonus** explorer.

2. **[Verification Methodology Report (`methodology.md`)](methodology.md)**
   - **Context-Sliced Assume-Guarantee Verification** across 5 strata:
     - **Stratum 0**: `solc` AST & call-graph slicing along `IHubBase.sol`
     - **Stratum 1**: Compiler & `solc` AST structural gates
     - **Stratum 2**: Bytecode-bound symbolic & SMT proofs (Halmos / Certora CVL)
     - **Stratum 3**: Multi-Spoke stateful adversarial fuzzing (Foundry)
     - **Stratum 4**: Synthetic `AdversarialSpoke.sol` injection + SHA-256 `ProofKernel` receipt
   - Comparative rationale against unit tests alone, disconnected Python Z3 scripts, and un-sliced monolithic symbolic execution.

## Local Preview

```bash
python3 -m http.server 8080
# Open http://localhost:8080
```
