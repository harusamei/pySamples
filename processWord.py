from docx import Document

# 打开Word文件
doc = Document('data/ai.docx')

# 读取内容
content = []
for paragraph in doc.paragraphs:
    content.append(paragraph.text)

# 保存为TXT文件
with open('data\output.txt', 'w',encoding='utf-8') as file:
    file.write('\n'.join(content))
