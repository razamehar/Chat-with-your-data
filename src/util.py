from urllib.parse import urlparse
from loader import load_pdf, load_word, load_excel, load_url


def is_url(file_path: str) -> bool:
    parsed_url = urlparse(file_path)
    return all([parsed_url.scheme, parsed_url.netloc])


def load_document(choice: str, file_path: str, file_type: str) -> str:
    if choice == '1':
        load_pdf(file_path, file_type)
    elif choice == '2':
        load_word(file_path, file_type)
    elif choice == '3':
        load_excel(file_path, file_type)
    elif choice == '4':
        load_url(file_path, file_type)
    else:
        return "Invalid choice. Please select a valid document type."


def initiate():
    print('Hello. I am Taira. I can help you chat with your documents. Please select the type of document you would '
          'like to load:')
    print('1. PDF')
    print('2. Word')
    print('3. Excel')
    print('4. URL')

    choice = input('Enter your choice: ')

    if choice not in ['1', '2', '3', '4']:
        print('Goodbye. Have a great day.')
        return

    file_path = input('Enter the path to the document: ')

    if is_url(file_path):
        load_document(choice, file_path, 'webpage')

    extension = file_path.split('.')[-1]

    if extension in ['docx', 'doc']:
        load_document(choice, file_path, 'Word')

    elif extension in ['docx', 'doc', 'xlsx', 'xls']:
        load_document(choice, file_path, 'Excel')

    elif extension in ['pdf']:
        load_document(choice, file_path, 'PDF')
