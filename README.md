# Trend Micro Deep Security Migrator

Moves settings to the cloud.... at some point

Please do some code review if you want :)

## To Set Up MVP
1. Install the `.whl` file from the [releases page](https://github.com/beattheprose/ds-migrator/releases)
2. Run `pip install </path/to/.whl>`
3. Set the following environment variables: 
    - OLD_HOST originating tenant url (e.g. https://192.168.1.1:4119/) 
    - OLD_API_KEY originating tenant 'full access' api key 
    - NEW_HOST destination tenant url (e.g. https://cloudone.trendmicro.com/) 
    - NEW_API_KEY destination tenant 'full access' api key
4. Run `dsmg`

## Contributing

1. Run ./dev-setup.sh, which will download nix and nix flakes
2. run `nix develop` which will download and build dependencies, and drop you in a shell

(only tested on Arch and Ubuntu atm, so your mileage may vary)

