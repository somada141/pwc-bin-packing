#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `solvers` module."""


import pytest

from pbp import solvers


@pytest.fixture(name="ref_6_2_3_5")
def fixture_ref_6_2_3_5():
    """Reference for (load, bins) of 6, [2, 3, 5]."""

    ref = {
        "load": 6,
        "bins": [2, 3, 5],
        "solutions": {
            key: [(3, 3)] for key in ["length", "capacity", "combo"]
        }
    }

    return ref


@pytest.fixture(name="ref_9_2_3_5")
def fixture_ref_9_2_3_5():
    """Reference for (load, bins) of 9, [2, 3, 5]."""

    ref = {
        "load": 9,
        "bins": [2, 3, 5],
        "solutions": {
            "length": [(5, 5)],
            "capacity": [(2, 2, 5), (3, 3, 3)],
            "combo": [(2, 2, 5), (3, 3, 3)]
        }
    }

    return ref


@pytest.fixture(name="ref_11_2_3_5")
def fixture_ref_11_2_3_5():
    """Reference for (load, bins) of 11, [2, 3, 5]."""

    ref = {
        "load": 11,
        "bins": [2, 3, 5],
        "solutions": {
            key: [(3, 3, 5)] for key in ["length", "capacity", "combo"]
        }
    }

    return ref


def test_ref_6_2_3_5(ref_6_2_3_5):

    ref = ref_6_2_3_5

    for solver_type in ["length", "capacity", "combo"]:
        solver = solvers.create_solver(
            load=ref["load"],
            bins=ref["bins"],
            solver_type=solver_type
        )

        result = solver.solve()

        solutions_refr = ref["solutions"][solver_type]
        solutions_eval = result
        assert solutions_refr == solutions_eval


def test_ref_9_2_3_5(ref_9_2_3_5):

    ref = ref_9_2_3_5

    for solver_type in ["length", "capacity", "combo"]:
        solver = solvers.create_solver(
            load=ref["load"],
            bins=ref["bins"],
            solver_type=solver_type
        )

        result = solver.solve()

        solutions_refr = ref["solutions"][solver_type]
        solutions_eval = result
        assert solutions_refr == solutions_eval


def test_ref_11_2_3_5(ref_11_2_3_5):

    ref = ref_11_2_3_5

    for solver_type in ["length", "capacity", "combo"]:
        solver = solvers.create_solver(
            load=ref["load"],
            bins=ref["bins"],
            solver_type=solver_type
        )

        result = solver.solve()

        solutions_refr = ref["solutions"][solver_type]
        solutions_eval = result
        assert solutions_refr == solutions_eval
