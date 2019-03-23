# Java Coding Style <!-- omit in toc -->

- [0 - General rules](#0---general-rules)
  - [0.1 - Be consistent](#01---be-consistent)
  - [0.2 - Write for humans, not for machines](#02---write-for-humans-not-for-machines)
- [1 - Formatting](#1---formatting)
  - [Use spaces, not tabs.](#use-spaces-not-tabs)
  - [Indent with 4 spaces](#indent-with-4-spaces)
  - [Always use braces](#always-use-braces)
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

### Always use braces

---

## 2 - Naming Scheme
### 2.1 - Basic rules

Use `camelCase` for:
- Variables (except for constants/enums)
- Methods 
- Loop variables (where applicable, see [Meaningful Names](#22---examples))

Use `PascalCase` for:
- Classes
- Interfaces
- Abstract Classes

Use `UPPERCASE_WITH_UNDERSCORES` for:
- Enum constants
- Static variables and other constants

### 2.2 - Meaningful names
Having code that reads itself is far better than trying to remember if you mean `j` instead of `i` or vice-versa.
Using meaningful names increases the clarity of code + reduces the time taken to debug something.
Win-win situation.

Using names as `i` and `j` are okay for simple loops.

#### 2.2 - Examples:
```java
// Bad
for (int i = 0; i < teams.length; i++) {
    for (int j = 0; j < games.length; j++) {
        score[i][j] = 0;
    }
}
// Good 
for (int teamIndex = 0; teamIndex < teams.length; teamIndex++) {
    for (int gameIndex = 0; gameIndex < games[teamIndex]; gameIndex++) {
        score[teamIndex][gameIndex] = 0;
    }
}

// Good
for (int i = 0; i < nums.length; i++){
    System.out.println(nums[i]);
}

// Also good, but unnecessary
for (int numsIndex = 0; numsIndex < nums.length; numsIndex++){
    System.out.println(nums[numsIndex]);
}

```
## 3 - Comments

---

## 4 - Programming Pratices


---
