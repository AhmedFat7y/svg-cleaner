import os
from xml.dom import minidom
import pdb
def get_files_list(base_dir):
	print base_dir
	return os.listdir(base_dir)

def filter_files_list(files_list):
	return [f for f in files_list if f[-3:] == 'svg']

def remove_empty_g_tags(svg_content):
	for node in svg_content.getElementsByTagName('g'):
		# print '--------------------------------------'
		# print '- Cleaning g element'
		# print node.childNodes
		for child_node in list(node.childNodes):
			# print '-- childNode: ', child_node
			if child_node.attributes == None:
				# print '-- Removed'
				node.childNodes.remove(child_node)
			else:
				# print '-- Passed'
				continue
		if len(node.childNodes) == 0:
			# print '-- g element removed because it\'s empty'
			# print '- Done'
			# print '-----------------------------------'
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

def clean_svg_file(base_dir, file_name):
	svg_content = minidom.parse(os.path.join(base_dir, file_name))
	svg_content = remove_empty_g_tags(svg_content)
	svg_content = flatten_path_nodes(svg_content)
	svg_content = change_svg_id(file_name, svg_content)
	return svg_content

def save_cleaned_file(base_dir, file_name, cleaned_svg_dom):
	pretty_xml_str = cleaned_svg_dom.toprettyxml()
	pretty_xml_str = '\n'.join([line for line in pretty_xml_str.split('\n') if line.strip()])
	#backup
	with open(os.path.join(base_dir, file_name)) as in_file:
		with open(os.path.join(base_dir, file_name + ".bkup"), 'wb') as out_file:
			out_file.write(in_file.read())
	#override the file
	with open(os.path.join(base_dir, file_name), 'wb') as out_file:
		out_file.write(pretty_xml_str)

def start_cleaning():
	base_dir = os.path.dirname(os.path.realpath(__file__))
	files_list = get_files_list(base_dir)
	files_list = filter_files_list(files_list)
	print files_list
	for file_name in files_list:
		print '--------------------------------------'
		print 'cleaning file %s.' % file_name
		cleaned_svg_dom = clean_svg_file(base_dir, file_name)
		# print cleaned_svg_dom.getElementsByTagName('g')
		save_cleaned_file(base_dir, file_name, cleaned_svg_dom)
		print 'file %s is cleaned.' % file_name
		print ''



if __name__ == "__main__":
	start_cleaning()