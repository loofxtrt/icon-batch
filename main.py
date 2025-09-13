import argparse
import sys
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QMainWindow, QListWidget, QListWidgetItem
from PyQt6.QtGui import QPixmap, QIcon, QShortcut, QKeySequence

ROOT = Path('/mnt/seagate/workspace/coding/projects/icons/copycat/copycat')

def set_parser():
    # definir o parser e seus parâmetros
    parser = argparse.ArgumentParser()
    parser.add_argument('search_term')
    return parser

def search_for(search_term: str) -> list:
    # procurar recursivamente por arquivos contendo o termo pesquisado no nome
    # a partir do diretório raiz, e incluir apenas arquivos
    found = [f for f in ROOT.rglob('**/*') if f.is_file() and search_term in f.name]
    return found

def build_qlist(paths: list[Path]) -> QListWidget:
    list_widget = QListWidget()
    list_widget.setSelectionMode(QListWidget.SelectionMode.MultiSelection) # permitir múltiplas seleções

    # criar uma entrada na lista pra cada path de ícone achado
    for p in paths:
        # define o ícone da entrada, convertendo o path pra pixmap
        pixmap = QPixmap(str(p))
        icon = QIcon(pixmap)

        # cria a entrada em si, exibindo o nome do ícone sem extensão ao lado
        entry = QListWidgetItem(icon, p.stem)

        # adiciona a lista final
        list_widget.addItem(entry)

    return list_widget

def copy_selected_items(qlist: QListWidget, qapp: QApplication):
    # obter todos os ícones selecionados e retornar uma string com os nomes deles
    # o .text() faz adicionar apenas o texto e não o ícone em si
    selected = qlist.selectedItems()
    final_string = '\n'.join(s.text() for s in selected)

    # copiar a string pra clipboard do sistema
    clipboard = qapp.clipboard()
    clipboard.setText(final_string)

def main():
    # obter os argumentos passados pro parser
    parser = set_parser()
    args = parser.parse_args()
    search_term = args.search_term

    # construir o app
    app = QApplication(sys.argv)

    # construir a janela
    window = QMainWindow()
    window.setGeometry(0, 0, 1000, 600)

    # chamar a pesquisa e construir a lista de resultados
    found = search_for(search_term)
    qlist = build_qlist(found)

    window.setCentralWidget(qlist)

    # definir o atalho pra copiar os nomes dos itens selecionados
    shortcut = QShortcut(QKeySequence('Ctrl+C'), window)
    shortcut.activated.connect(lambda: copy_selected_items(qlist, app))

    # executar o app
    window.show()
    sys.exit(app.exec())

main()