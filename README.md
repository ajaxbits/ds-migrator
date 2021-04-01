# Trend Micro Deep Security Migrator

* [Quickstart](#quickstart)
* [Requirements](#requirements)
* [Usage](#usage)
  * [Command Reference](#command-reference)
  * [Use Environment Variables](#use-environment-variables)
* [Contributing](#contributing)

**Moves your existing on-prem DS deployment to CloudOne Workload security. Automatically.**

## Quickstart

1. `pip install dsmigrator` on a machine with access to your DSM
2. Run `dsmg -k` and fill out the credential prompts

## Requirements

- Python3 (only tested on Python 3.7 or greater so far, so your mileage may vary)
- An api key for your old DSM with "Full Access" permissions
- An api key for your Cloud One account with "Full Access" permissions
- A resolvable FQDN to your old DSM

## Usage

### Command Reference

```text
Usage: dsmg [OPTIONS]

  Moves your on-prem DS deployment to the cloud!

Options:
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

### Use Environment Variables

You can optionally use the following environment variables to pass in your credentials:

- ORIGINAL_API_KEY
- ORIGINAL_URL
- CLOUD_ONE_API_KEY

## Contributing

1. Run ./dev-setup.sh, which will download nix and nix flakes
2. run `nix develop` which will download and build dependencies, and drop you in a shell

(only tested on Arch and Ubuntu so far, so your mileage may vary)

