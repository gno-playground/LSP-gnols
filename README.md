# LSP-gnols

This is a helper package that automatically installs and updates [`gnols`][1] 
for Sublime Text. 

## Requirements

To use this package, you must install the [Gno][6], [Terminus][4], and 
[LSP][3] packages.

> **Note** 
>
> It's recommended, but not required, to install the [LSP-json][2] package 
> which will provide auto-completion and validation for this package's 
> settings.

You also need to have the [`gno`][7] binary installed. If the server can't find it on your `$PATH`, you'll need to manually specify its location in your settings:

```json
{
    "settings": {
        "gno": "/path/to/gno"
    }
}
```

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
                    "settings": {
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
[6]: https://packagecontrol.io/packages/Gno
[7]: https://github.com/gnolang/gno
