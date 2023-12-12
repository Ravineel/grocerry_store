from jinja2 import Template
from weasyprint import HTML
import os
from datetime import datetime


def create_report(user, total_orders, total_expense, frequent_product,frequency, most_bought_product,product_bought_qty, message_type):
  try:
    
    
    template_path = './templates/user_report.html'
    
    # template_path = path+'/templates/user_report'
    
    
    template = Template(open(template_path).read())
    
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "Octomber", "November", "December"]
    
    current_month = datetime.now().month
    current_year  = datetime.now().year
    
    html = template.render(
      user=user, 
      total_orders=total_orders, 
      total_expense=total_expense, 
      frequent_product=frequent_product,
      frequency=frequency, 
      most_bought_product=most_bought_product,
      product_bought_qty=product_bought_qty,
      current_month=months[current_month-1],
      current_year=current_year
    )
   
    
    if message_type == "html":
      reponse = {
        "file_name": "",
        "html_message": html
      }
      return reponse
    else:
      print("in pdf")
      pdf = HTML(string=html)
      print("pdf")
      file_name = "./reports/report_"+str(user.first_name)+"_"+str(user.last_name)+".pdf"
      pdf.write_pdf(target=file_name)
      
      reponse = {
        "file_name": file_name,
        "html_message": ""
      }
      
      return reponse
  except Exception as e:
    print(e)
    raise e
  
    
    
  
  