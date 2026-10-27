# Graphify Execution Steps

## Step 1: Open PowerShell

Open the Graphify project folder:

```powershell
cd "C:\Users\acer\Downloads\graphify-8 (1)"
```

## Step 2: Check Graphify

```powershell
graphify --help
```

## Step 3: Extract the Graph

Run the extraction command supported by your installed version. The standard path-based command is:

```powershell
graphify extract .
```

This generates graph data and analysis output.

## Step 4: Refresh Clustering

If the graph already exists and you only need to refresh clustering:

```powershell
graphify cluster-only .
```

## Step 5: Open the Interactive Graph

```powershell
explorer .\graphify-out\graph.html
```

The graph opens in your default browser.

## Step 6: Read the Report

Open this file in VS Code:

```text
graphify-out/GRAPH_REPORT.md
```

## Step 7: Check Git Status

```powershell
git status
```

## Step 8: Upload Changes to GitHub

```powershell
git add .
git status
git commit -m "Add project documentation and notes"
git push origin main
```

If Git reports that there is nothing to commit, there may be no new saved changes. Check that your Markdown files were saved in VS Code.
