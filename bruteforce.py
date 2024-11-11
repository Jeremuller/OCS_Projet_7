import csv
import itertools


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
                return_on_investment = return_on_investment.replace('%', '').strip()
                action = Action(name, float(cost), float(return_on_investment))
                actions_list.append(action)
        return actions_list


class InvestmentCalculator:
    @classmethod
    def calculate_investments(cls, actions_pool):
        potential_investments = []
        budget = 500

        for r in range(1, len(actions_pool) + 1):
            for combination in itertools.combinations(actions_pool, r):
                total_cost = sum(action.cost for action in combination)
                if total_cost <= budget:
                    total_benefit = sum(action.benefit for action in combination)
                    potential_investments.append((combination, total_benefit))
        return potential_investments


class ManageResults:
    @classmethod
    def sort_results(cls, investment_list):
        investment_list.sort(key=lambda x: x[1], reverse=True)
        return investment_list

    @classmethod
    def display_results(cls, results):
        print("Top 5 Investments by total Benefit:")
        for i, (investment, benefit) in enumerate(results[:5], 1):
            print(f"{i}. Total Benefit= {benefit}")
            print(f"{len(investment)}")
            for action in investment:
                print(f"{action.name} {action.cost} {action.benefit}")


action_pool = ActionPool("actions_list.csv")
actions = action_pool.load_actions()
investments = InvestmentCalculator.calculate_investments(actions)

sorted_results = ManageResults.sort_results(investments)
ManageResults.display_results(sorted_results)
