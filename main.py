import os
import sys

# CatShizuku PNG -> Header Tool
# by zichuan

WORK_DIR = "/storage/emulated/0/猫羽雫"
COUNT_FILE = os.path.join(WORK_DIR, "run_count.txt")


LANG = {
    "zh": {
        "title": "猫羽雫图片工具",
        "mode": "请输入图片路径 (PNG) 或输入 folder 批量处理:",
        "folder": "请输入文件夹路径:",
        "not_found": "找不到目标路径",
        "not_folder": "找不到目标文件夹",
        "var_name": "请输入变量名称:",
        "done": "处理完成",
        "keep": "请不要删除本工具生成的运行文件",
        "end": "感谢使用"
    },

    "en": {
        "title": "CatShizuku Image Tool",
        "mode": "Input png path or type folder:",
        "folder": "Input folder path:",
        "not_found": "Target file not found",
        "not_folder": "Target folder not found",
        "var_name": "Input variable name:",
        "done": "Finished",
        "keep": "Please do not delete runtime files",
        "end": "Thanks for using"
    }
}


BLUE = "\033[1;34m"
GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
PINK = "\033[1;35m"
RESET = "\033[0m"


def choose_language():
    print("1. 中文")
    print("2. English")

    c = input("> ").strip()

    if c == "2":
        return LANG["en"]

    return LANG["zh"]


TXT = choose_language()


def increase_run_count():
    os.makedirs(WORK_DIR, exist_ok=True)

    if not os.path.exists(COUNT_FILE):
        with open(COUNT_FILE, "w") as f:
            f.write("1")
        return

    try:
        with open(COUNT_FILE, "r") as f:
            count = int(f.read().strip())
    except:
        count = 0

    with open(COUNT_FILE, "w") as f:
        f.write(str(count + 1))


def png_to_header(file_path, var_name):
    with open(file_path, "rb") as f:
        raw = f.read()

    hex_data = ", ".join(
        f"0x{x:02x}"
        for x in raw
    )

    return (
        "/* CatShizuku PNG Tool */\n"
        f"unsigned char {var_name}[] = {{\n"
        f"{hex_data}\n"
        "};\n"
    )


def save_header(name, content):
    output = os.path.join(WORK_DIR, f"{name}.h")

    with open(output, "w", encoding="utf-8") as f:
        f.write(content)

    return output


def handle_single():
    path = input().strip()

    if not os.path.isfile(path):
        print(TXT["not_found"])
        sys.exit()

    var_name = input(
        f"{TXT['var_name']} "
    ).strip()

    data = png_to_header(path, var_name)

    file_name = os.path.splitext(
        os.path.basename(path)
    )[0]

    save_header(file_name, data)

    print(
        f"{GREEN}{TXT['done']}:{RESET}",
        f"{YELLOW}{file_name}.h{RESET}"
    )


def handle_folder():
    folder = input(
        f"{BLUE}{TXT['folder']}{RESET}\n"
    ).strip()

    if not os.path.isdir(folder):
        print(TXT["not_folder"])
        return

    total = 0

    for file in os.listdir(folder):

        if not file.lower().endswith(".png"):
            continue

        path = os.path.join(folder, file)

        name = os.path.splitext(file)[0]

        header = png_to_header(path, name)

        save_header(name, header)

        total += 1

        print(
            f"{GREEN}{TXT['done']}:{RESET}",
            f"{YELLOW}{name}.h{RESET}"
        )

    print(f"Total : {total}")


def main():

    increase_run_count()

    print(
        f"{PINK}{TXT['title']}{RESET}"
    )

    print(
        f"{BLUE}{TXT['mode']}{RESET}"
    )

    mode = input().strip()

    if mode.lower() == "folder":
        handle_folder()
    else:

        if not os.path.exists(mode):
            print(TXT["not_found"])
            return

        var_name = input(
            f"{TXT['var_name']} "
        ).strip()

        name = os.path.splitext(
            os.path.basename(mode)
        )[0]

        header = png_to_header(
            mode,
            var_name
        )

        save_header(name, header)

        print(
            f"{GREEN}{TXT['done']}:{RESET}",
            f"{YELLOW}{name}.h{RESET}"
        )

    print()
    print(
        f"{GREEN}{TXT['keep']}:{RESET}"
    )
    print(WORK_DIR)
    print(TXT["end"])
    print("tg @ZCYMOD")


if __name__ == "__main__":
    main()