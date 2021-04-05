# Trend Micro Deep Security Migrator

**Moves your existing on-prem DS deployment to CloudOne Workload security. Automatically.**

* [Quickstart](#quickstart)
* [Usage](#usage)
  * [Command Reference](#command-reference)
  * [Use Environment Variables](#use-environment-variables)
* [Requirements](#requirements)
* [Contributing](#contributing)

## Quickstart

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install dsmigrator.

1. Run ```pip install dsmigrator``` on a machine with access to your DSM.

2. Run ```dsmg -k``` and fill out the credential prompts.

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

## Requirements

- Python3 (only tested on Python 3.7 or greater so far, so your mileage may vary)
- One api key for your old Deep Security Manager with "Full Access" permissions
- One api key for your Cloud One account with "Full Access" permissions
- A resolvable FQDN to your old Deep Security Manager

**NOTE:** DS Migrator has only been tested on Arch Linux and Ubuntu -- your milage may vary.

**NOTE:** DS Migrator currently only supports migrations from Deep Security 20 and 12.

## Contributing

1. Run ./dev-setup.sh, which will download nix and nix flakes.
2. Run `nix develop` which will download and build dependencies, and drop you in a shell.

(only tested on Arch and Ubuntu so far, so your mileage may vary)

## Support

For support, please open an issue on Github.

## License

GNU General Public License
