# Sync Icon Descriptions (figma plugin)

This Figma plugin synchronizes the descriptions of components in the current page using data from a remote JSON file. The plugin ensures descriptions are updated consistently for all components, whether they are inside frames/groups or free-standing on the page.

## Features

- **Selective Processing**: Operates only on components within the current page.
- **JSON Integration**: Fetches descriptions from a remote JSON file hosted on GitHub.
- **Batch Processing**: Optimized to handle large numbers of components efficiently.
- **Support for Nested Components**: Processes components inside frames, groups, and other containers.
- **Fallback Logic**: Handles components with missing descriptions gracefully.

## How It Works

1. The plugin fetches a JSON file containing descriptions for components.
2. It processes components on the current page, updating their descriptions based on the JSON data.
3. If a match is found in the JSON, the description is updated along with a link to additional documentation.
4. The plugin provides a summary of how many components were updated.

## Installation

1. Clone or download the repository.
2. Open Figma and go to `Plugins > Development > New Plugin`.
3. Choose the `Manifest` option and select the plugin's manifest file.

## Usage

1. Open a Figma file and navigate to the desired page.
2. Run the plugin.
3. The plugin will update descriptions for all components in the page, whether selected, nested, or free-standing.

## JSON Structure

The JSON file should be structured as follows:

```json
{
  "ComponentName": ["Description part 1", "Description part 2"],
  "AnotherComponent": ["Another description"]
}
```

- The keys represent the base names of the components.
- Values are arrays of description strings that will be concatenated.

## Development

The main logic is in `code.js`. Just import manifest.json to Figma and run plugin in Figma.

## Debugging

- Open the Figma Console (`Cmd + Option + I` on Mac or `Ctrl + Shift + I` on Windows) to view debug logs.
- Logs include information about processed components, updated descriptions, and any errors encountered.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
