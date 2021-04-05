# Trend Micro Deep Security Migrator

Moves settings from on premise Deep Security to the cloud (Cloud One Workload Security).

## Installation

(Python3 only, has only been tested on =>3.7, so your mileage may vary)

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install dsmigrator.

```bash
pip install -i https://test.pypi.org dsmigrator
```

## Usage

```bash
dsmg
```

## Flags

Optional flags:

To see a list of optional flags, run `dsmg --help`
Alternatively, credentials may be entered through an interactive prompt.

NOTE: Insecure connections will produce multiple warnings unless the `-k` flag is used.

## Requirements

DS Migrator has only been tested on Arch Linux and Ubuntu -- you're milage may vary.

## Support

For support, please open an issue on the Github repository.

## License

License choice goes here.

## Contributing

1. Run ./dev-setup.sh, which will download nix and nix flakes.
2. Run `nix develop` which will download and build dependencies, and drop you in a shell.
