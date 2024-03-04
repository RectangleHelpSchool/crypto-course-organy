
const EmptyContract = artifacts.require("EmptyContract");
const SuicidalContract = artifacts.require("SuicidalContract");

async function sendEther(fromAddress, privateKey, toAddress, amountInEther) {
    try {
      const value = web3.utils.toWei(amountInEther.toString(), 'ether');
      const gasPrice = await web3.eth.getGasPrice();
  
      const transaction = {
        from: fromAddress,
        to: toAddress,
        value,
        gasLimit: 2181270,
        gasPrice,
      };
  
      const signedTx = await web3.eth.accounts.signTransaction(transaction, privateKey);
      console.log("rawTx: ", signedTx)
      const txHash = await web3.eth.sendSignedTransaction(signedTx.rawTransaction);
  
      console.log(`Transaction hash: ${txHash}`);
      return txHash;
  
    } catch (error) {
      console.error("Error transferring Ether:", error);
      throw error;
    }
  }
  


module.exports = async (deployer) => {
    // Create the empty contract 
    await deployer.deploy(EmptyContract);
    let emptyContractInstance = await EmptyContract.deployed();
    const emptyContractAddress = emptyContractInstance.address;
    console.log("Address is: ", emptyContractAddress);

    // Create the suicidal contract
    await deployer.deploy(SuicidalContract, emptyContractAddress);

    let suicidalContract = await SuicidalContract.deployed();
    const suicidalContractAddress = suicidalContract.address

    const PRIVATE_KEY = "0xdea09ca9ee451ff590c0c62e2e269488caf3f882b0a5c3e9dcb1ca552541da23";
    const FROM_ADDRESS = "0x50DA4998c366d7026C6E688B49CE109f462B703B";
    const AMOUNT = 10;

    // Move funds to suicidal contract
    await sendEther(FROM_ADDRESS, PRIVATE_KEY, suicidalContractAddress, AMOUNT);

    // Make the suicidal contract suicide and fund the unpayable contract
    await suicidalContract.methods["fund_receiver()"].sendTransaction()
};
