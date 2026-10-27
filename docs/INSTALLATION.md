# Graphify Installation Guide

## 1. Prerequisites
- Windows
- PowerShell
- Python 3.10 or newer, if required by the installed Graphify release
- Git
- Visual Studio Code (recommended)

## 2. Check the Tools

Run these commands in PowerShell:

```powershell
python --version
git --version
graphify --help
```

If `graphify` is not recognized, check the Graphify installation and PATH configuration.

## 3. Install Graphify

Use the installation method described in the official documentation:

https://www.graphiffy.com/docs

For the current official package, the documented installation command is:

```powershell
uv tool install graphifyy
```

If `uv` is not installed, follow its official installation instructions first. Do not install Graphify again if it is already working.

## 4. Verify Installation

```powershell
graphify --help
```

If the command displays Graphify's help information, the CLI is available.

## 5. Open the Project

```powershell
cd "C:\Users\acer\Downloads\graphify-8 (1)"
code .
```

Note: Exact requirements and commands can differ by Graphify version. Follow the documentation for the version you have installed.
