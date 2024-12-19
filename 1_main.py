# -*- coding: utf-8 -*-
import re
import os

# 转换全角字符为半角字符;# 定义正则表达式模式来匹配形如 ![](images/...) 的行;# 删除空白行
def f1(directory_path,target_directory):
    def convert_latex_to_plain_text(latex_text):
        # 定义替换规则
        replacements = [
            (r'\$', ''),  # 移除所有$
            (r'\\mathrm\{([^}]*)\}', r'\1'),  # 移除\mathrm{}并保留内容
            (r'\{([^}]*)\}', r'\1'),  # 移除{}并保留内容
            (r'\\pm', '±'),  # 替换 \pm 为 ±
            (r'\\left\(', '('),  # 替换\left(为(
            (r'\\right\)', ')'),  # 替换\right)为)
            (r'\\rightarrow', '→'),  # 替换\rightarrow为→
            (r'\\longrightarrow', '→'), # longrightarrow
            (r'\\sim', '~'),  # 替换\sim为~
            (r'\\text\{([^}]*)\}', r'\1'),  # 移除\text{}并保留内容
            (r'\\', ''),  # 移除所有反斜杠
        ]

        # 逐一应用替换规则
        for pattern, replacement in replacements:
            latex_text = re.sub(pattern, replacement, latex_text)
        
        return latex_text

    def fullwidth_to_halfwidth(text):
        """
        将文本中的全角字符转换为半角字符，同时保留数字和字母之间的空格
        """
        result = []
        for char in text:
            code = ord(char)
            # 全角空格直接转换
            if code == 0x3000:
                result.append(chr(0x0020))
            # 其他全角字符（根据Unicode编码）
            elif 0xFF01 <= code <= 0xFF5E:
                result.append(chr(code - 0xFEE0))
            else:
                result.append(char)
        return ''.join(result)

    def remove_image_lines(text):
        # 定义正则表达式模式来匹配形如 ![](images/...) 的行
        pattern = r'^!.*\s*$'  # 正确的正则表达式模式
        # 使用正则表达式替换这些行为空字符串
        cleaned_text = re.sub(pattern, '', text, flags=re.MULTILINE)
        return cleaned_text

    # 删除空白行
    def remove_blank_lines(text):
        # 分割文本为行
        lines = text.splitlines()
        # 过滤掉空白行
        non_blank_lines = [line for line in lines if line.strip()]
        # 将非空行重新组合成文本
        cleaned_text = '\n'.join(non_blank_lines)
        return cleaned_text

    # 删除每一行多余的空格 解决1.全角字符转换为半角字符多余的空格 2.多余的中文之间的空格
    # def remove_blank_in_lines(text):
    #     cleaned_text = []
    #     for line in text.split('\n'):
    #         cleaned_line = ' '.join(line.split())
    #         cleaned_text.append(cleaned_line)
    #     return '\n'.join(cleaned_text)

    # def remove_blank_in_lines(text):
    #     # 删除单个空格
    #     text = re.sub(r'(?<=\S) (?=\S)', '', text)
        
    #     # 将连续三个或更多的空格替换为一个空格
    #     text = re.sub(r'\s{3,}', ' ', text)
        
    #     return text


    # # 示例段落
    # latex_text = """
    # 印支期是区域主碰撞造山高峰期，也是大规模岩浆活动与 Cu-Ni-Pt-Pd 硫化物矿床、VMS 型 Cu-Pb-Zn 矿床及斑岩型 Cu- $\mathrm{{Au}}$ 矿床成矿集中期,其中老王寨金矿含金黄铁矿的 $\mathrm{{Re}}$ -Os 等时线年龄为 ${229} \pm {38}\mathrm{{Ma}}$ 。燕山期成矿年龄数据分散于 ${180}\mathrm{{Ma}}$ 、 ${135}\mathrm{{Ma}}\text{、}{110}\mathrm{{Ma}}$ 和 ${90}\mathrm{{Ma}}$ 左右等多个时段，其中最晚时段年龄谱的最小视年龄值 $\left( {{91} \pm 1\mathrm{{Ma}}}\right)$ 可能代表了一次较为重要的构造动力体制转换,该期(约 ${90} \sim {70}\mathrm{{Ma}}$ ) 的区域成岩成矿(斑岩及斑岩型 Cu-Mo-W-Au 矿床) 规模较大,表明增生造山 $\rightarrow$ 碰撞造山构造体制转换在研究区存在重要的成岩成矿响应。喜马拉雅期可能经历了早（63. 09 ~ 61. 55 Ma）、主( 36. 10 ~ 33. 76 Ma) 和晚 (30. ${80} \sim$ 26. ${40}$ Ma) 三期金矿成矿-热事件，分别受控于印度-亚洲大陆碰撞早期的强烈汇聚挤压、早-晚期转换构造动力学体制，并可能受青藏高原物质东向逃逸和软流圈脉动隆起的联合制约，金矿大规模成矿作用与构造动力体制转换过程中的壳幔物质强烈交换与构造变形密切相关。
    # """

    # # 转换为普通文本
    # plain_text = convert_latex_to_plain_text(latex_text)
    # print(plain_text)


    def process_files_in_directory(directory_path):
        if not os.path.exists(target_directory):
            os.makedirs(target_directory)
        # 遍历文件夹中的所有文件
        for filename in os.listdir(directory_path):
            if filename.endswith(".txt"):
                file_path = os.path.join(directory_path, filename)
                with open(file_path, 'r', encoding='utf-8') as file:
                    latex_text = file.read()
                    plain_text = convert_latex_to_plain_text(latex_text)
                    converted_text = fullwidth_to_halfwidth(plain_text)  # 转换全角字符为半角字符
                    converted_text_f = remove_image_lines(converted_text)  # 定义正则表达式模式来匹配形如 ![](images/...) 的行
                    converted_text_g = remove_blank_lines(converted_text_f)  # 删除空白行
                    # 删除每一行多余的空格  需要以每个txt的每一行为单位进行处理 避免以一个txt为单位 删除了所有的空格

                
                # 将处理后的内容保存到新文件中
                new_file_path = os.path.join(target_directory, f"processed_{filename}")
                with open(new_file_path, 'w', encoding='utf-8') as new_file:
                    new_file.write(converted_text_g)
                    print(f"Saved processed file: {new_file_path}")

    # # 设置文件夹路径
    # directory_path = "txtToDelLatex_lite"  # 替换为你的txt文件夹路径
    # target_directory = "txtHaveDel_1"  # 处理后的目标文件夹路径

    # 处理文件夹中的所有文件
    process_files_in_directory(directory_path)

# 删除单个字母之间的空格
def f2(directory_path,target_directory):
    # 删除单个字母之间的空格
    def clean_text(line):
        # 删除单个字母之间的空格
        line = re.sub(r'(?<=\b\w) (?=\w\b)', '', line)
        # 将连续三个或更多的空格替换为一个空格
        line = re.sub(r'\s{3,}', ' ', line)
        return line

    def process_files_in_directory(directory_path, target_directory):
        if not os.path.exists(target_directory):
            os.makedirs(target_directory)

        # 遍历文件夹中的所有文件
        for filename in os.listdir(directory_path):
            if filename.endswith(".txt"):
                file_path = os.path.join(directory_path, filename)
                new_file_path = os.path.join(target_directory, filename)
                
                with open(file_path, 'r', encoding='utf-8') as file, open(new_file_path, 'w', encoding='utf-8') as new_file:
                    for line in file:
                        cleaned_line = clean_text(line.strip())
                        new_file.write(cleaned_line + '\n')
                
                print(f"Processed and saved: {new_file_path}")

    # # 示例用法
    # directory_path = "txtHaveDel_1"  # txt文件夹路径
    # target_directory = "txtHaveDel_2"  # 处理后的目标文件夹路径
    process_files_in_directory(directory_path, target_directory)

# # 如果找到了“参考文献”，删除该行及其后的所有行
def f3(directory_path,target_directory):
    def remove_references(text_lines):
        last_reference_index = -1
        # 查找最后一次出现“参考文献”这四个字的行索引
        for i, line in enumerate(text_lines):
            if "参考文献" in line:
                last_reference_index = i
        
        # 如果找到了“参考文献”，删除该行及其后的所有行
        if last_reference_index != -1:
            return text_lines[:last_reference_index]
        else:
            return text_lines

    def process_files_in_directory(directory_path, target_directory):
        if not os.path.exists(target_directory):
            os.makedirs(target_directory)

        # 遍历文件夹中的所有文件
        for filename in os.listdir(directory_path):
            if filename.endswith(".txt"):
                file_path = os.path.join(directory_path, filename)
                new_file_path = os.path.join(target_directory, filename)
                
                with open(file_path, 'r', encoding='utf-8') as file:
                    lines = file.readlines()
                
                cleaned_lines = remove_references(lines)
                
                with open(new_file_path, 'w', encoding='utf-8') as new_file:
                    for line in cleaned_lines:
                        new_file.write(line)
                
                print(f"Processed and saved: {new_file_path}")

    # # 示例用法
    # directory_path = "txtHaveDel_6"  # txt文件夹路径
    # target_directory = "txtHaveDel_7"  # 处理后的目标文件夹路径
    process_files_in_directory(directory_path, target_directory)

if __name__ == "__main__":
    # 转换全角字符为半角字符;# 定义正则表达式模式来匹配形如 ![](images/...) 的行;# 删除空白行
    directory_path = "tushu"  # 替换为你的txt文件夹路径
    target_directory = "txtHaveDel_1"  # 处理后的目标文件夹路径
    f1(directory_path,target_directory)
    
    # 删除单个字母之间的空格 全角字符为半角字符之后还有多余的空格
    directory_path = "txtHaveDel_1"  # txt文件夹路径
    target_directory = "txtHaveDel_2"  # 处理后的目标文件夹路径
    f2(directory_path,target_directory)

    # 如果找到了“参考文献”，删除该行及其后的所有行
    directory_path = "txtHaveDel_2"  # txt文件夹路径
    target_directory = "txtHaveDel_3"  # 处理后的目标文件夹路径
    f3(directory_path,target_directory)



