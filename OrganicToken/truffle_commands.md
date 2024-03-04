# Truffle commands

Followed [this guide](https://dev.to/willkre/create-deploy-an-erc-20-token-in-15-minutes-truffle-openzeppelin-goerli-33lb})

Start developer console using the "truffle develop" command

## Deploy the contract

```bash
compile 
migrate --reset

# Now the contract can be interacted locally as follows:
truffle(develop)> token = await MyToken.deployed();
truffle(develop)> name = await token.name();
'OrganicToken'
truffle(develop)> symbol = await token.symbol();
'MYT'
truffle(develop)> decimals = (await token.decimals()).toString()
'18'

# Upload the contract to goerli network
migrate --reset --network goerli
```