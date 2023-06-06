import os
import sys
import json
import Commands
import Actions
import Statements
import pandas as pd



def ActionsDataLoader():

	#Robot_Activation_Actions#

	with open("Data/Actions/Robot_Activation_Actions.json") as activationActions:
		data = json.load(activationActions)

		for action in data["Robot_Activation_Actions"]:
			action = action.lower()
			action = action.strip()
			Actions.Robot_Activation_Actions_List.append(action)

	with open("Data/Actions/Action-1.json") as how_are_you_action:
		data = json.load(how_are_you_action)

		for actionHow in data["Action-1_how_are_you"]:
			actionHow = actionHow.lower()
			actionHow = actionHow.strip()
			Actions.How_are_you_Actions_List.append(actionHow)

	with open("Data/Actions/Action-2.json") as names:
		data = json.load(names)

		for name in data["Asking_name_actions"]:
			name = name.lower()
			name = name.strip()
			Actions.Robot_Name_List.append(name)

	with open("Data/Actions/Action-3.json") as talking_name:
		data = json.load(talking_name)

		for namesD in data["talking_about_names"]:
			namesD = namesD.lower()
			namesD = namesD.strip()
			Actions.talking_about_name.append(namesD)

	with open("Data/Actions/Action-4.json") as work:
		data = json.load(work)

		for da in data['talking_about_work']:
			da = da.lower()
			da = da.strip()
			Actions.talking_about_work_1.append(da)

		for da1 in data['duration_of_work']:
			da1 = da1.lower()
			da1 = da1.strip()
			Actions.talking_about_work_duration_3.append(da1)

		for da2 in data["place_of_work"]:
			da2 = da2.lower()
			da2 = da2.strip()
			Actions.talking_about_work_place_2.append(da2)

		for da3 in data["salary_of_work"]:
			da3 = da3.lower()
			da3 = da3.strip()
			Actions.talking_about_work_salary_4.append(da3)


	with open("Data/Actions/Action-4_Extra.json") as not_paid:
		data = json.load(not_paid)

		for d in data["reason_for_not_paid"]:
			d = d.lower()
			d = d.strip()
			Actions.talking_about_work_salary_Extra.append(d)

	with open("Data/Actions/Action-9.json") as da:
		data =json.load(da)

		for d in data["answers"]:
			d = d.lower()
			d = d.strip()
			Actions.Gender.append(d)

	with open("Data/Actions/Action-10.json") as d:
		data = json.load(d)

		for d in data["charman"]:
			d = d.lower()
			d = d.strip()
			Actions.Charman.append(d)

		for d2 in data["vision"]:
			d2 = d2.lower()
			d2 = d2.strip()
			Actions.vision.append(d2)

		for d3 in data["mission"]:
			d3 = d3.lower()
			d3 = d3.strip()
			Actions.mission.append(d3)

		for d4 in data["chairman"]:
			d4 = d4.lower()
			d4 = d4.strip()
			Actions.manager.append(d4)


	with open("Data/Actions/Action-12.json") as das:
		data = json.load(das)

		for xe in data["question-1"]:
			xe = xe.lower()
			xe = xe.strip()
			Actions.action_12_question_1.append(xe)

		for xe1 in data["question-2"]:
			xe1 = xe1.lower()
			xe1 = xe1.strip()
			Actions.action_12_question_2.append(xe1)

		for xe3 in data["question-3"]:
			xe3 = xe3.lower()
			xe3 = xe3.strip()
			Actions.action_12_question_3.append(xe3)

		for xe4 in data["question-4"]:
			xe4 = xe4.lower()
			xe4 = xe4.strip()
			Actions.action_12_question_4.append(xe4)

		for xe5 in data["question-5"]:
			xe5 = xe5.lower()
			xe5 = xe5.strip()
			Actions.action_12_question_5.append(xe5)

		for xe6 in data["question-6"]:
			xe6 = xe6.lower()
			xe6 = xe6.strip()
			Actions.action_12_question_6.append(xe6)

	with open("Data/Actions/Action-13.json") as Ds:
		data =json.load(Ds)

		for x1 in data["answer-1"]:
			x1 = x1.lower()
			x1 = x1.strip()
			Actions.Action_13_question_1.append(x1)

		for x2 in data["answer-2"]:
			x2 = x2.lower()
			x2 = x2.strip()
			Actions.Action_13_question_2.append(x2)





def CommandsDataLoader():
	
	#Robot_Activation_Commands#

	with open('Data/Commands/Robot_Activation_Commands.json') as activationCommands:
		data = json.load(activationCommands)

		for command in data["Robot_Activation_Commands"]:
			command = command.lower()
			command = command.strip()
			Commands.Robot_Activation_Commands_List.append(command)

	with open('Data/Commands/Command-1.json') as how_are_you_command:
		data = json.load(how_are_you_command)

		for command in data["Command-1_how_are_you"]:
			command = command.lower()
			command = command.strip()
			Commands.How_are_you_Commands_List.append(command)

	with open("Data/Commands/Command-2.json") as AskingNames:
		data = json.load(AskingNames)

		for name in data["Asking_name"]:
			name = name.lower()
			name = name.strip()
			Commands.AskingTheNamesofRobotCommands.append(name)

	with open("Data/Commands/Robot_Deactivation_Commands.json") as deactivatingCommands:
		data = json.load(deactivatingCommands)

		for deactivation in data["Robot_deactivation_Commands"]:
			deactivation = deactivation.lower()
			deactivation = deactivation.strip()
			Commands.Robot_Deactivation_Commands_List.append(deactivation)

	with open("Data/Commands/command-3.json") as talking_name:
		data = json.load(talking_name)

		for de in data["talking_about_name"]:
			de = de.lower()
			de = de.strip()
			Commands.talking_about_name.append(de)

	with open("Data/Commands/Command-4.json") as work:
		data = json.load(work)

		for wr in data["talking_about_work"]:
			wr = wr.lower()
			wr = wr.strip()
			Commands.talking_about_work.append(wr) 

		for wr1 in data["duration_of_work"]:
			wr1 = wr1.lower()
			wr1 = wr1.strip()
			Commands.talking_about_work_duration_3.append(wr1)

		for wr2 in data["place_of_work"]:
			wr2 = wr2.lower()
			wr2 = wr2.strip()
			Commands.talking_about_work_place_2.append(wr2)

		for wr3 in data["salary_of_work"]:
			wr3 = wr3.lower()
			wr3 = wr3.strip()
			Commands.talking_about_work_salary_4.append(wr3)

	with open("Data/Commands/Command-4_Extra.json") as not_paid:
		data = json.load(not_paid)

		for x in data["reason_for_not_paid"]:
			x = x.lower()
			x = x.strip()
			Commands.talking_about_work_salary_Extra.append(x)

	with open("Data/Commands/Command-5.json") as greeting:
		data = json.load(greeting)

		for x in data["All_Questions"]:
			x = x.lower()
			x = x.strip()
			Commands.Greetings.append(x)

	with open("Data/Commands/Command-6.json") as da:
		data = json.load(da)

		for d in data["All_Questions"]:
			d = d.lower()
			d = d.strip()
			Commands.YesOrNo.append(d)

	with open("Data/Commands/Command-7.json") as da:
		data = json.load(da)

		for d in data["All_Questions"]:
			d = d.lower()
			d = d.strip()
			Commands.YesOrNoNegative.append(d)

	with open("Data/Commands/Command-8.json") as da:
		data = json.load(da)

		for d in data["All_Questions"]:
			d = d.lower()
			d = d.strip()
			Commands.youare.append(d)

		for d1 in data["asking_sorry"]:
			d1 = d1.lower()
			d1 = d1.strip()
			Commands.sorry.append(d1)

	with open("Data/Commands/Command-9.json") as s:
		data = json.load(s)

		for d in data["All_Questions"]:
			d = d.lower()
			d = d.strip()
			Commands.Gender.append(d)

	with open("Data/Commands/Command-10.json") as d:
		data = json.load(d)

		for all_ques in data["All_question"]:
			all_ques = all_ques.lower()
			all_ques = all_ques.strip()
			Commands.All_QuestionsOfCommand10.append(all_ques)

		for d in data["char_man"]:
			d = d.lower()
			d = d.strip()
			Commands.Charman.append(d)

		for d2 in data["vision"]:
			d2 = d2.lower()
			d2 = d2.strip()
			Commands.vision.append(d2)

		for d3 in data["mission"]:
			d3 = d3.lower()
			d3 = d3.strip()
			Commands.mission.append(d3)

		for d4 in data["manager"]:
			d4 = d4.lower()
			d4 = d4.strip()
			Commands.manager.append(d4)

	with open("Data/Commands/Command-11.json") as ds:
		data = json.load(ds)

		for x in data["asking_about_bcas"]:
			x = x.lower()
			x = x.strip()
			Commands.asking_about_bcas.append(x)

	with open("Data/Commands/Command-12.json") as das:
		data = json.load(das)

		for alls in data["All-questions"]:
			alls = alls.lower()
			alls = alls.strip()
			Commands.command_12_all_questions.append(alls)

		for xe in data["question-1"]:
			xe = xe.lower()
			xe = xe.strip()
			Commands.command_12_question_1.append(xe)

		for xe1 in data["question-2"]:
			xe1 = xe1.lower()
			xe1 = xe1.strip()
			Commands.command_12_question_2.append(xe1)

		for xe3 in data["question-3"]:
			xe3 = xe3.lower()
			xe3 = xe3.strip()
			Commands.command_12_question_3.append(xe3)

		for xe4 in data["question-4"]:
			xe4 = xe4.lower()
			xe4 = xe4.strip()
			Commands.command_12_question_4.append(xe4)

		for xe5 in data["question-5"]:
			xe5 = xe5.lower()
			xe5 = xe5.strip()
			Commands.command_12_question_5.append(xe5)

		for xe6 in data["question-6"]:
			xe6 = xe6.lower()
			xe6 = xe6.strip()
			Commands.command_12_question_6.append(xe6)

	with open("Data/Commands/Command-13.json") as ds:
		
		data = json.load(ds)

		for x1 in data["All-questions"]:
			x1 = x1.lower()
			x1 = x1.strip()
			Commands.Small_questions.append(x1)


	with open("Data/Commands/Command-14.json") as Ds:
		data =json.load(Ds)

		for x1 in data["Question-1"]:
			x1 = x1.lower()
			x1 = x1.strip()
			Commands.Command_13_question_1.append(x1)

		for x2 in data["Question-2"]:
			x2 = x2.lower()
			x2 = x2.strip()
			Commands.Command_13_question_2.append(x2)

		for x3 in data["Question-3"]:
			x3 = x3.lower()
			x3 = x3.strip()
			Commands.Command_13_question_3.append(x3)

		for x4 in data["Question-4"]:
			x4 = x4.lower()
			x4 = x4.strip()
			Commands.Command_13_question_4.append(x4)

		for x5 in data["Question-5"]:
			x5 = x5.lower()
			x5 = x5.strip()
			Commands.Command_13_question_5.append(x5)

		for x6 in data["Question-6"]:
			x6 = x6.lower()
			x6 = x6.strip()
			Commands.Command_13_question_6.append(x6)

	with open("Data/Commands/Command-16.json") as ds:
		data = json.load(ds)

		for xv in data["Question-1"]:
			xv = xv.lower()
			xv = xv.strip()
			Commands.Command_14_question_1.append(xv)

	with open("Data/Commands/Command-17.json") as ds:
		data = json.load(ds)

		for x in data["Question-1"]:
			x = x.lower()
			x = x.strip()
			Commands.Command_15_question_2.append(x)





def StatementsDataLoader():

	with open('Data/Statements/Robot_Activation_Statements_cant_hear.json') as cantHearStatements:
		data = json.load(cantHearStatements)

		for statement in data["Robot_Activation_Statements"]:
			statement = statement.lower()
			statement = statement.strip()
			Statements.Robot_Activation_Statements_cant_hear.append(statement)

	with open('Data/Statements/Robot_Activation_Statements_Network_problem.json') as networkProblems:
		data = json.load(networkProblems)

		for problem in data["Robot_Activation_Statements_Network"]:
			problem = problem.lower()
			problem = problem.strip()
			Statements.Robot_Activation_Statements_network_problem.append(problem)

	with open("Data/Statements/Robot_Deactivation_Statements.json") as deactivatingCommands:
		data = json.load(deactivatingCommands)

		for commandDe in data["Robot_Deactivation_Statements"]:
			commandDe = commandDe.lower()
			commandDe = commandDe.strip()
			Statements.Robot_Deactivation_Statements.append(commandDe)

	with open("Data/Statements/Robot_Activation_Greeting.json") as greeting:
		data = json.load(greeting)

		for com in data["Robot_Activation_Greeting"]:
			com = com.lower()
			com = com.strip()
			Statements.Robot_Activation_Greeting.append(com)




def loadDataset_set1():

	dataset1 = pd.read_table("Dataset/Set_1/dataset1.tsv")
	dataset1 = dataset1[["Question","Answer"]].values.tolist()

	dataset2 = pd.read_table("Dataset/Set_1/dataset2.tsv")
	dataset2 = dataset2[["Question","Answer"]].values.tolist()

	dataset3 = pd.read_table("Dataset/Set_1/dataset3.tsv")
	dataset3 = dataset3[["Question","Answer"]].values.tolist()

	dataset4 = pd.read_table("Dataset/Set_1/dataset4.tsv")
	dataset4 = dataset4[["Question","Answer"]].values.tolist()

	dataset5 = pd.read_table("Dataset/Set_1/dataset5.tsv")
	dataset5 = dataset5[["Question","Answer"]].values.tolist()

	
	for data in dataset1:
		Statements.dataset1.append([x.lower().strip() for x in data])

	for data in dataset2:
		Statements.dataset2.append([x.lower().strip() for x in data])

	for data in dataset3:
		Statements.dataset3.append([x.lower().strip() for x in data])

	for data in dataset4:
		Statements.dataset4.append([x.lower().strip() for x in data])

	for data in dataset5:
		Statements.dataset5.append([x.lower().strip() for x in data])





	


















	 


