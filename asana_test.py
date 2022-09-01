#!/usr/bin/python3

import os
import sys
import asana
import urllib.request

#***** THE PROBLEM ******
#List newest task ID
#List all attachments
#Download attachments
#Delete Attachments
#Reupload attachments
#Delete files

#Read in Personal Access Token and other sensitive info
f = open('info.txt', 'r')
lines = f.readlines()
project_gid = lines[0].strip()
personal_access_token = lines[1].strip()

#Client initialization
client = asana.Client.access_token(personal_access_token)
#me = client.users.me()


#def list_projects(workspace_id):
#def list_attachments(task_id):

def list_tasks(project_id):
	for tasks in client.tasks.find_all({'project': project_gi}):
		print(tasks)

#returns most recent tasks gid
def most_recent_task(project_gid):
	tasks_list = client.tasks.find_all({'project': project_gid})
	tasks_list = list(tasks_list)
	#find the most recent task
	most_recent_task = tasks_list[len(tasks_list) - 1]
	m_r_t_gid = most_recent_task['gid']
	return m_r_t_gid

def attachment_reload(attachments_list, m_r_t_gid):
#get a list of all the attachments on most recent task
#for each attachment reattach to fix thumbnail
	for a in attachments_list:
		attach_object = client.attachments.find_by_id(a['gid'])
		a_url = attach_object['download_url']
		try:
			response = urllib.request.urlopen(a_url)
			data = response.read()
		except:
			print("Error Opening/Reading URL")
			break
		client.attachments.create_attachment_for_task(m_r_t_gid, file_content=data, file_name='IMAGE.PNG',file_content_type='image/png')
		print("New Attachment Uploaded to Task ID: " + m_r_t_gid)
		#delete old attachment?

mrt_gid = most_recent_task(project_gid)
attach_list = client.attachments.find_by_task(mrt_gid)
attachment_reload(attach_list, mrt_gid)

