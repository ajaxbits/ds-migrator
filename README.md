# Trend Micro Deep Security Migrator

Moves settings to the cloud.... at some point

Please do some code review if you want :)

## To Set Up MVP
1. Install [Poetry](https://github.com/python-poetry/poetry) ==> `pip install --user poetry`
2. Clone this repo
3. Run `poetry install` at project root
4. Set the following environment variables:
        - `OLD_HOST` originating tenant url (e.g. https://192.168.1.1:4119/)
        - `OLD_API_KEY` originating tenant 'full access' api key
        - `NEW_HOST` destination tenant url (e.g. https://cloudone.trendmicro.com/)
        - `NEW_API_KEY` destination tenant 'full access' api key
5. Run `dsmg`

## Contributing

1. Run ./dev-setup.sh, which will download nix and nix flakes
2. run `nix develop` which will download and build dependencies, and drop you in a shell

(only tested on Arch and Ubuntu atm, so your mileage may vary)

