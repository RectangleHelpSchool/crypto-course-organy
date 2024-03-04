pragma solidity >=0.8.0;


contract SuicidalContract {
    address payable _receiver;
    constructor(address payable receiver) {
        _receiver = receiver;
    }

    fallback() external payable {
        // Just receive some money
    }

    function fund_receiver() public {
        selfdestruct(_receiver);
    }
}