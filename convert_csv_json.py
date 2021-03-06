#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json


class Convert2Json(object):
    recap = False
    chapter = 0
    csv_dict = {}

    #Get Command Line Arguments
    def run(self):
        self.read_csv("database.csv", "database.json", 1)
        self.read_csv("part.csv", "part.json", 0)
        self.read_csv("index.csv", "index.json", 2)

    def parse_part(self, row):
        fields = row.split("::")
        exists_paragraph = False
        paragraphs = [p['id'] for p in self.csv_dict['paragraph'] if p['chapter'] == int(fields[0])]
        if paragraphs:
            exists_paragraph = True
        return {'id': int(fields[0]),
                'parent': int(fields[1]),
                'name': fields[2],
                'exist_paragraph': exists_paragraph}

    def parse_index(self, row):
        fields = row.split("::")
        key_dict = {'Á': 'A', 'Ú': 'U',
                    'Ď': 'D', 'ú': 'u', 'ď': 'd'}
        name = fields[2].strip()
        if name.startswith("<b>"):
            if name.startswith("<b>ch"):
                key = "ch"
            else:
                key = name[3]
        else:
            key = name[0]
        if key in key_dict.keys():
            key = key_dict[key]
        refs = self.parse_refs(fields[1])
        return {'see': fields[0], 'refs': refs, 'key': key.upper(), 'name': fields[2].strip()}

    def parse_refs(self, refs):
        if '-' in refs:
            list_refs = []
            for r in refs.split(','):
                if '-' in r:
                    begin, end = r.split('-')
                    list_refs.extend(map(str, range(int(begin), int(end)+1)))
                else:
                    list_refs.append(r)
            return ','.join(list_refs)
        else:
            return refs

    def parse_database(self, row):
        fields = row.split("::")
        if "souhrn" in fields[2].lower():
            self.recap = True
            self.chapter = int(fields[3])
        else:
            try:
                if self.chapter != int(fields[3]) or fields[2] != "":
                    self.recap = False
            except ValueError:
                fields[3] = 0
                self.recap = False
        refs = self.parse_refs(fields[4])
        return {'id': int(fields[0]),
                'caption': fields[1],
                'caption_no_html': fields[2],
                'chapter': int(fields[3]),
                'refs': refs,
                'text': fields[5],
                'text_no_html': fields[6],
                'recap': int(self.recap),
                }

    #Read CSV File
    def read_csv(self, input_file, output_file, fnc):
        csv_content = []
        if fnc == 0:
            name = "chapters"
        elif fnc == 1:
            name = "paragraph"
        else:
            name = "index"
        with open(input_file, 'r') as csvfile:
            for row in csvfile.readlines():
                if fnc == 0:
                    csv_content.append(self.parse_part(row))
                elif fnc == 1:
                    csv_content.append(self.parse_database(row))
                else:
                    csv_content.append(self.parse_index(row))
            self.write_json(csv_content, name, output_file)

    #Convert csv data into json and write it
    def write_json(self, data, name, json_file):
        data_to_write = {name: data}
        self.csv_dict[name] = data
        with open(json_file, "w") as f:
            json.dump(data_to_write, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    cj = Convert2Json()
    cj.run()
