from skfuzzy import control as ctrl
import skfuzzy as fuzz
import numpy as np

def compute_washing_parameters(type_of_dirt,degree_of_dirt):

    if type_of_dirt < 0.0 or type_of_dirt > 100.0:
        raise Exception("Invalid Type of Dirtiness: %lf" %type_of_dirt)
    if degree_of_dirt < 0.0 or type_of_dirt > 100.0:
        raise Exception("Invalid Degree of Dirtiness: %lf" %degree_of_dirt)

    type_fuzzy = laundry(type_of_dirt,degree_of_dirt)

    return type_fuzzy

def laundry(fuzz_type,fuzz_degree):


		degree_dirt = ctrl.Antecedent(np.arange(0, 101, 1), 'degree_dirt')
		type_dirt = ctrl.Antecedent(np.arange(0, 101, 1), 'type_dirt')
		wash_time = ctrl.Consequent(np.arange(0, 61, 1), 'wash_time')

		degree_names = ['Low', 'Average', 'High']
		level_names = ['Light', 'Medium', 'Heavy']

		#Outputing them into auto-membership functions
		degree_dirt.automf(names=degree_names)
		type_dirt.automf(names=level_names)

		# Washing Time Universe
		wash_time['short'] = fuzz.trimf(wash_time.universe, [8, 12, 20])
		wash_time['average'] = fuzz.trimf(wash_time.universe, [12, 20, 40])
		wash_time['long'] = fuzz.trimf(wash_time.universe, [20, 40, 60])

		# Rule Application
		rule1 = ctrl.Rule(degree_dirt['Average'] | type_dirt['Light'], wash_time['long'])
		rule2 = ctrl.Rule(degree_dirt['Low'] | type_dirt['Light'], wash_time['long'])
		rule3 = ctrl.Rule(degree_dirt['High'] | type_dirt['Medium'], wash_time['long'])
		rule4 = ctrl.Rule(degree_dirt['Average'] | type_dirt['Medium'], wash_time['average'])
		rule5 = ctrl.Rule(degree_dirt['Low'] | type_dirt['Medium'], wash_time['average'])
		rule6 = ctrl.Rule(degree_dirt['High'] | type_dirt['Heavy'], wash_time['average'])
		rule7 = ctrl.Rule(degree_dirt['Average'] | type_dirt['Heavy'], wash_time['short'])

		# Washing Control Simulation
		washing_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7])
		washing = ctrl.ControlSystemSimulation(washing_ctrl)
		
		washing.input['type_dirt'] = fuzz_type
		washing.input['degree_dirt'] = fuzz_degree

		washing.compute()

		wash_time.view(sim=washing)

		return washing.output['wash_time']

if __name__ == "__main__":
    type_of_dirt = float(input("Enter Level of Dirtiness [0-100]"))
    degree_of_dirt = float(input("Enter Degree of Dirtiness [0-100]"))
    washing_parameters = compute_washing_parameters(type_of_dirt,degree_of_dirt)
    print(washing_parameters)
