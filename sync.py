import os
import sys
import glob
OUTPUT_FILE = "output.txt"
FILE_MARK = "===== FILE: "
IGNORE_DIRS = {
   ".gradle",
   ".git",
   ".idea",
   "node_modules",
   "build"
}
IGNORE_EXT = {
   ".png", ".jpg", ".jpeg", ".webp",
   ".mp4", ".zip", ".apk", ".aar"
}
IGNORE_DIR_PATTERNS = {
   "src/test",
   "src/androidTest"
}
ONLY_SRC = False
CODE_ONLY = False
SPLIT_LINES = None

def is_binary(file):
   ext = os.path.splitext(file)[1].lower()
   return ext in IGNORE_EXT

def is_code_file(file):
   ext = os.path.splitext(file)[1].lower()
   return ext in {".kt", ".java"}

def should_ignore_path(path):
   normalized = path.replace("\\", "/")
   for pattern in IGNORE_DIR_PATTERNS:
       if pattern in normalized:
           return True
   return False

def build_tree(root_dir):
   tree = []
   for root, dirs, files in os.walk(root_dir):
       dirs[:] = [
           d for d in dirs
           if d not in IGNORE_DIRS
           and not should_ignore_path(os.path.join(root, d))
       ]
       level = root.replace(root_dir, "").count(os.sep)
       indent = "│   " * level
       if root != root_dir:
           tree.append(f"{indent}├── {os.path.basename(root)}/")
       for file in files:
           if file in [OUTPUT_FILE, "folder_sync.py"]:
               continue
           if is_binary(file):
               continue
           full_path = os.path.join(root, file)
           if os.path.islink(full_path):
               continue
           normalized = full_path.replace("\\", "/")
           # src filter
           if ONLY_SRC and "/src/main/" not in normalized:
               continue
           # test filter
           if should_ignore_path(full_path):
               continue
           # code-only filter
           if CODE_ONLY and not is_code_file(file):
               continue
           file_indent = "│   " * (level + 1)
           tree.append(f"{file_indent}├── {file}")
   return "\n".join(tree)

def export_folder(root_dir):
   all_lines = []
   # ===== TREE =====
   all_lines.append("PROJECT TREE\n")
   all_lines.append("============\n\n")
   all_lines.append(build_tree(root_dir) + "\n\n\n")
   for root, dirs, files in os.walk(root_dir):
       dirs[:] = [
           d for d in dirs
           if d not in IGNORE_DIRS
           and not should_ignore_path(os.path.join(root, d))
       ]
       for file in files:
           if file in [OUTPUT_FILE, "folder_sync.py"]:
               continue
           if is_binary(file):
               continue
           full_path = os.path.join(root, file)
           if os.path.islink(full_path):
               continue
           normalized = full_path.replace("\\", "/")
           # src filter
           if ONLY_SRC and "/src/main/" not in normalized:
               continue
           # test filter
           if should_ignore_path(full_path):
               continue
           # code-only filter
           if CODE_ONLY and not is_code_file(file):
               continue
           try:
               rel_path = os.path.relpath(full_path, root_dir).replace("\\", "/")
           except ValueError:
               continue
           all_lines.append(f"{FILE_MARK}{rel_path} =====\n")
           try:
               with open(full_path, "r", encoding="utf-8") as f:
                   content = f.read().rstrip()
                   all_lines.append(content + "\n\n")
           except:
               all_lines.append("[BINARY_FILE_SKIPPED]\n\n")
   # ===== WRITE =====
   if not SPLIT_LINES:
       with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
           f.writelines(all_lines)
       print("Export completed → output.txt")
   else:
       chunk = []
       count = 0
       file_index = 1
       for line in all_lines:
           chunk.append(line)
           count += 1
           if count >= SPLIT_LINES:
               with open(f"output_part{file_index}.txt", "w", encoding="utf-8") as f:
                   f.writelines(chunk)
               chunk = []
               count = 0
               file_index += 1
       if chunk:
           with open(f"output_part{file_index}.txt", "w", encoding="utf-8") as f:
               f.writelines(chunk)
       print(f"Export completed → {file_index} part(s)")

def import_folder(root_dir):
   part_files = sorted(glob.glob("output_part*.txt"))
   if part_files:
       print(f"Importing from {len(part_files)} parts...")
       files_to_read = part_files
   elif os.path.exists(OUTPUT_FILE):
       files_to_read = [OUTPUT_FILE]
   else:
       print("ERROR: No output file found")
       return
   current_file = None
   buffer = []
   start = False
   def flush():
       nonlocal buffer, current_file
       if current_file:
           file_path = os.path.join(root_dir, current_file)
           os.makedirs(os.path.dirname(file_path), exist_ok=True)
           with open(file_path, "w", encoding="utf-8") as wf:
               wf.write("".join(buffer))
       buffer = []
   for file_name in files_to_read:
       with open(file_name, "r", encoding="utf-8") as f:
           lines = f.readlines()
       for line in lines:
           if line.startswith(FILE_MARK):
               start = True
               flush()
               path = line.replace(FILE_MARK, "").replace("=====", "").strip()
               current_file = path
               continue
           if not start:
               continue
           buffer.append(line)
   flush()
   print("Import completed → project restored")

def main():
   global ONLY_SRC, CODE_ONLY, SPLIT_LINES
   if len(sys.argv) < 2:
       print("Usage:")
       print("python folder_sync.py export [path] [--src] [--code-only] [--split N]")
       print("python folder_sync.py import [path]")
       return
   mode = sys.argv[1]
   # ===== FLAGS =====
   ONLY_SRC = "--src" in sys.argv
   CODE_ONLY = "--code-only" in sys.argv
   if "--split" in sys.argv:
       idx = sys.argv.index("--split")
       if idx + 1 < len(sys.argv):
           SPLIT_LINES = int(sys.argv[idx + 1])
   # ===== PATH =====
   if len(sys.argv) >= 3 and not sys.argv[2].startswith("--"):
       root_dir = sys.argv[2]
   else:
       root_dir = os.getcwd()
   root_dir = os.path.abspath(root_dir)
   if not os.path.exists(root_dir):
       print(f"ERROR: path not found -> {root_dir}")
       return
   print(f"Working directory: {root_dir}")
   # ===== RUN =====
   if mode == "export":
       export_folder(root_dir)
   elif mode == "import":
       os.chdir(root_dir)
       import_folder(root_dir)
   else:
       print("Invalid mode")

if __name__ == "__main__":
   main()

