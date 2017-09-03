# -*- coding: utf-8 -*-

""" Solver-classes for the bin-packing problem variant.

This module contains several different classes aimed at solving the proposed
bin-packing problem variant.
"""

from __future__ import unicode_literals

import abc
import itertools


class RegistrySolvers(type):
    """Registry metaclass for the solver classes

    This metaclass can be set under a given base class so that any classes
    deriving that base will be added to a `registry` dictionary available to
    all registered classes.

    This registry will be key'ed on the class name while the value will contain
    a reference to that class object.

    This registry can be used as a discovery mechanism for derived classes
    without having to register them explicitly.
    """

    def __init__(cls, class_name, class_bases, class_dict):
        # if the class doesn't have a 'registry' dict then create an empty one
        if not hasattr(cls, 'registry'):
            cls.registry = {}

        # add the registered class as an entry in the registry
        cls.registry[class_name] = cls

        # initialise the base class
        super(RegistrySolvers, cls).__init__(
            class_name,
            class_bases,
            class_dict
        )

    def __new__(mcs, class_name, class_bases, class_dict):
        # if the class doesn't have a 'registry' dict then create an empty one
        if not hasattr(mcs, 'registry'):
            mcs.registry = {}

        # add the registered class as an entry in the registry
        mcs.registry[class_name] = mcs

        newclass = super(mcs, RegistrySolvers).__new__(
            mcs,
            class_name,
            class_bases,
            class_dict
        )

        return newclass


class SolverBase(object):
    """Solver base-class"""

    # Use the registry metaclass to autoregister this base-class as well as all
    # classes deriving it.
    __metaclass__ = RegistrySolvers

    solver_type = None

    def __init__(
        self,
        load,
        bins,
    ):

        # Internalize arguments
        self._load = load
        self._bins = bins

    @property
    def load(self):
        """The load defined upon instantiation."""
        return self._load

    @property
    def bins(self):
        """The available bins defined upon instantiation."""
        return self._bins

    def fit_n_bins(self, n):
        """Finds an n-length minimum-capacity combination of bins for the load

        This method attempts to find all n-length combinations of bins (using
        the bins defined upon instantiation of the class) that can accommodate
        the defined load while minimizing capacity.

        Note:
            There is no guarantee that any combinations can be found for a
            defined length `n`. Should no such combinations be found an empty
            list is returned.

        Args:
            n (int): The length of the bin-combinations through which the
                search is performed.

        Returns:
            list: A list of the found n-length bin combinations or an empty
                list if not combinations were found.
        """

        # Lazily evaluate all replacement-combinations of the defined bin
        # sizes.
        combinations = itertools.combinations_with_replacement(
            self.bins, r=n
        )

        # Initialize the minimum capacity as a infinite number.
        capacity_min = float("inf")

        # List to hold all n-length combinations of bins that can accomodate
        # the defined load.
        combos = []
        for combination in combinations:

            # Calculate the capacity of the current bin combination.
            capacity = sum(combination)

            # Skip combinations that can't accommodate the current load.
            if capacity < self.load:
                continue

            # Should the combination have a capacity lower than the current
            # `capacity_min` then replace any previously accepted combinations
            # and skip to the next combination.
            if capacity_min > capacity:
                capacity_min = capacity
                combos = [combination]
                continue

            # Append any combinations with a capacity identical to the current
            # minimum, i.e., store alternative combinations.
            if capacity_min == capacity:
                combos.append(combination)

        # If new combination(s) that can accommodate the current load were found
        # then return them.
        if capacity_min >= self.load and capacity_min != float("inf"):
            return combos

        # At this point no n-length combinations that can accommodate the
        # defined load were found so an empty list is returned.
        return []

    @abc.abstractmethod
    def solve(self):
        raise NotImplementedError


class SolverLengthFirst(SolverBase):
    """Solver focusing on finding the shortest bin-combination.

    This class solves the defined problem by finding the shortest
    bin-combination that can accommodate the defined load.

    Note:
        The solution(s) may yield to over-capacity.
    """

    solver_type = "length"

    def __init__(
        self,
        load,
        bins
    ):

        # Initialize base-class.
        super(SolverLengthFirst, self).__init__(
            load=load,
            bins=bins
        )

    def solve(self):
        """Solves the problem minimizing combination length."""

        n = 0

        # Keep iterating while incrementing the allowed combination length until
        # a combination that can accommodate the defined load has been found.
        while True:
            n += 1
            combos = self.fit_n_bins(n=n)
            if combos:
                return combos


class SolverCapacityFirst(SolverBase):
    """Solver focusing on finding the minimum-capacity bin-combination.

    This class solves the defined problem by finding the bin-combination with
    the minimum over-capacity.

    Note:
        The solution(s) may yield to longer bin-combinations.
    """

    solver_type = "capacity"

    def __init__(
        self,
        load,
        bins
    ):

        # Initialize base-class.
        super(SolverCapacityFirst, self).__init__(
            load=load,
            bins=bins
        )

    def solve(self):
        """Solves the problem minimizing combination over-capacity."""

        n = 0

        # Keep iterating while incrementing the allowed combination length until
        # a combination with a capacity identical to the defined load has been
        # found.
        while True:
            n += 1
            combos = self.fit_n_bins(n=n)
            if combos and sum(combos[0]) == self.load:
                return combos


class SolverCombo(SolverBase):
    """Solver combining the two objectives.

    This class solves the defined problem by evaluating combinations of a length
    n and n + 1 and should an n + 1 combination yield less over-capacity chooses
    that combination over the shorter one. Essentially this solver prioritises
    the over-capacity objective over the minimum-length objective.
    """

    solver_type = "combo"

    def __init__(
        self,
        load,
        bins
    ):
        # Initialize base-class.
        super(SolverCombo, self).__init__(
            load=load,
            bins=bins
        )

    def solve(self):
        """Solves the problem with min over-capacity over min length"""

        n = 1

        # Get the n-length combinations (if any) that can accommodate the
        # defined load.
        combos_n = self.fit_n_bins(n=n)

        while True:
            # Get the n+1-length combinations (if any) that can accommodate the
            # defined load.
            combos_np1 = self.fit_n_bins(n=n + 1)

            # If no viable combinations were found for both n and n + 1 lengths
            # the increment the defined length, swap the combinations and skip
            # to the next iteration
            if not combos_n or not combos_np1:
                combos_n = combos_np1
                n += 1
                continue

            # if the n + 1 length combinations happen to offer decreased
            # capacity then prefer those combinations over the shorter yet more
            # wasteful combinations
            if sum(combos_n[0]) > sum(combos_np1[0]):
                return combos_np1
            else:
                return combos_n


def create_solver(load, bins, solver_type):
    """Instantiates a solver of given `solver_type`

    This function iterates over the solver registry and creates a solver for a
    given `solver_type` with the defined `load` and `bins`.

    Note:
        Should the defined `solver_type` not be supported by any of the
        registered classes then `None` is returned.

    Args:
        load (int): The load to be fit into the bins.
        bins (tuple, list): The capacities of the bins in which the load will
            be fitted.
        solver_type (str, unicode): The type of solver to be used in solving
            the problem. Can take values of "length", "capacity", and "combo".

    Returns:
        SolverBase: A derived class supporting the defined `solver_type`
            instantiated with the given `load` and `bins`.
    """

    # Iterate over the solvers registry and create an instance for the
    # solver with the defined `solver_type` attribute.
    for solver_name, solver_cls in SolverBase.registry.items():
        if solver_cls.solver_type == solver_type:
            return solver_cls(load=load, bins=bins)
