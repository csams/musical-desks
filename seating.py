#!/usr/bin/env python
import argparse
import yaml
from collections import Counter
from itertools import chain

from constraint import (
    Problem,
    AllDifferentConstraint,
    InSetConstraint,
    NotInSetConstraint,
)
from tabulate import tabulate

from model import Room


def keep_away(a, b):
    return not a.is_beside(b)


def keep_near(a, b):
    return a.is_beside(b)


class Config(object):
    def __init__(self, cfg):
        self.name = cfg.get("class", "Unknown Class")
        self.assigned = {}
        self.allowed_rows = {}
        self.disallowed_rows = {}
        self.allowed_columns = {}
        self.disallowed_columns = {}
        self.separate = []
        self.keep_near = []
        self.counter = Counter()
        for kid in cfg["kids"]:
            name = kid["name"]
            self.counter[name] = 0

            for k in kid.get("keep_away_from", []):
                ka = set([k, name])
                self.counter[name] += 1
                if ka not in self.separate:
                    self.separate.append(ka)

            for k in kid.get("keep_near", []):
                self.counter[name] += 1
                sn = set([k, name])
                if sn not in self.keep_near:
                    self.keep_near.append(sn)

            if "assigned" in kid:
                self.counter[name] += 1
                self.assigned[name] = [x - 1 for x in kid["assigned"]]
            else:
                if "allowed_rows" in kid:
                    self.counter[name] += len(kid["allowed_rows"])
                    self.allowed_rows[name] = [x - 1 for x in kid["allowed_rows"]]

                if "disallowed_rows" in kid:
                    self.counter[name] += len(kid["disallowed_rows"])
                    self.disallowed_rows[name] = [x - 1 for x in kid["disallowed_rows"]]

                if "allowed_columns" in kid:
                    self.counter[name] += len(kid["allowed_columns"])
                    self.allowed_columns[name] = [x - 1 for x in kid["allowed_columns"]]

                if "disallowed_columns" in kid:
                    self.counter[name] += len(kid["disallowed_columns"])
                    self.disallowed_columns[name] = [x - 1 for x in kid["disallowed_columns"]]

        self.kids = [k[0] for k in self.counter.most_common()]
        self.room = Room(width=cfg["columns"], height=cfg["rows"])


def load_problem(cfg):
    room = cfg.room

    problem = Problem()

    # only one kid to a seat
    problem.addConstraint(AllDifferentConstraint())

    assigned = set()
    # kids with assigned seats
    for k, a in cfg.assigned.items():
        seat = room.get(*a)
        assigned.add(seat)
        problem.addConstraint(InSetConstraint([seat]), [k])

    # keep kids apart
    for s in cfg.separate:
        problem.addConstraint(keep_away, s)

    # sit kids next to each other
    for s in cfg.keep_near:
        problem.addConstraint(keep_near, s)

    # allow kids only in certain rows
    for k, a in cfg.allowed_rows.items():
        allowed = list(chain.from_iterable(room.row(r) for r in a))
        problem.addConstraint(InSetConstraint(allowed), [k])

    # disallow kids in certain rows
    for k, d in cfg.disallowed_rows.items():
        disallowed = list(chain.from_iterable(room.row(r) for r in d))
        problem.addConstraint(NotInSetConstraint(disallowed), [k])

    # allow kids only in certain columns
    for k, a in cfg.allowed_columns.items():
        allowed = list(chain.from_iterable(room.column(c) for c in a))
        problem.addConstraint(InSetConstraint(allowed), [k])

    # disallow kids in certain columns
    for k, d in cfg.disallowed_columns.items():
        disallowed = list(chain.from_iterable(room.column(c) for c in d))
        problem.addConstraint(NotInSetConstraint(disallowed), [k])

    # populate from the front back
    num_kids = len(cfg.kids)
    front = sorted(set(room.desks[:num_kids]) | assigned)
    problem.addVariables(cfg.kids, front)

    return problem


def main():
    p = argparse.ArgumentParser()
    p.add_argument("config")
    args = p.parse_args()

    with open(args.config) as f:
        cfg = Config(yaml.safe_load(f))

    num_desks = len(cfg.room.desks)
    num_kids = len(cfg.kids)
    if num_desks < num_kids:
        print(f"{num_kids} kids won't fit into {num_desks} desks.")
        return
    problem = load_problem(cfg)

    print()
    print(f"{cfg.name}:")
    solution = problem.getSolution()
    if solution:
        desks = [["" for _ in range(cfg.room.width)] for _ in range(cfg.room.height)]
        for kid, desk in solution.items():
            desks[desk.pos.y][desk.pos.x] = kid

        print(tabulate(desks, tablefmt="fancy_grid"))


if __name__ == "__main__":
    main()
