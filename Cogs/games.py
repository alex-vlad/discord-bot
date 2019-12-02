from string import ascii_letters

from discord.ext import commands
import random
import asyncio
from database import update_bank, get_player


class Games(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='bet')
    async def slot(self, ctx, amount):
        """ Roll the slot machine """

        emojis = [":tangerine:", ":lemon:", ":banana:", ":watermelon:", ":strawberry:", ":peach:", ":cherries:",
                  ":pineapple:", ":apple:"]
        player = get_player(ctx.message.author.id)

        a = random.choice(emojis)
        b = random.choice(emojis)
        c = random.choice(emojis)
        slotmachine = f"**{a}{b}{c}\n{ctx.author.name}**,"

        if player['bank'] == 0:
            await ctx.send("Bank account is empty.")
            return
        elif int(amount) > player['bank']:
            await ctx.send("Not enough coins.")
            return
        else:
            if a == b == c:
                update_bank(ctx.message.author, int(amount) * 10)
                player = get_player(ctx.message.author.id)
                await ctx.send(f"{slotmachine} All matching, you won!\nBank Account: %s coins" % (player['bank']))
            elif (a == b) or (a == c) or (b == c):
                update_bank(ctx.message.author, int(amount) * 5)
                player = get_player(ctx.message.author.id)
                await ctx.send(f"{slotmachine} 2 in a row, you won!\nBank Account: %s coins" % (player['bank']))
            else:
                update_bank(ctx.message.author, -int(amount))
                player = get_player(ctx.message.author.id)
                await ctx.send(f"{slotmachine} No match, you lost.\nBank Account: %s coins" % (player['bank']))

    @commands.command(name='dr')
    async def dice_roll(self, ctx, user_guess):
        """Roll a dice and guess the number to win a big prize. You lose 100 coins per try."""

        member = ctx.message.author
        player = get_player(ctx.message.author.id)
        if player['bank'] == 0:
            await ctx.send("Bank account is empty.")
            return
        else:
            update_bank(member, -100)
            max_value = 12
            if int(user_guess) > max_value:
                await ctx.send("The input is higher than the max value.\nExiting...")
                return
            else:
                first_roll = random.randint(1, max_value)
                second_roll = random.randint(1, max_value)
                await ctx.send("Rolling... :game_die:")
                await asyncio.sleep(2)
                await ctx.send("First roll is: %d" % first_roll)
                await asyncio.sleep(1)
                await ctx.send("Second roll is: %d" % second_roll)
                total_roll = first_roll + second_roll
                await ctx.send("Total roll is: %d" % total_roll)
                await ctx.send("Result...:game_die:")
                if int(user_guess) > total_roll:
                    await ctx.send("YOU WON 1000 coins {}!!".format(member.mention))
                    update_bank(member, 1000)
                    return
                else:
                    await ctx.send("YOU LOST {}".format(member.mention))
                    return

    @commands.command(name='cf')
    async def coin_flip(self, ctx, user_guess):
        """Flip a coin to win a big prize. You lose 200 coins per try."""
        member = ctx.message.author
        player = get_player(ctx.message.author.id)
        if player['bank'] == 0:
            await ctx.send("Bank account is empty.")
            return
        else:
            update_bank(member, -200)
            if user_guess.upper() == 'T' or user_guess.upper() == 'H':
                roll = random.randint(1, 2)
                if roll == 1:
                    comp_guess = 'T'
                else:
                    comp_guess = 'H'
                if user_guess == comp_guess:
                    await ctx.send("It was {}\nYOU WON 500 coins {}!!".format(comp_guess, member.mention))
                    update_bank(member, 500)
                    return
                else:
                    await ctx.send("It was {} \nYOU LOST {}".format(comp_guess, member.mention))
                    return
            else:
                await ctx.send("The input is not valid.\nExiting...")
                return

    @commands.command(name='rps')
    async def rock_paper_scissors(self, ctx, user_choice):
        """Rock, paper, scissors game. Beat the AI to win a big prize. You lose 500 coins per try."""

        member = ctx.message.author
        player = get_player(ctx.message.author.id)
        if player['bank'] == 0:
            await ctx.send("Bank account is empty.")
            return
        else:
            update_bank(member, -500)
            # Options list which will not change
            OPTIONS = ["R", "P", "S"]

            # Messages to user
            LOSE_MESSAGE = "\nYou Lost!"
            WIN_MESSAGE = "\nYou Won 2000 coins!"

            user_choice = user_choice.upper()
            if user_choice == "P" or user_choice == "R" or user_choice == "S":
                computer_choice = OPTIONS[random.randint(0, len(OPTIONS) - 1)]
            else:
                await ctx.send("Invalid choice\nExiting...")
                return

            user_choice_index = OPTIONS.index(user_choice)
            computer_choice_index = OPTIONS.index(computer_choice)

            if user_choice_index == computer_choice_index:
                # Set a draw if both indexes are the same
                await asyncio.sleep(1)
                await ctx.send("\nDRAW!")
            elif (user_choice_index == 0 and computer_choice_index == 2) or (
                    user_choice_index == 1 and computer_choice_index == 0) or (
                    user_choice_index == 2 and computer_choice_index == 1):
                # One condition to handle all the events where the user will win
                await ctx.send(WIN_MESSAGE)
                update_bank(member, 2000)
                return
            else:
                await ctx.send(LOSE_MESSAGE)
                return

    @commands.command(name='hangman')
    async def hangman(self, ctx):
        """Hangman game. Guess the word to win a big prize."""
        member = ctx.message.author

        await ctx.send('You can only guess one letter a time.')
        await ctx.send('You have 8 lives!')

        # List
        answer = ["lion", "umbrella", "window", "computer", "glass", "juice", "chair", "desktop",
                  "laptop", "dog", "cat", "lemon", "cabel", "mirror", "hat"]

        # Word Picker
        answer_new = random.choice(answer).upper()

        # Guessed word
        guess = []
        word = []
        what_guessed = []
        lifes = 8
        count = 0

        # Changes all characters aside from spaces to an underscore, appends to guess
        for items in answer_new:
            word.append(items)
            if items == ' ':
                guess.append(' ')
            else:
                guess.append('-')

        await ctx.send(' '.join(guess))
        await ctx.send('Number of lifes left: {}'.format(lifes))

        # Constraints the number of guesses
        while count < 8:
            def check(m):
                lst = list(ascii_letters)
                for i in lst:
                    if m.content == i and m.channel == ctx.channel:
                        return m.content

            async def get_input_of_type():
                while True:
                    try:
                        msg = await self.bot.wait_for('message', check=check)
                        return msg.content
                    except ValueError:
                        continue

            guess1 = await get_input_of_type()
            guessed = guess1.upper()
            what_guessed += guessed
            # Checks the guessed in word and then replaces the underscore with chars.
            for character in guessed:
                for char in range(0, len(word)):
                    if character == word[char]:
                        guess[char] = word[char]

            # Terminates the python function if code is correct, else, keeps going
            if (''.join(guess)) == answer_new:
                break
            if guessed not in answer_new:
                lifes = lifes - 1
                count += 1

            # Print out the guess(with underscores) and word(original word)
            await ctx.send(''.join(guess))
            await ctx.send('Number of lifes left:{}'.format(lifes))
            await ctx.send('What you have guessed so far:{}'.format(what_guessed))

        if count < 8:
            await ctx.send('YOU WIN! Word was {}'.format(answer_new))
            update_bank(member, 1000)
        else:
            await ctx.send('You Lose! The president we were looking for is {}'.format(answer_new))


class Lottery(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.ticketCost = 1000
        self.winningTicket = 0
        self.ticketCounter = 0
        self.prizePool = 0
        self.generate_tickets(100)

    @commands.command(name="buyticket")
    async def buy_ticket(self, ctx):

        user = ctx.message.author
        player = get_player(ctx.message.author.id)
        if player['bank'] == 0:
            await ctx.send("Bank account is empty.")
            return
        else:
            update_bank(user, -1000)
            if self.ticketCounter == self.winningTicket:
                self.generate_tickets(100)
                update_bank(user, self.prizePool)
                await ctx.send("{}, Congratulations, you won the lottery with a prizepool of ".format(user.mention)
                               + str(self.prizePool))
            else:
                self.ticketCounter += 1
                await ctx.send("{}, You lost, better luck next time!".format(user.mention))

    # Creates a new winning number, while resetting the counter, where the nr_of_tickets represents the odds of winning
    def generate_tickets(self, nr_of_tickets):
        self.ticketCounter = 1
        self.prizePool = nr_of_tickets * self.ticketCost / 2
        self.winningTicket = random.randint(1, nr_of_tickets)


def setup(bot):
    bot.add_cog(Games(bot))
    bot.add_cog(Lottery(bot))
