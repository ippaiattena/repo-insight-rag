import os

def get_project_structure(root_path: str) -> str:
    """
    指定されたルートディレクトリ以下のフォルダ・ファイル構成を文字列として返す。
    
    Parameters:
    - root_path: プロジェクトのルートパス
    
    Returns:
    - str: treeコマンド風のテキスト構造
    """
    lines = []

    def walk(dir_path, prefix=""):
        entries = sorted(os.listdir(dir_path))
        for idx, entry in enumerate(entries):
            full_path = os.path.join(dir_path, entry)
            connector = "└── " if idx == len(entries) - 1 else "├── "
            lines.append(f"{prefix}{connector}{entry}")
            if os.path.isdir(full_path):
                extension = "    " if idx == len(entries) - 1 else "│   "
                walk(full_path, prefix + extension)

    project_name = os.path.basename(os.path.abspath(root_path))
    lines.append(project_name + "/")
    walk(root_path)

    return "\n".join(lines)
