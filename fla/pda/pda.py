# -*- coding: utf-8 -*-

# Copyright (c) 2019 Marco Aurélio Graciotto Silva
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import copy
import logging

from fla.pda.instance import Instance


class PushDownAutomaton:
    def __init__(self, states, initial_state, acceptance_states, initial_stack_symbol, transitions):
        self.states = states
        self.initial_state = initial_state
        self.initial_stack_symbol = initial_stack_symbol
        self.acceptance_states = acceptance_states
        self.transitions = transitions
        self.restart()

    def restart(self):
        self.stack = []
        self.stack.append(self.initial_stack_symbol)
        self.current_configuration = []
           
    def verify_status(self, configuration):
        if len(configuration.current_word) == 0:
            if len(configuration.current_stack) == 0 or configuration.current_state in self.acceptance_states:
                configuration.acceptance_status = True
            else:
                configuration.acceptance_status = False
    
    def get_decision(self):
        for configuration in self.current_configurations:
            if len(configuration.current_word) == 0:
                if len(configuration.current_stack) == 0 or configuration.current_state in self.acceptance_states:
                    return True
        return False

    def get_initial_configurations(self, word):
        configurations = []
        stack = []
        stack.append(self.initial_stack_symbol)
        configuration = Instance(self, self.initial_state, word, stack)
        configurations.append(configuration)
        return configurations
    
    def load_configurations(self, configurations):
        self.current_configurations = configurations

    def step_forward(self):
        configurations_current_step = copy.copy(self.current_configurations)
        self.current_configurations = []
        for configuration in configurations_current_step:
            for transition in configuration.get_valid_transitions():
                new_configuration = configuration.apply_transition(transition)
                self.current_configurations.append(new_configuration)
                logging.debug(str(configuration) + " -> " + str(new_configuration))

    def run(self):
        pertinence_decision = self.get_decision()
        if pertinence_decision == True:
            return True
        halted_configurations = []
        while self.current_configurations:
            self.step_forward()
            for configuration in self.current_configurations:
                self.verify_status(configuration)
                if configuration.acceptance_status != None:
                    halted_configurations.append(configuration)
        self.current_configurations = halted_configurations
        return self.get_decision()
        
