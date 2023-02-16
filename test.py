from collections import defaultdict
import xml.etree.ElementTree as ET

filepath = r"C:\Program Files\ANSYS Inc\v232\commonfiles\help\en-us\fluent_gui_help\fluent_gui_help.xml"

def get_prefix(id):
    prefix_by_id = {
        "enableturbo" : "twf",
        "lbws" : "lbapp",
        "aerws" : "aeroworkflow",
        "gpuws" : "gpuapp",
        "postws" : "post_analysis",
        "postws_file" : "file_results",
        "postws_live" : "live_results",
        "fluent_tui_field_help" : "flu",
    }
    return prefix_by_id.get(id, id)

tree = ET.parse(filepath)
data = defaultdict(lambda: defaultdict(str))
for article in tree.findall("article"):
    for sect1 in article.findall("sect1"):
        sect1_id = sect1.get("id")
        for sect2 in sect1.findall("sect2"):
            sect2_id = sect2.get("id")
            prefix = get_prefix(sect1_id)
            sect2_id = sect2_id.removeprefix(prefix + "_")
            data[sect1_id][sect2_id] = "".join(sect2.find("p").itertext())

with open("duplicates.txt", "w") as f:
    for k in data["enablecleancad"]:
        if k in data["enabledirtycad"]:
            clean_cad_help = data["enablecleancad"][k].strip()
            dirty_cad_help = data["enabledirtycad"][k].strip()
            if clean_cad_help != dirty_cad_help:
                f.write(f"{k}:\n{clean_cad_help}\n{dirty_cad_help}\n\n")
