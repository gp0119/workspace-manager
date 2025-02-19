# Workspace Manager Alfred Workflow

A powerful Alfred workflow that allows you to quickly open projects in different IDEs.

## Features

- Support multiple workspace directories
- Multiple IDE configurations (up to 6)
- Exclude specific folders
- Fuzzy search project names
- Hold Command key to reveal in Finder

## Configuration

### Environment Variables

1. `workspace`: Workspace paths (comma-separated) Example: `~/Projects,~/Work`

2. `exclude`: Folders to exclude (comma-separated) Example: `xxx/xxx`

3. IDE Configuration (up to 6):
   - `key1` - `key6`: Trigger keywords
   - `app1` - `app6`: Corresponding application paths

> Note: You can configure any IDE, but custom icons are only available for the IDEs listed in the "Supported IDEs" section.

Configuration example:

```
key1: vs
app1: /Applications/Visual Studio Code.app

key2: ij
app2: /Applications/IntelliJ IDEA.app
```

## Usage

1. Type the configured keyword (e.g., `vs`) in Alfred
2. Enter project name to search
3. Press Enter to open the selected project in the corresponding IDE
4. Hold Command while selecting to reveal in Finder

<image src="./usage1.png" width="580">
<br />
<br />
<image src="./usage2.png" width="580">

## Supported IDEs

The workflow includes icons for:

- Visual Studio Code
- IntelliJ IDEA (Ultimate & Community)
- PyCharm (Professional & Community)
- WebStorm
- PhpStorm
- CLion
- GoLand
- Fleet
- Rider
- RustRover
- Cursor
