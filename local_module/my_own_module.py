#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: my_own_module
short_description: Создаем текстовый файл
version_added: "1.0.0"
description:
  - Создаёт/обновляет текстовый файл
options:
  path:
    description: Путь к файлу.
    required: true
    type: str
  content:
    description: Содержимое файла.
    required: true
    type: str
author:
  - Egor (@n0rthf1ght3r)
'''
EXAMPLES = r'''
- name: Создать файл
  my_own_module:
    path: /tmp/hello.txt
    content: "Hello, Ansible!"
'''
RETURN = r'''
changed: {type: bool}
path: {type: str}
size: {type: int}
message: {type: str}
'''

import os
from ansible.module_utils.basic import AnsibleModule

def run_module():
    module_args = dict(
        path=dict(type='str', required=True),
        content=dict(type='str', required=True),
    )
    result = dict(changed=False, path='', size=0, message='')
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    path, content = module.params['path'], module.params['content']
    result['path'] = path

    current = None
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            current = f.read()

    will_change = (current != content)

    if module.check_mode:
        result['changed'] = will_change
        result['message'] = 'check_mode'
        module.exit_json(**result)

    os.makedirs(os.path.dirname(path) or '.', exist_ok=True)

    if will_change or not os.path.exists(path):
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        result.update(changed=True, message='file written', size=len(content))
    else:
        result.update(message='already up-to-date', size=len(content))

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
