from xml.dom import minidom
import pdb
def get_files_list():
	return ['telephone5.svg'];

def remove_empty_g_tags(svg_content):
	for node in svg_content.getElementsByTagName('g'):
		print '--------------------------------------'
		print '- Cleaning g element'
		print node.childNodes
		for child_node in list(node.childNodes):
			print '-- childNode: ', child_node
			if child_node.attributes == None:
				print '-- Removed'
				node.childNodes.remove(child_node)
			else:
				print '-- Passed'
				continue
		if len(node.childNodes) == 0:
			print '-- g element removed because it\'s empty'
			print '- Done'
			print '-----------------------------------'
			node.parentNode.childNodes.remove(node)
	return svg_content


def flatten_path_nodes(svg_content):
	for node in svg_content.getElementsByTagName('path'):
		node.attributes['d'].value = ' '.join(node.attributes['d'].value.split())
		pass
	return svg_content

def change_svg_id(file_name, svg_content):
	for node in svg_content.getElementsByTagName('svg'):
		node.attributes['id'].value = "icon-%s" % file_name[:file_name.rfind('.')]
	return svg_content

def clean_svg_file(file_name):
	svg_content = minidom.parse(file_name)
	svg_content = remove_empty_g_tags(svg_content)
	svg_content = flatten_path_nodes(svg_content)
	svg_content = change_svg_id(file_name, svg_content)
	return svg_content

def save_cleaned_file(file_name, cleaned_svg_dom):
	pretty_xml_str = cleaned_svg_dom.toprettyxml()
	pretty_xml_str = '\n'.join([line for line in pretty_xml_str.split('\n') if line.strip()])
	#backup
	with open(file_name) as in_file:
		with open(file_name + ".bkup", 'wb') as out_file:
			out_file.write(in_file.read())
	#override the file
	with open(file_name + ".cleaned", 'wb') as out_file:
		out_file.write(pretty_xml_str)

def start_cleaning():
	files_list = get_files_list()
	for file_name in files_list:
		cleaned_svg_dom = clean_svg_file(file_name)
		print cleaned_svg_dom.getElementsByTagName('g')
		save_cleaned_file(file_name, cleaned_svg_dom)



if __name__ == "__main__":
	start_cleaning()