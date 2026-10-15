# data-platform-blueprint

A reference architecture for a governed data platform. The architecture
stays fixed and the implementations vary: each capability is defined by a
contract that any stack can meet, and an implementation shows how its
components meet each contract.

Status: in development.

## Develop

```sh
nix develop --command just          # list the recipes
nix develop --command just check    # what every change must pass
```

## Licence

Apache License 2.0. See [LICENSE](LICENSE).
