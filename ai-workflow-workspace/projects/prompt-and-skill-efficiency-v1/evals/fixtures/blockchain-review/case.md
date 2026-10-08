# Synthetic Solidity Review Target

Read-only fixture. Do not deploy or contact a chain provider.

```solidity
pragma solidity ^0.8.24;

contract Escrow {
    mapping(address => uint256) public balances;
    bool public refundsOpen;

    function deposit() external payable { balances[msg.sender] += msg.value; }

    function openRefunds() external { refundsOpen = true; }

    function refund() external {
        require(refundsOpen, "closed");
        uint256 amount = balances[msg.sender];
        require(amount > 0, "empty");
        (bool ok,) = msg.sender.call{value: amount}("");
        require(ok, "send failed");
        balances[msg.sender] = 0;
    }
}
```
