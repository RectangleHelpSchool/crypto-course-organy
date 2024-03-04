const OrganicToken = artifacts.require("OrganicToken");
const OrganicTokenSale = artifacts.require("OrganicTokenSale");

module.exports = async (deployer) => {
    const accounts = await web3.eth.getAccounts();
    deployer.deploy(OrganicToken, "OrganicToken", "ORG", 100000);
    const tokenInstance = await OrganicToken.deployed()
    await deployer.deploy(OrganicTokenSale, 1, accounts[0], tokenInstance.address)
    const organicTokenInstance = await OrganicTokenSale.deployed()
    await tokenInstance.transfer(organicTokenInstance.address, 1000000)
};
