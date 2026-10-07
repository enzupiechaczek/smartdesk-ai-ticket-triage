import csv


def load(p):
    return {
        r["ticket_text"].strip().lower()
        for r in csv.DictReader(open(p, encoding="utf-8"))
    }


print("overlap:", load("ai/data/tickets.csv") & load("tests/held_out_tickets.csv"))
