# Reentency Description

> Describe reentrancy in oyur own words

Reentency is a vulnarablility in smart contract in which a transaction to a vulnerable contract is sent through an attacker's contract. The attacker's contract reenters the vulnerable contract over and over again, making a certain code section run in a loop this loop will be stopped only when the attacker decides to. This may lead to draining all the funds of a contract if somewhere in the repeated code, funds are being transfered to an address.