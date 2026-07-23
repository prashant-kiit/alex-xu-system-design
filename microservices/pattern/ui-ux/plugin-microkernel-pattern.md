# Explain Microkernel / Plugin Pattern

## Definition

**Plugin Architecture** is an architectural pattern where new functionality is added to a software system **without modifying the original application's source code**.

Instead of changing the core codebase every time a new feature is needed, the application is built with a **stable core** plus well-defined extension points. New capabilities are delivered as separate, independently installable units called **plugins**, which "plug into" the core and extend it.

> **Core idea:** the core application stays unchanged and stable. Functionality grows by adding plugins, not by editing the core.

## Real-world example: VS Code

VS Code itself is just a basic code editor with core features like syntax highlighting. Additional capabilities — database integration, Git support, language-specific highlighting, themes, etc. — are **not** added by modifying VS Code's source code.

Instead, users simply **install extensions**. Each extension is a plugin that adds new functionality on top of the unchanged core. Anyone (VS Code's team or the community) can build and ship these plugins independently.

## Why use it

* Lets users (or third-party developers) extend software **without touching the original codebase**.
* Keeps the core application small, stable, and easy to maintain.
* New features can be developed, tested, and released independently of the core.
* Encourages a community/marketplace of plugins (as seen with VS Code extensions).

## Code example

The core defines a plugin contract (interface). Plugins implement it. The core discovers and runs plugins without knowing their implementation details in advance.

```python
# core/plugin_interface.py
from abc import ABC, abstractmethod

class Plugin(ABC):
    @abstractmethod
    def name(self) -> str:
        ...

    @abstractmethod
    def execute(self, data):
        ...
```

```python
# core/application.py
class Application:
    def __init__(self):
        self.plugins = []

    def register_plugin(self, plugin: Plugin):
        self.plugins.append(plugin)

    def run(self, data):
        for plugin in self.plugins:
            print(f"Running plugin: {plugin.name()}")
            data = plugin.execute(data)
        return data
```

```python
# plugins/uppercase_plugin.py
from core.plugin_interface import Plugin

class UppercasePlugin(Plugin):
    def name(self) -> str:
        return "UppercasePlugin"

    def execute(self, data):
        return data.upper()
```

```python
# plugins/reverse_plugin.py
from core.plugin_interface import Plugin

class ReversePlugin(Plugin):
    def name(self) -> str:
        return "ReversePlugin"

    def execute(self, data):
        return data[::-1]
```

```python
# main.py
from core.application import Application
from plugins.uppercase_plugin import UppercasePlugin
from plugins.reverse_plugin import ReversePlugin

app = Application()
app.register_plugin(UppercasePlugin())
app.register_plugin(ReversePlugin())

result = app.run("hello world")
print(result)  # DLROW OLLEH
```

Notice that `Application` (the core) never changes when a new plugin like `ReversePlugin` is added. New behavior is introduced purely by writing a new class that implements `Plugin` and registering it.

## One-line summary

> **Plugin Architecture lets you add new functionality to software by installing independent plugins that conform to a fixed interface, without ever modifying the original core application.**
