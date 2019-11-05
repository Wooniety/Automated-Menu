# Reading an excel file using Python 
  
# Give the location of the file 
stock = ("../data/menu.xlsx") 
  
# To open Workbook 
wb = xlrd.open_workbook(stock) 
sheet = wb.sheet_by_index(0) 
  
# For row 0 and column 0 
print(sheet.cell_value(0, 0)) 
