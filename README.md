# Trend Micro Deep Security Migrator

Moves your existing on-prem DS deployment to CloudOne Workload security. Automatically.

## Quickstart

Simply run `pip install dsmigrator`

## Usage

```bash
Usage: dsmg [OPTIONS]

  Moves your on-prem DS deployment to the cloud!

Options:
  --config-file PATH
  -ou, --original-url TEXT        A resolvable FQDN for the old DSM, with port
                                  number (e.g. https://192.168.1.1:4119)

  -oa, --original-api-key TEXT    API key for the old DSM with Full Access
                                  permissions

  -nu, --new-url TEXT             Destination url  [default:
                                  https://cloudone.trendmicro.com/]

  -coa, --cloud-one-api-key TEXT  API key for Cloud One Workload Security with
                                  Full Access permissions

  -k, --insecure                  Suppress the InsecureRequestWarning for
                                  self-signed certificates

  -c, --cert TEXT                 (Optional) Allows the use of a cert file
                                  [default: False]

  --help                          Show this message and exit.
```
## To Set Up MVP

(Python3 only, has only been tested on =>3.7, so your mileage may vary)

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

(only tested on Arch and Ubuntu so far, so your mileage may vary)

