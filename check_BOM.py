"""
Checks BOM files for format and integrity to assure LCI can be generated
"""

import xlrd
import os

bom_directory = os.path.realpath('data-foreground/')
files = ["BOM_1.xlsx", "BOM_2.xlsx"]

def main():

    for f in files:
        wb_path = bom_directory + os.path.sep + f
        wb = xlrd.open_workbook(wb_path)
        print("Check file", f)
        for sheet_name in wb.sheet_names():
            print("  Check sheet", sheet_name)
            sheet = wb.sheet_by_name(sheet_name)

            stack = []
            for r in range(1, sheet.nrows):
                part_number = _cell_str(sheet, r, 1)
                if part_number == "":
                    break

                level = int(sheet.cell_value(r, 0))
                while len(stack) > level:
                    stack.pop()

                if level > 0:
                    parent = _cell_str(sheet, r, 5)
                    if stack[level - 1] != parent:
                        print("    err: row %i next=%s but parent=%s" % (
                            r, parent, stack[level - 1]))
                stack.append(part_number)


def _cell_str(sheet, row, col) -> str:
    cell = sheet.cell(row, col)
    if cell is None:
        return ""
    if cell.value is None:
        return ""
    return str(cell.value).strip()


if __name__ == "__main__":
    main()
