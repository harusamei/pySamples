from docx import Document
import csv
# 打开Word文件
doc = Document('data/xai.docx')

# 读取段落
content = []
for paragraph in doc.paragraphs:
    if paragraph.text !='':
        content.append({"text":paragraph.text,
                        "stylename":paragraph.style.name})
# 读取表格
tables = []
for table in doc.tables:
        for row in table.rows:
            tstr='\t'.join(cell.text for cell in row.cells)
            tables.append({"table":tstr})
                 
# 保存为csv文件
with open('data\output.csv', 'w', newline='', encoding='utf-8-sig') as file:
    writer = csv.DictWriter(file, fieldnames=["text", "stylename","table"])
    writer.writeheader()
    writer.writerows(content)
    writer.writerows(tables)

    

