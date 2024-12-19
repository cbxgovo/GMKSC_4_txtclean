# -*- coding: utf-8 -*-
import os

# 将txtHaveDel_3文件夹下的每个txt文件全都合并到一起，保存到all.txt文件当中
def f1(folder_path,output_file):
    # # 指定文件夹路径
    # folder_path = 'txtHaveDel_3'
    # output_file = 'all.txt'

    # 打开输出文件
    with open(output_file, 'w', encoding='utf-8') as outfile:
        # 遍历文件夹中的所有文件
        for filename in os.listdir(folder_path):
            if filename.endswith('.txt'):
                file_path = os.path.join(folder_path, filename)
                # 打开并读取每个txt文件的内容
                with open(file_path, 'r', encoding='utf-8') as infile:
                    # 将内容写入输出文件
                    outfile.write(infile.read())
                    # 添加一个换行符，以分隔文件内容
                    outfile.write('\n')

    print(f"所有txt文件已合并到 {output_file} 中")

# 遍历all.txt文件的每一行，把少于10个字符的行删除
# 只保留字符数大于等于10的行
def f2_1(input_file,output_file):
    # # 指定输入和输出文件路径
    # input_file = 'all.txt'
    # output_file = 'all_1.txt'


    # 读取原始文件内容并过滤行
    with open(input_file, 'r', encoding='utf-8') as infile:
        lines = infile.readlines()

    # 只保留字符数大于等于x的行
    filtered_lines = [line for line in lines if len(line.strip()) >= 20]

    # 写入过滤后的内容到新文件
    with open(output_file, 'w', encoding='utf-8') as outfile:
        outfile.writelines(filtered_lines)

    print(f"已将过滤后的内容保存到 {output_file}")

"""
遍历filtered_all.txt文件的每一行，应用以下规则：
1.“图”开头的行删除
2.第一个字符为英文字母或者数字开头的行删除
3.字符“#”开头的行删除
将处理后的文件保存到filtered_all_new.txt
"""
def f2_2():
    input_file = 'all_1.txt'
    output_file = 'all_2.txt'
    # 打开并读取文件内容
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # 创建一个新的列表来存储符合规则的行
    filtered_lines = []

    # 遍历每一行并应用规则
    for line in lines:
        # 去掉行首尾的空白字符
        line = line.strip()
        
        # 检查行是否为空
        if not line:
            continue

        # 提取每一行的第一个字符
        first_char = line[0]
        # print(first_char)

        # 规则1：删除第一个字符为汉字“图”的行
        if first_char == '图' or first_char == '表':
            continue
        
        # 规则2：删除第一个字符为英文字母的行
        if 'A' <= first_char <= 'Z' or 'a' <= first_char <= 'z':
            continue
        
        # 规则3：删除第一个字符为“#”的行
        if first_char == '#':
            continue

        else:
            # 如果该行符合所有规则，将其添加到filtered_lines中
            filtered_lines.append(line)


    # 将过滤后的内容写入新的文件
    with open(output_file, 'w', encoding='utf-8') as file:
        for line in filtered_lines:
            file.write(line + '\n')

    print(f"已将过滤后的内容保存到 {output_file}")

# 遍历filtered_all.txt文件的每一行，如果该行的所有字符英文字母的占比超过0.5，就删除该行
def f2_3():
    input_file = 'all_2.txt'
    output_file = 'all_3.txt'
    # 打开并读取文件内容
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # 创建一个新的列表来存储符合规则的行
    filtered_lines = []

    # 遍历每一行
    for line in lines:
        # 去掉行首尾的空白字符
        line = line.strip()

        # 如果该行为空，则跳过
        if not line:
            continue

        # 统计英文字母的数量
        num_alpha = sum(1 for char in line if ('A' <= char <= 'Z' or 'a' <= char <= 'z'))
        total_chars = len(line)

        # 如果英文字母占比超过 0.5，删除该行
        if num_alpha / total_chars > 0.2:
            # print(f'该行删除{num_alpha / total_chars}')
            continue

        # 将符合条件的行添加到filtered_lines中
        # print(f'该行保留{num_alpha / total_chars}')
        filtered_lines.append(line)

    # 将过滤后的内容写入新的文件
    with open(output_file, 'w', encoding='utf-8') as file:
        for line in filtered_lines:
            file.write(line + '\n')

    print(f"已将过滤后的内容保存到 {output_file}")

# 每一行大于200字符就按照句号分割为多句
def split_lines_by_period(input_file, output_file, max_length=200):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            # 判断是否超过最大字符数
            if len(line.strip()) > max_length:
                # 按句号分割行，去除每个子句的左右空白
                sentences = [sentence.strip() for sentence in line.split('。') if sentence.strip()]
                # 每个子句写入新行，末尾加上句号
                for sentence in sentences:
                    outfile.write(sentence + '。\n')
            else:
                # 如果字符数不大于200，直接写入新文件
                outfile.write(line)
    print(f"已将过滤后的内容保存到 {output_file}")

if __name__ == "__main__":
    # # 将txtHaveDel_3文件夹下的每个txt文件全都合并到一起，保存到all.txt文件当中
    folder_path = 'txtHaveDel_3'
    output_file = 'all.txt'
    f1(folder_path,output_file)

    # 指定输入和输出文件路径
    in_path = 'all.txt'
    out_file = 'all_1.txt'
    f2_1(in_path,out_file) # # 遍历all.txt文件的每一行，把少于10个字符的行删除

    f2_2() # 1.“图”开头的行删除;2.第一个字符为英文字母或者数字开头的行删除;3.字符“#”开头的行删
    f2_3() # # 遍历txt文件的每一行，如果该行的所有字符英文字母的占比超过0.5，就删除该行

    # 每一行大于200字符就按照句号分割为多句
    input_file = 'all_3.txt'  # 输入文件名
    output_file = 'all_4.txt'   # 输出文件名
    split_lines_by_period(input_file, output_file)

    # 拆分行之后再调用f2_1,把少于10个字符的行删除
    in_path = 'all_4.txt'
    out_file = 'all_5.txt'
    f2_1(in_path,out_file) # # 遍历all.txt文件的每一行，把少于10个字符的行删除



