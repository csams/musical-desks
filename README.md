# musical-desks
Automatically create seating charts given a set of students and constraints.


```yaml
class: Example Class

# A row is a line of desks across the the room. A column is a line of desks
# going from the front to the back of the class.
rows: 7  # pick a desk in front of you and count to the back of the room.
columns: 5  # count the number of desks in the front row.
kids:
    - name: Chris
      # valid values here are keep_away_from, keep_near, assigned,
      # allowed_rows, allowed_columns, disallowed_rows, and disallowed_columns
      # if "assigned" is set, all of the allowed and disallowed values are
      # ignored.

      keep_away_from:
          - Jon
          - Thomas
      keep_near:
          - Jo Ellen
          - Joyce
          - Samantha
      allowed_rows: [1, 2]
    - name: Lloyd
      keep_near:
          - Lydia
          - Thomas
    - name: Thomas
    - name: Jo Ellen
      keep_near:
          - Phil
          - Sharon
    - name: Jesse
      keep_near:
          - Amber
    - name: Amber
    - name: Danny
      keep_near:
          - Chrissy
    - name: Chrissy
    - name: Mike
      keep_near:
          - Linda
    - name: Linda
    - name: Derek
    - name: Julie
    - name: Jon
      keep_near:
          - Julie
    - name: Rob
    - name: Andrew
      keep_near:
          - Rob
    - name: Bob
      keep_near:
          - Laura
    - name: Son
    - name: Lydia
    - name: Terry
      keep_near:
          - Jake
          - Joey
          - Jeremy
    - name: Jeremy
      keep_near:
          - Shawntel
    - name: Jake
    - name: Joey
    - name: Samantha
      keep_near:
          - Joyce
    - name: Phil
    - name: Sharon
    - name: Joyce
    - name: Joseph
      keep_near:
          - Mary
    - name: Mary
    - name: Laura
    - name: Shawntel
    - name: Paul
      keep_near:
          - Joyce
```

Here's an example of running with the above configuration.
```bash
┌[alonzo]  (musical-desks) musical-desks/ (master *%=)
└> ./seating.py config.yaml

Social Studies, 7th period:
╒════════╤═════════╤══════════╤══════════╤══════════╕
│ Amber  │ Mary    │ Linda    │ Mike     │ Son      │
├────────┼─────────┼──────────┼──────────┼──────────┤
│ Derek  │ Jesse   │ Joseph   │ Samantha │ Chris    │
├────────┼─────────┼──────────┼──────────┼──────────┤
│ Danny  │ Chrissy │ Laura    │ Joyce    │ Jo Ellen │
├────────┼─────────┼──────────┼──────────┼──────────┤
│ Lydia  │ Bob     │ Paul     │ Phil     │ Sharon   │
├────────┼─────────┼──────────┼──────────┼──────────┤
│ Lloyd  │ Rob     │ Shawntel │ Joey     │ Jake     │
├────────┼─────────┼──────────┼──────────┼──────────┤
│ Thomas │ Julie   │ Andrew   │ Jeremy   │ Terry    │
├────────┼─────────┼──────────┼──────────┼──────────┤
│ Jon    │         │          │          │          │
╘════════╧═════════╧══════════╧══════════╧══════════╛
```
