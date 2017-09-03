# -*- coding: utf-8 -*-

import click

from . import solvers


@click.command()
@click.argument(
    "load",
    type=click.INT,
    required=True
)
@click.argument(
    "bins",
    type=click.INT,
    nargs=-1,
    required=True
)
@click.option(
    "--solver-type",
    type=click.Choice([
        "length",
        "capacity",
        "combo",
        "all"
    ]),
    default="all",
)
def main(load, bins, solver_type):
    """
    Simple bin-packing solver for the PwC interview process.

    Args:
        load (int): The load to be fit into the bins.
        bins (tuple, list): The capacities of the bins in which the load will
            be fitted.
        solver_type (str, unicode): The type of solver to be used in solving
            the problem. Can take values of "length", "capacity", "combo", and
            "all".
    """

    # If an `all` type was defined, iterate over the solvers registry and create
    # an instance for each solver with a defined `solver_type` attribute.
    if solver_type == "all":
        solver_objs = [
            solvers.create_solver(
                load=load,
                bins=bins,
                solver_type=solver_type
            )
            for solver_type in ["length", "capacity", "combo"]
        ]
    else:
        solver_objs = [
            solvers.create_solver(
                load=load,
                bins=bins,
                solver_type=solver_type
            )
        ]

    solutions = {}

    # Iterate over the instantiated solver objects and solve the problem for the
    # defined load and bins.
    for solver_obj in solver_objs:
        # Echo defined conditions.
        _solver_type = solver_obj.solver_type
        msg = ("Applying '{0}' solver to a load of {1} and the following "
               "bins: {2}")
        msg_fmt = msg.format(_solver_type, load, bins)
        click.echo(msg_fmt)

        # Solve the problem.
        solution = solver_obj.solve()

        # Output the solution.
        click.echo("Solution: {0}".format(solution))

        solutions[_solver_type] = solution

    return solutions


# Main sentinel.
if __name__ == "__main__":
    main()
