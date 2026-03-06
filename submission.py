import zipfile
import os
from datetime import datetime
from pathlib import Path


def find_report():
    candidates = []

    for f in os.listdir("."):
        p = Path(f)
        if p.is_file() and p.suffix.lower() in {".pdf", ".md"} and "report" in p.stem.lower():
            candidates.append(p)

    if not candidates:
        return None

    # 优先 pdf，其次 md；同类型下按文件名字典序
    candidates.sort(key=lambda x: (x.suffix.lower() != ".pdf", x.name.lower()))
    return candidates[0]


def main():
    print("Please enter your name (e.g. Xiao Ming): ", end="")
    name = input().strip()
    print("Please enter your student ID (e.g. 123090613): ", end="")
    student_id = input().strip()

    meta = (
        f"student_id: {student_id}\n"
        f"name: {name}\n"
        f"date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    )
    meta_file = Path(".metainfo.txt")
    meta_file.write_text(meta, encoding="utf-8")

    report = find_report()
    if report is None:
        print("Warning: No report file found (any .pdf/.md containing 'report', case-insensitive)")

    src_files = list(Path("src").rglob("*")) if Path("src").exists() else []
    extra_files = [Path("CMakeLists.txt")] if Path("CMakeLists.txt").exists() else []

    zip_name = f"{student_id}_submission.zip"
    with zipfile.ZipFile(zip_name, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.write(meta_file, arcname=meta_file.name)

        for f in src_files:
            if f.is_file():
                zf.write(f, arcname=str(f))

        for f in extra_files:
            zf.write(f, arcname=f.name)

        if report:
            new_report_name = f"{student_id}_report{report.suffix.lower()}"
            zf.write(report, arcname=new_report_name)

    meta_file.unlink()
    print(f"Generate to: {zip_name}")


if __name__ == "__main__":
    main()