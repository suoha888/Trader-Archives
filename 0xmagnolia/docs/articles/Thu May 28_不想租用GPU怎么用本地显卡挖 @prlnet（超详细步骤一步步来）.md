# 不想租用GPU怎么用本地显卡挖 @prlnet（超详细步骤一步步来）

> **作者**：magnolia (@0xmagnolia)  
> **发表日期**：Thu May 28 13:21:57 +0000 2026  
> **原文链接**：https://x.com/0xmagnolia/status/2059988548389093739 (Article: https://x.com/i/article/2059987702708322304)  
> **全文字数**：1774 字  

---

1. win➕s 搜索“启用或关闭 Windows 功能”（或在控制面板里找）
打开后，勾选下面两项：
适用于 Linux 的 Windows 子系统 （Windows Subsystem for Linux）
虚拟机平台 （Virtual Machine Platform）
点击 确定 → 系统会自动下载组件 → 重启电脑
2.前期准备（Windows 端）
安装 WSL + Ubuntu
以管理员身份打开 PowerShell，
执行：wsl --install
（有可能因为挂了VPN无法下载，需要关闭VPN）本人用的powershell7版本，建议单独再下一个。
重启电脑，然后搜索打开 Ubuntu，设置用户名和密码
（因为Ubuntu又需要挂梯子下载，所以重启后挂梯子直接在Win商城下载Ubuntu）
3.在光标闪烁的位置输入用户名，然后按 Enter（回车）。
建议：
用英文和小写字母（推荐）
简单好记，比如：magnolia、user、admin 等
不要用中文，不要用太复杂的名字
输入用户名后回车，系统会让你设置密码：
输入密码（输入时不会显示，正常打就行）
再输入一次确认密码
回车
设置完后，就会进入正常的 Ubuntu 命令行界面（出现 username@computer:\~$ 这样的提示符）。
4.先更新系统（非常重要）
复制下面整行命令，粘贴到终端后按 Enter（  :不需要粘贴哦  ）
：sudo apt update && sudo apt upgrade -y
输入你的密码（输入时不会显示字符），然后回车
这个过程可能会花几分钟，耐心等待它完成。
更新完后，再运行
：sudo apt install -y curl wget git vim unzip
 换成国内软件源（推荐，速度会快很多）
：sudo cp /etc/apt/sources.list /etc/apt/sources.list.bak
sudo sed -i 's|http://archive.ubuntu.com|https://mirrors.tuna.tsinghua.edu.cn|g' /etc/apt/sources.list
sudo apt update
5.启用 NVIDIA CUDA 支持
更新系统
：sudo apt update && sudo apt upgrade -y
安装必要工具
: sudo apt install -y build-essential cmake curl wget git
配置 NVIDIA（关键步骤）
：sudo cp /usr/lib/wsl/lib/nvidia-smi /usr/local/bin/nvidia-smi
sudo chmod +x /usr/local/bin/nvidia-smi
echo 'export PATH="/usr/lib/wsl/lib:$PATH"' >> \~/.zshrc
source \~/.zshrc
验证显卡
: nvidia-smi
（必须要看到你的显卡型号才算成功 比如 RTX5090）
6. 创建钱包 https://compute.pearlresearch.ai/wallet
创建完后记得复制钱包地址
7. 回到我们的Ubuntu，安装矿工
下载 Alpha Miner（直接复制粘贴下面指令）
cd \~
curl -L -o alpha-miner https://github.com/AlphaMine-Tech/alpha-miner/releases/latest/download/alpha-miner
chmod +x alpha-miner
启动挖矿（香港节点推荐命令）
./alpha-miner --pool stratum+tcp://sg1.alphapool.tech:5566 --address 这里是你的钱包地址记得粘贴进去我的这行中文要删除 --worker 4090hk
出现图片里的内容就是在挖 $prl 了，按 Ctrl➕C就可以停止挖矿
这是矿池网址，可以搜索你的钱包地址查询出块
https://pearl.alphapool.tech/
