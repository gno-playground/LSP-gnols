import os
import shutil
import urllib.request
import zipfile

import sublime

# LSP
from LSP.plugin import (
    AbstractPlugin,
    Session,
    parse_uri,
    register_plugin,
    unregister_plugin,
)
from LSP.plugin.core.typing import (
    Any,
    Callable,
    Dict,
    List,
    Mapping,
    Optional,
    Tuple,
    Union,
)

try:
    import Terminus  # type: ignore
except ImportError:
    Terminus = None

SESSION_NAME = "gnols"

# Update this single git tag to download a newer version.
#
# After changing this tag, go through the server settings again to see if any
# new server settings are added or old ones removed.
TAG = "v0.5.0"
URL = "https://github.com/jdkato/gnols/releases/download/{tag}/gnols_{platform}_{arch}.zip"


def get_setting(
    session: Session,
    key: str,
    default: Optional[Union[str, bool, List[str]]] = None,
) -> Any:
    value = session.config.settings.get(key)
    if value is None:
        return default
    return value


def arch() -> str:
    if sublime.arch() == "x64":
        return "x86_64"
    elif sublime.arch() == "x32":
        raise RuntimeError("Unsupported platform: 32-bit is not supported")
    elif sublime.arch() == "arm64":
        return "arm64"
    else:
        raise RuntimeError("Unknown architecture: " + sublime.arch())


def platform() -> str:
    if sublime.platform() == "windows":
        return "Windows"
    elif sublime.platform() == "osx":
        return "Darwin"
    else:
        return "Linux"


def open_tests_in_terminus(
    session: Session,
    window: Optional[sublime.Window],
    command_name: str,
    arguments: Tuple[str, List[str], None],
) -> None:
    if not window:
        return

    if len(arguments) < 3:
        return

    view = window.active_view()
    if not view:
        return
    pkg = os.path.dirname(parse_uri(arguments[1])[1])

    cmd = None
    if command_name == "gnols.test":
        cmd = [
            arguments[0],  # bin
            "test",
            "-timeout",
            "30s",
            "-run",
            "^{}\\$".format(arguments[2]),  # test(s)
            pkg,  # directory
        ]
    else:
        # TODO: no -bench flag(s)?
        cmd = [
            arguments[0],  # bin
            "test",
            "-timeout",
            "30s",
            "-run",
            "^{}\\$".format(arguments[2]),  # bench(s)
            pkg,  # directory
        ]

    print("Running tests: {}".format(cmd))
    terminus_args = {
        "title": "Gno Test",
        "cmd": cmd,
        "cwd": pkg,
        "auto_close": False,
        "panel_name": "Gno Test",
    }

    window.run_command("terminus_open", terminus_args)


class GnoLS(AbstractPlugin):
    @classmethod
    def name(cls) -> str:
        return SESSION_NAME

    @classmethod
    def basedir(cls) -> str:
        return os.path.join(cls.storage_path(), __package__)

    @classmethod
    def server_version(cls) -> str:
        return TAG

    @classmethod
    def additional_variables(cls) -> Optional[Dict[str, str]]:
        return {
            "gnols_bin": "gnols.exe"
            if sublime.platform() == "windows"
            else "gnols"
        }

    @classmethod
    def current_server_version(cls) -> str:
        with open(os.path.join(cls.basedir(), "VERSION"), "r") as fp:
            return fp.read()

    @classmethod
    def needs_update_or_installation(cls) -> bool:
        try:
            return cls.server_version() != cls.current_server_version()
        except OSError:
            return True

    @classmethod
    def install_or_update(cls) -> None:
        try:
            if os.path.isdir(cls.basedir()):
                shutil.rmtree(cls.basedir())
            os.makedirs(cls.basedir(), exist_ok=True)

            version = cls.server_version()
            url = URL.format(tag=TAG, platform=platform(), arch=arch())

            zip_path, _ = urllib.request.urlretrieve(url)
            with zipfile.ZipFile(zip_path, "r") as f:
                f.extractall(cls.basedir())

            serverfile = os.path.join(
                cls.basedir(),
                "gnols.exe" if sublime.platform() == "windows" else "gnols",
            )

            os.remove(zip_path)
            os.chmod(serverfile, 0o744)

            with open(os.path.join(cls.basedir(), "VERSION"), "w") as fp:
                fp.write(version)

        except BaseException:
            shutil.rmtree(cls.basedir(), ignore_errors=True)
            raise

    def on_pre_server_command(
        self, command: Mapping[str, Any], done_callback: Callable[[], None]
    ) -> bool:
        if not Terminus:
            return False

        command_name = command["command"]
        if command_name in ("gnols.test", "gnols.bench"):
            session = self.weaksession()
            if not session:
                return False
            try:
                open_tests_in_terminus(
                    session,
                    sublime.active_window(),
                    command_name,
                    command["arguments"],
                )
                done_callback()
                return True
            except Exception as ex:
                print(
                    "Exception handling command {}: {}".format(
                        command_name, ex
                    )
                )
        return False


def plugin_loaded() -> None:
    register_plugin(GnoLS)


def plugin_unloaded() -> None:
    unregister_plugin(GnoLS)
