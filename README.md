# LSP-gnols

This is a helper package that automatically installs and updates [`gnols`][1] 
for Sublime Text. 

## Requirements

To use this package, you must have [LSP][3] and [Terminus][4] installed.

> It's recommended, but not required, to install the [LSP-json][2] package 
> which will provide auto-completion and validation for this package's 
> settings.

## Configuration

There are multiple ways to configure the package and the language server.

- Global configuration: `Preferences > Package Settings > LSP > Servers > LSP-gnols`
- Project-specific configuration:
  from the Command Palette run `Project: Edit Project` and add your settings in:

    ```js
    {
        "settings": {
            "LSP": {
                "LSP-gnols": {
                    "initializationOptions": {
                        // Put your settings here
                    }
                }
            }
        }
    }
    ```

[1]: https://github.com/jdkato/gnols
[2]: https://packagecontrol.io/packages/LSP-json
[3]: https://packagecontrol.io/packages/LSP
[4]: https://www.sublimetext.com/
[5]: https://packagecontrol.io/packages/Terminus
