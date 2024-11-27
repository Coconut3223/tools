"""https://github.com/zyzcss/python-diff/tree/main"""


import re
from typing import List, Optional

class Separator:

    EN_Word = "( |.|!|,)"
    ZH_Word = "(|\s|\n|\r\n)"
    EN_Char = ""

class DemoDiff:

    def __init__(self):

        pass

    def tokenize(self, separator:str, value:str):
        ret_lines = []
        lines_and_newlines = re.split(separator, value)
        if not lines_and_newlines[-1]:
            lines_and_newlines.pop()

        for i, line in enumerate(lines_and_newlines):
            if i % 2:
                ret_lines[-1] += line
            else:
                ret_lines.append(line)
        return ret_lines
    
    def equals(self, left, right):
        return left == right

    def push_component(self, components, insertion, deletion):
        last = components[-1] if len(components) > 0 else False
        if last and last.get('ins') == insertion and last.get('del') == deletion:
            components[-1] = {'count': last.get('count') + 1, 'ins': insertion, 'del': deletion}
        else:
            components.append({'count': 1, 'ins': insertion, 'del': deletion})

    def extract_common(self, base_path, new_string, old_string, diagonal_path):
        new_len = len(new_string)
        old_len = len(old_string)
        new_pos = base_path.get('new_pos')
        old_pos = new_pos - diagonal_path

        common_count = 0

        while new_pos + 1 < new_len and old_pos + 1 < old_len and self.equals(new_string[new_pos + 1],
                                                                              old_string[old_pos + 1]):
            new_pos += 1
            old_pos += 1
            common_count += 1

        if common_count:
            base_path.get('components').append({'count': common_count})

        base_path['new_pos'] = new_pos
        return old_pos

    def remove_empty(self, array):
        ret = []
        for arr in array:
            if arr:
                ret.append(arr)
        return ret

    def join(self, chars):
        return ''.join(chars)

    def run(self, old_string, new_string, unit='word', lang='zh'):

        if unit == "word" and lang == "zh":
            separator = Separator.ZH_Word

        old_string, new_string = map(lambda x: self.remove_empty(self.tokenize(separator, x)), 
                                     [old_string, new_string])
        old_len = len(old_string)
        new_len = len(new_string)
        # 编辑长度
        self.edit_len = 1
        max_len = old_len + new_len

        best_path = {0: {'new_pos': -1, 'components': []}}

        old_pos = self.extract_common(best_path.get(0), new_string, old_string, 0)
        if best_path.get(0).get('new_pos') + 1 >= new_len and old_pos + 1 >= old_len:
            return [{'value': ''.join(new_string), 'count': len(new_string)}]

        def build_values(diff, components, new_string, old_string, use_longest_token):
            component_pos = 0
            component_len = len(components)
            _new_pos = 0
            _old_pos = 0

            while component_pos < component_len:
                component = components[component_pos]
                count = component.get('count')
                if not component.get('del'):
                    component['value'] = ''.join(new_string[_new_pos: _new_pos + count])
                    _new_pos += count

                    if not component.get('ins'):
                        _old_pos += count
                else:
                    component['value'] = ''.join(old_string[_old_pos: _old_pos + count])
                    _old_pos += count
                    if component_pos and components[component_pos - 1].get('ins'):
                        tmp = components[component_pos - 1]
                        components[component_pos - 1] = components[component_pos]
                        components[component_pos] = tmp
                component_pos += 1

            last_component = components[component_len - 1]
            if component_len > 1 and type(last_component.get('value')) == str and (
                    last_component.get('ins') or last_component.get('del')) and '' == last_component.get(
                                                                                                      'value'):
                components[component_len - 2]['value'] += last_component.get('value')
                components.pop()
            return components

        def clone_path(path):
            return {
                'new_pos': path.get('new_pos'),
                'components': path.get('components').copy(),
            }

        def exec_edit_length(self):
            diagonal_path = -1 * self.edit_len
            while diagonal_path <= self.edit_len:
                base_path = False
                add_path = best_path.get(diagonal_path - 1)
                remove_path = best_path.get(diagonal_path + 1)
                _old_pos = (remove_path.get('new_pos') if remove_path else 0) - diagonal_path

                if add_path:
                    best_path[diagonal_path - 1] = False

                can_add = add_path and add_path.get('new_pos') + 1 < new_len
                can_remove = remove_path and (0 <= _old_pos) and (_old_pos < old_len)

                if not can_add and not can_remove:
                    best_path[diagonal_path] = False
                    diagonal_path += 2
                    continue

                if not can_add or (can_remove and add_path.get('new_pos') < remove_path.get('new_pos')):
                    base_path = clone_path(remove_path)
                    self.push_component(base_path.get('components'), False, True)
                else:
                    base_path = add_path
                    base_path['new_pos'] += 1
                    self.push_component(base_path.get('components'), True, False)

                _old_pos = self.extract_common(base_path, new_string, old_string, diagonal_path)

                if (base_path.get('new_pos') + 1) >= new_len and (_old_pos + 1) >= old_len:
                    return build_values(self, base_path.get('components'), new_string, old_string, False)
                else:
                    best_path[diagonal_path] = base_path
                diagonal_path += 2
            self.edit_len += 1

        while self.edit_len <= max_len:
            ret = exec_edit_length(self)
            if ret:
                return ret
        return []
    
    
    def show_md(self, results: List[List[dict]], md_path:str=None, keywords:Optional[List[str]]=None):
        
        md_styles = {
            "ins": (
                f"<span style='color:green;font-weight:500;'>",
                "</span>",
            ),
            "del": (
                f"<span style='color:red;font-weight:500;text-decoration:line-through;'>",
                "</span>",
            ),
            "ins_keys": (
                f"<span style='color:green;font-weight:700;background-color:#FFF3CC;'>",
                "</span>",
            ),
            "del_keys": (
                f"<span style='color:red;font-weight:700;text-decoration:line-through;background-color:#FFF3CC;'>",
                "</span>",
            ),
            "keys": (
                f"<span style='font-weight:700;background-color:#FFF3CC;'>",
                "</span>",
            )
        }


        def filer_keys(v):
            import re
            return True if re.search(f"({'|'.join(keywords)})", v) else False

        md_contents = []
        for res in results:
            contents = []
            for item in res:
                k = item.keys()
                v = item['value'].replace('$', '\$')
                
                if 'ins' in k and v != ' ':
                    if item['ins'] == True:
                        tag = 'ins'
                    elif item['del'] == True:
                        tag = 'del'
                    
                    if keywords and filer_keys(v):
                        tag += '_keys'
                    
                    content = fr"{v}".join(md_styles[tag])

                else:
                    if keywords and filer_keys(v):
                        content = fr"{v}".join(md_styles["keys"])
                    else:
                        content = v

                contents.append(content)

            md_contents.append(''.join(contents))
        md_content = '\n\n'.join(md_contents)

        if md_path:
            with open(md_path, 'w', encoding='utf-8') as f:
                f.write(md_content)
        else:
            print(md_content)

        return md_content

demo_diff =  DemoDiff()


if __name__ == "__main__":

    a = """嗯，政府法案首度，二零一四年，今年撥款條例草案二，讀蔡英文政司司長。 主席 主席 各位議員，各位市民早晨。 本港喺疫後復上嘅一年，社會同市民迎來期待已久嘅正常生活，旅客量回升，經濟會回復增長，連串盛事活動帶動市面氣氛回復暢旺。\n"""
    b = """嗯，政府法案首度於二零一四年，今年撥款條例草案第二，讀蔡英文政司司長。主席，主席，各位議員，各位市民早晨。本港在疫後復甦的一年，社會及市民迎來期待已久的正常生活，旅客量回升，經濟會回復增長，連串盛事活動帶動市面氣氛回復暢旺。"""
    res = demo_diff.run(a, b)
    demo_diff.show_md([res], "ddd.md")