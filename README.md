# Endfield Launcher

## What is this
A very simple launcher for a certain factory building anime game.
Written in python with PySide6.

This application will download the OS client from online hosting source and set it up for you so you can install the game just like using the official launcher.

It can also deploy the server for you. It will pull the dev branch of from https://github.com/SuikoAkari/ArkFieldPS and compile it on your device.

## How do I use it

You can either run the python file directly or use a bundled exe version. You can find it in the releases section.

**If you don't have python env, DOWNLOAD THE BUNDLED VERSION from the releases section. Do not download the source code as you won't be able to run them!**

The launcher is hardcoded to download the game client in `./EndfieldGame` and save the server files to `./EndfieldServer`. You can change that by changing the constants in `main.py` and rebundle it with Nuitka. If you want to use game data that you have already downloaded from somewhere else, copy them to `./EndfieldGame/Beyond_Release-2089329-32_os_prod_cbt` folder and ensure the game executable is at `./EndfieldGame/Beyond_Release-2089329-32_os_prod_cbt/Endfield_TBeta_OS.exe`. The launcher should recognize them with no issues. To migrate your server instance to this launcher, copy your server data (including the tables, jsons) to `./EndfieldServer/ArkfieldPS/bin/Release/net8.0` folder and ensure the executable of the server is at `./EndfieldServer/ArkfieldPS/bin/Release/net8.0/ArkfieldPS.exe`.

You don't have to install any dependency if you are just trying to download the game client, but it does require a working installation of Visual Studio 2022, .Net 8.0 SDK, and msbuild if you want to deploy the server. You will also need MongoDB on your computer to run the server. It will, however, download the latest game asset (tables, jsons) and put them in the right place so you don't have to worry about them.

You will also need to set up some proxy if you want to play on a publically hosted server or your own server. I'm trying to figure out how to put that into the launcher but it won't happen very soon. Refer to https://github.com/SuikoAkari/ArkFieldPS for more information on how you can set up the proxy.

## 这是什么

这是一个针对某工厂建筑类二次元游戏的启动器。  
用 Python 和 PySide6 写的，代码很烂，请见谅

该应用程序会从在线托管源下载游戏客户端，并为你进行设置，这样你就可以像使用官方启动器一样安装游戏。

它还可以为你部署服务器。它会拉取来自 https://github.com/SuikoAkari/ArkFieldPS 的 dev 分支，并在你的设备上编译。

----------

## 我该如何使用

你可以直接运行 Python 文件（如果你有 Python 环境的话），也可以使用打包好的 exe 版本。你可以在 releases 页面下载。

**如果你没有 Python 环境，去 releases 里下载打包好的 exe！不要直接克隆项目或者下载源代码，运行不了的！**

启动器写死了将游戏下载到 `./EndfieldGame` 里，并将服务器文件保存到 `./EndfieldServer` 。你可以通过修改 `main.py` 中的常量并使用 Nuitka 重新打包来更改（当然你想直接运行也是可以的）。如果你想要使用你已经下载好的客户端/服务端，把游戏文件复制到 `./EndfieldGame/Beyond_Release-2089329-32_os_prod_cbt` 目录里面，确保游戏可执行文件在 `./EndfieldGame/Beyond_Release-2089329-32_os_prod_cbt/Endfield_TBeta_OS.exe` 就可以被启动器识别了。服务端的话，你需要把服务器文件（以及数据，table json 那些）放在 `./EndfieldServer/ArkfieldPS/bin/Release/net8.0` 目录下，确保服务器可执行文件在 `./EndfieldServer/ArkfieldPS/bin/Release/net8.0/ArkfieldPS.exe`，这样子应该就没问题了。

如果你只是想下载游戏客户端，则不必安装任何依赖，但如果你想部署服务器，则需要在你的电脑上安装 VS2022、.Net 8.0 SDK 和 msbuild（应该会随着 VS 自动安装的）。你还需要安装 MongoDB 来运行服务器。不过，它会自动下载最新的游戏资源（表格、JSON 文件）并放置到正确的位置，所以你不必担心它们。

如果你想在公共服务器或你自己的服务器上进行游戏，则还需要设置一些代理。我正在尝试将这部分功能整合到启动器中，但这不会很快实现。有关如何设置代理的更多信息，请参阅 https://github.com/SuikoAkari/ArkFieldPS 。

## Waning / 注意
I don't want to see this, as well as any other assets being sold for money ANYWHERE. You may modify, customize, improve and share without any limitation ( and I will not be responsible for any consequence thereof), but NO MONETIZATION. 挂咸鱼 / 挂B站卖钱的，或者以任何其他方式倒卖的，包4全家。
