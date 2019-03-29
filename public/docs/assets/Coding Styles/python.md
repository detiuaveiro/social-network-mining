# Python Coding Style <!-- omit in toc -->

- [0 - General rules](#0---general-rules)
  - [0.1 - Be consistent](#01---be-consistent)
  - [0.2 - Write for humans, not for machines](#02---write-for-humans-not-for-machines)
- [1 - Formatting](#1---formatting)
  - [Use spaces, not tabs.](#use-spaces-not-tabs)
  - [Indent with 4 spaces](#indent-with-4-spaces)
- [2 - Naming Scheme](#2---naming-scheme)
  - [2.1 - Basic rules](#21---basic-rules)
  - [2.2 - Meaningful names](#22---meaningful-names)
    - [2.2 - Examples:](#22---examples)
- [3 - Comments](#3---comments)
- [4 - Programming Pratices](#4---programming-pratices)

## 0 - General rules
### 0.1  - Be consistent
If you're editing a file, follow its coding style, even if it doesn't match this guide.
Doing this makes it easier for the reader since they won't be thrown out of their rhythm.

### 0.2 - Write for humans, not for machines
Self-explanatory.

---

## 1 - Formatting
### Use spaces, not tabs. 
Most modern editors are able to use spaces for indenting and using spaces avoids common issues when line-wrapping for visual aligment.
Also prevents rendering differently in different editors.

### Indent with 4 spaces

---

## 2 - Naming Scheme
### 2.1 - Basic rules

Use `snake_case` for:
- Variables (except for constants/enums)
- Functions/Lambdas
- Loop variables

Use `PascalCase` for:
- Classes
- Enums

Use `UPPERCASE_WITH_UNDERSCORES` for:
- Enum variables
- Constants
Where necessary, append a `_` to indicate it's a private variable.


### 2.2 - Meaningful names
Having code that reads itself is far better than trying to remember if you mean `j` instead of `i` or vice-versa.
Using meaningful names increases the clarity of code + reduces the time taken to debug something.
Win-win situation.

Using names as `i` and `j` are okay for simple loops **only when iterating over indexes**, otherwise use a relevant name, even if it's redundant.
In the case of shadowing, use your best judgment

#### 2.2 - Examples:
```python
# Bad
for i in range(total_teams):
    for j in range(total_games):
        score[i][j] = 0

# Good 
for team_ind in range(total_teams):
    for games_ind in range(total_games):
        score[team_ind][game_ind] = 0

# Bad
for i in nums:
    print(i)

# Good
for num in nums:
    print(i)

# Worst
for id in ids:
    print(id)

# Preffered, but the variable ids might be the issue here
for id_elem in ids:
    print(id_elem)
```
## 3 - Comments

---

## 4 - Programming Pratices


---
