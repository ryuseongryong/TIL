// cargo new exampleCreate a new cargo package at <path>

Usage: cargo new [OPTIONS] <path>

Arguments:
  <path>  

Options:
  -q, --quiet                Do not print cargo log messages
      --registry <REGISTRY>  Registry to use
      --vcs <VCS>            Initialize a new repository for the given version control system (git, hg, pijul, or fossil) or do not initialize any version control at all (none), overriding a global configuration. [possible values: git, hg, pijul, fossil, none]
      --bin                  Use a binary (application) template [default]
  -v, --verbose...           Use verbose output (-vv very verbose/build.rs output)
      --lib                  Use a library template
      --color <WHEN>         Coloring: auto, always, never
      --edition <YEAR>       Edition to set for the crate generated [possible values: 2015, 2018, 2021]
      --name <NAME>          Set the resulting package name, defaults to the directory name
      --frozen               Require Cargo.lock and cache are up to date
      --locked               Require Cargo.lock is up to date
      --offline              Run without accessing the network
      --config <KEY=VALUE>   Override a configuration value
  -Z <FLAG>                  Unstable (nightly-only) flags to Cargo, see 'cargo -Z help' for details
  -h, --help                 Print help

Run `cargo help new` for more detailed information.
