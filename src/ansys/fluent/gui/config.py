
def _report_definition_output_procesor(output):
    processed_output = eval(output)
    formatted_output= "********************************\n"
    formatted_output+= "   Report definitions Output\n"
    formatted_output+= "********************************\n"
    for report_name, report_data in  processed_output.items():
        formatted_output+=f"{report_name:15}:  {report_data[0]:15.5E}\n"
    return formatted_output   

async_commands = {"solution/run-calculation": ["iterate"]}

commands_output={
    "solution/report-definitions":{
        "compute":{
            "output": _report_definition_output_procesor,
            "style": {'width': '100%', 'height': 300}           
      
        }
    
    }
}
