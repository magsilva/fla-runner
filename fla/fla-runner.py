#!/usr/bin/python
# -*- coding: utf-8 -*-

from fla.dfa.dfa import DeterministicFiniteAutomaton
from fla.dfa.transition import Transition as DFATransition 

from fla.ndfa.ndfa import NonDeterministicFiniteAutomaton
from fla.ndfa.transition import Transition as NDFATransition 

from fla.pda.pda import PushDownAutomaton
from fla.pda.transition import Transition as PDATransition 

from fla.turing.turing_machine import TuringMachine
from fla.turing.tape import Tape
from fla.turing.transition import Transition as TuringTransition

class FlaRunner(object):

	def dfa(lines, cmdline_args):
		input_alphabet    = lines[0].split()
	    states            = lines[2].split()
		initial_state     = lines[3]
	    acceptance_states = lines[4].split()
		transitions = []
	    for description in lines[5:]:
		    splited_description = description.split()
			transition = DFATransition(splited_description[0], splited_description[1], splited_description[2])
	        transitions.append(transition)
		dfa = DeterministicFiniteAutomaton(states, initial_state, acceptance_states, transitions)
	    initial_configuration = dfa.get_initial_configuration(cmdline_args[0])
		dfa.load_configuration(initial_configuration)
	    result = dfa.run()
		return dfa.get_decision()

	def ndfa(lines, cmdline_args):
		input_alphabet    = lines[0].split()
	    whitespace        = lines[1]
		states            = lines[2].split()
	    initial_states    = lines[3].split()
		acceptance_states = lines[4].split()
	    transitions = []
		for description in lines[5:]:
			splited_description = description.split()
	        if splited_description[1] == whitespace:
		        splited_description[1] = None
	        transition = NDFATransition(splited_description[0], splited_description[1], splited_description[2])
		    transitions.append(transition)
	    ndfa = NonDeterministicFiniteAutomaton(states, initial_states, acceptance_states, transitions)
		initial_configurations = ndfa.get_initial_configurations(cmdline_args[0])
	    ndfa.load_configurations(initial_configurations)
		result = ndfa.run()
	    return ndfa.get_decision()

	def pda(lines, cmdline_args):
		input_alphabet    = lines[0].split()
	    stack_alphabet    = lines[1].split()
		whitespace        = lines[2]
	    initial_stack_symbol = lines[3]
		states            = lines[4].split()
	    initial_state     = lines[5]
	    acceptance_states = lines[6].split()
		transitions = []
	    for description in lines[7:]:
		    splited_description = description.split()
			if splited_description[1] == whitespace:
	            splited_description[1] = None
		    if splited_description[2] == whitespace:
	            splited_description[2] = None
		    if splited_description[4] == whitespace:
	            splited_description[4] = None
		    transition = PDATransition(splited_description[0], splited_description[1], splited_description[2], splited_description[3], splited_description[4])
			transitions.append(transition)
	    pda = PushDownAutomaton(states, initial_state, acceptance_states, initial_stack_symbol, transitions)
		configurations = pda.get_initial_configurations(cmdline_args[0])
	    pda.load_configurations(configurations)
		result = pda.run()
	    return  pda.get_decision()

	def turing_machine(lines, cmdline_args):
		input_alphabet   = lines[0].split()
	    tape_alphabet    = lines[1]
	    whitespace       = lines[2]
	    states           = lines[3].split()
	    initial_state    = lines[4]
	    final_states     = lines[5].split()
	    number_of_tapes  = lines[6]
	    transitions = []
	    for description in lines[7:]:
		    splited_description = description.split()
			transition = TuringTransition(splited_description[0], splited_description[1])
	        for tape_part in zip(*(splited_description[2:][i::3] for i in range(3))):
		        transition.add_tape_part(tape_part[0], tape_part[1], tape_part[2])
			transitions.append(transition)
	    tapes = []
		for i in range(0, int(number_of_tapes)):
			tapes.append(Tape(whitespace, tape_alphabet, list(cmdline_args[i])))
	    tm = TuringMachine(states, initial_state, final_states, whitespace, transitions)
		initial_configurations = tm.get_initial_configurations(tapes)
	    tm.load_configurations(initial_configurations)
		result = tm.run()
	    if result == True:
		    return tm.get_decision()
	    else:
		    return None