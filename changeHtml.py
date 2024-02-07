from bs4 import BeautifulSoup

def addNewDiv(html_content,divContent):
    # 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # 创建新的div元素
    new_div = soup.new_tag('div')
    new_div.string = divContent

    # 将新的div元素添加到HTML文件中
    soup.body.append(new_div)

    return str(soup)

if __name__ == "__main__":
    with open('form.html', 'r') as file:
        html_content = file.read()
    
    with open('modified_index.html', 'w') as file:
        file.write(addNewDiv(html_content))

