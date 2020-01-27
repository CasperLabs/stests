1.  create accounts:

    - 1 faucet
    - 1 contract owner
    - N users

    - create a key pair
    - cache new account

2.  fund accounts

    - transfer 10e8 validator --> faucet
    - transfer 10e7 faucet --> contract owner
    - transfer 10e7 faucet --> user(s)

    - payment-amount = 10e7
    - gas-price 1
    - validator private key pem file
    - validator public key (hex)
    - faucet private key pem file
    - faucet public key (hex)
    - user public key (hex)

3.  deploy ERC20 contract

    - open wasm 
    - deploy wasm
    - dispatch signed deploy
    - cache uref

    - contract-owner private key pem file
