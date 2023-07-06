class CoffeeMachine:
    def __init__(self):
        self.milk = 540
        self.coffee = 120
        self.water = 400
        self.money = 550
        self.cups = 9
        self.state = 'choosing_action'
        self.x = True

    def action(self, user_input):
        if self.state == 'choosing_action':
            if user_input == 'buy':
                self.state = 'choosing_coffee'
                self.buy_coffee()
            elif user_input == 'fill':
                self.filling()
            elif user_input == 'take':
                self.money = 0
                self.state = 'choosing_action'
            elif user_input == 'remaining':
                self.remaining()
            elif user_input == 'exit':
                 self.x = False
        elif self.state == 'choosing_coffee':
            if user_input == '1':
                self.make_coffee('espresso', 250, 16, 4, 0, 1)
                self.state = 'choosing_action'
            elif user_input == '2':
                self.make_coffee('latte', 350, 20, 7, 75, 1)
                self.state = 'choosing_action'
            elif user_input == '3':
                self.make_coffee('cappuccino', 200, 12, 6, 100, 1)
                self.state = 'choosing_action'
            elif user_input == 'back':
                self.state = 'choosing_action'

    def remaining(self):
        print(f'The coffee machine has:\n'
        f'{self.water} ml of water\n'
        f'{self.milk} ml of milk\n'
        f'{self.coffee} g of coffee beans\n'
        f'{self.cups} disposable cups\n'
        f'${self.money} of money')
    def filling(self):
        self.water += int(input('Write how many ml of water you want to add:\n'))
        self.milk += int(input('Write how many ml of milk you want to add:\n'))
        self.coffee += int(input('Write how many grams of coffee beans you want to add:\n'))
        self.cups += int(input('Write how many disposable cups you want to add:\n'))

    def buy_coffee(self):
        print('What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino, back - to main menu:')
        user_input = input()
        self.action(user_input)

    def make_coffee(self, coffee_type, water_needed, beans_needed, cost, milk_needed, cups_needed):
        if self.water >= water_needed and self.coffee >= beans_needed and self.milk >= milk_needed and self.cups >= cups_needed:
            self.water -= water_needed
            self.coffee -= beans_needed
            self.milk -= milk_needed
            self.cups -= cups_needed
            self.money += cost
            print('I have enough resources, making you a coffee!')
        elif water_needed > self.water:
            print('Sorry, not enough water!')
            self.state = 'choosing_action'
        elif beans_needed > self.coffee:
            print('Sorry, not enough coffee beans!')
            self.state = 'choosing_action'
        elif milk_needed > self.milk:
            print('Sorry, not enough milk!')
            self.state = 'choosing_action'
        elif cups_needed > self.cups:
            print('Sorry, not enough disposable cups!')
            self.state = 'choosing_action'

coffee_machine = CoffeeMachine()
while coffee_machine.x == True:
    user_input = input("Write action (buy, fill, take, remaining, exit):\n")
    coffee_machine.action(user_input)

