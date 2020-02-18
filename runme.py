import io
import sys
import logging
from lxml import etree as ET
from datetime import datetime as dt

# Для записи нового файла
class File(object):
    def __init__(self, file_name, method):
        self.file_obj = open(file_name, method)
    def __enter__(self):
        return self.file_obj
    def __exit__(self, type, value, traceback):
        self.file_obj.close()

# Путь к файлам
def path_to_file(name):
    return input(f'Enter the path to the {name} file: ')


# Валидация входного XML файла
def validate(xml_path, xsd_path):
    xmlschema_doc, xml_doc = ET.parse(xsd_path), ET.parse(xml_path)
    xmlschema = ET.XMLSchema(xmlschema_doc)
    result = xmlschema.validate(xml_doc)
    if result:
        logging.info(f'{dt.today().strftime("Date %d.%m.%Y time %H:%M:%S")}# Input XML file has validated! Path: {xml_path}')
        return result
    logging.error(f'{dt.today().strftime("Date %d.%m.%Y time %H:%M:%S")}# Input XML file does NOT validate. Path: {xml_path}.')
    sys.exit(1)


# Трансформация XML файла используя XSL файл
def transform_xml(xml_path, xslt_path):
    try:
        xml, xslt = ET.parse(xml_path), ET.parse(xslt_path)
        transform = ET.XSLT(xslt)
        result = transform(xml)
        logging.info(f'{dt.today().strftime("Date %d.%m.%Y time %H:%M:%S")}# '
                     f'Input XML file has transformed! Path: {xml_path}')
        return str(result)
    except:
        logging.error(f'{dt.today().strftime("Date %d.%m.%Y time %H:%M:%S")}# '
                      f'Input XML file does NOT transform. Path: {xml_path}.')
        sys.exit(1)


# Валидация полученных данных после трансформации и отправка после валидации на запись
def result_valid(result, xsd_path, xml_file_name):
    xmlschema_doc, xml_doc_string = ET.parse(xsd_path), io.StringIO(result)
    xmlschema = ET.XMLSchema(xmlschema_doc)
    xml_doc = ET.parse(xml_doc_string)
    is_validate = xmlschema.validate(xml_doc)
    if is_validate:
        logging.info(f'{dt.today().strftime("Date %d.%m.%Y time %H:%M:%S")}# '
                     f'New XML file has validated! Name new file: {xml_file_name}')
        return write_file(result, xml_file_name)
    logging.error(f'{dt.today().strftime("Date %d.%m.%Y time %H:%M:%S")}# '
                  f'New XML file does NOT validate. Name new file: {xml_file_name}')
    sys.exit(1)


# Запись данных в новый XML файл
def write_file(result, xml_file_name):
    try:
        with File(xml_file_name, 'w') as opened_file:
            opened_file.write(result)
        logging.info(f'{dt.today().strftime("Date %d.%m.%Y time %H:%M:%S")}# New XML file recorded! Name new file: {xml_file_name}')
    except:
        logging.error(f'{dt.today().strftime("Date %d.%m.%Y time %H:%M:%S")}# Input XML file does NOT recorded. Name new file: {xml_file_name}')
        sys.exit(1)


# Для ввода данных
def input_data():
    return path_to_file('xml'), path_to_file('xsd'), path_to_file('xslt'), path_to_file('result (new)')


# Подготовленные данные для demo mode
def run_script_demo_mode():
    return 'xml_file.xml', 'xsd_file.xsd', 'xls_file.xsl', 'RESULT_xml_file.xml'


def main():
    logging.basicConfig(filename="logs.log", level=logging.INFO)
    logging.info('\n============= NEW =============')
    xml_path, xsd_path, xslt_path, new_xml = input_data()
    logging.info(f'Used next files: \n{xml_path}, \n{xsd_path}, \n{xslt_path}, \n{new_xml}')
    validate(xml_path, xsd_path)
    new_data_xml = transform_xml(xml_path, xslt_path)
    result_valid(new_data_xml, xsd_path, new_xml)

def main_demo():
    logging.basicConfig(filename="logs.log", level=logging.INFO)
    logging.info('\n============= DEMO MODE =============')
    xml_path, xsd_path, xslt_path, new_xml = run_script_demo_mode()
    logging.info(f'Used next files: \n{xml_path}, \n{xsd_path}, \n{xslt_path}, \n{new_xml}')
    validate(xml_path, xsd_path)
    new_data_xml = transform_xml(xml_path, xslt_path)
    result_valid(new_data_xml, xsd_path, new_xml)
    print('Well done!')


# Меню для возможности запуска demo режима.
# demo = input('Press "Y" to enter your data or "N" to start the demo mode: ').lower()
# if demo == 'n':
#     main_demo()
#     exit(0)
# else:
#     main()
#     exit(0)


if __name__ == "__main__":
    # execute only if run as a script
    main()