#!/usr/bin/env python3
"""
Silly Rat Run - a tiny, random, funny terminal game

Run: python3 silly_rat_run.py

You're Ratty, a very dramatic rat who wants to escape the TV studio.
Make choices, survive random events, and try to reach the exit before your snack meter runs out.
"""
import random
import sys
import time

NAME = "Ratty"
MAX_SNACK = 5
MAX_HEALTH = 5
STEPS_TO_EXIT = 8

EVENTS = [
    ("a spotlight", "You momentarily become a celebrity. Cameras flash and you strike a pose.'"),
    ("a camera cable", "You trip spectacularly and invent modern interpretive dance."),
    ("a very large panda plush", "You mistake it for a chew toy. It does not consent."),
    ("a suspicious-looking sandwich", "It looks like cheese, smells like regret."),
    ("a janitor singing badly", "The janitor's song confuses time itself. You lose a beat (and a snack)."),
]

ACTIONS = [
    "run",
    "hide",
    "eat",
    "dance",
]


def slow_print(s, delay=0.012):
    for ch in s:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)
    print()


def intro():
    slow_print("Welcome to Silly Rat Run! (very silly edition)\n")
    slow_print("You are {}. You must escape the TV studio before your snacks and dignity run out.\n".format(NAME))
    slow_print("Controls: type one of: run, hide, eat, dance, or help. Press Ctrl+C to quit.\n")


def rand_event():
    thing, desc = random.choice(EVENTS)
    return thing, desc


def prompt_action():
    while True:
        try:
            action = input('What do you do? (run/hide/eat/dance/help) > ').strip().lower()
        except EOFError:
            print('\nGoodbye!')
            sys.exit(0)
        if action in ACTIONS or action == 'help':
            return action
        print("I don't understand that action. Try run/hide/eat/dance/help.")


def play():
    snacks = MAX_SNACK
    health = MAX_HEALTH
    step = 0
    score = 0

    intro()

    while step < STEPS_TO_EXIT and health > 0 and snacks >= 0:
        print('\n--- Step {}/{} ---'.format(step + 1, STEPS_TO_EXIT))
        thing, desc = rand_event()
        slow_print('You encounter {}...'.format(thing))
        slow_print(desc)

        action = prompt_action()

        if action == 'help':
            slow_print('\nHints: run to cover ground, hide to avoid trouble, eat to refill snacks, dance for chaos.')
            continue

        # Randomness + action outcomes
        roll = random.randint(1, 6)

        if action == 'run':
            slow_print('You bolt like a fluffy missile! (roll {})'.format(roll))
            if roll >= 3:
                step += 1
                score += 2
                slow_print('You gain ground!')
            else:
                health -= 1
                slow_print('You stumble and lose 1 health.')

        elif action == 'hide':
            slow_print('You blend with the scenery. (roll {})'.format(roll))
            if roll >= 4:
                score += 1
                slow_print('Nice hiding! Nothing notices you.')
            else:
                health -= 1
                slow_print('A broom finds you. -1 health.')

        elif action == 'eat':
            slow_print('You attempt to eat the suspicious thing. (roll {})'.format(roll))
            if snacks <= 0:
                slow_print('No snacks left! You chew your feelings instead. -1 health')
                health -= 1
            else:
                if roll >= 2:
                    snacks = min(MAX_SNACK, snacks + 2)
                    score += 1
                    slow_print('Snack delicious! +2 snacks (but maybe it was a prop).')
                else:
                    snacks -= 1
                    health -= 1
                    slow_print('That was a prop. -1 snack, -1 health.')

        elif action == 'dance':
            slow_print('You perform the ancient Rat Ballet. (roll {})'.format(roll))
            if roll >= 5:
                score += 3
                step += 1
                slow_print('Your dance distracts staff — you sneak forward AND gain points!')
            else:
                snacks -= 1
                slow_print('The crowd is unimpressed; you lose a snack.')

        # small chance of a totally silly event
        silly = random.random()
        if silly < 0.08:
            slow_print('\nA producer appears and offers you an acting contract. You consider, then politely decline.')
            score += 5

        # status
        slow_print('\nStatus: Health: {} | Snacks: {} | Score: {} | Steps: {}/{}\n'.format(health, snacks, score, step, STEPS_TO_EXIT))

    # final outcomes
    if step >= STEPS_TO_EXIT:
        slow_print('\nYou burst through the exit, triumphant and a little crunchy. YOU WIN!')
        slow_print('Final score: {}'.format(score))
    elif health <= 0:
        slow_print('\nYou faint dramatically. A cameraman captures it and your career is born as an influencer of naps. GAME OVER.')
    else:
        slow_print('\nYou ran out of snacks and motivation. The studio hires you as their official cheese grader. GAME OVER.')


if __name__ == '__main__':
    try:
        play()
    except KeyboardInterrupt:
        print('\nInterrupted. May your crumbs be plentiful.')
