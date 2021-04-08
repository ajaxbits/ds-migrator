# Trend Micro Deep Security Migrator

**Moves your existing on-prem DS deployment to CloudOne Workload security. Automatically.**

* [Quickstart](#quickstart)
* [Capabilities](#capabilities)
  * [Known limitations](#known-limitations)
* [Usage](#usage)
  * [Command Reference](#command-reference)
  * [Use Environment Variables](#use-environment-variables)
* [Requirements](#requirements)
* [Contributing](#contributing)
* [Support](#support)
* [License](#license)

## Quickstart

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install dsmigrator.

1. Run ```pip install dsmigrator``` on a machine with access to your DSM.

2. Run ```dsmg -k``` and fill out the credential prompts.

## Capabilities

Here's the current feature map of what the tool can migrate:

- [x] Policies
- [x] Policy settings
- [x] Global manager settings
- [x] Anti-Malware Scan Configurations
- [x] IPS, LI, and IM custom rules
- [x] Firewall rules
- [x] Schedules
- [x] Contexts
- [x] IP lists
- [x] MAC lists
- [x] Port lists
- [x] [BETA] Tasks (still quite buggy)
- [x] [BETA] Computer Groups
- [ ] Application Control (everything)
- [ ] Certificate support for authenticated requests

### Known limitations

- Cannot migrate customized IM/LI/IP rules. Another tool will be incoming to help aid a manual process in identifying each rule that has been customized, but they will never migrate automatically due to an API limitation
- Won't migrate cloud accounts. Must be reconfigured/reauthenticated in Cloud One

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

  -d, --delete-policies / --keep-policies
                                  Wipes existing policies in Cloud One (not
                                  required, but will give best results)

  -t, --tasks                     (BETA) Enable the task migrator (may be
                                  buggy)

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

**NOTE:** DS Migrator currently only supports migrations from Deep Security 20 and 12.

## Contributing

1. Run ./dev-setup.sh, which will download nix and nix flakes.
2. Run `nix develop` which will download and build dependencies, and drop you in a shell.

(only tested on Arch and Ubuntu so far, so your mileage may vary)

## Support

For support, please open an issue on Github.

## License

GNU General Public License

GNU General Public License
