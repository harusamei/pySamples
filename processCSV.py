import csv
import json

def read_csv(csv_filename):
    csv_rows = []
    with open(csv_filename, 'r',encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            csv_rows.append(row)
    return csv_rows

def csv2jsonfile(csv_rows, json_filename):
    with open(json_filename, 'w') as json_file:
        json.dump(csv_rows, json_file, indent=4)

def oneRow2json(csv_row):
    # 不加ensure_ascii=False的话，中文会被转换为Unicode编码,\uXXXX
    return json.dumps(csv_row, indent=4, ensure_ascii=False)

def json2dict(json_str):
    return json.loads(json_str)
 

if __name__ == '__main__':
    csv_filename = 'data/xiaoxin.csv'
    json_filename = 'data/xiaoxin.json'

    csv_rows = read_csv(csv_filename)
    csv2jsonfile(csv_rows, json_filename)
    print(oneRow2json(csv_rows[0]))
    print(json2dict(oneRow2json(csv_rows[0])))
    
