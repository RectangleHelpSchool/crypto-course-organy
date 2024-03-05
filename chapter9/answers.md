# Answers

Answers to the questions asked in this chapter.

## 1 - Reentency Description

> Describe reentrancy in oyur own words

Reentency is a vulnarablility in smart contract in which a transaction to a vulnerable contract is sent through an attacker's contract. The attacker's contract reenters the vulnerable contract over and over again, making a certain code section run in a loop this loop will be stopped only when the attacker decides to. This may lead to draining all the funds of a contract if somewhere in the repeated code, funds are being transfered to an address.

## 2 - Underflow
> Describe how solidity 0.8 approaches this problem

Before solitiy 0.8, contract developers had 2 options:
1) Use the regular operators (multiplication, division, addition, etc...) and hope not to experience overflows/underflows.
2) Use the openzeppelin's SafeMath library which was used as follows:

```solidity
pragma solidity ^0.7.0;

import "@openzeppelin/contracts/math/SafeMath.sol";

contract MyContract {
  using SafeMath for uint256;

  function add(uint256 a, uint256 b) public pure returns (uint256) {
    // Use SafeMath's add function with overflow check
    return a.add(b);
  }
  // ...
}
```


SafeMath validates during runtime that the value does not overflow, and if it does, it calls `revert` to terminate the prodcut and ensure there's no effect.

In solidity 0.8, this behavior is built in, there's bytecode defaultly added to each operation that validates overflows/underflows do not occur.

## 3 - Unexpected Ether 



