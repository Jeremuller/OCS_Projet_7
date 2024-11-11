import csv


class Action:
    def __init__(self, name, cost, return_on_investment):
        self.name = name
        self.cost = cost
        self.return_on_investment = return_on_investment
        self.benefit = self.calculate_benefit()

    def calculate_benefit(self):
        return self.cost * (self.return_on_investment/100)


class ActionPool:
    def __init__(self, file_path):
        self.file_path = file_path
        self.actions_pool = self.load_actions()

    def load_actions(self):
        actions_list = []
        with open(self.file_path, "r", encoding="utf-8") as file:
            csv_reader = csv.reader(file)
            next(csv_reader)
            for row in csv_reader:
                name, cost, return_on_investment = row
                try:
                    cost = float(cost)
                    return_on_investment = float(return_on_investment.replace('%', '').strip())
                    if cost > 0 and return_on_investment > 0:
                        action = Action(name, cost, return_on_investment)
                        actions_list.append(action)
                except ValueError:
                    print(f"Skipping invalid entry: {row}")
        return actions_list


class InvestmentCalculator:
    @classmethod
    def sort_actions(cls, action_list):
        sorted_actions = sorted(action_list, key=lambda action: action.return_on_investment, reverse=True)
        return sorted_actions

    @ classmethod
    def generate_combination(cls, action_list):
        budget = 500
        investment_benefit = 0
        combination = []

        for action in action_list:
            if action.cost <= budget:
                budget -= action.cost
                investment_benefit += action.benefit
                combination.append(action)

        total_cost = sum(action.cost for action in combination)
        print(f"Total cost: {total_cost}")
        print(f"Total benefit: {investment_benefit}")

        for action in combination:
            print(f"{action.name} {action.cost} {action.benefit}")


action_pool = ActionPool("dataset_1.csv")
actions = action_pool.load_actions()
sorted_actions_list = InvestmentCalculator.sort_actions(actions)
InvestmentCalculator.generate_combination(sorted_actions_list)
